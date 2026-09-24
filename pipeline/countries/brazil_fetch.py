"""Download a Brazilian city's raw inputs - shared by every Brazilian city's
fetch_sources.py, which is a config and one call. NOT a step: drift_check.py
never runs it, and the steps read only what it caches.

Per city: every CNEFE zip in `cfg.CNEFE_FILES` ((state folder, file name) -
a regional page lists each município), any agency layers in `extra`, and two
OSM queries over `cfg.BBOX`: every admin_level-8 relation with an IBGE code
(scope and naming) and every rail route relation (`subway|light_rail|
monorail|train|tram`, whitelisted by step 1), `out geom; node(r); out tags
center;` - the `node(r)` clause is what gives stops their names.

A cached file is kept, never silently refreshed (`--force` re-downloads), and
recorded in the city's provenance.json with bytes and sha256. When a cached
file has no record yet, its `retrieved` is the file's own modification time,
marked so - a true date for when it arrived, never a neighbour's.
"""
import argparse
import hashlib
import json
import sys
import urllib.request
from datetime import datetime, timezone

from pipeline import osm
from pipeline.countries import brazil as BR

HEADERS = {"User-Agent": "expanded-heatmap (portfolio map; see the project's public repo)"}


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def _mtime(path):
    return (datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            .isoformat(timespec="seconds") + " (cache file time)")


def _record(prov, key, path, url, retrieved):
    prov[key] = {"file": path.name, "url": url, "bytes": path.stat().st_size,
                 "sha256": _sha256(path), "retrieved": retrieved}


def fetch(url, dest, magic, prov, key, force, timeout=3600):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and not force:
        old = prov.get(key, {})
        if old.get("sha256") != _sha256(dest):
            _record(prov, key, dest, url, old.get("retrieved") or _mtime(dest))
        print(f"  {dest.name:44s} cached ({dest.stat().st_size:,} bytes)")
        return
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r, open(tmp, "wb") as fh:
        while chunk := r.read(1 << 22):
            fh.write(chunk)
    if magic and not tmp.read_bytes()[:len(magic)].startswith(magic):
        tmp.unlink()
        sys.exit(f"  {dest.name}: wrong magic bytes - not the file asked for")
    tmp.replace(dest)
    _record(prov, key, dest, url, datetime.now(timezone.utc).isoformat(timespec="seconds"))
    print(f"  {dest.name:44s} {dest.stat().st_size:13,} bytes downloaded")


def osm_queries(bbox):
    s, w, n, e = bbox
    municipios = ('[out:json][timeout:180];rel["boundary"="administrative"]["admin_level"="8"]'
                  f'["IBGE:GEOCODIGO"]({s},{w},{n},{e});out geom;')
    rail = ('[out:json][timeout:240];'
            f'(relation["type"="route"]["route"~"^(subway|light_rail|monorail|train|tram)$"]'
            f'({s},{w},{n},{e}););out geom;node(r);out tags center;')
    return municipios, rail


def run(cfg, extra=()):
    """extra: (key, url, dest path, magic bytes) for agency layers."""
    ap = argparse.ArgumentParser(description=f"Download {cfg.NAME}'s raw inputs.")
    ap.add_argument("--force", action="store_true")
    force = ap.parse_args().force
    for d in (cfg.DATA_RAW, cfg.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    prov = (json.loads(cfg.PROVENANCE_JSON.read_text(encoding="utf-8"))
            if cfg.PROVENANCE_JSON.exists() else {})
    print("IBGE CNEFE 2022:")
    for state, name in cfg.CNEFE_FILES:
        fetch(f"{BR.CNEFE_BASE_URL}{state}/{name}", cfg.DATA_RAW / name, b"PK", prov,
              f"cnefe:{name}", force)
    if extra:
        print("\nAgency layers:")
        for key, url, dest, magic in extra:
            fetch(url, dest, magic, prov, key, force, timeout=300)
    print("\nOpenStreetMap:")
    municipios, rail = osm_queries(cfg.BBOX)
    for key, query, dest in (("osm_municipios", municipios, cfg.OSM_MUNICIPIOS_JSON),
                             ("osm_rail", rail, cfg.OSM_RAIL_JSON)):
        existed = dest.exists()
        els, host = osm.fetch(query, dest, force=force)
        if key == "osm_rail" and any(not x.get("members") for x in els if x["type"] == "relation"):
            sys.exit("  a route relation came back without members - `out geom` is required")
        prov[key] = {"file": dest.name, "host": host,
                     "retrieved": (_mtime(dest) if existed and not force
                                   else datetime.now(timezone.utc).isoformat(timespec="seconds"))}
        print(f"  {dest.name:44s} {sum(1 for x in els if x['type'] == 'relation')} relations via {host}")
    cfg.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {cfg.PROVENANCE_JSON.name}. The steps read these files and never fetch.")
