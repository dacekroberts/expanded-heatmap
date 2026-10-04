"""Mexico City heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.mexico_city.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_data_age,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Mexico City Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Mexico City")
render_city_title('Mexico City')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/mexico_city/step3_map.py` to generate it.")

render_data_age('Mexico City')

# No counts in this prose, deliberately: add-city Step 8's rule is that a
# station count or a "twelve lines" in page text is literal and goes stale when
# the pipeline changes. Line names are safe - they are the operator's, not
# computed.
st.markdown(
    """
**The lines**

- Metro CDMX runs twelve lines — Líneas 1 to 9, A, B and 12 — and this map draws all of them
  alongside the STE Tren Ligero, which continues south from Tasqueña to Xochimilco.
- Each line is labeled directly on the map in the name its riders use, and appears in the
  legend.
- Only stations inside Ciudad de México are mapped. Líneas A and B run north and east into
  the State of Mexico, and Línea 2 ends just across the city line at Cuatro Caminos; those
  stations are left out because this map has no business data there. They are listed below.
- **The line geometry here comes from OpenStreetMap, not from the operator.** None of the
  public servers of the Mexico City government, STC Metro or the STE could be reached from
  where this was built, and the Metro's transit feed refused the download.
- So the alignments are OpenStreetMap contributors' mapping of the network rather than the
  agency's own file. For the same reason, the station count has not been checked against
  what STC Metro publishes.

**The businesses**

- **The businesses are a census, not a license register, and that changes what the map
  means.** Most cities here are built from business licenses: a record of who registered.
  Mexico City is built from DENUE, the national business register of INEGI (Mexico's
  statistics agency), compiled by surveying premises and recording the name on the shopfront.
- It is far more complete than a license register, so the density shown here is **not
  comparable** with the license-register cities' — read it as a fact about how the data was
  collected as much as about Mexico City's streets.
- Fixed premises only. DENUE separately records semi-fixed units — stalls and street posts —
  and those are not shown, although street commerce is a real and substantial part of the
  city's retail.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Mexico City")
render_country_links('Mexico City')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. This page did not call it until
# 2026-09-22; the scaffold template omitted it.
render_site_notices("Mexico City")
