"""Le Mans heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.le_mans.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Le Mans Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Le Mans")
render_city_title("Le Mans")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/le_mans/step3_map.py` to generate it.")

# The snapshot, read from outputs/le_mans/provenance.json rather than
# hardcoded so it cannot go stale on the next fetch. Licence Ouverte 2.0 asks for the producer and the date of the data.
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
            _line = "Transit data © CU Le Mans Métropole (SETRAM), via transport.data.gouv.fr"
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

st.markdown(
    """
**The trams**

- Two SETRAM tram lines are drawn, **Tram T1 and Tram T2**, each labelled on the map and in the legend, from the operator's own published timetable feed.
- Le Mans has no metro: its trams are its rapid transit, as Riga's are, so every tram stop gets rings.
- **Tram stops sit closer together than metro stations**, a median of 440 m here, so the rings are drawn at half the usual size (0.05 to 0.3 mi), as on the other French maps.
- The map covers the **commune of Le Mans**.

**The businesses**

- Businesses come from **SIRENE**, France's national register of établissements, joined to INSEE's geolocation file, the same sources as Paris, Marseille, Toulouse, Lille and Rennes.
- About 16% of active establishments here are marked non-diffusible by INSEE, which withholds their name, address and coordinates together, so they never reach this map.
- Where SIRENE records no shop sign or trading name, the dot shows the address instead.
- **About 73% of storefronts sit within a ring.**

**Reading the density**

- **Read the density as a register, not a street survey.** SIRENE records where a business is *registered*, and some registered establishments have no customer-facing shopfront; nothing in the data says which.
- Against OpenStreetMap's mapped restaurants in the commune of Le Mans, where the two schemes mean nearly the same thing, this map carries about **1.8 times** as many points.
"""
)

render_map_help("three business categories (Retail, Food service and Personal services)")
render_excluded_stations("Le Mans")
render_country_links("Le Mans")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
