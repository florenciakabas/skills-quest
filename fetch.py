"""Download the public data for one track into data/.

    uv run python fetch.py bayes          # hospital readmissions, ~1 MB
    uv run python fetch.py rag            # clinical trial records, ~2,000 studies
    uv run python fetch.py spark          # Medicare Part D, several GB
    uv run python fetch.py spark --sample-mb 50   # first 50 MB of each file
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import requests

DATA = Path(__file__).parent / "data"

# CMS Hospital Readmissions Reduction Program, FY2026 (data.cms.gov/provider-data, dataset 9n3s-kdb3)
HRRP_URL = (
    "https://data.cms.gov/provider-data/sites/default/files/resources/"
    "a171bc36c488d3e0dc33ec63abb469a6_1770163617/FY_2026_Hospital_Readmissions_Reduction_Program_Hospital.csv"
)

# ClinicalTrials.gov API v2
TRIALS_URL = "https://clinicaltrials.gov/api/v2/studies"
TRIAL_CONDITIONS = ["type 2 diabetes", "heart failure", "breast cancer", "alzheimer disease"]
TRIALS_PER_CONDITION = 500

# CMS Medicare Part D Prescribers, data year 2024 (data.cms.gov)
PART_D_URLS = {
    "partd_by_provider_and_drug_2024.csv": (
        "https://data.cms.gov/sites/default/files/2026-05/0ae165f4-eb44-495d-8cac-67f4571b6b83/"
        "MUP_DPR_RY26_P04_V10_DY24_NPIBN.csv"
    ),
    "partd_by_provider_2024.csv": (
        "https://data.cms.gov/sites/default/files/2026-08/373e45e5-33ec-452c-9302-a4bdbc203459/"
        "mup_dpr_ry26_p04_v20_dy24_npi.csv"
    ),
}


def download(url: str, dest: Path, max_bytes: int | None = None) -> None:
    """Stream url to dest. With max_bytes, stop there and cut back to the last full line."""
    written = 0
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20):
                if max_bytes is not None and written + len(chunk) >= max_bytes:
                    chunk = chunk[: max_bytes - written]
                    chunk = chunk[: chunk.rfind(b"\n") + 1]
                    f.write(chunk)
                    written += len(chunk)
                    break
                f.write(chunk)
                written += len(chunk)
                print(f"\r{dest.name}: {written / 1e6:,.0f} MB", end="")
    print(f"\r{dest.name}: {written / 1e6:,.1f} MB")


def fetch_bayes() -> None:
    download(HRRP_URL, DATA / "hrrp_fy2026.csv")


def fetch_rag() -> None:
    out = DATA / "trials.jsonl"
    n = 0
    with open(out, "w", encoding="utf-8") as f:
        for condition in TRIAL_CONDITIONS:
            token, got = None, 0
            while got < TRIALS_PER_CONDITION:
                params = {"query.cond": condition, "pageSize": min(1000, TRIALS_PER_CONDITION - got)}
                if token:
                    params["pageToken"] = token
                r = requests.get(TRIALS_URL, params=params, timeout=60)
                r.raise_for_status()
                page = r.json()
                for study in page.get("studies", []):
                    f.write(json.dumps({"condition": condition, **study}) + "\n")
                    got += 1
                token = page.get("nextPageToken")
                if not token:
                    break
            n += got
            print(f"{condition}: {got} studies")
    print(f"trials.jsonl: {n} studies")


def fetch_spark(sample_mb: int | None) -> None:
    max_bytes = sample_mb * 1_000_000 if sample_mb else None
    for name, url in PART_D_URLS.items():
        download(url, DATA / name, max_bytes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("track", choices=["bayes", "rag", "spark"])
    parser.add_argument("--sample-mb", type=int, default=None, help="spark only: download just the first N MB")
    args = parser.parse_args()
    DATA.mkdir(exist_ok=True)
    {"bayes": fetch_bayes, "rag": fetch_rag, "spark": lambda: fetch_spark(args.sample_mb)}[args.track]()


if __name__ == "__main__":
    main()
