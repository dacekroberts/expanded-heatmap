"""San Diego heatmap page - embeds the pre-rendered Folium HTML.

Reading the saved file as a raw component is faster than re-rendering the
map through streamlit-folium, and avoids pulling folium into the deployed
app's dependencies - see Overview.py's docstring for why
this is the decided pattern for every city's detail page, not just this
one.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.san_diego.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="San Diego Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("San Diego")
render_city_title('San Diego')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/san_diego/step3_map.py` to generate it.")

render_data_age('San Diego')

st.markdown(
    """
**The lines**

- Stations are represented by blue dots along the MTS Trolley's five lines: Blue, Orange, Green,
  Copper and Silver, each labeled directly on the map.
"""
)

render_map_help('NAICS-geocoded storefronts')
render_excluded_stations("San Diego")
render_country_links('San Diego')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES.
render_site_notices()
