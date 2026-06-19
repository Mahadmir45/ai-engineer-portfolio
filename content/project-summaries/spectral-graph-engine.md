# Spectral Graph Compression Engine

**Domain:** ML / graph algorithms  
**GitHub:** Mahadmir45/mathematical-projects

## Overview

High-performance C++ implementation of spectral graph compression for investor clustering and Max-Cut approximation, derived from published research (Liu, Lee, Constantinides 2025).

## Pipeline stages

1. **Graph construction** — correlation-based adjacency from investor feature profiles
2. **Normalized Laplacian** — L_norm = I - D^(-1/2) A D^(-1/2)
3. **Spectral embedding** — smallest k eigenvectors via LAPACK (LAPACKE_dsyevd)
4. **Graph compression** — B = U^T A U
5. **Max-Cut** — greedy local search + Goemans-Williamson rounding
6. **Label reconstruction** — sign((U * l_B)_i)

## Performance

- OpenBLAS + LAPACK CPU path
- Optional CUDA acceleration (cuBLAS, cuSolver) for Linux+NVIDIA
- GoogleTest unit tests and published benchmark reproduction
- Live Chart.js dashboard at localhost:8765

## Tech stack

C++17, CMake, OpenBLAS, LAPACK, GoogleTest, Python dashboard server, Chart.js

## Portfolio relevance

Demonstrates performance-critical ML infrastructure, spectral methods, and rigorous benchmarking — skills transferable to large-scale retrieval and graph-based context systems.
