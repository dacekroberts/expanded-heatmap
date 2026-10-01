"""Chicago heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.chicago.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_data_age,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Chicago Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Chicago")
render_city_title("Chicago")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/chicago/step3_map.py` to generate it.")

render_data_age("Chicago")

st.markdown(
    """
**The lines**

- Stations are represented by dots along the CTA 'L': the Red, Blue, Brown, Green, Orange, Pink
  and Purple Lines, each labeled directly on the map and in the legend, in the CTA's own line
  colors.
- Only stations inside the City of Chicago are shown. The lines also serve Evanston, Oak Park,
  Forest Park, Cicero and other suburbs, whose businesses come from separate registries.
- The Yellow Line is not drawn, since its only station in the city (Howard) is also served by
  the Red and Purple Lines.
- Metra commuter rail is not included.

**The businesses**

- The data is Chicago's business-license registry, limited to currently active licenses.
- Storefronts are grouped into Retail, Food service and Personal services from the city's own
  business license types.
- Some licenses carry no coordinates (mostly home-based businesses with redacted addresses) and
  are left off the map.
"""
)

render_map_help("license-classified storefronts")
render_country_links("Chicago")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES.
render_site_notices()
