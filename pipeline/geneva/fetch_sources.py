"""Download Geneva (Regional)'s raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py.

    python pipeline/geneva/fetch_sources.py [--register]

  * The canton's business register (REG), SITG's CSV zip. KEPT, not re-taken,
    unless --register is given: the register is daily, and the map states the
    extract date of the one file it was built from. A cached zip whose sha256
    differs from its .json record stops the script rather than passing
    silently.
  * OpenStreetMap: every tram and light-rail relation in the box with its
    stop nodes, every tram stop node, and the admin_level 8 commune
    boundaries, in ONE Overpass query (osm-rail: one query per city), split
    into the two files step 1 reads. Rolling, so re-taken on every run.

Each file is recorded in outputs/geneva/provenance.json.
"""
import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.geneva import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_date(zpath):
    """The zip's own creation stamp, from DOC/Informations_date.txt."""
    text = zipfile.ZipFile(zpath).read(config.REG_DATE_MEMBER).decode("utf-8", "replace")
    for line in text.splitlines():
        if "Date de création" in line:
            return line.split(":", 1)[1].strip()
    sys.exit(f"{config.REG_DATE_MEMBER}: no creation date - re-read the file")


def fetch_register(force=False):
    meta_path = config.REG_ZIP.with_name(config.REG_ZIP.name + ".json")
    if force or not config.REG_ZIP.exists():
        r = requests.get(config.REG_URL, headers=HEADERS, timeout=600)
        r.raise_for_status()
        if not r.content.startswith(b"PK"):
            sys.exit("  register: the answer is not a zip - nothing written")
        config.REG_ZIP.write_bytes(r.content)
        meta = {"url": config.REG_URL, "fetched": _now()[:10], "bytes": len(r.content),
                "sha256": sha256(config.REG_ZIP),
                "licence": "SITG Level A, Conditions d'utilisation (read 2026-10-04)"}
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    digest = sha256(config.REG_ZIP)
    if digest != meta["sha256"]:
        sys.exit(f"  register: the cached zip's sha256 {digest[:12]}... differs from its record "
                 f"{meta['sha256'][:12]}... - re-fetch with --register")
    with zipfile.ZipFile(config.REG_ZIP) as z:
        if config.REG_MEMBER not in z.namelist():
            sys.exit(f"  register: {config.REG_MEMBER} missing from the zip")
    created = extract_date(config.REG_ZIP)
    print(f"  register: {config.REG_ZIP.name} ({config.REG_ZIP.stat().st_size:,} bytes), "
          f"zip created {created}")
    return {"url": config.REG_URL, "page": config.REG_DATASET_PAGE, "file": config.REG_ZIP.name,
            "bytes": config.REG_ZIP.stat().st_size, "sha256": digest,
            "fetched": meta.get("fetched"), "zip_created": created,
            "conditions": config.REG_CONDITIONS_URL}


def split(els):
    """The one answer as the two files step 1 reads: route relations with
    their stop nodes and the tram stop nodes; the commune boundaries."""
    bnd = [e for e in els if e["type"] == "relation"
           and e.get("tags", {}).get("boundary") == "administrative"]
    rail = [e for e in els if e not in bnd]
    return rail, bnd


def fetch_osm():
    s, w, n, e = config.RAIL_BBOX
    box = f"({s},{w},{n},{e})"
    q = ("[out:json][timeout:300];"
         f'relation["type"="route"]["route"~"^(tram|light_rail)$"]{box}->.r;'
         f'relation["boundary"="administrative"]["admin_level"="8"]{box}->.b;'
         ".r out geom;"
         f'(node(r.r);node["railway"="tram_stop"]{box};);out body;'
         ".b out geom;")
    els, host = osm.fetch(q, config.OSM_ALL_JSON, force=True, timeout=300)
    payload = json.loads(config.OSM_ALL_JSON.read_text(encoding="utf-8"))
    rail, bnd = split(els)
    rels = [x for x in rail if x["type"] == "relation"]
    if not rels or any(not r.get("members") for r in rels):
        sys.exit("  rail: no relations, or one without members - a FAILED fetch")
    if not bnd:
        sys.exit("  communes: no boundary relations - a FAILED fetch")
    for part, dest in ((rail, config.OSM_ROUTES_JSON), (bnd, config.OSM_COMMUNES_JSON)):
        dest.write_bytes(json.dumps({"osm3s": payload.get("osm3s", {}), "elements": part},
                                    ensure_ascii=False).encode("utf-8"))
    print(f"  rail: {len(rels)} relations; communes: {len(bnd)} boundaries; via {host}")
    return {"host": host, "query": q, "bbox": config.RAIL_BBOX,
            "osm_base": payload.get("osm3s", {}).get("timestamp_osm_base"),
            "sha256": sha256(config.OSM_ALL_JSON)}


def main():
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    print("Canton of Geneva, REG (SITG Level A):")
    register = fetch_register(force="--register" in sys.argv)
    print("\nOpenStreetMap (keyless):")
    osm_meta = fetch_osm()
    prov = {"written_utc": _now(), "register": register, "osm": osm_meta,
            "osm_fetched_utc": datetime.fromtimestamp(
                config.OSM_ALL_JSON.stat().st_mtime, timezone.utc).isoformat(timespec="seconds")}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
