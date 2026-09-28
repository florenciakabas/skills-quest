# skills-quest

Bayesian modeling, retrieval, and PySpark, learned by building, on US public health data.

| Track | Question | Data |
|---|---|---|
| Bayes (PyMC) | Which hospitals truly readmit more than expected, and which only look bad because they're small? | CMS Hospital Readmissions Reduction Program, FY2026 |
| Retrieval | Given a patient-style question, find the right clinical trials and answer with citations that hold up. | ClinicalTrials.gov API |
| PySpark | Where does Medicare drug spending concentrate, by specialty, state and drug? | CMS Medicare Part D Prescribers, 2024 |

## Plan and progress

[PLAN.md](PLAN.md): every step, its rules, and the log.

## Run it

Needs [uv](https://docs.astral.sh/uv/) and, for PySpark, Java 17.

```
uv sync
uv run python fetch.py bayes
uv run python fetch.py rag
uv run python fetch.py spark --sample-mb 50   # drop the flag for the full files (several GB)
```

Data lands in `data/` (not committed). All sources are public and need no account.
