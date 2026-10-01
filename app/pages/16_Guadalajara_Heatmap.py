"""Guadalajara heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.guadalajara.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Guadalajara (Regional) Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Guadalajara (Regional)")
render_city_title('Guadalajara (Regional)')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/guadalajara/step3_map.py` to generate it.")

render_data_age('Guadalajara (Regional)')

# No station or business counts in this prose, deliberately: add-city Step 8's
# rule is that a count in page text is literal and goes stale when the pipeline
# changes. Line names, opening years and the operator's own published figures
# are safe - they are facts about the system, not computed values.
st.markdown(
    """
**The lines**

- Guadalajara's Tren Ligero runs four lines and this map draws all of them. Each line is
  labelled directly on the map in the name its riders use, and appears in the legend.
- Líneas 1 and 2 are the original network, from 1989 and 1994; Línea 3 opened in 2020,
  connecting Zapopan, Guadalajara and Tlaquepaque; Línea 4 opened in December 2025, running
  south to Tlajomulco de Zúñiga.
- **This is a regional map, not a city one.** Two of the four lines exist to connect
  separate municipios, so mapping only the municipio of Guadalajara would cut both of them
  short.
- Stations across Guadalajara, Zapopan, San Pedro Tlaquepaque and Tlajomulco de Zúñiga are
  included. Tonalá is not included: no line reaches it.
- **The line geometry comes from OpenStreetMap, not from a transit feed.** A GTFS feed for
  Guadalajara does exist, but it contains three lines: building from it would have produced
  a map missing an operating line, eight stations and twenty-one kilometres, while looking
  complete. OpenStreetMap has all four.
- Where SITEUR publishes a station count, this map matches it: ten for Línea 2 and eight for
  Línea 4.

**The businesses**

- **The businesses are a census, not a licence register, and that changes what the map
  means.** Most cities here are built from business licences: a record of who registered.
  Guadalajara, like Mexico City, is built from INEGI's DENUE, compiled by surveying premises
  and recording the name on the shopfront.
- It is far more complete than a licence register, so the density shown here is **not
  comparable** with the licence-register cities' — read it as a fact about how the data was
  collected as much as about Guadalajara's streets.
- Fixed premises only. DENUE separately records semi-fixed units — stalls and street posts —
  and those are not shown, although street commerce is a real part of the region's retail.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Guadalajara (Regional)")
render_country_links('Guadalajara (Regional)')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. This page did not call it until
# 2026-09-22; the scaffold template omitted it.
render_site_notices()
