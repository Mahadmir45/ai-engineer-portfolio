from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .rag import HybridRetriever, route_query, stream_llm_response

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT / "frontend"

app = FastAPI(title="Hybrid Knowledge Agent", version="1.0.0")

cors_origins = os.getenv("CORS_ORIGIN", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if cors_origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

retriever = HybridRetriever()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


class SourceItem(BaseModel):
    title: str
    project: str
    snippet: str
    score: float
    domain: str


class ChatInitResponse(BaseModel):
    route: str
    sources: list[SourceItem]


app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/")
def index() -> FileResponse:
    fp = FRONTEND_DIR / "index.html"
    if not fp.exists():
        raise HTTPException(status_code=500, detail="Missing frontend/index.html")
    return FileResponse(fp)


@app.get("/api/health")
def health() -> dict[str, str]:
    stats = retriever.get_corpus_stats()
    indexed = sum(stats.values())
    return {
        "status": "ok" if indexed > 0 else "no_index",
        "indexed_chunks": str(indexed),
    }


@app.get("/api/corpus-stats")
def corpus_stats() -> dict[str, int]:
    return retriever.get_corpus_stats()


@app.post("/api/chat/init", response_model=ChatInitResponse)
def chat_init(body: ChatRequest) -> ChatInitResponse:
    route = route_query(body.message)
    chunks = retriever.retrieve(body.message, route)
    sources = [
        SourceItem(
            title=c.source,
            project=c.project,
            snippet=c.text[:300] + ("..." if len(c.text) > 300 else ""),
            score=round(c.score, 4),
            domain=c.domain,
        )
        for c in chunks
    ]
    return ChatInitResponse(route=route, sources=sources)


@app.post("/api/chat")
async def chat_stream(body: ChatRequest) -> StreamingResponse:
    route = route_query(body.message)
    chunks = retriever.retrieve(body.message, route)

    async def event_generator():
        meta = {
            "type": "meta",
            "route": route,
            "sources": [
                {
                    "title": c.source,
                    "project": c.project,
                    "snippet": c.text[:300],
                    "score": round(c.score, 4),
                    "domain": c.domain,
                }
                for c in chunks
            ],
        }
        yield f"data: {json.dumps(meta)}\n\n"

        async for token in stream_llm_response(body.message, chunks):
            payload = {"type": "token", "content": token}
            yield f"data: {json.dumps(payload)}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
