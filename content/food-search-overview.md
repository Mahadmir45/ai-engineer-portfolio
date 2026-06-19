# Food Search & Nutrition Data Platform Overview

End-to-end nutrition data platform combining web search, entity resolution, and large-scale retail data ingestion.

## Food Search Engine

FastAPI web app for glycemic index food lookup and USDA SR Legacy matching:

- SQLite FTS5 full-text search with all-keywords matching
- Ranking: exact match > phrase > token match
- Batch save merges FDC IDs to Excel and database
- Frontend tabs: Search, AI Matches, Accuracy Check, Category Progress

## AI-Based Matching Module

Multi-signal text similarity pipeline for automated food entity resolution:

- Normalized text comparison with domain-specific food knowledge
- Fuzzy matching for variant spellings and bilingual names
- Confidence scoring for human-in-the-loop verification

## Supermarket Scraping Pipeline

Production data engineering for Hong Kong retail:

- **Chains:** Wellcome, ParknShop, 7-Eleven
- **Languages:** English and Chinese product listings
- **OCR:** RapidOCR (ONNX) for image-based extraction
- **Master DB:** Unified product catalog with brand dimensions
- **USDA matching:** Fuzzy pipeline mapping retail products to FoodData Central FDC IDs
- **Warehouse:** Databricks SQL schemas for analytics deployment

## O2EZ Database

Hong Kong CFS nutrient data scraping with USDA cross-referencing and Chinese encoding handling (Selenium, BeautifulSoup, pdfplumber, thefuzz).

## Relevance to retrieval systems

This platform demonstrates production-grade retrieval, entity resolution over heterogeneous datasets, and data pipeline engineering — foundational capabilities for RAG systems that must ground answers in messy real-world data.
