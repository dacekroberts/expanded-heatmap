"""Los Angeles heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview_&_Introduction.py's docstring for why this is the decided pattern
for every city's detail page.
"""

import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.los_angeles.config import HEATMAP_HTML  # noqa: E402
from components import render_city_nav, set_base_font  # noqa: E402

st.set_page_config(page_title="Los Angeles Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Los Angeles")

st.title("Los Angeles: commercial density around Metro Rail station areas")

st.markdown(
    """
Stations are represented by blue dots along LA Metro Rail (the A, B, C, D, E
and K Lines - each labeled directly on the map and in the legend, in Metro's
own line colors). Only stations inside the City of Los Angeles are shown:
the lines also serve Long Beach, Pasadena, Santa Monica and many other
cities, whose businesses come from separate city registries. The stations
left out are listed in `outputs/los_angeles/excluded_stations.csv`.
Concentric ring boundaries and NAICS-coded storefronts are toggleable via
the layer control in the top left. When enabled, business density will
display as numbered circles summing areas when zoomed out. Zooming in will
show individual dots; hover over those to see further details.

Some businesses in the city's registry carry corrupt coordinates, mostly
recent registrations; these were placed by geocoding their street address
instead of being dropped.

The heat layer is illustrative. Leaflet applies a visual blur rather than a
statistical density estimate, so read the colour as "roughly where things
cluster."
"""
)

if HEATMAP_HTML.exists():
    heatmap_html = HEATMAP_HTML.read_text(encoding="utf-8")
    components.html(heatmap_html, width=1000, height=650, scrolling=True)
else:
    st.info("No map yet. Run `python pipeline/los_angeles/step4_map.py` to generate it.")
