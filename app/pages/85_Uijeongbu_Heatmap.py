"""Uijeongbu heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.uijeongbu.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Uijeongbu Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Uijeongbu")

st.title("Uijeongbu: commercial density around subway stations")

# Bucheon's text (approved by the owner 2026-09-29), with Uijeongbu's lines; written
# under the owner's pre-approval of this build's prose (2026-09-30).
st.markdown(
    """
Three lines are drawn — the **U Line** (the Uijeongbu light rail), **Line 1** and **Line 7** —
each labelled on the map and in the legend, in the operators' colours. Routes and stations
come from OpenStreetMap. Businesses are counted around stations inside Uijeongbu only; the
lines are still drawn to their ends. Hoeryong is served by Line 1 and the U Line; Line 7 has
one station in the city, Jangam. No other rail line has a station in the city.

Businesses come from the **Small Enterprise and Market Service's commercial-district register**
(소상공인시장진흥공단 상가(상권)정보), a national record of trading storefronts with a map
position for every one: restaurants, cafés and bars; shops of every kind, from convenience
stores and supermarkets to clothing, phones and pharmacies; and hair, nail and skin-care salons,
laundries, bathhouses and massage. Left out, as on this project's other maps: offices and
professional services, clinics, schools and academies, estate agents, lodging, gyms and
entertainment, repairs, funeral services, staff canteens, hostess bars and household fuel
dealers. The register is compiled nationally, and it is a different kind of record from the
city licence data behind Seoul's, Daegu's and Busan's maps, which count only licensed trades: so
**Uijeongbu's Retail category is complete where those cities' is thin**, and density is not
directly comparable between them.

Each dot carries the storefront's name, in Korean, with its branch where it has one, and its
kind in English. Where a registered name is a bare personal name at what reads as a home
address, the name is withheld. The whole city is included; storefronts beyond walking distance
of a station add to the all-city layer and nothing to the rings.

Concentric ring boundaries and the three business categories (Food service, Retail and Personal
services) are toggleable via the layer control in the top left. When enabled, business density
will display as numbered circles summing areas when zoomed out. Zooming in will show individual
dots; hover over those to see further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a statistical density
estimate, so read the colour as "roughly where things cluster."
"""
)

# The register's edition, read from outputs/uijeongbu/provenance.json so it
# cannot go stale on the next fetch.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _ed = (_prov.get("semas") or {}).get("edition")
        if _ed:
            st.caption(f"Snapshot: SEMAS's storefront register, edition of **{_ed}**.")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/uijeongbu/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices()
