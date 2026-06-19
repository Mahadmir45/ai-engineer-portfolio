"""Domain routing, hybrid retrieval, and LLM synthesis."""

from __future__ import annotations

import json
import os
import pickle
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncIterator, Literal

import chromadb
from chromadb.config import Settings
from openai import AsyncOpenAI
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shared.chunks import Chunk

DATA_DIR = ROOT / "data"
CHROMA_DIR = DATA_DIR / "chroma"
BM25_DIR = DATA_DIR / "bm25"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5
RRF_K = 60

FINANCE_KEYWORDS = {
    "mmm", "bayesian", "pymc", "quantfin", "quant", "portfolio", "options",
    "marketing", "mix", "adstock", "saturation", "roi", "budget", "channel",
    "trading", "backtest", "topology", "alpha", "finance", "financial",
    "equity", "volatility", "tableau", "strategy", "investment",
}

NUTRITION_KEYWORDS = {
    "food", "nutrition", "usda", "fdc", "glycemic", "gi", "matching",
    "entity", "supermarket", "wellcome", "scraping", "ocr", "retail",
    "product", "bilingual", "chinese", "pipeline", "search", "sr legacy",
}


@dataclass
class RetrievedChunk:
    text: str
    source: str
    project: str
    domain: str
    score: float


DomainRoute = Literal["finance", "nutrition", "both"]


def route_query(query: str) -> DomainRoute:
    tokens = set(re.findall(r"[a-z0-9]+", query.lower()))
    finance_hits = len(tokens & FINANCE_KEYWORDS)
    nutrition_hits = len(tokens & NUTRITION_KEYWORDS)

    if finance_hits > 0 and nutrition_hits == 0:
        return "finance"
    if nutrition_hits > 0 and finance_hits == 0:
        return "nutrition"
    if finance_hits > 0 and nutrition_hits > 0:
        return "both"
    return "both"


class HybridRetriever:
    def __init__(self) -> None:
        self._model: SentenceTransformer | None = None
        self._client: chromadb.ClientAPI | None = None
        self._bm25_cache: dict[str, dict] = {}

    def _ensure_loaded(self) -> None:
        if self._model is None:
            self._model = SentenceTransformer(EMBED_MODEL)
        if self._client is None:
            self._client = chromadb.PersistentClient(
                path=str(CHROMA_DIR),
                settings=Settings(anonymized_telemetry=False),
            )

    def _load_bm25(self, collection_name: str) -> dict | None:
        if collection_name in self._bm25_cache:
            return self._bm25_cache[collection_name]
        path = BM25_DIR / f"{collection_name}.pkl"
        if not path.exists():
            return None
        with path.open("rb") as f:
            data = pickle.load(f)
        self._bm25_cache[collection_name] = data
        return data

    def _reciprocal_rank_fusion(
        self,
        dense_results: list[tuple[str, float, dict]],
        sparse_results: list[tuple[str, float, object]],
    ) -> list[tuple[str, float, dict | object]]:
        scores: dict[str, float] = {}
        payloads: dict[str, tuple] = {}

        for rank, (doc_id, _score, payload) in enumerate(dense_results):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (RRF_K + rank + 1)
            payloads[doc_id] = ("dense", payload)

        for rank, (doc_id, _score, payload) in enumerate(sparse_results):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (RRF_K + rank + 1)
            if doc_id not in payloads:
                payloads[doc_id] = ("sparse", payload)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [(doc_id, score, payloads[doc_id][1]) for doc_id, score in ranked[:TOP_K]]

    def retrieve(self, query: str, route: DomainRoute) -> list[RetrievedChunk]:
        self._ensure_loaded()
        assert self._model is not None
        assert self._client is not None

        collections = []
        if route in ("finance", "both"):
            collections.append("finance_kb")
        if route in ("nutrition", "both"):
            collections.append("nutrition_kb")

        all_results: list[RetrievedChunk] = []
        seen_ids: set[str] = set()

        for coll_name in collections:
            try:
                collection = self._client.get_collection(coll_name)
            except Exception:
                continue

            query_embedding = self._model.encode([query]).tolist()
            dense = collection.query(
                query_embeddings=query_embedding,
                n_results=min(TOP_K * 2, 10),
                include=["documents", "metadatas", "distances"],
            )

            id_to_doc: dict[str, tuple[str, dict]] = {}
            dense_results: list[tuple[str, float, dict]] = []
            if dense["ids"] and dense["ids"][0]:
                for i, doc_id in enumerate(dense["ids"][0]):
                    dist = dense["distances"][0][i] if dense["distances"] else 0
                    meta = dense["metadatas"][0][i] if dense["metadatas"] else {}
                    doc_text = dense["documents"][0][i] if dense["documents"] else ""
                    id_to_doc[doc_id] = (doc_text, meta)
                    dense_results.append((doc_id, 1 - dist, meta))

            bm25_data = self._load_bm25(coll_name)
            sparse_results: list[tuple[str, float, object]] = []
            if bm25_data:
                bm25 = bm25_data["bm25"]
                chunks = bm25_data["chunks"]
                tokenized_query = query.lower().split()
                bm25_scores = bm25.get_scores(tokenized_query)
                top_indices = sorted(
                    range(len(bm25_scores)),
                    key=lambda i: bm25_scores[i],
                    reverse=True,
                )[:TOP_K * 2]
                for idx in top_indices:
                    if bm25_scores[idx] > 0:
                        chunk = chunks[idx]
                        sparse_results.append((chunk.chunk_id, bm25_scores[idx], chunk))
                        id_to_doc[chunk.chunk_id] = (chunk.text, {
                            "source": chunk.source,
                            "project": chunk.project,
                            "domain": chunk.domain,
                        })

            if dense_results or sparse_results:
                merged = self._reciprocal_rank_fusion(dense_results, sparse_results)
                for doc_id, score, payload in merged:
                    if doc_id in seen_ids:
                        continue
                    seen_ids.add(doc_id)

                    if doc_id in id_to_doc:
                        doc_text, meta = id_to_doc[doc_id]
                    elif hasattr(payload, "text"):
                        doc_text = payload.text
                        meta = {
                            "source": payload.source,
                            "project": payload.project,
                            "domain": payload.domain,
                        }
                    else:
                        doc_text = ""
                        meta = payload if isinstance(payload, dict) else {}

                    all_results.append(
                        RetrievedChunk(
                            text=doc_text,
                            source=meta.get("source", "unknown"),
                            project=meta.get("project", "unknown"),
                            domain=meta.get("domain", coll_name),
                            score=score,
                        )
                    )

        all_results.sort(key=lambda c: c.score, reverse=True)
        return all_results[:TOP_K]

    def get_corpus_stats(self) -> dict[str, int]:
        stats_path = DATA_DIR / "corpus_stats.json"
        if stats_path.exists():
            return json.loads(stats_path.read_text())
        return {"finance_kb": 0, "nutrition_kb": 0}


def build_prompt(query: str, chunks: list[RetrievedChunk]) -> str:
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        context_parts.append(
            f"[{i}] Project: {chunk.project} | Source: {chunk.source}\n{chunk.text}"
        )
    context = "\n\n".join(context_parts)
    return f"""You are an AI assistant for Mahad's portfolio. Answer using ONLY the provided context.
Cite sources using [1], [2], etc. If context is insufficient, say so briefly.

Context:
{context}

Question: {query}

Answer:"""


async def stream_llm_response(
    query: str,
    chunks: list[RetrievedChunk],
) -> AsyncIterator[str]:
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    prompt = build_prompt(query, chunks)

    if provider == "ollama":
        import httpx

        base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
        model = os.getenv("OLLAMA_MODEL", "llama3.2")
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream(
                "POST",
                f"{base_url}/api/generate",
                json={"model": model, "prompt": prompt, "stream": True},
            ) as response:
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        token = data.get("response", "")
                        if token:
                            yield token
        return

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        yield (
            "Error: Set OPENAI_API_KEY or use LLM_PROVIDER=ollama for local inference. "
            "Retrieved context is available in citations below."
        )
        return

    client = AsyncOpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    stream = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        temperature=0.3,
        max_tokens=1024,
    )
    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
