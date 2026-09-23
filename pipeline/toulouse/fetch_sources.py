"""Download Toulouse's raw inputs into data/toulouse/raw/ (gitignored), and the
national SIRENE parquets into the shared country cache.

DELIBERATELY NOT NAMED step*.py. `drift_check.py` globs step*.py, so a download
living in a step would turn every drift check into a question about the current
upstream rather than about the committed code.

    python pipeline/toulouse/fetch_sources.py [--force] [--skip-parquet]

WHERE THIS DIFFERS FROM MARSEILLE:

  * **The feed does NOT self-attest.** There is no feed_info.txt at all - the
    zip carries 11 files and that is not one of them. This is Paris's gap, not
    Marseille's Mecatran window, so staleness is unknowable from the artifact.
  * **But a second attestation DOES exist**, which Paris had to go to the NAP
    for: Toulouse Métropole's Opendatasoft catalogue publishes a `modified`
    timestamp for the dataset. Captured here alongside the fetch date, so the
    provenance record carries the publisher's own word for when the data
    changed and not merely when this machine downloaded it.
  * **No API key.** Marseille's URL carries one (published by the operator);
    this one is a bare public path. The long file id in it IS load-bearing -
    see the note in config.GTFS_URL.

The parquets are shared and national - 3 GB for the pair, read by all five
French cities - so they land in `france.SHARED_RAW` and a second city downloads
nothing. Paris's run already populated it.
"""
import argparse
import io
import json
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries import france
from pipeline.toulouse import config

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}

# The catalogue record behind config.GTFS_URL. Read for its `modified` field
# only - the file itself comes from the download path in the config.
CATALOGUE_URL = ("https://data.toulouse-metropole.fr/api/datasets/1.0/search/"
                 "?q=tisseo-gtfs&rows=5")


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
    # Magic bytes, never the filename the server claims. A truncated file id
    # returns a 404 HTML page here, which would otherwise be written as a zip.
    if body[:4] != b"PK\x03\x04":
        sys.exit(f"  gtfs.zip is not a zip - first bytes {body[:8]!r}. A "
                 f"truncated file id in GTFS_URL returns 404 'Unknown image' "
                 f"rather than refusing, and lands here.")
    config.GTFS_ZIP.write_bytes(body)
    print(f"  {'gtfs.zip':20s} {len(body):13,} bytes")
    return body


def feed_window(body):
    """Toulouse has NO feed_info.txt. Assert the absence rather than assume it.

    Paris shipped the same gap. If a future refresh adds one, this prints it
    and the config's GTFS_SELF_ATTESTS should be revisited - so the check is
    not merely defensive, it reports a change in the publisher's behaviour.
    """
    with zipfile.ZipFile(io.BytesIO(body)) as z:
        names = z.namelist()
    if "feed_info.txt" in names:
        print("  ⚠ feed_info.txt has APPEARED - config.GTFS_SELF_ATTESTS says "
              "False and should be re-measured.")
        return {"unexpected_feed_info": True}
    print(f"  no feed_info.txt (expected; {len(names)} files) - staleness "
          f"comes from the catalogue's `modified`, captured below")
    return {}


def catalogue_modified():
    """The publisher's own word for when the dataset last changed.

    This is what Toulouse has and Paris did not: an attestation outside the
    artifact, from the portal that serves it.
    """
    try:
        js = json.loads(_get(CATALOGUE_URL, timeout=120))
    except Exception as exc:                         # noqa: BLE001
        print(f"  ⚠ catalogue metadata unavailable ({exc!r}) - the fetch date "
              f"is then the only freshness signal, as in Paris")
        return {}
    for d in js.get("datasets", []):
        if d.get("datasetid") == "tisseo-gtfs":
            meta = d.get("metas", {})
            out = {k: meta.get(k) for k in ("modified", "records_count", "title")
                   if meta.get(k) is not None}
            print(f"  catalogue says: {out}")
            return out
    print("  ⚠ tisseo-gtfs not found in the catalogue search result")
    return {}


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
            "gtfs_url": config.GTFS_URL,
            "boundary_url": config.BOUNDARY_URL,
            "gtfs_self_attests": config.GTFS_SELF_ATTESTS}

    print("Rail and boundary:")
    if config.GTFS_ZIP.exists() and not args.force:
        print(f"  {'gtfs.zip':20s} cached")
        prov["feed_info"] = feed_window(config.GTFS_ZIP.read_bytes())
    else:
        prov["feed_info"] = feed_window(fetch_gtfs())
    prov["catalogue"] = catalogue_modified()
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
