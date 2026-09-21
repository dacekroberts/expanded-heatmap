"""Download Boston's five raw inputs. Run this before the steps.

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline.

    python pipeline/boston/fetch_sources.py [--force]

The food source is the only awkward one. It is a 902,651-row violation-level
inspection history, and what this build needs is one row per active premises,
so the collapse happens SERVER-SIDE in SQL rather than by downloading the lot:
CKAN's datastore_search_sql accepts GROUP BY, so the download is ~2,600 rows
instead of ~900,000.
"""

import argparse
import csv
import io
import sys
import zipfile
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.boston.config import (  # noqa: E402
    BOUNDARY_ENVELOPE,
    BOUNDARY_SERVICE_URL,
    CANNABIS_CSV,
    CANNABIS_RESOURCE,
    CKAN_SQL_URL,
    DATA_RAW,
    GTFS_URL,
    GTFS_ZIP,
    ISD_FOOD_CSV,
    ISD_FOOD_RESOURCE,
    LICENSING_BOARD_CSV,
    LICENSING_BOARD_RESOURCE,
    TOWN_BOUNDARIES_GEOJSON,
)

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}

# One row per active premises. MIN() on the descriptive columns is safe because
# they are constant within a property_id + licensecat group; `location` is the
# "(lat, lon)" string this file publishes instead of numeric columns.
#
# `businessname`, NOT `dbaname`: in this registry dbaname is blank on 99.0% of
# rows and businessname always holds the trade name - the reverse of every
# other city here. `legalowner`, `namelast` and `namefirst` exist in this table
# and are deliberately NOT selected: they are people's names.
ISD_SQL = f"""
SELECT "property_id",
       MIN("businessname")  AS businessname,
       MIN("licensecat")    AS licensecat,
       MIN("descript")      AS descript,
       MIN("address")       AS address,
       MIN("city")          AS city,
       MIN("zip")           AS zip,
       MIN("location")      AS location
FROM "{ISD_FOOD_RESOURCE}"
WHERE "licstatus" = 'Active'
  AND "property_id" IS NOT NULL AND "property_id" <> ''
GROUP BY "property_id", "licensecat"
"""

# Package stores only - the rest of this register is the same restaurants as
# the ISD source, plus dormitories and clubs. `applicant`, `manager`,
# `day_phone` and `evening_phone` exist here and are NOT selected: names and
# contact details.
LICENSING_BOARD_SQL = f"""
SELECT "license_num", "business_name", "dba_name", "license_type",
       "address", "city", "zip", "gpsx", "gpsy"
FROM "{LICENSING_BOARD_RESOURCE}"
WHERE "status" = 'Active'
  AND ("license_type" LIKE 'Retail%' OR "license_type" = 'Druggist')
"""

CANNABIS_SQL = f"""
SELECT "license_num", "business_name", "dba_name", "license_type",
       "address", "city", "zip", "gpsx", "gpsy"
FROM "{CANNABIS_RESOURCE}"
WHERE "status" = 'Active'
"""


def ckan_sql(sql: str, out_path: Path, label: str, force: bool):
    if out_path.exists() and not force:
        print(f"have {out_path.name} ({out_path.stat().st_size:,} bytes) - skipping")
        return
    r = requests.get(CKAN_SQL_URL, params={"sql": sql}, timeout=600,
                     headers=HEADERS)
    if r.status_code != 200:
        sys.exit(f"{label}: HTTP {r.status_code}\n{r.text[:400]}")
    j = r.json()
    if not j.get("success"):
        sys.exit(f"{label}: CKAN reported failure\n{str(j)[:400]}")
    records = j["result"]["records"]
    if not records:
        sys.exit(f"{label}: query returned 0 rows - the resource id or a "
                 f"column name has probably changed upstream.")
    fields = [f["id"] for f in j["result"]["fields"] if f["id"] != "_full_text"]
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    tmp = out_path.with_suffix(".partial")
    with open(tmp, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(records)
    tmp.replace(out_path)
    print(f"{label}: wrote {len(records):,} rows to {out_path}")


def fetch_gtfs(force: bool):
    if GTFS_ZIP.exists() and not force:
        print(f"have {GTFS_ZIP.name} ({GTFS_ZIP.stat().st_size:,} bytes) - skipping")
        return
    r = requests.get(GTFS_URL, timeout=900, headers=HEADERS)
    if r.status_code != 200 or r.content[:2] != b"PK":
        sys.exit(f"GTFS download failed: HTTP {r.status_code}, "
                 f"{len(r.content):,} bytes")
    zipfile.ZipFile(io.BytesIO(r.content)).testzip()
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    GTFS_ZIP.write_bytes(r.content)
    print(f"GTFS: wrote {len(r.content):,} bytes to {GTFS_ZIP}")


def fetch_boundaries(force: bool):
    if TOWN_BOUNDARIES_GEOJSON.exists() and not force:
        print(f"have {TOWN_BOUNDARIES_GEOJSON.name} "
              f"({TOWN_BOUNDARIES_GEOJSON.stat().st_size:,} bytes) - skipping")
        return
    r = requests.get(f"{BOUNDARY_SERVICE_URL}/query", params={
        "where": "1=1",
        "geometry": BOUNDARY_ENVELOPE,
        "geometryType": "esriGeometryEnvelope",
        "spatialRel": "esriSpatialRelIntersects",
        "inSR": "4326", "outSR": "4326",
        "outFields": "TOWN",
        "f": "geojson"}, timeout=600, headers=HEADERS)
    if r.status_code != 200 or b'"features"' not in r.content:
        sys.exit(f"boundary download failed: HTTP {r.status_code}\n"
                 f"{r.text[:400]}")
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    TOWN_BOUNDARIES_GEOJSON.write_bytes(r.content)
    import json
    n = len(json.loads(r.content)["features"])
    print(f"boundaries: wrote {n} town polygon(s), "
          f"{len(r.content):,} bytes to {TOWN_BOUNDARIES_GEOJSON}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    fetch_gtfs(args.force)
    fetch_boundaries(args.force)
    ckan_sql(ISD_SQL, ISD_FOOD_CSV, "ISD food (active, one row per premises)",
             args.force)
    ckan_sql(LICENSING_BOARD_SQL, LICENSING_BOARD_CSV,
             "Licensing Board (package stores)", args.force)
    ckan_sql(CANNABIS_SQL, CANNABIS_CSV, "Cannabis", args.force)


if __name__ == "__main__":
    main()
