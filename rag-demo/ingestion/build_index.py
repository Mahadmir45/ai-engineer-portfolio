"""Document loading, chunking, embedding, and index building."""

from __future__ import annotations

import json
import pickle
import re
import sys
from pathlib import Path

import chromadb
from chromadb.config import Settings
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shared.chunks import Chunk

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT.parent / "content"
DATA_DIR = ROOT / "data"
CHROMA_DIR = DATA_DIR / "chroma"
BM25_DIR = DATA_DIR / "bm25"

FINANCE_FILES = [
    CONTENT_DIR / "quantfin-overview.md",
    CONTENT_DIR / "project-summaries" / "quantfin-mmm.md",
    CONTENT_DIR / "project-summaries" / "quantfin-library.md",
    CONTENT_DIR / "project-summaries" / "quantfin-tableau.md",
    CONTENT_DIR / "project-summaries" / "hybrid-knowledge-agent.md",
]

NUTRITION_FILES = [
    CONTENT_DIR / "food-search-overview.md",
    CONTENT_DIR / "project-summaries" / "food-search-engine.md",
    CONTENT_DIR / "project-summaries" / "supermarket-pipeline.md",
    CONTENT_DIR / "project-summaries" / "spectral-graph-engine.md",
    CONTENT_DIR / "project-summaries" / "return-points-portal.md",
]

COLLECTIONS = {
    "finance_kb": FINANCE_FILES,
    "nutrition_kb": NUTRITION_FILES,
}

CHUNK_SIZE = 512
CHUNK_OVERLAP = 64
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def _tokenize_for_chunking(text: str) -> list[str]:
    return re.findall(r"\S+", text)


def chunk_text(text: str, source: str, project: str, domain: str) -> list[Chunk]:
    words = _tokenize_for_chunking(text)
    if not words:
        return []

    chunks: list[Chunk] = []
    start = 0
    idx = 0
    while start < len(words):
        end = min(start + CHUNK_SIZE, len(words))
        chunk_words = words[start:end]
        chunk_text_str = " ".join(chunk_words)
        chunks.append(
            Chunk(
                text=chunk_text_str,
                source=source,
                project=project,
                domain=domain,
                chunk_id=f"{Path(source).stem}_{idx}",
            )
        )
        idx += 1
        if end >= len(words):
            break
        start = end - CHUNK_OVERLAP

    return chunks


def load_documents(files: list[Path], domain: str) -> list[Chunk]:
    all_chunks: list[Chunk] = []
    for fp in files:
        if not fp.exists():
            print(f"Warning: missing {fp}")
            continue
        text = fp.read_text(encoding="utf-8")
        project = fp.stem.replace("-", " ").title()
        all_chunks.extend(chunk_text(text, str(fp.name), project, domain))
    return all_chunks


def build_indexes() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    BM25_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Loading embedding model: {EMBED_MODEL}")
    model = SentenceTransformer(EMBED_MODEL)

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )

    for collection_name, files in COLLECTIONS.items():
        domain = "finance" if "finance" in collection_name else "nutrition"
        chunks = load_documents(files, domain)
        if not chunks:
            print(f"No chunks for {collection_name}, skipping")
            continue

        # Reset collection
        try:
            client.delete_collection(collection_name)
        except Exception:
            pass

        collection = client.create_collection(
            name=collection_name,
            metadata={"domain": domain},
        )

        texts = [c.text for c in chunks]
        ids = [c.chunk_id for c in chunks]
        metadatas = [
            {"source": c.source, "project": c.project, "domain": c.domain}
            for c in chunks
        ]
        embeddings = model.encode(texts, show_progress_bar=True).tolist()

        collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings,
        )

        # BM25 index
        tokenized = [doc.lower().split() for doc in texts]
        bm25 = BM25Okapi(tokenized)
        bm25_path = BM25_DIR / f"{collection_name}.pkl"
        with bm25_path.open("wb") as f:
            pickle.dump({"bm25": bm25, "chunks": chunks}, f)

        print(f"Indexed {len(chunks)} chunks in {collection_name}")

    stats = {
        name: len(load_documents(files, "finance" if "finance" in name else "nutrition"))
        for name, files in COLLECTIONS.items()
    }
    stats_path = DATA_DIR / "corpus_stats.json"
    stats_path.write_text(json.dumps(stats, indent=2))
    print(f"Corpus stats written to {stats_path}")


if __name__ == "__main__":
    build_indexes()
