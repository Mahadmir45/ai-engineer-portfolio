# AI Engineer Portfolio + Hybrid RAG Demo

Interactive portfolio and hybrid retrieval-augmented generation (RAG) demo aligned with **AI Engineer (RAG/LLM)** roles — built to showcase multi-source data synthesis, probabilistic ML, and production retrieval systems.

**Live portfolio:** [https://mahadmir45.github.io/ai-engineer-portfolio/](https://mahadmir45.github.io/ai-engineer-portfolio/)

## Structure

```
├── portfolio-site/     # Static site (GitHub Pages)
├── rag-demo/           # Hybrid RAG agent (FastAPI + ChromaDB)
├── content/            # Curated project summaries (RAG corpus)
└── .github/workflows/  # CI + Pages deploy
```

## Quick start — Portfolio

The static site requires no build step. Open `portfolio-site/index.html` locally or deploy via GitHub Pages.

## Quick start — RAG Demo

```bash
cd rag-demo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Build vector indexes from content/
python -m ingestion.build_index

# Set LLM provider (OpenAI or Ollama)
export OPENAI_API_KEY=sk-...
# OR for local dev: export LLM_PROVIDER=ollama

uvicorn backend.main:app --reload --port 8080
```

Open [http://127.0.0.1:8080](http://127.0.0.1:8080) for the chat UI.

## Deploy RAG Demo (Render)

1. Push this repo to GitHub
2. Create a **Web Service** on [Render](https://render.com) using `rag-demo/render.yaml`
3. Set `OPENAI_API_KEY` in Render environment variables
4. Update `RAG_DEMO_URL` in `portfolio-site/script.js` with your Render URL

## Knowledge corpora

| Collection | Domain | Sources |
|------------|--------|---------|
| `finance_kb` | QuantFin / analytics | MMM docs, quant strategies, portfolio optimization |
| `nutrition_kb` | Food search / data | Entity matching, USDA pipeline, scraping |
| Both | Portfolio meta | Project summaries in `content/project-summaries/` |

## Featured projects

- **Hybrid Knowledge Agent** — multi-corpus RAG with domain routing
- **QuantFin Bayesian MMM** — PyMC marketing mix modeling
- **Food Search Engine** — entity resolution + FastAPI retrieval
- **Spectral Graph Engine** — C++ spectral embedding + Max-Cut
- **Supermarket Data Pipeline** — bilingual scraping + OCR + fuzzy matching

## License

MIT
