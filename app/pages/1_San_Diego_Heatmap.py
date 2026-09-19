"""San Diego heatmap page - embeds the pre-rendered Folium HTML.

Reading the saved file as a raw component is faster than re-rendering the
map through streamlit-folium, and avoids pulling folium into the deployed
app's dependencies - see Overview_&_Introduction.py's docstring for why
this is the decided pattern for every city's detail page, not just this
one.
"""

import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.san_diego.config import HEATMAP_HTML  # noqa: E402
from components import render_city_nav, set_base_font  # noqa: E402

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

The heat layer is illustrative. Leaflet applies a visual blur rather than
a statistical density estimate, so read the colour as "roughly where
things cluster."
"""
)

if HEATMAP_HTML.exists():
    # folium always saves this file as UTF-8. On Windows, Path.read_text()
    # without an explicit encoding falls back to the OS codepage, which
    # mangles multi-byte characters - not a bug in the saved file, only in
    # how it's read back here.
    heatmap_html = HEATMAP_HTML.read_text(encoding="utf-8")
    # Matches the Folium map's own fixed pixel size (width=1000, height=650
    # in pipeline/san_diego/step3_map.py) exactly.
    components.html(heatmap_html, width=1000, height=650, scrolling=True)
else:
    st.info("No map yet. Run `python pipeline/san_diego/step3_map.py` to generate it.")
