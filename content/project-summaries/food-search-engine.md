# Food Search & Entity Matching Platform

**Domain:** Nutrition / retrieval  
**GitHub:** UNI_of_Sydney_GI_Matching (local: web_app_search engine)

## Overview

A local web application for searching UNI Sydney Glycemic Index foods and matching them to USDA SR Legacy database entries. Supports multi-keyword retrieval, entity resolution, and persistent mapping of FDC IDs back to Excel and SQLite.

## Matching logic

- **All-keywords search:** Query split into tokens; rows match only if every keyword appears in the name (order and punctuation insensitive)
- **Ranking boosts:** Exact normalized match → phrase containment → token match
- **Filters:** Product category, country (Uni Sydney); main category (SR Legacy)
- **Persistence:** Saves append selected `fdc_id` values to Excel column and SQLite cache

## Tech stack

- **Backend:** Python, FastAPI, Uvicorn, Pandas, OpenPyXL, SQLite FTS
- **Frontend:** Vanilla HTML/CSS/JS with tabs for Search, AI Matches, Accuracy Check, Category Progress
- **Data:** Excel imports (`UNI_Sydney_cleaned_glycemic_index.xlsx`, `READY_processed_sr_food.xlsx`)

## AI matching module

Separate multi-signal text similarity pipeline for automated food entity resolution using domain knowledge rules and fuzzy matching — production-grade retrieval without LLM embeddings.

## Portfolio relevance

Demonstrates production retrieval systems, entity resolution at scale, and FastAPI-backed search — directly applicable to multi-source data synthesis in AI market intelligence.
