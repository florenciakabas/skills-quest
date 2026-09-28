# skills-quest

Bayesian modeling, retrieval, and PySpark, learned by building, on US public health data.

| Track | Question | Data |
|---|---|---|
| Bayes (PyMC) | Which hospitals truly readmit more than expected, and which only look bad because they're small? | CMS Hospital Readmissions Reduction Program, FY2026 |
| Retrieval | Given a patient-style question, find the right clinical trials and answer with citations that hold up. | ClinicalTrials.gov API |
| PySpark | Where does Medicare drug spending concentrate, by specialty, state and drug? | CMS Medicare Part D Prescribers, 2024 |

## Progress

| Step | What | Status |
|---|---|---|
| B1 | No, complete and partial pooling; shrinkage | |
| B2 | Priors and diagnostics; non-centered parametrization | |
| B3 | Covariate, posterior predictive checks, LOO | |
| B4 | Decisions from posterior probabilities vs naive ranking | |
| R1 | BM25 baseline from scratch | |
| R2 | Embeddings, chunking, rerankers, retrieval metrics | |
| R3 | 30-question eval: BM25 vs dense retrieval | |
| R4 | Chunking experiment | |
| R5 | Vector store with metadata filters; hybrid search | |
| R6 | Cross-encoder reranking | |
| R7 | Cited answers with a deterministic faithfulness check | |
| R8 | Table-aware extraction from FDA drug labels | |
| P1 | Spark execution model | |
| P2 | DataFrame API: aggregations, windows, joins | |
| P3 | CSV to partitioned Parquet pipeline | |
| P4 | Query plans and one optimization | |
| P5 | Per-group scoring with `applyInPandas` | |

## Run it

Needs [uv](https://docs.astral.sh/uv/) and, for PySpark, Java 17.

```
uv sync
uv run python fetch.py bayes
uv run python fetch.py rag
uv run python fetch.py spark --sample-mb 50   # drop the flag for the full files (several GB)
```

Data lands in `data/` (not committed). All sources are public and need no account.
