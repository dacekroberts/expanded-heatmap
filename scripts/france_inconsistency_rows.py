"""Write a French tram city's rows into docs/map_inconsistencies.md's four
city-by-city tables (A rail, B business, C location, D vintage), after the
last French row already in each, from the city's own build.

    python scripts/france_inconsistency_rows.py <slug> [...]           # print
    python scripts/france_inconsistency_rows.py <slug> [...] --write   # insert

Idempotent: a city already named in a table is skipped there. The in-ring
counts are computed as the map counts them (nearest station, outer ring edge).
"""
import argparse
import csv
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
DOC = ROOT / "docs" / "map_inconsistencies.md"
TABLES = ("### A. Rail", "### B. Business data", "### C. Location", "### D. Vintage")


def in_ring_by_bucket(cfg):
    import geopandas as gpd
    import numpy as np
    import pandas as pd
    st = pd.read_csv(cfg.STATIONS_CSV)
    biz = pd.read_csv(cfg.BUSINESSES_CLEAN_CSV, dtype={"naf_code": str})
    s = gpd.GeoSeries(gpd.points_from_xy(st["longitude"], st["latitude"]), crs=4326).to_crs(cfg.CRS_PROJECTED)
    b = gpd.GeoSeries(gpd.points_from_xy(biz["longitude"], biz["latitude"]), crs=4326).to_crs(cfg.CRS_PROJECTED)
    sxy = np.column_stack([s.x, s.y])
    d = np.array([np.hypot(*(sxy - [p.x, p.y]).T).min() for p in b])
    inside = d <= cfg.RING_EDGES_METERS[-1]
    div = biz["naf_code"].str[:2]
    return {k: int((inside & (div == v)).sum()) for k, v in (("R", "47"), ("F", "56"), ("P", "96"))}, inside.mean()


def rows(slug):
    import scaffold_france_batch as sfb
    cfg = importlib.import_module(f"pipeline.{slug}.config")
    spec = sfb.BATCH[slug]
    name = spec["name"]
    facts = json.loads((cfg.OUTPUTS / "sirene_facts.json").read_text(encoding="utf-8"))
    prov = json.loads(cfg.PROVENANCE_JSON.read_text(encoding="utf-8"))
    lines = ", ".join(cfg.LINE_NAMES[k] for k in cfg.LINE_KEYS)
    dropped = getattr(cfg, "EXCLUDED_RAIL_ROUTES", {})
    not_drawn = "; ".join(f"{k} ({v.split(':')[0]})" for k, v in dropped.items()) or "—"
    out = 0
    if cfg.SCOPE != "regional" and cfg.EXCLUDED_STATIONS_CSV.exists():
        out = sum(1 for _ in csv.DictReader(open(cfg.EXCLUDED_STATIONS_CSV, encoding="utf-8")))
    scope = "Commune" if cfg.SCOPE == "commune" else f"{len(cfg.EXPECTED_SERVED_COMMUNES)} communes served"
    geom = "" if cfg.LINE_GEOMETRY == "gtfs" else " (geometry OSM)"
    a = f"| {name} | {lines} | {not_drawn} | {spec['operator']} GTFS{geom} | {scope} | {out} / 0 |"
    ring, share = in_ring_by_bucket(cfg)
    b = f"| {name} | same | same | same | {ring['R']:,} / {ring['F']:,} / {ring['P']:,} | — |"
    join = facts["joined"] / facts["to_join"] * 100
    masked = facts["masked"] / facts["active"] * 100
    c = (f"| {name} | same ({join:.2f}%) | Masking {masked:.1f}%"
         + (f"; {out} stops out" if out else "") + " | Same codes |")
    named = facts["named"] / facts["storefronts"] * 100
    d = (f"| {name} | SIRENE {prov.get('sirene_etab_title', '').split(' - ')[-1].split(' (')[0]} "
         f"({prov['fetched_utc'][:10]}) | B | 0.3 mi | Yes | {share * 100:.0f}% | "
         f"Sign/usual name (about {named:.0f}%), else address |")
    return name, (a, b, c, d)


def insert(doc, heading, row, name):
    start = doc.index(heading)
    nxt = re.search(r"^#{2,3} ", doc[start + len(heading):], re.M)
    end = start + len(heading) + nxt.start()
    sec = doc[start:end]
    if re.search(r"^\| " + re.escape(name) + r" \|", sec, re.M):
        return doc, False
    # After the last row of a French city already in the table (Rennes's, or the
    # batch's), else at the table's end.
    french = [m.end() for m in re.finditer(r"^\| (Paris|Marseille|Toulouse|Lille \(Regional\)|Rennes|"
                                           r"Le Mans|Besançon|Avignon|Tours|Dijon|Reims|Orléans|Mulhouse|"
                                           r"Brest|Saint-Étienne|Nice|Montpellier|Strasbourg|Le Havre|Caen|"
                                           r"Rouen \(Regional\)|Bordeaux \(Regional\)|Nantes \(Regional\)|"
                                           r"Grenoble \(Regional\)|Valenciennes \(Regional\)) \|.*\n", sec, re.M)]
    at = max(french) if french else max(m.end() for m in re.finditer(r"^\|.*\|\n", sec, re.M))
    sec = sec[:at] + row + "\n" + sec[at:]
    return doc[:start] + sec + doc[end:], True


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("slugs", nargs="+")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    doc = DOC.read_text(encoding="utf-8")
    for slug in args.slugs:
        name, four = rows(slug)
        for heading, row in zip(TABLES, four):
            if not args.write:
                print(row)
                continue
            doc, done = insert(doc, heading, row, name)
            print(f"{slug}: {heading} {'inserted' if done else 'already there'}")
    if args.write:
        DOC.write_text(doc, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
