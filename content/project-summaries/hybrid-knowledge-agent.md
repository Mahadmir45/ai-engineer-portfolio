# Hybrid Knowledge Agent

**Domain:** RAG / LLM  
**Project:** ai-engineer-portfolio (this repo)

## Overview

A hybrid retrieval-augmented generation agent that synthesizes answers across two knowledge domains: **financial ML** (QuantFin) and **nutrition data engineering** (Food Search). Built to demonstrate the retrieve → rank → synthesize pattern used in production AI market intelligence systems.

## Architecture

- **Domain router:** Keyword/heuristic classifier routes queries to `finance_kb`, `nutrition_kb`, or both
- **Hybrid retriever:** BM25 sparse search + dense embeddings (sentence-transformers/all-MiniLM-L6-v2) with reciprocal rank fusion
- **Vector store:** ChromaDB with separate collections per domain
- **LLM synthesis:** OpenAI gpt-4o-mini (production) or Ollama (local dev) with grounded citations
- **API:** FastAPI with Server-Sent Events (SSE) streaming

## Key endpoints

- `POST /api/chat` — Stream grounded answers with source citations
- `GET /api/corpus-stats` — Indexed document counts per collection
- `GET /api/health` — Deployment health check

## Tech stack

Python, FastAPI, ChromaDB, sentence-transformers, rank-bm25, OpenAI API, vanilla JS chat UI

## Why this matters for AI engineering

Demonstrates production RAG patterns: multi-corpus indexing, hybrid retrieval, domain routing, citation grounding, and streaming responses — the same building blocks used to synthesize hundreds of heterogeneous data sources into actionable insights.
