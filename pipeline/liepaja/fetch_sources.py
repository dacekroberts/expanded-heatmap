"""Download Liepāja's raw inputs. NOT a step: drift_check.py never runs this
file, and every step exits naming it when its cache is missing.

    python pipeline/liepaja/fetch_sources.py

  * OpenStreetMap (keyless): the tram's route=tram relations with geometry,
    their stop nodes and every railway=tram_stop in the box (two stops are on
    no relation, config.STATION_ADD); and the city's boundary relation.
  * data.gov.lv (keyless, CC BY 4.0): VZD's cadastral map for ATVK 0005000
    and VZD's national address file aw_eka.csv, each resolved by file name
    through CKAN and recorded with the portal's own last_modified.
  * NOT FETCHED: VID's excise register and VZD's premise groups, the national
    files Riga fetched; their provenance is copied from Riga's.
"""
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline import osm  # noqa: E402
from pipeline.liepaja import config  # noqa: E402

S = requests.Session()
S.headers["User-Agent"] = "expanded-heatmap (open-data portfolio map)"
RAIL_BBOX = (56.47, 20.96, 56.61, 21.11)          # south, west, north, east


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def download(url, dest):
    """Stream to a temporary file, then rename."""
    tmp = dest.with_suffix(dest.suffix + ".part")
    for attempt in range(4):
        try:
            with S.get(url, stream=True, timeout=600) as r:
                r.raise_for_status()
                h = hashlib.sha256()
                with open(tmp, "wb") as fh:
                    for chunk in r.iter_content(1 << 20):
                        fh.write(chunk)
                        h.update(chunk)
            tmp.replace(dest)
            return h.hexdigest()
        except requests.RequestException as e:
            if attempt == 3:
                raise
            print(f"  retry {attempt + 1} after {e}")
            time.sleep(10 * (attempt + 1))


def ckan_resource(dataset, filename):
    pkg = S.get(config.CKAN_API + "package_show", params={"id": dataset},
                timeout=60).json()["result"]
    hits = [r for r in pkg["resources"] if (r.get("url") or "").endswith("/" + filename)]
    if len(hits) != 1:
        sys.exit(f"{filename}: {len(hits)} resources in {dataset} - re-read the dataset")
    return hits[0]["url"], hits[0].get("last_modified") or hits[0].get("created")


def fetch_osm():
    s, w, n, e = RAIL_BBOX
    rail = ("[out:json][timeout:240];"
            f'relation["type"="route"]["route"="tram"]({s},{w},{n},{e})->.r;'
            ".r out geom;"
            f'(node(r.r);node["railway"="tram_stop"]({s},{w},{n},{e}););out body;')
    els, host = osm.fetch(rail, config.OSM_ROUTES_JSON)
    rels = [x for x in els if x["type"] == "relation"]
    if not rels or any(not r.get("members") for r in rels):
        sys.exit("  tram relations missing or without members - a FAILED fetch")
    print(f"  rail: {len(rels)} relations via {host}")
    city = f"[out:json][timeout:240];relation({config.OSM_CITY_RELATION});out geom;"
    els2, host2 = osm.fetch(city, config.OSM_CITY_JSON)
    print(f"  city boundary: relation {config.OSM_CITY_RELATION} via {host2}")
    return {"rail": {"host": host, "file_utc": now()},
            "city_boundary": {"host": host2, "file_utc": now()}}


def main():
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    prov = {"written_utc": now()}
    print("OpenStreetMap (keyless):")
    prov["osm"] = fetch_osm()
    print("\ndata.gov.lv (keyless):")
    for key, dataset, dest in (
            ("cadastral_map", config.CADASTRAL_MAP_DATASET, config.KK_ZIP),
            ("address_register", config.ADDRESS_REGISTER_DATASET, config.AW_EKA_CSV)):
        url, modified = ckan_resource(dataset, dest.name)
        sha = download(url, dest)
        size = dest.stat().st_size
        print(f"  {dest.name:24s} {size:>13,} bytes  (portal last_modified {modified})")
        prov[key] = {"file": dest.name, "url": url, "bytes": size, "sha256": sha,
                     "retrieved": now(), "last_modified": modified}
    print("\nRiga's national caches (not fetched):")
    if not config.NATIONAL_PROVENANCE.exists():
        sys.exit(f"  no {config.NATIONAL_PROVENANCE} - Riga's fetch records the national files")
    riga = json.loads(config.NATIONAL_PROVENANCE.read_text(encoding="utf-8"))
    for key in ("excise", "premise_groups"):
        prov[key] = dict(riga[key], cached_by="riga")
        print(f"  {riga[key]['file']:24s} last_modified {riga[key]['last_modified']}")
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2, ensure_ascii=False) + "\n",
                                      encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.relative_to(config.ROOT)}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
