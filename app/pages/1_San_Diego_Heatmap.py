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
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="San Diego Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("San Diego")

st.title("San Diego: commercial density around Trolley station areas")

st.markdown(
    """
Stations are represented by blue dots along the MTS Trolley's five lines
(Blue, Orange, Green, Copper, Silver - each labeled directly on the map).
Concentric ring boundaries and NAICS-geocoded storefronts are toggleable
via the layer control in the top left. When enabled, business density
will display as numbered circles summing areas when zoomed out. Zooming
in will show individual dots; hover over those to see further details.

Top right: a **Cities** menu and an **All cities** button for moving
between maps, and a light/dark switch. The map opens in whichever mode
the page is using; once you pick one, it carries across the other city
maps.

The heat layer is illustrative. Leaflet applies a visual blur rather than
a statistical density estimate, so read the colour as "roughly where
things cluster."
"""
)

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/san_diego/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES.
render_site_notices()
