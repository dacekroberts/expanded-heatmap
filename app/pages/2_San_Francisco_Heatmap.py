"""San Francisco heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview_&_Introduction.py's docstring for why this is the decided
pattern for every city's detail page.
"""

import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.san_francisco.config import HEATMAP_HTML  # noqa: E402
from components import render_city_nav, set_base_font  # noqa: E402

st.set_page_config(page_title="San Francisco Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("San Francisco")

st.title("San Francisco: commercial density around Muni Metro station areas")

st.markdown(
    """
Stations are represented by blue dots along Muni Metro's six lines (J
Church, K Ingleside, L Taraval, M Ocean View, N Judah, T Third Street -
each labeled directly on the map and in the legend). Every underground
subway station is shown; the street-running stretches of each line are
thinned to roughly one station per half mile (plus each line's terminals
and any transfer points) so the rings stay readable - the excluded
stations are documented in `outputs/san_francisco/excluded_stations.csv`.
Concentric ring boundaries and NAICS-geocoded storefronts are toggleable
via the layer control in the top left. When enabled, business density
will display as numbered circles summing areas when zoomed out. Zooming
in will show individual dots; hover over those to see further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than
a statistical density estimate, so read the colour as "roughly where
things cluster."
"""
)

if HEATMAP_HTML.exists():
    heatmap_html = HEATMAP_HTML.read_text(encoding="utf-8")
    components.html(heatmap_html, width=1000, height=650, scrolling=True)
else:
    st.info("No map yet. Run `python pipeline/san_francisco/step3_map.py` to generate it.")
