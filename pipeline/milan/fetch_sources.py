"""Download Milan's nine raw inputs into data/milan/raw/ (gitignored).

DELIBERATELY NOT NAMED step*.py. `drift_check.py` globs step*.py, so a download
living in a step would turn every drift check into a question about the current
upstream rather than about the committed code.

    python pipeline/milan/fetch_sources.py [--force]

Six business registers, one boundary, three ATM layers and the GTFS.
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.milan import config

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def _get(url, timeout=600):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_register(key, spec):
    """One CKAN register, paged to the end.

    `datastore_search` caps a page, so this pages until `total` is reached and
    ASSERTS the count against the brief rather than trusting the last page -
    a short read looks exactly like a shrinking register.
    """
    out = config.DATA_RAW / f"{key}.json"
    rows, offset = [], 0
    while True:
        q = urllib.parse.urlencode(
            {"resource_id": spec["resource"], "limit": 10000, "offset": offset})
        res = json.loads(_get(f"{config.CKAN}/datastore_search?{q}"))["result"]
        got = res["records"]
        rows += got
        offset += len(got)
        if not got or offset >= res["total"]:
            break
    if len(rows) < spec["rows"] * 0.8:
        sys.exit(f"  {key}: {len(rows):,} rows, brief recorded "
                 f"{spec['rows']:,}. A drop this large is a changed register "
                 f"or a truncated read, and either needs a person.")
    out.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    print(f"  {key:18s} {len(rows):6,} rows  (brief: {spec['rows']:,})")


def fetch_ckan_file(resource, package, dest, label):
    """A CKAN file resource, resolved through resource_show.

    The download URL embeds BOTH a package uuid and a resource uuid, and this
    project has been sent to a dead URL by a hardcoded one before (Madrid's
    rots on every refresh). resource_show is asked for the current one.
    """
    meta = json.loads(_get(
        f"{config.CKAN}/resource_show?id={resource}"))["result"]
    body = _get(meta["url"])
    dest.write_bytes(body)
    print(f"  {label:18s} {len(body):9,} bytes  <- {meta['url'][-52:]}")
    return body


def fetch_gtfs():
    body = _get(config.GTFS_URL)
    if body[:4] != b"PK\x03\x04":
        sys.exit(f"  gtfs.zip is not a zip - first bytes {body[:8]!r}. "
                 f"Check the magic bytes, never the filename the server "
                 f"claims.")
    config.GTFS_ZIP.write_bytes(body)
    print(f"  {'gtfs.zip':18s} {len(body):9,} bytes")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)

    print("Business registers:")
    for key, spec in config.SOURCES.items():
        path = config.DATA_RAW / f"{key}.json"
        if path.exists() and not args.force:
            print(f"  {key:18s} cached")
            continue
        fetch_register(key, spec)

    print("\nBoundary and rail:")
    jobs = [
        (config.BOUNDARY_RESOURCE, config.BOUNDARY_PACKAGE,
         config.BOUNDARY_GEOJSON, "boundary"),
        (config.METRO_STOPS_RESOURCE, None,
         config.METRO_STOPS_GEOJSON, "metro stops"),
        (config.METRO_LINES_RESOURCE, None,
         config.METRO_LINES_GEOJSON, "metro lines"),
        (config.METRO_SEQUENCE_RESOURCE, None,
         config.METRO_SEQUENCE_GEOJSON, "metro sequence"),
    ]
    for resource, package, dest, label in jobs:
        if dest.exists() and not args.force:
            print(f"  {label:18s} cached")
            continue
        fetch_ckan_file(resource, package, dest, label)

    if config.GTFS_ZIP.exists() and not args.force:
        print(f"  {'gtfs.zip':18s} cached")
    else:
        fetch_gtfs()

    print("\nDone. The steps read these files and never fetch.")
