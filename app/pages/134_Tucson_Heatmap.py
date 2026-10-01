"""Tucson heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.tucson.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Tucson Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Tucson")
render_city_title('Tucson')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/tucson/step3_map.py` to generate it.")

# The fetch dates, read from outputs/tucson/provenance.json so they cannot go
# stale: the City rebuilds the licence layer daily, so the fetch date is the
# data date.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _files = _prov.get("files_utc") or {}
        _reg = (_files.get("buslic_active.csv") or "")[:10]
        _rail = (_files.get("osm_rail.json") or "")[:10]
        if _reg and _rail:
            st.caption(f"Business licence data: City of Tucson, fetched **{_reg}**; the "
                       f"streetcar line and its stops from OpenStreetMap, fetched "
                       f"**{_rail}**.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# The tram-city skill's page-text template, approved by the owner word for
# word on 2026-09-30, filled from Tucson's own step 1 and step 2 figures; the
# business paragraphs follow Houston's, the template city for a US register.
# The licence is silent and read as permitted (owner, 2026-09-30): the City is
# credited (notice 81) and the pins are never called complete.
st.markdown(
    """
One streetcar line is drawn, **Sun Link**, labelled on the map and in the
legend, redrawn from OpenStreetMap's route geometry, in a colour this project
chose, since the source records none. Tucson has no metro: its streetcar is
its rapid transit, as Riga's trams are, so every stop gets rings. Streetcars
run about every 10 minutes on weekdays from 7 am to 6 pm, and every 20 minutes
in the evenings and at weekends. Buses are not drawn.

The map covers the **City of Tucson**, as the US Census Bureau draws its
limits. Every streetcar stop is inside it.

Businesses come from the City of Tucson's list of **active business
licences**, with each licence's industry code, placed at the point the City
records for it and kept only if that point falls inside the city. Licences for
a home occupation are left out, and so is any business at an apartment or
trailer address, as a home. About one licence in thirteen has no point and
cannot be placed. **Where the licence holder is a person rather than a
company, the map shows the street address instead of a name**, and so it does
where a business is named only as a person.

Online and mail-order sellers are left out by their industry code, as are
caterers, food trucks, contract canteens, parking, funeral services and the
catch-all "other personal services".

**Read the density as a register, not a street survey.** The City says its
list should not be considered a complete listing of all active businesses in
Tucson, and a licence is issued to a business at an address whether or not a
passer-by could walk in.

**Tram stops sit closer together than metro stations**, a median of 265 m
here, so the rings are drawn at half the usual size (0.05 to 0.3 mi). **About
one storefront in fifteen sits within a ring.**

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

render_map_help('three business categories (Retail, Food service and Personal services)')
render_country_links('Tucson')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
