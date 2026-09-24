"""Download Rome's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/rome/fetch_sources.py [--force]

Every source is keyless. A cached file is kept and recorded, never silently
refreshed - `--force` re-downloads. Magic bytes are checked on every download.
"""
import argparse
import hashlib
import json
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.rome import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (portfolio map; see the project's public repo)"}


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def _get(url, dest, label, magic, timeout=1800):
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r, open(tmp, "wb") as fh:
        while chunk := r.read(1 << 22):
            fh.write(chunk)
    head = tmp.read_bytes()[:len(magic) or 1]
    if magic and not head.startswith(magic):
        tmp.unlink()
        sys.exit(f"  {label}: wrong magic bytes {head!r} - not the file asked for")
    tmp.replace(dest)
    print(f"  {label:28s} {dest.stat().st_size:13,} bytes downloaded")


def _record(prov, key, path, url, fetched):
    prov[key] = {"file": path.name, "url": url, "bytes": path.stat().st_size,
                 "sha256": _sha256(path), "retrieved": fetched}


def fetch(url, dest, label, magic, prov, key, force):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and not force:
        print(f"  {label:28s} cached ({dest.stat().st_size:,} bytes)")
        old = prov.get(key, {})
        if old.get("sha256") != _sha256(dest):
            _record(prov, key, dest, url, old.get("retrieved") or "cached before provenance")
        return
    _get(url, dest, label, magic)
    _record(prov, key, dest, url, datetime.now(timezone.utc).isoformat(timespec="seconds"))


def anncsu_date(zip_path):
    with zipfile.ZipFile(zip_path) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".csv")]
    if len(names) != 1:
        sys.exit(f"  ANNCSU: expected one CSV in the zip, found {names}")
    return names[0]


def fetch_osm(force):
    bbox = "41.60,12.20,42.10,12.90"
    els, host = osm.fetch(f"[out:json][timeout:180];rel({config.OSM_BOUNDARY_RELATION});out geom;",
                          config.OSM_BOUNDARY_JSON, force=force)
    print(f"  {'osm_boundary':28s} {len(els)} relation via {host}")
    # THE RAIL SOURCE, on a recorded ground (see config.RAIL_SOURCE_GROUND).
    # `out geom` on the relations: step 1 reads their stop members and
    # map_common.load_osm_line_shapes their way geometry. OSM tags Metromare
    # (the Roma-Lido railway) route=subway, so it comes back with the metro.
    rail = ('[out:json][timeout:240];'
            f'(relation["type"="route"]["route"~"^(subway|light_rail)$"]({bbox}););'
            'out geom;node(r);out tags center;')
    els, host = osm.fetch(rail, config.OSM_RAIL_JSON, force=force)
    rels = [x for x in els if x["type"] == "relation"]
    if any(not r.get("members") for r in rels):
        sys.exit("  a route relation came back without members - `out geom` is required")
    print(f"  {'osm_rail':28s} {len(rels)} route relations via {host}")
    nb = ('[out:json][timeout:240];rel["boundary"="administrative"]["admin_level"="8"]'
          f'["ref:ISTAT"]({bbox});out geom;')
    els, host = osm.fetch(nb, config.OSM_NEIGHBOURS_JSON, force=force)
    print(f"  {'osm_neighbours (naming only)':28s} {len(els)} comune relations via {host}")
    # The food-and-drink control the owner's build check compares against,
    # with each place's street so the comparison can be made street by street.
    food = ('[out:json][timeout:300];area(3600041485)->.a;'
            'nwr["amenity"~"^(restaurant|cafe|fast_food|bar|pub|ice_cream|food_court|biergarten)$"](area.a);'
            'out tags center;')
    els, host = osm.fetch(food, config.OSM_FOOD_JSON, force=force, timeout=300)
    print(f"  {'osm_food (build check)':28s} {len(els)} elements via {host}")
    return host


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--skip-osm", action="store_true",
                    help="files only - when every Overpass mirror is down")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    prov = (json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8"))
            if config.PROVENANCE_JSON.exists() else {})

    print("Roma Capitale and ANNCSU:")
    fetch(config.SUAP_URL, config.SUAP_CSV, "opendata_suap_luglio_2025.csv", b"\xef\xbb\xbf",
          prov, "suap", args.force)
    fetch(config.ANNCSU_URL, config.ANNCSU_ZIP, "indirizzario_lazio.zip", b"PK", prov,
          "anncsu", args.force)
    prov["anncsu"]["member"] = anncsu_date(config.ANNCSU_ZIP)
    print(f"  {'':28s} member {prov['anncsu']['member']}")

    print("\nRail (OpenStreetMap - see config.RAIL_SOURCE_GROUND):")
    # Roma Mobilità's GTFS is NOT fetched: its terms are ambiguous and it is not
    # used. Recorded in docs/data_sources.md, not downloaded on every run.
    prov.pop("gtfs", None)
    prov.pop("gtfs_feed_info", None)
    if not args.skip_osm:
        prov["osm_host"] = fetch_osm(args.force)

    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}. The steps read these files "
          f"and never fetch.")
