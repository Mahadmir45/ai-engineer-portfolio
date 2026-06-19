# QuantFin Bayesian Marketing Mix Model

**Domain:** Finance / probabilistic ML  
**GitHub:** Mahadmir45/QuantFin

## Overview

A premier-grade Marketing Mix Modeling (MMM) framework built with Bayesian-first methodology using PyMC. Quantifies the impact of marketing channels (TV, digital, social, search) on business outcomes with full uncertainty quantification.

## Capabilities

1. **Revenue decomposition** — base, trend, seasonality, per-channel media contributions
2. **Adstock learning** — geometric, Weibull, and delayed carry-over effects
3. **Saturation curves** — Hill, logistic, Gompertz diminishing returns
4. **ROI computation** — per-channel with Bayesian credible intervals
5. **Budget optimization** — SLSQP allocation to maximize expected revenue
6. **Scenario analysis** — what-if budget increase/decrease simulations

## Architecture

```
Analytics/mmm_bayesian/
├── core/           # Config, scaling, Fourier features
├── transforms/     # Adstock + saturation (NumPy + PyTensor)
├── models/         # Full PyMC Bayesian MMM
├── optimization/   # Budget optimizer, response curves
├── visualization/  # Waterfall, ROI, response curve charts
└── pipeline/       # End-to-end: data → model → optimize → report
```

## Tech stack

Python 3.10+, PyMC, NumPy, Pandas, scikit-learn, YAML configs

## Portfolio relevance

Probabilistic synthesis of multi-channel signals parallels how AI market intelligence platforms combine hundreds of financial data sources into actionable insights. Demonstrates rigorous ML engineering beyond simple LLM wrappers.
