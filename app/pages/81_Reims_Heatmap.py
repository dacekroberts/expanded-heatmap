"""Reims heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.reims.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Reims Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Reims")

st.title("Reims: commercial density around tram stops")

st.markdown(
    """
Two Grand Reims Mobilités tram lines are drawn, **Tram T1 and Tram T2**, each labelled on the map and in the legend, from the operator's own published timetable feed. Reims has no metro: its trams are its rapid transit, as Riga's are, so every tram stop gets rings.

The map covers the **commune of Reims**. **Tram T1 and Tram T2 run past it**, so three stops beyond the boundary are left out: Gare de Champagne-Ardenne TGV and Polyclinique in Bezannes; Neufchatel in Bétheny. The lines are still drawn to their ends, but those stops get no ring and their businesses are not counted; they are listed in `outputs/reims/excluded_stations.csv`. Their communes' businesses are in the same national register this map reads, so leaving them out is a choice rather than a limit of the data: the map keeps to the commune, as the other French maps do.

Businesses come from **SIRENE**, France's national register of établissements, joined to INSEE's geolocation file, the same sources as Paris, Marseille, Toulouse, Lille and Rennes. About 18% of active establishments here are marked non-diffusible by INSEE, which withholds their name, address and coordinates together, so they never reach this map. Where SIRENE records no shop sign or trading name, the dot shows the address instead.

**Read the density as a register, not a street survey.** SIRENE records where a business is *registered*, and some registered establishments have no customer-facing shopfront; nothing in the data says which. Against OpenStreetMap's mapped restaurants in the commune of Reims, where the two schemes mean nearly the same thing, this map carries about **2.6 times** as many points.

**Tram stops sit closer together than metro stations**, a median of 370 m here, so the rings are drawn at half the usual size (0.05 to 0.3 mi), as on the other French maps. **About 55% of storefronts sit within a ring.**

Concentric ring boundaries and the three business categories (Retail, Food
service and Personal services) are toggleable via the layer control in the top
left. When enabled, business density will display as numbered circles summing
areas when zoomed out. Zooming in will show individual dots; hover over those
to see further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a
statistical density estimate, so read the colour as "roughly where things
cluster."
"""
)

# The snapshot, read from outputs/reims/provenance.json rather than
# hardcoded so it cannot go stale on the next fetch. Licence Ouverte 2.0 asks for the producer and the date of the data.
# SIRENE's line carries INSEE's prescribed « Source : Insee ».
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _taken = (_prov.get("fetched_utc") or "")[:10]
        _fi = _prov.get("feed_info") or {}
        _nap = _prov.get("nap") or {}

        def _iso(d):
            d = str(d or "")
            return f"{d[:4]}-{d[4:6]}-{d[6:8]}" if len(d) == 8 and d.isdigit() else d

        _start = _iso(_fi.get("feed_start_date") or _nap.get("start_date"))
        _end = _iso(_fi.get("feed_end_date") or _nap.get("end_date"))
        if _taken:
            _line = "Transit data © CU du Grand Reims (Grand Reims Mobilités), via transport.data.gouv.fr"
            if _start and _end:
                _line += f", from the feed published for **{_start}** to **{_end}**"
            st.caption(_line + f"; snapshot taken **{_taken}**.")
            _edition = (_prov.get("sirene_etab_title") or "").split(" - ")[-1].split(" (")[0]
            st.caption("Business data: Source : Insee, SIRENE"
                       + (f" ({_edition} edition)" if _edition else "")
                       + " and its geolocation file.")
    except (ValueError, OSError):
        # A malformed provenance file must not take the page down.
        pass

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/reims/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
