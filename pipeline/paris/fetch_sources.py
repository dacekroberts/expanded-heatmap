"""Download Paris's four raw inputs into data/paris/raw/ (gitignored).

DELIBERATELY NOT NAMED step*.py. `drift_check.py` globs step*.py, so a download
living in a step would turn every drift check into a question about the current
upstream rather than about the committed code.

    python pipeline/paris/fetch_sources.py [--force] [--skip-parquet]

One GTFS, one boundary, and two parquets totalling ~3 GB. `--skip-parquet` gets
the rail leg moving without waiting for the business leg.

WHAT THIS SCRIPT DOES THAT NO OTHER CITY'S DOES: it records the feed's
last-updated date and update interval, because **nothing inside the artifact
carries them.** The IDFM zip has no feed_info.txt, and notice 24 (Licence
Mobilites Art. 5.7) requires both to be DISPLAYED. They are only available
here, at download time, from the National Access Point's metadata - so a fetch
that does not capture them makes the city undeployable rather than merely
undocumented.
"""
import argparse
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.paris import config

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def _get(url, timeout=600):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _stream(url, dest, label, timeout=1800):
    """Download to disk in chunks.

    The SIRENE parquet is 2.2 GB; reading it into memory the way the other
    cities' fetchers read a CSV would need the whole file resident before a
    single byte is written.
    """
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        total = int(r.headers.get("Content-Length", 0))
        done = 0
        tmp = dest.with_suffix(dest.suffix + ".part")
        with open(tmp, "wb") as fh:
            while True:
                chunk = r.read(1 << 22)          # 4 MB
                if not chunk:
                    break
                fh.write(chunk)
                done += len(chunk)
                if total and done % (1 << 28) < (1 << 22):   # every ~256 MB
                    print(f"    {label}: {done / 1e6:,.0f} / {total / 1e6:,.0f} MB",
                          flush=True)
    tmp.replace(dest)
    print(f"  {label:20s} {done:13,} bytes")
    return done


def resolve_parquet(slug, title_test, label):
    """Find a dataset's parquet resource through the data.gouv API.

    Never hard-coded: the filename carries its own monthly release date
    ("01 septembre 2026"), so a pinned URL rots every month. Madrid's did.
    """
    meta = json.loads(_get(f"https://www.data.gouv.fr/api/1/datasets/{slug}/"))
    hits = [r for r in meta.get("resources", [])
            if title_test(r.get("title", ""))
            and "parquet" in (r.get("format", "") or "").lower()]
    if not hits:
        titles = [r.get("title", "")[:64] for r in meta.get("resources", [])][:15]
        sys.exit(f"  {label}: no parquet resource matched. Titles seen:\n    "
                 + "\n    ".join(titles))
    if len(hits) > 1:
        sys.exit(f"  {label}: {len(hits)} parquet resources matched, expected 1:\n    "
                 + "\n    ".join(r.get("title", "")[:64] for r in hits))
    return hits[0]


def fetch_gtfs():
    body = _get(config.PARIS_GTFS_URL)
    # Magic bytes, never the filename the server claims. A delegated download
    # once returned a PNG under a CSV's name elsewhere in this project.
    if body[:4] != b"PK\x03\x04":
        sys.exit(f"  gtfs.zip is not a zip - first bytes {body[:8]!r}")
    config.GTFS_ZIP.write_bytes(body)
    print(f"  {'gtfs.zip':20s} {len(body):13,} bytes")
    return len(body)


def fetch_boundary():
    body = _get(config.BOUNDARY_URL)
    obj = json.loads(body)
    geom = (obj.get("geometry") or {}).get("type")
    # THE TRAP THIS CHECK EXISTS FOR: `fields=contour` answers 200 with a
    # 120-byte Point - the commune's centre - and scoping a build to one
    # coordinate produces an empty map, not an error.
    if geom not in ("Polygon", "MultiPolygon"):
        sys.exit(f"  boundary is a {geom!r}, not a polygon ({len(body)} bytes). "
                 f"Check that the URL says geometry=contour, not fields=contour.")
    config.CITY_BOUNDARY_GEOJSON.write_bytes(body)
    print(f"  {'city_boundary':20s} {len(body):13,} bytes  ({geom})")
    return obj


def nap_metadata():
    """The two Art. 5.7 values, which exist nowhere inside the zip."""
    try:
        datasets = json.loads(_get(config.NAP_API, timeout=180))
    except Exception as exc:                      # noqa: BLE001
        print(f"  NAP metadata unavailable ({type(exc).__name__}) - the fetch "
              f"date is still recorded, but the update interval is not.")
        return {}
    for d in datasets:
        for r in (d.get("resources") or []):
            if r.get("original_url") == config.PARIS_GTFS_URL or \
                    r.get("url") == config.PARIS_GTFS_URL:
                md = r.get("metadata") or {}
                return {
                    "dataset_title": d.get("title"),
                    "dataset_id": d.get("id"),
                    "page_url": d.get("page_url"),
                    "licence": d.get("licence"),
                    "updated": d.get("updated") or r.get("updated"),
                    "start_date": md.get("start_date"),
                    "end_date": md.get("end_date"),
                }
    print("  the IDFM resource was not found in the NAP listing - recording "
          "the fetch date only.")
    return {}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--skip-parquet", action="store_true",
                    help="rail leg only; the two parquets are ~3 GB")
    args = ap.parse_args()
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)

    prov = {"fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}

    print("Rail and boundary:")
    if config.GTFS_ZIP.exists() and not args.force:
        print(f"  {'gtfs.zip':20s} cached")
    else:
        prov["gtfs_bytes"] = fetch_gtfs()
    if config.CITY_BOUNDARY_GEOJSON.exists() and not args.force:
        print(f"  {'city_boundary':20s} cached")
    else:
        fetch_boundary()
    if config.IDF_COMMUNES_GEOJSON.exists() and not args.force:
        print(f"  {'idf_communes':20s} cached")
    else:
        body = _get(config.IDF_COMMUNES_URL)
        obj = json.loads(body)
        feats = obj.get("features", [])
        polys = sum(1 for f in feats
                    if (f.get("geometry") or {}).get("type")
                    in ("Polygon", "MultiPolygon"))
        if polys < 1000:
            sys.exit(f"  idf_communes: {polys} polygons of {len(feats)} "
                     f"features - Ile-de-France has ~1,268 communes, so this "
                     f"is a truncated or point-geometry response.")
        config.IDF_COMMUNES_GEOJSON.write_bytes(body)
        print(f"  {'idf_communes':20s} {len(body):13,} bytes  "
              f"({polys:,} polygons)")

    prov["gtfs_url"] = config.PARIS_GTFS_URL
    prov["boundary_url"] = config.BOUNDARY_URL
    prov["nap"] = nap_metadata()

    if not args.skip_parquet:
        print("\nBusiness register (large):")
        jobs = [
            (config.SIRENE_DATASET_SLUG,
             lambda t: t.startswith(config.SIRENE_RESOURCE_TITLE_PREFIX),
             config.SIRENE_PARQUET, "sirene_etab"),
            (config.GEOLOC_DATASET_SLUG,
             lambda t: config.GEOLOC_RESOURCE_TITLE_CONTAINS in t.lower(),
             config.GEOLOC_PARQUET, "sirene_geoloc"),
        ]
        for slug, test, dest, label in jobs:
            if dest.exists() and not args.force:
                print(f"  {label:20s} cached ({dest.stat().st_size:,} bytes)")
                continue
            res = resolve_parquet(slug, test, label)
            print(f"  {label}: {res.get('title', '')[:64]}")
            _stream(res["url"], dest, label)
            prov[label] = {"title": res.get("title"), "url": res["url"],
                           "filesize": res.get("filesize")}
    else:
        print("\nBusiness register: SKIPPED (--skip-parquet)")

    config.PROVENANCE_JSON.write_text(
        json.dumps(prov, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}")
    nap = prov.get("nap") or {}
    if nap.get("end_date"):
        print(f"  feed valid to {nap['end_date']} (NAP metadata, NOT the zip - "
              f"there is no feed_info.txt)")
    print("  these two values are what notice 24 requires the page to DISPLAY.")
