"""Sydney heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.sydney.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Sydney Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Sydney")
render_city_title('Sydney')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/sydney/step3_map.py` to generate it.")

# The survey year, read from outputs/sydney/provenance.json so it cannot go
# stale on the next fetch.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _year = _prov.get("fes_year")
        if _year:
            st.caption(f"Snapshot: the City of Sydney's Floor Space and Employment Survey, "
                       f"**{_year}**.")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

# Approved by the owner 2026-09-28.
st.markdown(
    """
Seven lines are drawn: Sydney Trains' **T1, T2, T3, T4, T8 and T9** and Sydney
Metro's **M1**, each labelled on the map, with its full name in the legend,
redrawn from OpenStreetMap. The colours are close to Transport for NSW's but
not the same: some are too close to the dot colours, so T4 and M1 appear in
slate. Sydney Trains is suburban rail that runs as a metro through the city
centre; every station in the area is shown. **Light rail is not drawn.** The
L1, L2 and L3 lines have 22 stops in the area; with them, about nine
storefronts in ten would sit within a ring, against eight in ten without
them. NSW TrainLink services and ferries are not drawn either.

The map covers the **City of Sydney** council area only: the CBD, Pyrmont and
Ultimo, Surry Hills, Redfern, Green Square, Kings Cross and the inner suburbs
to Glebe and Newtown. Neighbouring councils publish no comparable survey, so
they are not on the map. Lines are cut at the boundary, and the stations
beyond it are left out.

**The businesses come from the City of Sydney's Floor Space and Employment
Survey**, a count of every business establishment in the area that the City
takes every five years. This map uses the **2022** survey, the latest. It
gives each business an industry class and a map point but **no name**, so a
dot shows what kind of business it is, not what it is called. Points are
placed per building, so the shops in a shopping centre share one point.

Shops, food and personal services are all shown; car and fuel retailers count
as shops, as in the other cities. Left out: parking, catering firms, funeral
services, religious and membership organisations, licensed members' clubs,
brothels, and the survey's "other personal services" class, which in
Melbourne's census holds mostly consultancies in office suites.

**About five storefronts in six sit within a station ring.**

Concentric ring boundaries and the business categories (Retail, Food service
and Personal services) are toggleable via the layer control in the top left.
When enabled, business density will display as numbered circles summing areas
when zoomed out. Zooming in will show individual dots; hover over those to see
further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a
statistical density estimate, so read the colour as "roughly where things
cluster."
"""
)

render_map_help('business categories (Retail, Food service and Personal services)')
render_country_links('Sydney')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices()
