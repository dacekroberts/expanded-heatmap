"""Write a French tram city's app page from the owner's approved template
(`.claude/skills/france-tram-city/SKILL.md`, section 6), with every brace filled
from the city's OWN build: step 1's stations and exclusions, step 2's
`sirene_facts.json`, and the in-ring share computed the way the map counts it.

    python scripts/france_page.py <slug> [<slug> ...]            # print the prose
    python scripts/france_page.py <slug> --write                 # write the page

Run it after steps 1-3. It overwrites the city's existing page file (found by
slug, as scaffold_city.py names it). The controls paragraph and the heat caveat
are Rennes's, verbatim; the transit caption names the feed's producer (the NAP
dataset's legal owner) and the operator, with the feed window from
`provenance.json`; a business caption carries INSEE's « Source : Insee ».

DEPARTURES FROM THE TEMPLATE are only the owner-approved ones (2026-09-30):
Rouen's first paragraph, Brest's cable car, and the count including Nice's
Line B. Anything else is a proposed sentence for the owner, never an edit here.
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

SCREEN = ROOT / "data" / "_staging_scratch_2026-09-27" / "second_cities" / "france"
NUMBERS = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six"}
EPCI_NAMES = {
    "bordeaux": "Bordeaux Métropole", "nantes": "Nantes Métropole",
    "grenoble": "Grenoble-Alpes Métropole", "rouen": "the Métropole Rouen Normandie",
    "valenciennes": "Valenciennes Métropole and the Porte du Hainaut",
}
# The LO credit names the producer: the NAP dataset's legal owner, which the
# licence reads confirmed where they were read (Bordeaux Métropole; Syndicat
# mixte Atoumod for the Normandie aggregate).
PRODUCER = {"caen": "Syndicat mixte Atoumod", "rouen": "Syndicat mixte Atoumod",
            "bordeaux": "Bordeaux Métropole"}

CONTROLS = """Concentric ring boundaries and the three business categories (Retail, Food
service and Personal services) are toggleable via the layer control in the top
left. When enabled, business density will display as numbered circles summing
areas when zoomed out. Zooming in will show individual dots; hover over those
to see further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a
statistical density estimate, so read the colour as "roughly where things
cluster.\""""


def readable(name):
    """An ALL-CAPS feed name in title case for the prose ("POLYCLINIQUE" ->
    "Polyclinique"). Prose only: the station tables keep the feed's names
    unchanged (the owner's pure-extract rule), and a mixed-case name is left
    exactly as the feed spells it."""
    small = {"De", "Du", "Des", "La", "Le", "Les", "Et", "En", "Sur", "Sous", "Aux", "Au"}
    keep = {"TGV", "CHU", "SNCF", "ZI", "ZA"}
    if name == name.upper():
        words = re.split(r"(\s+|-|')", name.title())
        return "".join(w.lower() if i and w in small else
                       (w.upper() if w.upper() in keep else w)
                       for i, w in enumerate(words))
    # Mixed case with a capitalised commune prefix (Dijon's "CHENÔVE Centre"):
    # title-case each all-caps word longer than three letters.
    return re.sub(r"\b[^\W\d_]{4,}\b",
                  lambda m: m.group(0).title() if m.group(0) == m.group(0).upper()
                  and m.group(0) not in keep else m.group(0), name)


def joined(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def legal_owner(cfg):
    nap = json.loads((SCREEN / "nap_datasets.json").read_text(encoding="utf-8"))
    for d in nap:
        if d["datagouv_id"] == cfg.GTFS_NAP_ID:
            owners = [o["name"] for o in d.get("legal_owners", [])]
            return owners[0] if len(owners) == 1 else None
    return None


def measure(cfg):
    import geopandas as gpd
    import numpy as np
    import pandas as pd
    from shapely.geometry import shape
    from pipeline import stations as gates

    st = pd.read_csv(cfg.STATIONS_CSV)
    biz = pd.read_csv(cfg.BUSINESSES_CLEAN_CSV, dtype={"naf_code": str})
    nn = gates.nearest_neighbour_m(st["longitude"], st["latitude"], cfg.CRS_PROJECTED)
    s = gpd.GeoSeries(gpd.points_from_xy(st["longitude"], st["latitude"]), crs=4326).to_crs(cfg.CRS_PROJECTED)
    b = gpd.GeoSeries(gpd.points_from_xy(biz["longitude"], biz["latitude"]), crs=4326).to_crs(cfg.CRS_PROJECTED)
    sxy = np.column_stack([s.x, s.y])
    d = np.array([np.hypot(*(sxy - [p.x, p.y]).T).min() for p in b])
    in_ring = float((d <= cfg.RING_EDGES_METERS[-1]).mean())
    # OpenStreetMap's food count is the screen's, for the CORE commune, so the
    # ratio compares the core commune's food rows with it.
    core = shape(json.loads(cfg.CITY_BOUNDARY_GEOJSON.read_bytes())["geometry"])
    inside = gpd.GeoSeries(gpd.points_from_xy(biz["longitude"], biz["latitude"]), crs=4326).within(core)
    food_core = int(((biz["naf_code"].str[:2] == "56") & inside.values).sum())
    slug = cfg.OUTPUTS.name
    scr = {r["slug"]: r for r in csv.DictReader(open(SCREEN / "screen_results.csv", encoding="utf-8"))}[slug]
    facts = json.loads((cfg.OUTPUTS / "sirene_facts.json").read_text(encoding="utf-8"))
    ex = []
    if cfg.SCOPE != "regional" and cfg.EXCLUDED_STATIONS_CSV.exists():
        ex = list(csv.DictReader(open(cfg.EXCLUDED_STATIONS_CSV, encoding="utf-8")))
    return {"median_m": float(np.median(nn)), "in_ring": in_ring,
            "osm_ratio": food_core / int(scr["osm_food"]),
            "masked_share": facts["masked"] / facts["active"], "excluded": ex}


def scope_paragraph(cfg, name, m):
    slug = cfg.OUTPUTS.name
    if cfg.SCOPE == "regional":
        n = len(cfg.EXPECTED_SERVED_COMMUNES)
        verb = "the métro serves" if slug == "rouen" else "the trams serve"
        return f"The map covers the **{n} communes of {EPCI_NAMES[slug]}** that {verb}."
    text = f"The map covers the **commune of {name}**."
    if not m["excluded"]:
        return text
    by_place = {}
    for r in m["excluded"]:
        place = re.sub(r"^in (.*?)(?: \(\d+\))?, outside commune \d+$", r"\1", r["reason"])
        by_place.setdefault(place, []).append(readable(r["station"]))
    lines = sorted({l for r in m["excluded"] for l in r["lines"].split("/")},
                   key=cfg.LINE_KEYS.index)
    names = joined(cfg.LINE_NAMES[l] for l in lines)
    k = len(m["excluded"])
    places = "; ".join(f"{joined(sorted(v))} in {p}" for p, v in by_place.items())
    run = "runs" if len(lines) == 1 else "run"
    one = k == 1
    return (f"{text} **{names} {run} past it**, so {NUMBERS.get(k, str(k)).lower()} "
            f"stop{'s' if not one else ''} beyond the boundary {'are' if not one else 'is'} "
            f"left out: {places}. The line{'s are' if len(lines) != 1 else ' is'} still "
            f"drawn to {'their' if len(lines) != 1 else 'its'} ends, but "
            + ("that stop gets no ring and its businesses are not counted; it is listed in "
               if one else
               "those stops get no ring and their businesses are not counted; they are "
               "listed in ")
            + f"`outputs/{slug}/excluded_stations.csv`. "
            + ("Its commune's" if one else "Their communes'")
            + " businesses are in the same national register this map reads, so leaving "
            + ("it" if one else "them")
            + " out is a choice rather than a limit of the data: the map keeps to the "
              "commune, as the other French maps do.")


def source_clause(cfg, n):
    """The template says the lines come "from the operator's own published
    timetable feed". Where the track is OpenStreetMap's (no usable shapes in the
    feed: Montpellier, Strasbourg, Le Havre, Caen, Rouen) that would be untrue,
    so those pages say which part comes from where - a departure from the
    approved wording, flagged for the owner at review time."""
    feed = ("the Normandie region's published timetable feed"
            if getattr(cfg, "GTFS_AGENCY_ID", None) else
            "the operator's own published timetable feed")
    if cfg.LINE_GEOMETRY != "osm":
        return f"from {feed}"
    its = "its" if n == 1 else "their"
    return f"{its} stops from {feed} and {its} track from OpenStreetMap"


def first_paragraph(cfg, name, operator):
    slug = cfg.OUTPUTS.name
    names = [cfg.LINE_NAMES[k] for k in cfg.LINE_KEYS]
    if slug == "rouen":   # approved departure, owner 2026-09-30
        return (f"One {operator} line is drawn, **{names[0]}**, labelled on the map and in "
                f"the legend, {source_clause(cfg, len(cfg.LINE_KEYS))}. Rouen's métro "
                f"is a light rail running mostly on the street, so every stop gets rings.")
    if slug == "brest":   # approved departure, owner 2026-09-30
        trams = [cfg.LINE_NAMES[k] for k in cfg.LINE_KEYS if k != "C"]
        return (f"Two {operator} tram lines and the cable car are drawn, "
                f"**{joined(trams + [cfg.LINE_NAMES['C']])}**, each labelled on the map and in "
                f"the legend, {source_clause(cfg, len(cfg.LINE_KEYS))}. {name} has no "
                f"metro: its trams are its rapid transit, as Riga's are, so every tram stop "
                f"gets rings.")
    n = len(names)
    return (f"{NUMBERS[n]} {operator} tram line{'s are' if n != 1 else ' is'} drawn, "
            f"**{joined(names)}**, {'each ' if n != 1 else ''}labelled on the map and in the "
            f"legend, {source_clause(cfg, len(cfg.LINE_KEYS))}. {name} has no metro: "
            f"its trams are its rapid transit, as Riga's are, so every tram stop gets rings.")


def prose(cfg, name, operator, m):
    share = round(m["masked_share"] * 100)
    stops = "Stops" if cfg.OUTPUTS.name == "rouen" else "Tram stops"
    return "\n\n".join([
        first_paragraph(cfg, name, operator),
        scope_paragraph(cfg, name, m),
        "Businesses come from **SIRENE**, France's national register of établissements, "
        "joined to INSEE's geolocation file, the same sources as Paris, Marseille, Toulouse, "
        f"Lille and Rennes. About {share}% of active establishments here are marked "
        "non-diffusible by INSEE, which withholds their name, address and coordinates "
        "together, so they never reach this map. Where SIRENE records no shop sign or trading "
        "name, the dot shows the address instead.",
        "**Read the density as a register, not a street survey.** SIRENE records where a "
        "business is *registered*, and some registered establishments have no customer-facing "
        "shopfront; nothing in the data says which. Against OpenStreetMap's mapped restaurants "
        f"in the commune of {name}, where the two schemes mean nearly the same thing, this map "
        f"carries about **{m['osm_ratio']:.1f} times** as many points.",
        f"**{stops} sit closer together than metro stations**, a median of "
        f"{round(m['median_m'] / 10) * 10:,.0f} m here, so the rings are drawn at half the usual "
        f"size (0.05 to 0.3 mi), as on the other French maps. **About {round(m['in_ring'] * 100)}% "
        "of storefronts sit within a ring.**",
        CONTROLS,
    ])


PAGE = '''"""@@DISPLAY@@ heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py; the prose
written by scripts/france_page.py from the French tram-city template the owner
approved word for word (2026-09-29; france-tram-city skill, section 6), every
brace filled from this city's own build. Re-run that script after a rebuild
rather than editing the figures by hand.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.@@SLUG@@.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="@@DISPLAY@@ Heatmap", page_icon="\\U0001f5fa\\ufe0f", layout="wide")
set_base_font()

render_city_nav("@@DISPLAY@@")

st.title("@@DISPLAY@@: commercial density around @@STOPS@@")

st.markdown(
    """
@@PROSE@@
"""
)

# The snapshot, read from outputs/@@SLUG@@/provenance.json rather than
# hardcoded so it cannot go stale on the next fetch. @@LICENCE_NOTE@@
_edition = ""
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _edition = (_prov.get("sirene_etab_title") or "").split(" - ")[-1].split(" (")[0]
        _taken = (_prov.get("fetched_utc") or "")[:10]
        _fi = _prov.get("feed_info") or {}
        _nap = _prov.get("nap") or {}

        def _iso(d):
            d = str(d or "")
            return f"{d[:4]}-{d[4:6]}-{d[6:8]}" if len(d) == 8 and d.isdigit() else d

        _start = _iso(_fi.get("feed_start_date") or _nap.get("start_date"))
        _end = _iso(_fi.get("feed_end_date") or _nap.get("end_date"))
        if _taken:
            _line = "Transit data © @@CREDIT@@, via transport.data.gouv.fr"
            if _start and _end:
                _line += f", from the feed published for **{_start}** to **{_end}**"
            st.caption(_line + f"; snapshot taken **{_taken}**.")
    except (ValueError, OSError):
        # A malformed provenance file must not take the page down.
        pass

# INSEE's prescribed credit, verbatim: « Source : Insee »
# (docs/licenses/france-licence-ouverte-2.0.md, MUST DISPLAY 1). Outside the
# provenance block so a missing or malformed provenance file cannot drop it;
# only the edition comes from that file. Check M of
# scripts/check_provenance.py refuses a page that nests it again.
st.caption("Business data: Source : Insee, SIRENE"
           + (f" ({_edition} edition)" if _edition else "")
           + " and its geolocation file.")

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/@@SLUG@@/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
'''

LICENCE_NOTES = {
    "lov2": "Licence Ouverte 2.0 asks for the producer and the date of the data.",
    "fr-lo": ("Licence Ouverte 1.0 (read 2026-09-29): Bordeaux Métropole is the producer "
              "credited, with the feed's own date; not TBM, Keolis or Mecatran."),
    "odc-odbl": ("ODbL: the §4.3 notice naming this database is in components._NOTICES; "
                 "this caption credits the producer and the date."),
}


def main():
    import scaffold_france_batch as sfb
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("slugs", nargs="+")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    for slug in args.slugs:
        cfg = importlib.import_module(f"pipeline.{slug}.config")
        spec = sfb.BATCH[slug]
        display = spec["name"]
        name = re.sub(r" \(Regional\)$", "", display)
        m = measure(cfg)
        text = prose(cfg, name, spec["operator"], m)
        owner = PRODUCER.get(slug) or legal_owner(cfg)
        if slug == "bordeaux":
            # LO 1.0 read (2026-09-29): Bordeaux Métropole is the producer
            # credited; not TBM, Keolis or the exporter Mecatran.
            credit = "Bordeaux Métropole"
        elif not owner:
            credit = spec["operator"]
        elif "(" in owner:
            credit = f"{owner}, {spec['operator']}"
        else:
            credit = f"{owner} ({spec['operator']})"
        print(f"===== {display}\n{text}\n\n  caption credit: {credit}\n")
        if not args.write:
            continue
        pages = sorted((ROOT / "app" / "pages").glob(f"*_{'_'.join(p.capitalize() for p in slug.split('_'))}_Heatmap.py"))
        if len(pages) != 1:
            sys.exit(f"{slug}: expected one page file, found {[p.name for p in pages]}")
        page = PAGE
        for k, v in {"DISPLAY": display, "SLUG": slug, "PROSE": text,
                     "STOPS": "métro stops" if slug == "rouen" else "tram stops",
                     "CREDIT": credit, "LICENCE_NOTE": LICENCE_NOTES[cfg.GTFS_LICENCE]}.items():
            page = page.replace(f"@@{k}@@", v)
        compile(page, str(pages[0]), "exec")
        pages[0].write_text(page, encoding="utf-8", newline="\n")
        print(f"  wrote {pages[0].relative_to(ROOT)}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
