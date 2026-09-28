# Plan

Personal project. Bayesian modeling, retrieval, and PySpark, learned by building, on US public health data. For fun, for work, for life.

This file is the single source of truth: the plan, the rules, and the log. Tick boxes here.

## Data

| Track | Data | Source |
|---|---|---|
| Bayes | Hospital readmissions, FY2026, per hospital and condition | CMS Hospital Readmissions Reduction Program (data.cms.gov, dataset 9n3s-kdb3) |
| RAG | Clinical trial records | ClinicalTrials.gov API v2 |
| PySpark | Medicare Part D, by prescriber and drug, 2024 (tens of millions of rows) | CMS Medicare Part D Prescribers (data.cms.gov) |

`uv run python fetch.py <track>` downloads each.

## Rules

- **Artifact or it didn't happen.** A box is ticked with an artifact (notebook, script, table, write-up) plus a two-minute spoken explanation. Log date and link.
- **Five-minute grill.** A claim counts only if it survives five minutes of "why did you do it that way."
- **Order: Bayes, RAG, PySpark.** One box at a time.
- **Every session ends by ticking here and adding a log line.**

## Bayes (6 h), PyMC

Question: which hospitals truly readmit more than expected, and which just look bad because they're small?

- [ ] **B1** (1.5 h) Three models of hospital rates: no pooling, complete pooling, partial pooling (hierarchical logit). Plot the shrinkage. Explain why small hospitals move most. Evidence:
- [ ] **B2** (1.5 h) Priors and diagnostics: prior predictive check; R-hat, ESS, divergences; non-centered parametrization; show divergences before and after. Evidence:
- [ ] **B3** (2 h) Add a hospital-level covariate; posterior predictive checks; compare models with LOO (ArviZ). Evidence:
- [ ] **B4** (1 h) The decision: probability each hospital's rate exceeds the national rate vs the naive ranking. Where they disagree, and why it matters. Summary plus grill. Evidence:

## RAG (11 h)

Question: given a patient-style question, find the right trials and answer with citations that hold up.

- [ ] **R1** (1 h) Pull ~2,000 trial records for a few conditions; build a BM25 baseline retriever from scratch. Evidence:
- [ ] **R2** (1.5 h) Concepts, explained with the corpus at hand: embeddings, chunking, rerankers, recall@k, MRR, faithfulness. Evidence:
- [ ] **R3** (3 h) 30-question eval set with gold trial IDs; hit@3 and MRR for BM25 vs a sentence-transformer retriever. Evidence:
- [ ] **R4** (1 h) Chunking experiment: size and overlap on long trial descriptions, measured on the R3 eval. Evidence:
- [ ] **R5** (1 h) Vector store (local, e.g. Chroma or FAISS) with metadata filters (phase, status); hybrid BM25 plus vector. Evidence:
- [ ] **R6** (1 h) Cross-encoder reranker on the top 20; MRR gain. Evidence:
- [ ] **R7** (1 h) Answer with citations; a deterministic faithfulness check: every cited trial was retrieved, every quoted span exists in it. Evidence:
- [ ] **R8** (1 h) Multimodal-ish: FDA drug label PDFs with tables; text-only vs table-aware extraction, measured on five questions. Evidence:
- [ ] **R9** (0.5 h) Summary plus grill. Evidence:

## PySpark (9 h), local

Question: where does Medicare drug spending concentrate, by specialty, state and drug?

- [ ] **P1** (1.5 h) Concepts: lazy evaluation, DAG, transformations vs actions, partitions, shuffles, broadcast joins. Two minutes each, no notes. Evidence:
- [ ] **P2** (2 h) DataFrame drill on Part D: select, filter, withColumn, groupBy plus agg, a window (rank prescribers within specialty and state), a join to the by-provider table. Evidence:
- [ ] **P3** (2 h) Pipeline: raw CSV to cleaned Parquet partitioned by state; aggregate in Spark before any `toPandas()`. Evidence:
- [ ] **P4** (1 h) `.explain()` on P3; find the shuffle; one optimization (broadcast join or partition pruning); show the plan change and the timing. Evidence:
- [ ] **P5** (2 h) `applyInPandas`: a per-specialty model scoring cost per claim; flag outliers. Evidence:
- [ ] **P6** (0.5 h) Summary plus grill. Evidence:

Arithmetic: 6 + 11 + 9 = 26 h.

## Log

- **2026-09-28** Set up. Java 17 and uv environment; every track smoke-tested on real data: 18,330 hospital rows plus a PyMC fit; 2,000 trials with BM25, embeddings and FAISS; a local Spark job over a 138,429-row Part D sample. Next: B1.
