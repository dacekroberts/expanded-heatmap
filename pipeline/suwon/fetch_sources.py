"""Download everything Suwon's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/suwon/fetch_sources.py [--force]

  * SEMAS's 상가(상권)정보 ZIP, the national storefront register, into the
    country cache data/korea/raw/ (pipeline/countries/korea_sbiz_fetch.py);
  * OpenStreetMap: Suwon's rail route relations, station names and boundary,
    through pipeline/osm.py (Suwon's queries, with Suwon's box).

Each file is recorded in outputs/suwon/provenance.json.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline import osm  # noqa: E402
from pipeline.countries import korea_sbiz, korea_sbiz_fetch  # noqa: E402
from pipeline.suwon import config  # noqa: E402

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


def fetch_osm(force=False):
    s, w, n, e = config.OSM_BBOX
    box = f"({s},{w},{n},{e})"
    # Every urban-rail relation in the box by ROUTE TYPE - never by network -
    # plus the Suin-Bundang Line, a Korail line tagged train, by its ref. Step 1
    # refuses any relation it cannot place.
    rail_q = (f'[out:json][timeout:600];'
              f'(relation["type"="route"]["route"~"^(subway|light_rail|monorail|tram)$"]{box};'
              f'relation["type"="route"]["route"="train"]["ref"~"^({"|".join(config.OSM_TRAIN_REFS)})$"]{box};)->.r;'
              f'.r out geom;node(r.r);out body;')
    st_q = (f'[out:json][timeout:240];'
            f'(node["railway"="station"]{box};way["railway"="station"]{box};);out tags center;')
    bnd_q = (f'[out:json][timeout:240];'
             f'relation({config.BOUNDARY_RELATION})["name"="{config.BOUNDARY_NAME}"];out geom;')
    for key, q, dest in (("osm_rail", rail_q, config.RAIL_OSM_JSON),
                         ("osm_station_names", st_q, config.STATION_OSM_JSON),
                         ("osm_boundary", bnd_q, config.BOUNDARY_OSM_JSON)):
        els, host = osm.fetch(q, dest, force=force, timeout=300)
        kinds = {}
        for el in els:
            kinds[el["type"]] = kinds.get(el["type"], 0) + 1
        payload = json.loads(dest.read_text(encoding="utf-8"))
        print(f"  {dest.name:24s} {dest.stat().st_size:>11,} bytes  {kinds}  via {host}")
        PROV[key] = {"file": dest.name, "host": host, "query": q, "bytes": dest.stat().st_size,
                     "sha256": sha256(dest), "elements": kinds,
                     "osm_base": payload.get("osm3s", {}).get("timestamp_osm_base")}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    force = "--force" in sys.argv
    fetch_semas(force)
    fetch_osm(force)
    config.PROVENANCE_JSON.write_text(json.dumps(PROV, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"provenance -> {config.PROVENANCE_JSON.relative_to(config.ROOT)}")
