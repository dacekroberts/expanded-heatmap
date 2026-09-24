"""Download Oslo's raw inputs into data/oslo/raw/ (gitignored), and the two
national register files into the shared country cache.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/oslo/fetch_sources.py [--force]

Every source is keyless. Magic bytes are checked on every file, because two of
these hosts answer in ways that read as success:

  * Google Storage (the GTFS) answers HEAD with 200 and size 0;
  * a Geonorge path with the wrong kommune name 404s with an HTML page.
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

from pipeline.countries import norway as NO
from pipeline.oslo import config

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def _stream(url, dest, label, magic, timeout=1800):
    req = urllib.request.Request(url, headers=HEADERS)
    tmp = dest.with_suffix(dest.suffix + ".part")
    done = 0
    with urllib.request.urlopen(req, timeout=timeout) as r, open(tmp, "wb") as fh:
        while True:
            chunk = r.read(1 << 22)
            if not chunk:
                break
            fh.write(chunk)
            done += len(chunk)
    head = tmp.read_bytes()[:4]
    if not head.startswith(magic):
        tmp.unlink()
        sys.exit(f"  {label}: wrong magic bytes {head!r} - not the file asked for")
    tmp.replace(dest)
    print(f"  {label:22s} {done:13,} bytes")


def feed_info(path):
    """Entur's feed_info carries a publisher and NO validity window; assert
    the absence so a change in the publisher's behaviour is reported."""
    with zipfile.ZipFile(path) as z:
        if "feed_info.txt" not in z.namelist():
            print("  ⚠ feed_info.txt has DISAPPEARED")
            return {"missing_feed_info": True}
        head, row = z.read("feed_info.txt").decode("utf-8-sig").splitlines()[:2]
    info = dict(zip(head.split(","), row.split(",")))
    if info.get("feed_end_date"):
        print(f"  ⚠ feed_info now declares a window ({info.get('feed_start_date')} - "
              f"{info.get('feed_end_date')}): config.GTFS_SELF_ATTESTS should be revisited")
    else:
        print(f"  feed_info: publisher {info.get('feed_publisher_name')!r}, no window "
              f"(expected) - the fetch date pins the snapshot")
    return info


def fetch_boundary():
    req = urllib.request.Request(config.BOUNDARY_URL, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=120) as r:
        obj = json.loads(r.read())
    geom = obj.get("omrade") or obj
    if geom.get("type") not in ("Polygon", "MultiPolygon"):
        sys.exit(f"  boundary is a {geom.get('type')!r}, not a polygon")
    feature = {"type": "Feature", "geometry": geom,
               "properties": {"kommunenummer": obj.get("kommunenummer"),
                              "kommunenavn": obj.get("kommunenavn")}}
    config.CITY_BOUNDARY_GEOJSON.write_text(json.dumps(feature), encoding="utf-8")
    print(f"  {'city_boundary':22s} {geom.get('type')}, kommune "
          f"{obj.get('kommunenummer')} {obj.get('kommunenavn')}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS, NO.SHARED_RAW):
        d.mkdir(parents=True, exist_ok=True)

    prov = {"fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "gtfs_url": config.GTFS_URL, "boundary_url": config.BOUNDARY_URL,
            "address_url": config.ADDRESS_URL,
            "subunits_url": NO.SUBUNITS_URL, "units_url": NO.UNITS_URL,
            "gtfs_self_attests": config.GTFS_SELF_ATTESTS}

    print("Rail, boundary and addresses:")
    jobs = [(config.GTFS_URL, config.GTFS_ZIP, "gtfs.zip", b"PK\x03\x04"),
            (config.ADDRESS_URL, config.ADDRESS_ZIP, "adresser_0301.zip", b"PK\x03\x04")]
    for url, dest, label, magic in jobs:
        if dest.exists() and not args.force:
            print(f"  {label:22s} cached")
        else:
            _stream(url, dest, label, magic)
    prov["feed_info"] = feed_info(config.GTFS_ZIP)
    if config.CITY_BOUNDARY_GEOJSON.exists() and not args.force:
        print(f"  {'city_boundary':22s} cached")
    else:
        fetch_boundary()
    if config.NEIGHBOURS_GEOJSON.exists() and not args.force:
        print(f"  {'neighbour_kommuner':22s} cached")
    else:
        feats = []
        for code, name in config.NEIGHBOUR_KOMMUNER.items():
            url = config.KOMMUNE_BOUNDARY_URL_TEMPLATE.format(code=code)
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS),
                                        timeout=120) as r:
                obj = json.loads(r.read())
            feats.append({"type": "Feature", "geometry": obj.get("omrade") or obj,
                          "properties": {"kommunenummer": code, "kommunenavn": name}})
        config.NEIGHBOURS_GEOJSON.write_text(
            json.dumps({"type": "FeatureCollection", "features": feats}), encoding="utf-8")
        print(f"  {'neighbour_kommuner':22s} {len(feats)} kommune(s)")

    print("\nNational register (shared across every Norwegian city):")
    for url, dest, label in ((NO.SUBUNITS_URL, NO.SUBUNITS_CSV_GZ, "underenheter.csv.gz"),
                             (NO.UNITS_URL, NO.UNITS_CSV_GZ, "enheter.csv.gz")):
        if dest.exists() and not args.force:
            print(f"  {label:22s} cached ({dest.stat().st_size:,} bytes)")
        else:
            _stream(url, dest, label, b"\x1f\x8b")

    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}")
