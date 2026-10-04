"""Download everything Gwangju's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/gwangju/fetch_sources.py [--force]

  * SEMAS's 상가(상권)정보 ZIP, the national storefront register, into the
    country cache data/korea/raw/ (pipeline/countries/korea_sbiz_fetch.py);
  * OpenStreetMap: Gwangju's rail route relations, station names and
    boundary in ONE Overpass query (osm-rail: one query per city), through
    pipeline/osm.py, then split into the three files step 1 reads.

Each file is recorded in outputs/gwangju/provenance.json.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline import osm  # noqa: E402
from pipeline.countries import korea_sbiz, korea_sbiz_fetch  # noqa: E402
from pipeline.gwangju import config  # noqa: E402

PROV = {}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_semas(force=False):
    korea_sbiz_fetch.main(force)
    meta = json.loads(korea_sbiz.ZIP.with_suffix(".json").read_text(encoding="utf-8"))
    PROV["semas"] = {"file": korea_sbiz.ZIP.name, "page": korea_sbiz.PAGE, "url": meta.get("url"),
                     "bytes": meta.get("bytes"), "sha256": meta.get("sha256"),
                     "retrieved": meta.get("retrieved_utc"), "edition": korea_sbiz.edition()}


def split(els):
    """The one answer as the three files step 1 reads: route relations with
    their member nodes; station objects; the boundary relation."""
    routes = [e for e in els if e["type"] == "relation" and e.get("tags", {}).get("type") == "route"]
    member_ids = {m["ref"] for r in routes for m in r.get("members", []) if m["type"] == "node"}
    rail, seen = list(routes), set()
    for e in els:
        if e["type"] == "node" and e["id"] in member_ids and e["id"] not in seen and "lat" in e:
            rail.append(e)
            seen.add(e["id"])
    stations, seen = [], set()
    for e in els:
        if e["type"] in ("node", "way") and e.get("tags", {}).get("railway") == "station":
            if (e["type"], e["id"]) not in seen and ("lat" in e or "center" in e):
                stations.append(e)
                seen.add((e["type"], e["id"]))
    boundary = [e for e in els if e["type"] == "relation"
                and e.get("tags", {}).get("boundary") == "administrative"]
    return rail, stations, boundary


def fetch_osm(force=False):
    s, w, n, e = config.OSM_BBOX
    box = f"({s},{w},{n},{e})"
    # Every urban-rail relation in the box by ROUTE TYPE - never by network;
    # step 1 refuses any relation it cannot place. The boundary: any relation
    # named 광주광역시 at any level, and the five 구 at admin_level 6, since
    # the 2026 merger may have renamed or demoted the city's own relation;
    # step 1 checks what came back by id, name and area.
    districts = "|".join(config.BOUNDARY_DISTRICTS)
    q = (f'[out:json][timeout:600];'
         f'relation["type"="route"]["route"~"^(subway|light_rail|monorail|tram)$"]{box}->.r;'
         f'(node["railway"="station"]{box};way["railway"="station"]{box};)->.s;'
         f'(relation["boundary"="administrative"]["name"="{config.BOUNDARY_NAME}"]{box};'
         f'relation["boundary"="administrative"]["admin_level"="6"]["name"~"^({districts})$"]{box};)->.b;'
         f'.r out geom;node(r.r);out body;.s out tags center;.b out geom;')
    els, host = osm.fetch(q, config.OSM_ALL_JSON, force=force, timeout=300)
    payload = json.loads(config.OSM_ALL_JSON.read_text(encoding="utf-8"))
    base = payload.get("osm3s", {}).get("timestamp_osm_base")
    PROV["osm"] = {"file": config.OSM_ALL_JSON.name, "host": host, "query": q,
                   "bytes": config.OSM_ALL_JSON.stat().st_size,
                   "sha256": sha256(config.OSM_ALL_JSON), "osm_base": base}
    for key, part, dest in zip(("osm_rail", "osm_station_names", "osm_boundary"), split(els),
                               (config.RAIL_OSM_JSON, config.STATION_OSM_JSON, config.BOUNDARY_OSM_JSON)):
        if not part:
            sys.exit(f"the OSM answer holds nothing for {dest.name} - an empty part is not an empty city")
        dest.write_bytes(json.dumps({"osm3s": payload.get("osm3s", {}), "elements": part},
                                    ensure_ascii=False).encode("utf-8"))
        kinds = {}
        for el in part:
            kinds[el["type"]] = kinds.get(el["type"], 0) + 1
        print(f"  {dest.name:24s} {dest.stat().st_size:>11,} bytes  {kinds}  via {host}")
        PROV[key] = {"file": dest.name, "split_from": config.OSM_ALL_JSON.name,
                     "bytes": dest.stat().st_size, "sha256": sha256(dest), "elements": kinds,
                     "osm_base": base}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    force = "--force" in sys.argv
    fetch_semas(force)
    fetch_osm(force)
    config.PROVENANCE_JSON.write_text(json.dumps(PROV, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"provenance -> {config.PROVENANCE_JSON.relative_to(config.ROOT)}")
