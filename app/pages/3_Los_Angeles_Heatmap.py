"""Los Angeles heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.los_angeles.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Los Angeles (Regional) Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Los Angeles (Regional)")
render_city_title('Los Angeles (Regional)')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/los_angeles/step4_map.py` to generate it.")

render_data_age('Los Angeles (Regional)')

st.markdown(
    """
**The lines**

- Stations are represented by blue dots along LA Metro Rail: the A, B, C, D, E and K Lines, each
  labeled directly on the map and in the legend, in Metro's own line colors.
- Only stations inside the City of Los Angeles and the City of Long Beach are shown. The lines
  also serve Pasadena, Santa Monica and many other cities, whose businesses come from separate city
  registries.
- The stations left out are listed below.

**The businesses**

- Businesses in the City of Los Angeles come from its Office of Finance's list of active
  businesses; those in Long Beach come from the City of Long Beach's business licenses, sorted
  into the same three categories from each license's type.
- Some businesses in the Los Angeles registry carry corrupt coordinates, mostly recent
  registrations; these were placed from their street address instead of being dropped.
- In Long Beach, a license that gives no trade name shows its street address.
- Where a business is registered under a person's name alone, with no trade name, or a person's
  name sits at an apartment or other dwelling unit, the map shows its street address instead of a
  name.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Los Angeles (Regional)")
render_country_links('Los Angeles (Regional)')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES.
render_site_notices("Los Angeles (Regional)")
