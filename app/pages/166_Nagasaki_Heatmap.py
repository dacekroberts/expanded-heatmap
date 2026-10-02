"""Nagasaki heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py, in the
city-page format of 2026-10-01 (owner): title, map, captions, bullets, map help,
country links, notices.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.nagasaki.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_data_age,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Nagasaki Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Nagasaki")
render_city_title("Nagasaki")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/nagasaki/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Nagasaki")

# TODO: replace every TODO bullet with prose true for this city, as short
# bullets under bold headings (app/pages/43_Seoul_Heatmap.py is the model):
# the lines by name, what is not drawn, the area and the stations left out, the
# source and its limitations. Detail a reference page carries stays there.
st.markdown(
    """
**The lines**

- TODO: the lines drawn, by name (each is labeled on the map and in the legend).
- TODO: what is not drawn, and why.
- TODO: the area covered; stations left out are listed below.

**The businesses**

- TODO: the data source, and any category it is missing.
"""
)

render_map_help("three business categories (Retail, Food service and Personal services)")
render_excluded_stations("Nagasaki")
render_country_links("Nagasaki")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
