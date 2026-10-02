"""Write a French tram city's rows into docs/data_sources/france.md - its
business-registry row, its transit-feed row and its boundary rows - from the
city's own build (config, provenance.json, sirene_facts.json), so every
endpoint its config resolves is recorded, as check_provenance.py requires.

    python scripts/france_source_rows.py <slug> [...]           # print the rows
    python scripts/france_source_rows.py <slug> [...] --write   # insert them

Idempotent: a city whose name already heads a row in a table is skipped there.
The rows are data, dated to the fetch; the licence reads they cite are the
France kit's (DECISIONS "French tram feeds read", the Normandie read).
"""
import argparse
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
DOC = ROOT / "docs" / "data_sources" / "france.md"

LICENCE = {"lov2": "Licence Ouverte 2.0 (`lov2`)",
           "fr-lo": "**Licence Ouverte 1.0** (`fr-lo`), read 2026-09-29: credit Bordeaux Métropole and the feed's own date",
           "odc-odbl": "**ODbL 1.0** (`odc-odbl`) under the NAP's Conditions Particulières, read 2026-09-29: a §4.3 notice in `_NOTICES`, and the station table a pure extract"}


def rows(slug):
    import scaffold_france_batch as sfb
    cfg = importlib.import_module(f"pipeline.{slug}.config")
    spec = sfb.BATCH[slug]
    name = spec["name"]
    prov = json.loads(cfg.PROVENANCE_JSON.read_text(encoding="utf-8"))
    facts = json.loads((cfg.OUTPUTS / "sirene_facts.json").read_text(encoding="utf-8"))
    date = prov["fetched_utc"][:10]
    codes = ", ".join(f"`{c}`" for c in cfg.COMMUNE_PREFIXES)
    join = (f"{facts['joined'] / facts['to_join'] * 100:.2f}%" if facts.get("to_join")
            else "see step 2")
    # Wording owner-approved 2026-10-01 (prose pass, P1326).
    reg = (f"| {name} | **INSEE SIRENE `StockEtablissement`**, as Paris, joined on `siret` to "
           f"INSEE's geolocation file | All three categories via NAF rév. 2 at the "
           f"sous-classe. **{facts['storefronts']:,} storefronts** ({facts['retail']:,} retail, "
           f"{facts['food']:,} food, {facts['personal']:,} personal), coordinate coverage "
           f"**{join}** | As Paris; the national cache | "
           f"`codeCommuneEtablissement` in {codes}. {facts['active']:,} active rows, "
           f"**{facts['masked'] / facts['active'] * 100:.1f}% masked at source**; miscellaneous "
           f"classes 96.09Z and 56.29B excluded, as in Paris. Licence **Licence Ouverte 2.0** "
           f"(`lov2`), « Source : Insee » on the page | {date} |")
    fi = prov.get("feed_info") or {}
    nap = prov.get("nap") or {}
    window = (f"`feed_info.txt` self-attests: {fi.get('feed_publisher_name')}, "
              f"{fi.get('feed_start_date')} to {fi.get('feed_end_date')}" if fi else
              f"no dated `feed_info.txt`: the NAP's reading, {nap.get('start_date')} to "
              f"{nap.get('end_date')}, resource updated {str(nap.get('resource_updated'))[:10]}")
    lines = ", ".join(cfg.LINE_NAMES[k] for k in cfg.LINE_KEYS)
    geometry = ("line geometry from the feed's `shapes.txt`" if cfg.LINE_GEOMETRY == "gtfs"
                else "line geometry from OpenStreetMap (see the next table)")
    agency = f", filtered to agency `{cfg.GTFS_AGENCY_ID}`" if getattr(cfg, "GTFS_AGENCY_ID", None) else ""
    feed = (f"| {name} | {spec['operator']} - {lines} | `{cfg.GTFS_URL}` (NAP dataset "
            f"`{cfg.GTFS_NAP_ID}`, *{nap.get('dataset') or cfg.GTFS_DATASET}*{agency}) | {date} | "
            f"**Rolling: fetched fresh on every build run** (owner, 2026-09-29). {window}. "
            f"route_ids {', '.join(f'`{r}`' for r in cfg.ROUTE_IDS)}; {geometry}. Stations are "
            f"pure extracts (owner's rule). Gate 3: {cfg.OPERATOR_COUNTS_SOURCE}. Licence "
            f"{LICENCE[cfg.GTFS_LICENCE]} |")
    geo = []
    if cfg.LINE_GEOMETRY == "osm":
        geo.append(f"| {name} | OpenStreetMap route relations for {spec['operator']}'s lines "
                   f"(the feed has no usable shapes) | Overpass, one query per city, "
                   f"cached at `data/{slug}/raw/osm_routes.json`: route relations of `route` tram or "
                   f"light_rail in the bbox ({re.search(r'\(([\d.,-]+)\);out', cfg.OSM_ROUTES_QUERY).group(1)}), "
                   f"`out geom` (the exact query is in the config and `provenance.json`) | "
                   f"{date} | refs {cfg.OSM_REFS}. ODbL 1.0, covered by the OpenStreetMap "
                   f"notice |")
    bnd = [f"| {name} | **`geo.api.gouv.fr` commune contour**, code INSEE "
           f"**`{cfg.BOUNDARY_COMMUNE_CODE}`** | `{cfg.BOUNDARY_URL}` | "
           + ("the label focus; the scope is the served communes below |" if cfg.SCOPE == "regional"
              else f"the commune alone: **commune-only scope** (owner, 2026-09-30), asserted per "
                   f"line in `EXPECTED_INSIDE_PER_LINE` |")]
    for url in cfg.METROPOLE_COMMUNES_URLS:
        bnd.append(f"| {name} | **Every commune of the EPCI**, with contours | `{url}` | "
                   + (f"**the scope**: the {len(cfg.EXPECTED_SERVED_COMMUNES)} communes holding a "
                      f"station (owner, 2026-09-30), asserted in `EXPECTED_SERVED_COMMUNES` |"
                      if cfg.SCOPE == "regional" else
                      "not a scope: it names the commune each excluded station lies in |"))
    return {"## Business registries": [reg], "## Transit feeds": [feed],
            "### Rail geometry that is not a GTFS feed": geo, "## Boundary layers": bnd}, name


def insert(doc, heading, new_rows, name):
    start = doc.index(heading)
    nxt = re.search(r"^#{2,3} ", doc[start + len(heading):], re.M)
    end = start + len(heading) + (nxt.start() if nxt else len(doc) - start - len(heading))
    section = doc[start:end]
    if re.search(r"^\| " + re.escape(name) + r" \|", section, re.M):
        return doc, False
    last = max(m.end() for m in re.finditer(r"^\|.*\|\n", section, re.M))
    section = section[:last] + "".join(r + "\n" for r in new_rows) + section[last:]
    return doc[:start] + section + doc[end:], True


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("slugs", nargs="+")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    doc = DOC.read_text(encoding="utf-8")
    for slug in args.slugs:
        table, name = rows(slug)
        for heading, new in table.items():
            if not new:
                continue
            if not args.write:
                print("\n".join(new))
                continue
            doc, done = insert(doc, heading, new, name)
            print(f"{slug}: {heading} {'inserted' if done else 'already there'}")
    if args.write:
        DOC.write_text(doc, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
