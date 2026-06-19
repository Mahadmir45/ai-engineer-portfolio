# Deployment Guide

## Portfolio (GitHub Pages)

1. Push this repo to `Mahadmir45/ai-engineer-portfolio`
2. In GitHub repo **Settings → Pages → Build and deployment**, set source to **GitHub Actions**
3. Push to `main` — workflow `.github/workflows/deploy-portfolio.yml` deploys `portfolio-site/`
4. Site URL: `https://mahadmir45.github.io/ai-engineer-portfolio/`

## RAG Demo (Render)

1. Create account at [render.com](https://render.com)
2. **New → Blueprint** → connect this repo (uses root `render.yaml`)
3. Set `OPENAI_API_KEY` when prompted (sync: false in blueprint)
4. After deploy, copy the service URL (e.g. `https://hybrid-knowledge-agent.onrender.com`)
5. Update `portfolio-site/script.js`:

```javascript
const RAG_DEMO_URL = "https://your-service.onrender.com";
```

6. Push — portfolio iframe will load the live demo

## Local development

```bash
# Portfolio — open in browser
open portfolio-site/index.html

# RAG demo
cd rag-demo
source .venv/bin/activate
python ingestion/build_index.py
uvicorn backend.main:app --reload --port 8080
```

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes (unless Ollama) | OpenAI API key for LLM synthesis |
| `LLM_PROVIDER` | No | `openai` (default) or `ollama` |
| `OPENAI_MODEL` | No | Default `gpt-4o-mini` |
| `CORS_ORIGIN` | No | GitHub Pages URL for production |
| `OLLAMA_BASE_URL` | Ollama only | Default `http://127.0.0.1:11434` |

## EVG application checklist

- [ ] Portfolio live on GitHub Pages
- [ ] RAG demo deployed on Render with `OPENAI_API_KEY`
- [ ] Pin repos: ai-engineer-portfolio, QuantFin, mathematical-projects
- [ ] Apply at [evg.co/career](https://evg.co/career) — AI Engineer (RAG/LLM)
