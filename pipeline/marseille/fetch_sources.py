"""Download Marseille's raw inputs into data/marseille/raw/ (gitignored), and
the national SIRENE parquets into the shared country cache.

DELIBERATELY NOT NAMED step*.py. `drift_check.py` globs step*.py, so a download
living in a step would turn every drift check into a question about the current
upstream rather than about the committed code.

    python pipeline/marseille/fetch_sources.py [--force] [--skip-parquet]

TWO THINGS THIS DIFFERS FROM PARIS ON:

  * **The parquets are shared.** They are national, 3 GB for the pair, and five
    French cities read the same bytes - so they land in `france.SHARED_RAW` and
    a second city downloads nothing. Paris's run already populated it.
  * **The feed SELF-ATTESTS.** `feed_info.txt` carries Mecatran and
    20260922-20261231, so staleness is readable from the artifact. Paris's has
    no feed_info.txt at all and needed the NAP's metadata instead. The fetch
    date is still recorded, because a licence can require the snapshot date to
    be DISPLAYED even where the file can be checked for freshness.
"""
import argparse
import csv
import io
import json
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries import france
from pipeline.marseille import config

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def _get(url, timeout=900):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _stream(url, dest, label, timeout=1800):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        total = int(r.headers.get("Content-Length", 0))
        done = 0
        tmp = dest.with_suffix(dest.suffix + ".part")
        with open(tmp, "wb") as fh:
            while True:
                chunk = r.read(1 << 22)
                if not chunk:
                    break
                fh.write(chunk)
                done += len(chunk)
                if total and done % (1 << 28) < (1 << 22):
                    print(f"    {label}: {done / 1e6:,.0f} / {total / 1e6:,.0f} MB",
                          flush=True)
    tmp.replace(dest)
    print(f"  {label:20s} {done:13,} bytes")
    return done


def resolve_parquet(slug, title_test, label):
    """Find a dataset's parquet resource through the data.gouv API.

    Never hard-coded: the filename carries its own monthly release date, so a
    pinned URL rots every month.
    """
    meta = json.loads(_get(f"https://www.data.gouv.fr/api/1/datasets/{slug}/"))
    hits = [r for r in meta.get("resources", [])
            if title_test(r.get("title", ""))
            and "parquet" in (r.get("format", "") or "").lower()]
    if len(hits) != 1:
        titles = [r.get("title", "")[:64] for r in meta.get("resources", [])][:15]
        sys.exit(f"  {label}: expected 1 parquet resource, got {len(hits)}. "
                 f"Titles seen:\n    " + "\n    ".join(titles))
    return hits[0]


def fetch_gtfs():
    body = _get(config.GTFS_URL)
    # Magic bytes, never the filename the server claims.
    if body[:4] != b"PK\x03\x04":
        sys.exit(f"  gtfs.zip is not a zip - first bytes {body[:8]!r}. The feed "
                 f"URL carries an API key; a key the operator has rotated "
                 f"would look like this.")
    config.GTFS_ZIP.write_bytes(body)
    print(f"  {'gtfs.zip':20s} {len(body):13,} bytes")
    return body


def feed_window(body):
    """The feed's own declared validity - Marseille HAS one, unlike Paris."""
    with zipfile.ZipFile(io.BytesIO(body)) as z:
        if "feed_info.txt" not in z.namelist():
            print("  ⚠ no feed_info.txt - the artifact declares no validity "
                  "window, so staleness must come from elsewhere (Paris's case)")
            return {}
        with z.open("feed_info.txt") as fh:
            row = next(csv.DictReader(io.TextIOWrapper(fh, "utf-8-sig")), {})
    keep = {k: v for k, v in row.items()
            if k in ("feed_publisher_name", "feed_start_date", "feed_end_date",
                     "feed_version")}
    print(f"  feed self-attests: {keep}")
    return keep


def fetch_boundary():
    body = _get(config.BOUNDARY_URL)
    obj = json.loads(body)
    geom = (obj.get("geometry") or {}).get("type")
    # `fields=contour` answers 200 with a 120-byte POINT; scoping a build to one
    # coordinate produces an empty map, not an error.
    if geom not in ("Polygon", "MultiPolygon"):
        sys.exit(f"  boundary is a {geom!r}, not a polygon ({len(body)} bytes). "
                 f"Check the URL says geometry=contour, not fields=contour.")
    config.CITY_BOUNDARY_GEOJSON.write_bytes(body)
    print(f"  {'city_boundary':20s} {len(body):13,} bytes  ({geom})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--skip-parquet", action="store_true")
    args = ap.parse_args()
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)

    prov = {"fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "gtfs_url": config.GTFS_URL.split("?")[0] + "?apiKey=<in config>",
            "boundary_url": config.BOUNDARY_URL}

    print("Rail and boundary:")
    if config.GTFS_ZIP.exists() and not args.force:
        print(f"  {'gtfs.zip':20s} cached")
        prov["feed_info"] = feed_window(config.GTFS_ZIP.read_bytes())
    else:
        prov["feed_info"] = feed_window(fetch_gtfs())
    if config.CITY_BOUNDARY_GEOJSON.exists() and not args.force:
        print(f"  {'city_boundary':20s} cached")
    else:
        fetch_boundary()

    print("\nNational register (shared across every French city):")
    france.SHARED_RAW.mkdir(parents=True, exist_ok=True)
    if args.skip_parquet:
        print("  SKIPPED (--skip-parquet)")
    else:
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
                print(f"  {label:20s} cached ({dest.stat().st_size:,} bytes) "
                      f"- shared, downloaded by whichever French city ran first")
                continue
            res = resolve_parquet(slug, test, label)
            print(f"  {label}: {res.get('title', '')[:64]}")
            _stream(res["url"], dest, label)

    config.PROVENANCE_JSON.write_text(
        json.dumps(prov, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}")
