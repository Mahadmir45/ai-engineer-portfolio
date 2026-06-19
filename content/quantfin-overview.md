# QuantFin — Financial ML Overview

QuantFin is a comprehensive quantitative finance ecosystem spanning probabilistic marketing analytics, options pricing, portfolio optimization, and ML-driven trading strategies.

## Bayesian Marketing Mix Model (MMM)

The Analytics module implements a full Bayesian MMM pipeline using PyMC:

- **Media transforms:** Geometric, Weibull, and delayed adstock; Hill, logistic, Gompertz saturation
- **Model fitting:** Hierarchical priors, MCMC sampling, convergence diagnostics
- **Outputs:** Channel contribution waterfalls, ROI with credible intervals, response curves
- **Optimization:** Budget allocation via SLSQP constrained optimization
- **Scenarios:** Total budget +/- 20% what-if simulations

Configuration is YAML-driven (`config_retail.yaml`, `config_luxury.yaml`) for different brand verticals.

## Quant Library

Core quantfin package modules:

- **Options:** Black-Scholes, binomial trees, Monte Carlo; full Greeks suite
- **Portfolio:** Mean-variance, CVaR, risk parity; performance attribution
- **Strategies:** Pairs trading, momentum, XGBoost/LSTM ML strategies, Topology Alpha (TDA + Laplacian diffusion)
- **Backtesting:** Realistic execution simulation with slippage and commission models

## Topology Alpha

Novel strategy combining Topological Data Analysis persistent homology with graph Laplacian diffusion on correlation matrices. Identifies regime changes and generates alpha signals from market microstructure.

## Tableau Integration

QuantFin-Tableau exports model outputs to executive dashboards covering market data, strategy backtests, and MMM channel analytics.

## Relevance to AI market intelligence

QuantFin demonstrates probabilistic multi-source synthesis — decomposing revenue into channel contributions with uncertainty, optimizing allocations, and running scenarios. This mirrors how AI platforms synthesize hundreds of financial data feeds into actionable insights.
