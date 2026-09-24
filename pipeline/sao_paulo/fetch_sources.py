"""Download São Paulo's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/sao_paulo/fetch_sources.py [--force]

Every source is keyless. A cached file is kept and recorded, never silently
refreshed - `--force` re-downloads. Magic bytes are checked on every download.
"""
import argparse
import hashlib
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.sao_paulo import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (portfolio map; see the project's public repo)"}


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def _record(prov, key, path, url, fetched):
    prov[key] = {"file": path.name, "url": url, "bytes": path.stat().st_size,
                 "sha256": _sha256(path), "retrieved": fetched}


def fetch(url, dest, label, magic, prov, key, force, timeout=3600):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and not force:
        print(f"  {label:30s} cached ({dest.stat().st_size:,} bytes)")
        old = prov.get(key, {})
        if old.get("sha256") != _sha256(dest):
            _record(prov, key, dest, url, old.get("retrieved") or "cached before provenance")
        return
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r, open(tmp, "wb") as fh:
        while chunk := r.read(1 << 22):
            fh.write(chunk)
    if magic and not tmp.read_bytes()[:len(magic)].startswith(magic):
        tmp.unlink()
        sys.exit(f"  {label}: wrong magic bytes - not the file asked for")
    tmp.replace(dest)
    _record(prov, key, dest, url, datetime.now(timezone.utc).isoformat(timespec="seconds"))
    print(f"  {label:30s} {dest.stat().st_size:13,} bytes downloaded")


def fetch_osm(force):
    s, w, n, e = config.RAIL_BBOX
    b = ('[out:json][timeout:180];rel["boundary"="administrative"]["admin_level"="8"]'
         f'["IBGE:GEOCODIGO"="{config.IBGE_MUNICIPIO}"]({s},{w},{n},{e});out geom;')
    els, host = osm.fetch(b, config.OSM_BOUNDARY_JSON, force=force)
    print(f"  {'osm_boundary':30s} {len(els)} relation via {host}")
    rail = ('[out:json][timeout:240];'
            f'(relation["type"="route"]["route"~"^(subway|monorail)$"]({s},{w},{n},{e}););'
            'out geom;node(r);out tags center;')
    els, host = osm.fetch(rail, config.OSM_RAIL_JSON, force=force)
    rels = [x for x in els if x["type"] == "relation"]
    if any(not r.get("members") for r in rels):
        sys.exit("  a route relation came back without members - `out geom` is required")
    print(f"  {'osm_rail':30s} {len(rels)} route relations via {host}")
    # CPTM, for Line 9 (the owner's call of 2026-09-24); every other train
    # relation must be named in config.CPTM_NOT_DRAWN or step 1 stops.
    train = ('[out:json][timeout:240];'
             f'(relation["type"="route"]["route"="train"]({s},{w},{n},{e}););'
             'out geom;node(r);out tags center;')
    els, host = osm.fetch(train, config.OSM_TRAIN_JSON, force=force)
    print(f"  {'osm_train':30s} {sum(1 for x in els if x['type'] == 'relation')} "
          f"route relations via {host}")
    # Every município in the bbox, only to NAME a station outside São Paulo.
    mun = ('[out:json][timeout:180];rel["boundary"="administrative"]["admin_level"="8"]'
           f'["IBGE:GEOCODIGO"]({s},{w},{n},{e});out geom;')
    els, host = osm.fetch(mun, config.OSM_MUNICIPIOS_JSON, force=force)
    print(f"  {'osm_municipios':30s} {len(els)} relations via {host}")
    return host


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    prov = (json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8"))
            if config.PROVENANCE_JSON.exists() else {})
    print("IBGE:")
    fetch(config.CNEFE_URL, config.CNEFE_ZIP, "3550308_SAO_PAULO.zip", b"PK", prov, "cnefe",
          args.force)
    print("\nGeoSampa (status and count only):")
    fetch(config.GEOSAMPA_STATIONS_URL, config.GEOSAMPA_STATIONS_JSON,
          "geosampa_estacao_metro.json", b"{", prov, "geosampa_stations", args.force, timeout=300)
    fetch(config.GEOSAMPA_TRAIN_STATIONS_URL, config.GEOSAMPA_TRAIN_STATIONS_JSON,
          "geosampa_estacao_trem.json", b"{", prov, "geosampa_train_stations", args.force,
          timeout=300)
    print("\nOpenStreetMap:")
    prov["osm_host"] = fetch_osm(args.force)
    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}. The steps read these files "
          f"and never fetch.")
