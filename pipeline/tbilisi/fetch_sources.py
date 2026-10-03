"""Download everything Tbilisi's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/tbilisi/fetch_sources.py [--only register rail] [--force]

The register: Geostat's Statistical Business Register, 2,000-row pages
of JSON. The API has no column selection, so each page is reduced to
config.KEEP_COLUMNS plus three derived columns IN MEMORY, before anything is
written; no personal number, person's name, head, partner, contact or address
string reaches the disk. The API allows 50 requests per window and answers
429 with `retryAfter`: the script pauses between pages, honours retryAfter,
and writes the CSV only once every page is in (a partial pull leaves no file).

The rail: ONE Overpass query (config.OSM_JSON), through pipeline.osm.fetch().

Each download is recorded in outputs/tbilisi/provenance.json.
"""
import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline import osm  # noqa: E402
from pipeline.tbilisi import config  # noqa: E402

S = requests.Session()
S.headers["User-Agent"] = "expanded-heatmap (open-data portfolio map)"


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def record(key, **fields):
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    prov = {}
    if config.PROVENANCE_JSON.exists():
        prov = json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8"))
    prov[key] = fields
    config.PROVENANCE_JSON.write_bytes(
        (json.dumps(prov, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))


def get_page(page):
    """One page of the register, honouring the rate limit. A 429 (or a JSON
    body carrying retryAfter) waits and retries; anything else raises."""
    params = dict(config.GEOSTAT_QUERY, limit=config.GEOSTAT_PAGE_SIZE, page=page)
    for attempt in range(6):
        r = S.get(config.GEOSTAT_API, params=params, timeout=300)
        body = None
        try:
            body = r.json()
        except ValueError:
            pass
        retry = (body or {}).get("retryAfter") if isinstance(body, dict) else None
        if r.status_code == 429 or retry is not None:
            wait = max(int(retry or 60), 5) + 2
            print(f"    page {page}: rate limited, waiting {wait} s")
            time.sleep(wait)
            continue
        if r.status_code in (502, 503, 504):
            # The gateway in front of the API; a large page can outlast it.
            print(f"    page {page}: HTTP {r.status_code}, waiting 30 s")
            time.sleep(30)
            continue
        r.raise_for_status()
        if not isinstance(body, dict) or "data" not in body:
            sys.exit(f"page {page}: no `data` in the answer ({r.text[:200]!r})")
        return body
    sys.exit(f"page {page}: still refused after six waits")


def has_digit(s):
    return any(ch.isdigit() for ch in s)


def reduce_rows(rows):
    """Keep config.KEEP_COLUMNS and derive the three columns that need a
    dropped field, then forget the rest. Runs per page, in memory."""
    out = []
    for row in rows:
        keep = {c: row.get(c) for c in config.KEEP_COLUMNS}
        form = str(row.get("Legal_Form_ID") or "")
        person = form == config.INDIVIDUAL_ENTREPRENEUR_FORM
        keep["Full_Name"] = "" if person else (row.get("Full_Name") or "")
        factual = (row.get("Address2") or "").strip()
        legal = (row.get("Address") or "").strip()
        if not factual:
            keep["factual_address_key"] = ""
        elif person:
            keep["factual_address_key"] = "#"
        elif has_digit(factual):
            # A street address is kept only as a short hash, so step 2 can
            # find the commonest address at a point without storing any.
            norm = " ".join(factual.split()).casefold()
            keep["factual_address_key"] = "#" + hashlib.sha1(norm.encode("utf-8")).hexdigest()[:12]
        else:
            keep["factual_address_key"] = factual
        keep["legal_eq_factual"] = bool(factual) and factual == legal
        out.append(keep)
    return out


def fetch_register(force):
    dest = config.BUSINESSES_RAW_CSV
    if dest.exists() and not force:
        print(f"  cached: {dest.name}")
        return
    first = get_page(1)
    total = int(first["pagination"]["total"])
    pages = int(first["pagination"]["totalPages"])
    lo, hi = config.GEOSTAT_TOTAL_RANGE
    if not lo <= total <= hi:
        sys.exit(f"register total {total:,} outside {lo:,}-{hi:,}: a changed filter or "
                 f"register, not a refresh. Re-read docs/georgia_step0_endpoints.md")
    unexpected = set(config.PERSONAL_COLUMNS) - set(first["data"][0])
    if unexpected:
        sys.exit(f"the API no longer returns {sorted(unexpected)}: re-read its columns")
    print(f"  register: {total:,} active rows in {pages} pages")
    rows = reduce_rows(first["data"])
    del first
    for page in range(2, pages + 1):
        time.sleep(config.GEOSTAT_PAGE_PAUSE_S)
        body = get_page(page)
        rows.extend(reduce_rows(body["data"]))
        print(f"    page {page}/{pages}: {len(rows):,} rows")
        del body
    if len(rows) != total:
        sys.exit(f"{len(rows):,} rows for a total of {total:,}: a page came back short")
    df = pd.DataFrame(rows, columns=config.KEEP_COLUMNS + config.DERIVED_COLUMNS)
    if df["Stat_ID"].duplicated().any():
        sys.exit(f"{int(df['Stat_ID'].duplicated().sum())} Stat_IDs repeat: paging drifted")
    tmp = dest.with_suffix(".part")
    df.to_csv(tmp, index=False, encoding="utf-8", lineterminator="\n")
    tmp.replace(dest)
    data = dest.read_bytes()
    print(f"  {dest.name}: {len(df):,} rows, {len(data):,} bytes")
    record("geostat_register", file=dest.name, url=config.GEOSTAT_API,
           query=config.GEOSTAT_QUERY, rows=len(df), bytes=len(data),
           sha256=hashlib.sha256(data).hexdigest(), retrieved=now(),
           columns_written=list(df.columns), terms=config.GEOSTAT_TERMS_URL)


def fetch_rail(force):
    s, w, n, e = config.OSM_BBOX
    bbox = f"({s},{w},{n},{e})"
    q = ("[out:json][timeout:120];"
         f'rel["type"="route"]["route"="subway"]{bbox}->.r;'
         '(.r; rel(br.r)["type"="route_master"];)->.rr;'
         ".rr out body;"
         "node(r.r)->.n;.n out body;"
         "way(r.r)->.w;.w out geom;"
         f'node["station"="subway"]{bbox};out body;'
         f'rel["boundary"="administrative"]["name:en"="{config.OSM_BOUNDARY_NAME_EN}"]{bbox};'
         "out geom;")
    els, host = osm.fetch(q, config.OSM_JSON, force=force)
    rels = [x for x in els if x["type"] == "relation"]
    if not rels:
        sys.exit("  no relations came back - a FAILED fetch, not a negative")
    print(f"  rail and boundary: {len(els)} elements via {host}")
    data = config.OSM_JSON.read_bytes()
    record("osm", file=config.OSM_JSON.name, url=f"overpass ({host})", bytes=len(data),
           sha256=hashlib.sha256(data).hexdigest(), retrieved=now(), licence="ODbL 1.0")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-download cached files")
    ap.add_argument("--only", nargs="*", help="register, rail")
    args = ap.parse_args()
    only = set(args.only or ["register", "rail"])
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    if "register" in only:
        print("Geostat register:")
        fetch_register(args.force)
    if "rail" in only:
        print("\nOpenStreetMap:")
        fetch_rail(args.force)


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
