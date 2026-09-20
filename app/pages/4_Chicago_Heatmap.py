"""Chicago heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview_&_Introduction.py's docstring for why this is the decided pattern
for every city's detail page.
"""

import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.chicago.config import HEATMAP_HTML  # noqa: E402
from components import render_city_nav, set_base_font  # noqa: E402

st.set_page_config(page_title="Chicago Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Chicago")

st.title("Chicago: commercial density around 'L' station areas")

st.markdown(
    """
Stations are represented by dots along the CTA 'L' (the Red, Blue, Brown,
Green, Orange, Pink and Purple Lines - each labeled directly on the map and
in the legend, in the CTA's own line colors). Only stations inside the City of
Chicago are shown: the lines also serve Evanston, Oak Park, Forest Park,
Cicero and other suburbs, whose businesses come from separate registries. The
stations left out are listed in `outputs/chicago/excluded_stations.csv`. The
Yellow Line is not drawn, since its only station in the city (Howard) is also
served by the Red and Purple Lines. Metra commuter rail is not included.
Concentric ring boundaries and license-classified storefronts (Retail, Food
service and Personal services, grouped from the city's own business license
types) are toggleable via the layer control in the top left. When enabled,
business density will display as numbered circles summing areas when zoomed
out. Zooming in will show individual dots; hover over those to see further
details.

The data is Chicago's business-license registry, limited to currently
active licenses. Some licenses carry no coordinates (mostly home-based
businesses with redacted addresses) and are left off the map.

The heat layer is illustrative. Leaflet applies a visual blur rather than a
statistical density estimate, so read the colour as "roughly where things
cluster."
"""
)

if HEATMAP_HTML.exists():
    heatmap_html = HEATMAP_HTML.read_text(encoding="utf-8")
    components.html(heatmap_html, width=1000, height=650, scrolling=True)
else:
    st.info("No map yet. Run `python pipeline/chicago/step3_map.py` to generate it.")
