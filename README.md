# memsieve-agent

[![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF)](.github/workflows/ci.yml) [![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)](pyproject.toml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[**Live demo →**](https://sushxnthd.github.io/memsieve-agent/) · [Architecture](docs/architecture.md) · [Benchmarks](benchmarks/results.json)


A small memory controller for long-running agents: suppress near-duplicates, retain high-value items under a hard budget, and retrieve using relevance plus recency/importance/usage.

```bash
pip install -e .
memsieve "invoice due" "invoice 17 due friday" "weather sunny"
```

## Model

A memory's retention score combines importance, recency and historical use. Retrieval adds lexical relevance. The implementation is deterministic and dependency-free, so it is easy to benchmark against vector-memory systems instead of hiding behavior behind an embedding API.

## Benchmark

`python benchmarks/run.py` streams 81 memories into a 24-item store and measures whether the one high-value fact survives pruning and is retrieved at rank 1.

## Intended use

`memsieve` is useful as a baseline, a local fallback, or the policy layer around a more expensive embedding index. It does not attempt semantic retrieval beyond token overlap in v0.1.

## Roadmap

- pluggable embedding scorer
- memory merge/compression hooks
- temporal contradiction handling
- LongMemEval adapter

MIT licensed.

## Architecture

See [`docs/architecture.md`](docs/architecture.md) for the data flow and design boundaries.
