# Hybrid RAG Demo

FastAPI service with hybrid BM25 + dense retrieval over finance and nutrition knowledge bases.

## Setup

```bash
cd rag-demo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Build indexes (requires content/ from repo root)
python ingestion/build_index.py

cp .env.example .env
# Edit .env with OPENAI_API_KEY
```

## Run

From the `rag-demo` directory:

```bash
uvicorn backend.main:app --reload --port 8080
```

Open http://127.0.0.1:8080

## Local dev without OpenAI

```bash
export LLM_PROVIDER=ollama
ollama pull llama3.2
ollama serve  # in another terminal
uvicorn backend.main:app --reload --port 8080
```

## Deploy to Render

1. Push repo to GitHub
2. Connect Render to repo — uses root `render.yaml`
3. Set `OPENAI_API_KEY` in Render dashboard
4. Update `RAG_DEMO_URL` in `portfolio-site/script.js` with Render URL

## Architecture

- **Domain router:** keyword classifier → finance_kb | nutrition_kb | both
- **Hybrid retriever:** ChromaDB dense + BM25 with reciprocal rank fusion
- **LLM:** OpenAI gpt-4o-mini or Ollama with citation-grounded prompts
- **API:** SSE streaming at `POST /api/chat`
