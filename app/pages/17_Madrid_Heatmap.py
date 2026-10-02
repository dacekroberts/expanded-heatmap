"""Madrid heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.madrid.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Madrid Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Madrid")
render_city_title('Madrid')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/madrid/step3_map.py` to generate it.")

render_data_age('Madrid')

st.markdown(
    """
**The lines**

- **The rail network comes from CRTM's own published layers, not from a transit feed.**
- **Metro Ligero line 1 is drawn as well**, from the same CRTM layers. It runs from Pinar de
  Chamartín to Las Tablas through Sanchinarro, districts the Metro does not reach; all nine of its
  stations are inside the city, and two are shared with the Metro.
- Metro Ligero's lines 2 and 3 are not drawn: each has only one or two stations inside Madrid
  before running on into Pozuelo and Boadilla. Line 4 is Parla's own tram.
- **Stations outside the city are not mapped.** Forty-nine of the 249 stations on the lines drawn
  here lie in Alcorcón, Getafe, Arganda del Rey and fifteen other municipalities.
- Lines 10 and 12 run well past the city and are drawn in full, but mapping their stations would
  need each municipality's own business register. They are listed below.

**The businesses**

- **The businesses are a premises census, not a licence register, and that changes what the map
  means.** Most cities here are built from business licences - a record of who registered.
- Madrid is built from the Ayuntamiento's *Censo de locales*, which records the unit on the street
  and the sign above its door: the same shape as Montréal's commercial survey, and the density here
  is close to Montréal's for that reason.
- It is **not comparable** with the licence-register cities, where what is counted is a
  registration rather than a shopfront.
- Retail, food service and personal services, as the register's own activity classification
  defines them. Hotels and tourist flats are excluded - they are accommodation rather than food
  service.

**Reading the map**

- **About one storefront premises in eleven cannot be placed on this map.** The register gives
  every premises a coordinate, but 9.2% of the ones in these three categories carry a literal zero
  rather than a location. Those are left out rather than guessed at.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Madrid")
render_country_links('Madrid')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
