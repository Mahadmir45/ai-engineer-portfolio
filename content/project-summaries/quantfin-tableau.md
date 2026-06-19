# QuantFin Tableau Dashboards

**Domain:** Finance / visualization  
**GitHub:** Mahadmir45/QuantFin-Tableau

## Overview

Unified Tableau + Tableau Prep dashboards for the QuantFin monorepo: equity markets, Topology Alpha strategy, and Bayesian Marketing Mix Modeling (MMM).

## Dashboard tabs

- **Executive overview** — KPIs across quant strategies
- **Market data** — equity price/volume visualizations
- **Topology Alpha** — TDA strategy signals and backtest results
- **MMM analytics** — channel ROI, adstock curves, budget scenarios

## Data flow

1. Python export scripts pull from QuantFin Analytics and Quant_Portfolio
2. Tableau Prep flows clean and stage data
3. Tableau workbooks connect to staged CSV/Parquet outputs

## Tech stack

Tableau Desktop 2024+, Tableau Prep, Python export scripts, QuantFin library integration

## Portfolio relevance

Demonstrates end-to-end ML pipeline delivery — from Bayesian model fitting to executive-ready visualizations of probabilistic outputs.
