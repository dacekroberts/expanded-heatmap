"""Monterrey (Regional) heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.monterrey.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Monterrey (Regional) Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Monterrey (Regional)")
render_city_title('Monterrey (Regional)')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/monterrey/step3_map.py` to generate it.")

render_data_age('Monterrey (Regional)')

# No station or business counts in this prose, deliberately (add-city Step 8):
# a computed count in page text goes stale when the pipeline changes. The
# operator's own published per-line figures are facts about the system.
# Approved by the owner 2026-09-27; set as bullets 2026-10-01.
st.markdown(
    """
**The lines**

- Metrorrey runs three lines and this map draws all of them: Línea 1, east–west from
  Talleres to Exposición; Línea 2, north from the city centre to Sendero in General
  Escobedo; and Línea 3, from General I. Zaragoza north-east to Hospital Metropolitano.
- Each line is labelled directly on the map in the name its riders use, and appears in the
  legend.
- Líneas 4 and 6, a monorail network, are under construction and are not drawn.
- **This is a regional map, not a city one.** Línea 2 runs north out of Monterrey through
  San Nicolás de los Garza to General Escobedo, and Línea 1 reaches east into Guadalupe, so
  mapping only the municipio of Monterrey would cut Línea 2 short and lose its northern
  stations, Universidad among them.
- Stations and businesses across Monterrey, San Nicolás de los Garza, Guadalupe and General
  Escobedo are included.
- **The line geometry comes from OpenStreetMap, not from a transit feed.** Nuevo León
  publishes no transit feed or station data for Metrorrey, and neither the operator's nor
  the state's map services could be reached, so the alignments and stations are
  OpenStreetMap contributors' mapping of the network.
- Metrorrey's own network map names nineteen stations on Línea 1, thirteen on Línea 2 and
  nine on Línea 3, and this map matches all three.
- Línea 3 is drawn in red, as on that map; OpenStreetMap gives it orange, which the operator
  uses for Línea 6.

**The businesses**

- **The businesses are a census, not a licence register, and that changes what the map
  means.** Most cities here are built from business licences: a record of who registered.
  Monterrey, like Mexico City and Guadalajara, is built from DENUE, the national business register of INEGI (Mexico's
  statistics agency), compiled by surveying premises and recording the name on the shopfront.
- It is far more complete than a licence register, so the density shown here is **not
  comparable** with the licence-register cities' — read it as a fact about how the data was
  collected as much as about Monterrey's streets.
- Fixed premises only. DENUE separately records semi-fixed units — stalls and street posts —
  and those are not shown, although street commerce is a real part of the region's retail.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Monterrey (Regional)")
render_country_links('Monterrey (Regional)')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
