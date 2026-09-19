"""Entry page - project intro plus the city picker.

Architecture decision this implements (see docs/project_context.md,
"Architecture decision: made"): a lightweight overview - city markers
only, no business-level detail - that routes into each city's own
independent detail page. Deliberately built with Streamlit's native
st.map (pydeck-backed, no folium) rather than a folium/streamlit-folium
overview map: this project's app-side dependency is meant to stay lean
(see requirements.txt's own comment - "no geopandas, no GDAL, no
compiled geo stack"), and streamlit-folium's bidirectional Python<->JS
component is a heavier, different architecture than the static-HTML-embed
pattern the per-city detail pages use (see pages/1_San_Diego_Heatmap.py).
A plain marker overview plus explicit page-link buttons gets the "one
picker" feel without pulling folium into the app runtime at all.
"""

import pandas as pd
import streamlit as st

from components import set_base_font

st.set_page_config(page_title="Expanded Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

st.title("Commercial density near transit, city by city")

st.markdown(
    """
This project maps commercial/business density around rail transit station
areas, one city at a time. Each city below has its own independently
scoped detail map - its own map instance, its own data, its own viewport
bounds - rather than one shared map instance loading every city's
business points at once. See a city's own page for its heat map, transit
line overlays, and business category layers.
"""
)

# The city registry this picker iterates over. Still inline here rather
# than a shared data/registry.yaml loader - San Diego is the first and
# only city built so far (see docs/project_context.md, "San Diego: first
# city, built and running end-to-end"); this table gets pulled out into a
# real per-city YAML file once a second city makes the common shape
# clear, not guessed ahead of that.
CITIES = [
    {
        "name": "San Diego",
        "lat": 32.7157,
        "lon": -117.1611,
        "page": "pages/1_San_Diego_Heatmap.py",
        "blurb": "MTS Trolley (Blue, Orange, Green, Copper, Silver lines)",
    },
    {
        "name": "San Francisco",
        "lat": 37.7509,
        "lon": -122.4414,
        "page": "pages/2_San_Francisco_Heatmap.py",
        "blurb": "Muni Metro (J Church, K Ingleside, L Taraval, M Ocean View, N Judah, T Third Street)",
    },
]

st.subheader("Covered cities")
st.map(pd.DataFrame(CITIES)[["lat", "lon"]], size=200, color="#a50f15")

for city in CITIES:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{city['name']}** — {city['blurb']}")
    with col2:
        st.page_link(city["page"], label=f"Open {city['name']} →")
