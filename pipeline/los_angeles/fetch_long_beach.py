"""Download Long Beach's active, in-city, storefront-eligible business licences
for Los Angeles (Regional). DELIBERATELY NOT NAMED step*.py, so drift_check.py
never runs it; step 2 reads the cache and exits naming this script.

    python pipeline/los_angeles/fetch_long_beach.py [--force]

The City's "Business Licenses Public View" layer (MapsLB), queried with the
server-side filter in config.LONG_BEACH_WHERE and ONLY the columns in
config.LONG_BEACH_FIELDS, paged by OBJECTID. FULLNAME (the licence holder's
name) is never requested, and the script raises if any response carries it.
Points come back in EPSG:4326 (outSR). A sidecar JSON records the query, the
row count, the layer's last edit date and the retrieval time.
"""
import argparse
import csv
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.los_angeles import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (portfolio map; see the project's public repo)"}
PAGE = 2000  # the layer's maxRecordCount, read 2026-10-03
META = config.LONG_BEACH_CSV.with_suffix(".json")


def _get(url, params):
    req = urllib.request.Request(url + "?" + urllib.parse.urlencode(params), headers=HEADERS)
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    if "error" in d:
        sys.exit(f"Long Beach layer error: {d['error']}")
    return d


def main():
    ap = argparse.ArgumentParser(description="Download Long Beach's licence layer.")
    ap.add_argument("--force", action="store_true")
    if config.LONG_BEACH_CSV.exists() and not ap.parse_args().force:
        print(f"{config.LONG_BEACH_CSV.name} cached; --force re-downloads")
        return
    layer = _get(config.LONG_BEACH_URL.rsplit("/query", 1)[0], {"f": "json"})
    fields = list(config.LONG_BEACH_FIELDS)
    rows, offset = [], 0
    while True:
        d = _get(config.LONG_BEACH_URL, {
            "where": config.LONG_BEACH_WHERE, "outFields": ",".join(fields),
            "returnGeometry": "true", "outSR": "4326", "orderByFields": "OBJECTID",
            "resultOffset": offset, "resultRecordCount": PAGE, "f": "json"})
        feats = d.get("features", [])
        for f in feats:
            a = f["attributes"]
            bad = set(a) & set(config.LONG_BEACH_FORBIDDEN)
            if bad:
                sys.exit(f"the layer returned {sorted(bad)} although not requested - stopping")
            g = f.get("geometry") or {}
            rows.append({**{k: a.get(k) for k in fields},
                         "latitude": g.get("y"), "longitude": g.get("x")})
        print(f"  offset {offset:>6}: {len(feats)} rows")
        if len(feats) < PAGE and not d.get("exceededTransferLimit"):
            break
        offset += len(feats)
    ids = [r["OBJECTID"] for r in rows]
    if len(ids) != len(set(ids)):
        sys.exit("OBJECTID repeats across pages - the paging is not stable; re-run")
    config.LONG_BEACH_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(config.LONG_BEACH_CSV, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields + ["latitude", "longitude"], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    edited = (layer.get("editingInfo") or {}).get("dataLastEditDate")
    meta = {"url": config.LONG_BEACH_URL, "where": config.LONG_BEACH_WHERE, "fields": fields,
            "rows": len(rows),
            "data_last_edit": (datetime.fromtimestamp(edited / 1000, timezone.utc)
                               .isoformat(timespec="seconds") if edited else None),
            "retrieved": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    META.write_bytes(json.dumps(meta, indent=2).encode("utf-8"))
    print(f"\n{len(rows):,} rows -> {config.LONG_BEACH_CSV.name}; layer last edited "
          f"{meta['data_last_edit']}")


if __name__ == "__main__":
    main()
