"""Download Bremen's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py.

    python pipeline/bremen/fetch_sources.py [--survey]

  * The 2022 regional retail survey (Kommunalverbund Niedersachsen/Bremen
    e.V.), the zip on geoportal.bremen.de. KEPT, not re-taken, unless
    --survey is given: the survey is a 2022 snapshot, cached 2026-10-04 with
    a meta JSON beside it, and the map states its fieldwork dates. A cached
    zip whose sha256 differs from the meta JSON stops the script rather than
    passing silently.
  * OpenStreetMap: every tram relation in the box with its stop nodes, every
    tram stop node, and the Stadtgemeinde Bremen's and Lilienthal's
    boundaries, in ONE Overpass query (osm-rail: one query per city), split
    into the two files step 1 reads. Rolling, so re-taken on every run.

Each file is recorded in outputs/bremen/provenance.json.
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
from pipeline.bremen import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_survey(force=False):
    if force or not config.SURVEY_ZIP.exists():
        r = requests.get(config.SURVEY_URL, headers=HEADERS, timeout=300)
        r.raise_for_status()
        if not r.content.startswith(b"PK"):
            sys.exit("  survey: the answer is not a zip - nothing written")
        config.SURVEY_ZIP.write_bytes(r.content)
        meta = {"url": config.SURVEY_URL, "fetched": _now()[:10], "bytes": len(r.content),
                "sha256": sha256(config.SURVEY_ZIP),
                "last_modified_header": r.headers.get("Last-Modified"),
                "content": f"{config.SURVEY_MEMBER}, {config.CRS_SURVEY} points",
                "dataset": "Einzelhandelsbestand in der Region Bremen 2022 (Kommunalverbund "
                           "Niedersachsen/Bremen), fieldwork 2022-03 to 2022-09",
                "licence_as_stated": config.SURVEY_LICENCE}
        config.SURVEY_META.write_bytes(
            json.dumps(meta, ensure_ascii=False, indent=2).encode("utf-8"))
    if not config.SURVEY_META.exists():
        sys.exit(f"  survey: no meta JSON beside the cached zip ({config.SURVEY_META.name}) - "
                 f"re-fetch with --survey")
    meta = json.loads(config.SURVEY_META.read_text(encoding="utf-8"))
    digest = sha256(config.SURVEY_ZIP)
    if digest != meta["sha256"]:
        sys.exit(f"  survey: the cached zip's sha256 {digest[:12]}... differs from its record "
                 f"{meta['sha256'][:12]}... - re-fetch with --survey")
    with zipfile.ZipFile(config.SURVEY_ZIP) as z:
        if config.SURVEY_MEMBER not in z.namelist():
            sys.exit(f"  survey: {config.SURVEY_MEMBER} missing from the zip")
    print(f"  survey: {config.SURVEY_ZIP.name} ({config.SURVEY_ZIP.stat().st_size:,} bytes), "
          f"fetched {meta.get('fetched')}, sha256 matches its record")
    return {"url": config.SURVEY_URL, "record": config.SURVEY_RECORD,
            "file": config.SURVEY_ZIP.name, "bytes": config.SURVEY_ZIP.stat().st_size,
            "sha256": digest, "fetched": meta.get("fetched"),
            "last_modified_header": meta.get("last_modified_header"),
            "fieldwork": list(config.SURVEY_FIELDWORK), "publisher": config.SURVEY_PUBLISHER,
            "licence": config.SURVEY_LICENCE, "licence_url": config.SURVEY_LICENCE_URL}


def split(els):
    """The one answer as the two files step 1 reads: route relations with
    their stop nodes and the tram stop nodes; the boundaries."""
    bnd = [e for e in els if e["type"] == "relation"
           and e.get("tags", {}).get("boundary") == "administrative"]
    rail = [e for e in els if e not in bnd]
    return rail, bnd


def fetch_osm():
    s, w, n, e = config.RAIL_BBOX
    box = f"({s},{w},{n},{e})"
    ags = "|".join(sorted(config.PLACES))
    names = "|".join(sorted(set(config.PLACES.values())))
    # By AGS, and by name at admin levels 4 to 8 as well, so a wrong AGS in
    # config is corrected from the cache rather than by a second query (the
    # Land's relation comes too, and boundary.py never takes it).
    q = ("[out:json][timeout:240];"
         f'relation["type"="route"]["route"="tram"]{box}->.r;'
         f'(relation["boundary"="administrative"]["{config.AGS_TAG}"~"^({ags})$"]{box};'
         f'relation["boundary"="administrative"]["name"~"^({names})$"]'
         f'["admin_level"~"^[4-8]$"]{box};)->.b;'
         ".r out geom;"
         f'(node(r.r);node["railway"="tram_stop"]{box};);out body;'
         ".b out geom;")
    els, host = osm.fetch(q, config.OSM_ALL_JSON, force=True, timeout=240)
    payload = json.loads(config.OSM_ALL_JSON.read_text(encoding="utf-8"))
    rail, bnd = split(els)
    rels = [x for x in rail if x["type"] == "relation"]
    if not rels or any(not r.get("members") for r in rels):
        sys.exit("  rail: no relations, or one without members - a FAILED fetch")
    if not bnd:
        sys.exit("  boundaries: no boundary relations - a FAILED fetch")
    for part, dest in ((rail, config.OSM_ROUTES_JSON), (bnd, config.OSM_BOUNDARY_JSON)):
        dest.write_bytes(json.dumps({"osm3s": payload.get("osm3s", {}), "elements": part},
                                    ensure_ascii=False).encode("utf-8"))
    print(f"  rail: {len(rels)} relations; boundaries: {len(bnd)}; via {host}")
    return {"host": host, "query": q, "bbox": config.RAIL_BBOX,
            "osm_base": payload.get("osm3s", {}).get("timestamp_osm_base"),
            "sha256": sha256(config.OSM_ALL_JSON)}


def main():
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    print("Kommunalverbund Niedersachsen/Bremen e.V., retail survey 2022 (CC BY):")
    survey = fetch_survey(force="--survey" in sys.argv)
    print("\nOpenStreetMap (keyless):")
    osm_meta = fetch_osm()
    prov = {"written_utc": _now(), "survey": survey, "osm": osm_meta,
            "osm_fetched_utc": datetime.fromtimestamp(
                config.OSM_ALL_JSON.stat().st_mtime, timezone.utc).isoformat(timespec="seconds")}
    config.PROVENANCE_JSON.write_bytes(
        json.dumps(prov, ensure_ascii=False, indent=2).encode("utf-8"))
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
