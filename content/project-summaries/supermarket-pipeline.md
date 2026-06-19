# Supermarket Data Pipeline

**Domain:** Nutrition / data engineering  
**Location:** web_app_search engine/wellcome_scrapped

## Overview

Large-scale bilingual supermarket data pipeline scraping Hong Kong retail chains (Wellcome, ParknShop, 7-Eleven), building master product databases with USDA FoodData Central matching.

## Pipeline components

- **Scrapers:** Node.js crawlers for EN/CN product listings across categories
- **OCR:** RapidOCR (ONNX) for image-based product extraction
- **Master DB builder:** Merges EN/CN listings, brand dimension tables, category normalization
- **USDA matching:** Fuzzy matching pipeline (thefuzz) mapping retail SKUs to FDC IDs
- **Schemas:** Databricks SQL schemas for warehouse deployment

## Data scale

- Multi-chain, multi-language product catalogs
- Category-wise CSV exports (beverages, frozen, snacks, etc.)
- Brand master with merged CN/EN product listings

## Tech stack

Node.js, Python, Selenium, BeautifulSoup, RapidOCR, thefuzz, Pandas, Databricks SQL

## Portfolio relevance

Shows ability to ingest, normalize, and match heterogeneous real-world datasets at scale — the data foundation layer that RAG and AI intelligence systems depend on.
