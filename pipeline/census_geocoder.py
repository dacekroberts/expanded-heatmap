"""US Census Bureau bulk geocoder, for cities whose business export has
addresses but missing or corrupt coordinates (Los Angeles: 9% of storefront
rows). Free, no API key, US addresses only.

Batches are cached under the city's raw folder, keyed by a hash of the
batch's own contents, so re-running skips completed batches (a timeout
partway through costs one batch) and - unlike a bare batch-number key - a
changed input can never be served a stale answer. That also keeps
pipeline/drift_check.py deterministic and off the network after the first run.

Interface: geocode_addresses() returns only the rows the Census matched;
callers decide what to do with the rest and must sanity-check the returned
coordinates against the city's bounds.
"""

import hashlib
import io
import re
import time
from pathlib import Path

import pandas as pd
import requests

GEOCODER_URL = "https://geocoding.geo.census.gov/geocoder/locations/addressbatch"
BENCHMARK = "Public_AR_Current"
BATCH_SIZE = 5000  # under the 10k per-request ceiling; smaller batches fail less often
RESULT_COLUMNS = ["id", "input_address", "match", "match_type", "matched_address",
                  "coordinates", "tiger_line_id", "side"]

# Suite/unit designators are the main cause of misses; drop them and everything
# after (the street number and name are what the geocoder needs).
_UNIT_TAIL = re.compile(r"\s+(SUITE|STE|UNIT|APT|BLDG|FL|FLOOR|RM|ROOM)\b.*$|\s+#.*$", re.IGNORECASE)


def normalize_street(street) -> str:
    if not isinstance(street, str):
        return ""
    return " ".join(_UNIT_TAIL.sub("", street.strip()).split())


def _geocode_batch(payload: pd.DataFrame, cache_dir: Path, batch_num: int) -> pd.DataFrame:
    csv_bytes = payload.to_csv(index=False, header=False).encode("utf-8")
    key = hashlib.sha1(csv_bytes).hexdigest()[:10]
    cache_file = cache_dir / f"batch_{batch_num:03d}_{key}.csv"
    if cache_file.exists():
        print(f"  batch {batch_num}: cached")
        text = cache_file.read_text(encoding="utf-8")
    else:
        response = requests.post(
            GEOCODER_URL,
            files={"addressFile": ("batch.csv", csv_bytes, "text/csv")},
            data={"benchmark": BENCHMARK},
            timeout=600,
        )
        response.raise_for_status()
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(response.text, encoding="utf-8")
        text = response.text
        print(f"  batch {batch_num}: {len(payload):,} addresses geocoded")
    return pd.read_csv(io.StringIO(text), header=None, names=RESULT_COLUMNS, dtype=str)


def geocode_addresses(df: pd.DataFrame, *, id_col: str, street_col: str, zip_col: str,
                      city: str, state: str, cache_dir: Path) -> pd.DataFrame:
    """Geocode df's addresses. Returns DataFrame[id, latitude, longitude,
    match_type] for matched rows only (Census returns "lon,lat" in one field;
    it is split here, in that order)."""
    payload = pd.DataFrame({
        "id": df[id_col].astype(str),
        "street": df[street_col].map(normalize_street),
        "city": city,
        "state": state,
        "zip": df[zip_col].fillna("").astype(str).str[:5],
    })
    results = []
    for i in range(0, len(payload), BATCH_SIZE):
        results.append(_geocode_batch(payload.iloc[i:i + BATCH_SIZE], cache_dir, i // BATCH_SIZE))
        time.sleep(1)
    if not results:
        return pd.DataFrame(columns=["id", "latitude", "longitude", "match_type"])
    geo = pd.concat(results, ignore_index=True)
    matched = geo[geo["match"] == "Match"].copy()
    coords = matched["coordinates"].str.split(",", expand=True)
    matched["longitude"] = pd.to_numeric(coords[0], errors="coerce")
    matched["latitude"] = pd.to_numeric(coords[1], errors="coerce")
    return matched.dropna(subset=["latitude", "longitude"])[["id", "latitude", "longitude", "match_type"]]
