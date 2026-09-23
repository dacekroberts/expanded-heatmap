"""Download Rennes' raw inputs into data/rennes/raw/ (gitignored), and the
national SIRENE parquets into the shared country cache.

DELIBERATELY NOT NAMED step*.py. `drift_check.py` globs step*.py, so a download
living in a step would turn every drift check into a question about the current
upstream rather than about the committed code.

    python pipeline/rennes/fetch_sources.py [--force] [--skip-parquet]

WHERE THIS DIFFERS FROM TOULOUSE:

  * **The feed self-attests.** STAR's zip carries feed_info.txt with a real
    feed_end_date - Marseille's case - so staleness is read from the artifact
    and recorded here, not reconstructed from a catalogue timestamp.
  * **No catalogue call at all.** data.explore.star.fr's API runs on a
    domain-wide daily quota shared by every anonymous caller, and it was spent
    when first probed. The feed comes from Opendatasoft's file host, which does
    not count against it, so nothing here depends on that quota.
  * **A second boundary file**: every commune of Rennes Métropole, used only to
    NAME the commune an excluded station lies in.

The parquets are shared and national - 3 GB for the pair, read by all five
French cities - so they land in `france.SHARED_RAW` and a second city downloads
nothing.
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
from pipeline.rennes import config

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
        sys.exit(f"  gtfs.zip is not a zip - first bytes {body[:8]!r}")
    config.GTFS_ZIP.write_bytes(body)
    print(f"  {'gtfs.zip':20s} {len(body):13,} bytes")
    return body


def feed_window(body):
    """The feed's own declared validity - Rennes HAS one, like Marseille."""
    with zipfile.ZipFile(io.BytesIO(body)) as z:
        if "feed_info.txt" not in z.namelist():
            print("  ⚠ feed_info.txt has DISAPPEARED - config.GTFS_SELF_ATTESTS "
                  "says True and should be re-measured")
            return {"missing_feed_info": True}
        with z.open("feed_info.txt") as fh:
            row = next(csv.DictReader(io.TextIOWrapper(fh, "utf-8-sig")), {})
    keep = {k: v for k, v in row.items()
            if k in ("feed_publisher_name", "feed_start_date", "feed_end_date",
                     "feed_version")}
    print(f"  feed self-attests: {keep}")
    return keep


def fetch_polygon(url, dest, label):
    body = _get(url)
    obj = json.loads(body)
    # `fields=contour` answers 200 with a 120-byte POINT; scoping a build to one
    # coordinate produces an empty map, not an error.
    feats = obj.get("features") or [obj]
    kinds = {(f.get("geometry") or {}).get("type") for f in feats}
    if not kinds <= {"Polygon", "MultiPolygon"}:
        sys.exit(f"  {label} holds {sorted(map(str, kinds))}, not polygons "
                 f"({len(body)} bytes). Check the URL says geometry=contour.")
    dest.write_bytes(body)
    print(f"  {label:20s} {len(body):13,} bytes  ({len(feats)} "
          f"feature{'s' if len(feats) != 1 else ''})")
    return obj


def check_metropole(obj):
    """The EPCI file must hold Rennes AND the two communes line b reaches.

    A wrong EPCI code would answer 200 with some other intercommunality's
    communes, and step 1 would then fail to name an excluded station - loudly,
    but later and less legibly than here.
    """
    codes = {f["properties"].get("code") for f in obj.get("features", [])}
    need = {config.BOUNDARY_COMMUNE_CODE, "35051", "35281"}
    if not need <= codes:
        sys.exit(f"  EPCI {config.METROPOLE_EPCI_CODE} lacks {sorted(need - codes)} "
                 f"- is it still Rennes Métropole?")
    print(f"  EPCI {config.METROPOLE_EPCI_CODE}: {len(codes)} communes, "
          f"including Rennes, Cesson-Sévigné and Saint-Jacques-de-la-Lande")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--skip-parquet", action="store_true")
    args = ap.parse_args()
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)

    prov = {"fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "gtfs_url": config.GTFS_URL,
            "boundary_url": config.BOUNDARY_URL,
            "metropole_communes_url": config.METROPOLE_COMMUNES_URL,
            "gtfs_self_attests": config.GTFS_SELF_ATTESTS}

    print("Rail and boundaries:")
    if config.GTFS_ZIP.exists() and not args.force:
        print(f"  {'gtfs.zip':20s} cached")
        prov["feed_info"] = feed_window(config.GTFS_ZIP.read_bytes())
    else:
        prov["feed_info"] = feed_window(fetch_gtfs())
    if config.CITY_BOUNDARY_GEOJSON.exists() and not args.force:
        print(f"  {'city_boundary':20s} cached")
    else:
        fetch_polygon(config.BOUNDARY_URL, config.CITY_BOUNDARY_GEOJSON,
                      "city_boundary")
    if config.METRO_COMMUNES_GEOJSON.exists() and not args.force:
        print(f"  {'metropole_communes':20s} cached")
        check_metropole(json.loads(config.METRO_COMMUNES_GEOJSON.read_bytes()))
    else:
        check_metropole(fetch_polygon(config.METROPOLE_COMMUNES_URL,
                                      config.METRO_COMMUNES_GEOJSON,
                                      "metropole_communes"))

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
