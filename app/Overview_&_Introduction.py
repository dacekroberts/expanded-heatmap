"""Entry page - project intro plus the macro map (the city picker).

This is the macro level of the hybrid architecture (see docs/project_context.md):
one lightweight map of every mapped city, then an independent detail map per
city. Click a city marker and the app jumps to that city's page.

Built with pydeck, which ships with Streamlit (no extra dependency), rather
than folium/streamlit-folium: this project keeps folium out of the deployed
runtime (see requirements.txt). st.pydeck_chart(on_select="rerun") returns the
clicked marker, and st.switch_page navigates without a full page reload. A
plain list of page links sits below the map as a fallback (keyboard access,
and any browser where the map doesn't load).
"""

import math

import pandas as pd
import pydeck as pdk
import streamlit as st

from cities import CITIES
from components import set_base_font

st.set_page_config(page_title="Expanded Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

st.title("Commercial density near transit, city by city")

st.markdown(
    """
This project maps commercial/business density around rail transit station
areas, one city at a time. Each city has its own independently scoped detail
map - its own map instance, its own data, its own viewport bounds - rather
than one shared map instance loading every city's business points at once.
**Click a city on the map to open its detail map**; each city page also has a
switcher to jump straight to another city.
"""
)

st.subheader("Covered cities")

cities = pd.DataFrame(CITIES)
TEAL = [13, 148, 136, 235]
DARK = [28, 43, 42, 255]

markers = pdk.Layer(
    "ScatterplotLayer",
    id="cities",
    data=cities,
    get_position="[lon, lat]",
    get_radius=11,
    # pdk.types.String, not a bare str: pydeck would serialize "pixels" as the
    # expression "@@=pixels" (an undefined variable) and break the radius.
    radius_units=pdk.types.String("pixels"),
    get_fill_color=TEAL,
    get_line_color=[255, 255, 255, 255],
    stroked=True,
    line_width_min_pixels=2,
    pickable=True,
    auto_highlight=True,
    highlight_color=[251, 191, 36, 255],
)
# Permanent city-name labels (not hover-only), consistent with the per-city
# maps' rule that things a reader needs to identify are always visible.
labels = pdk.Layer(
    "TextLayer",
    id="city-labels",
    data=cities,
    get_position="[lon, lat]",
    get_text="name",
    get_size=15,
    get_color=DARK,
    get_pixel_offset=[0, -24],
    # Same typeface as the rest of the app (components.set_base_font). String()
    # for the same reason as radius_units above.
    font_family=pdk.types.String("Space Grotesk, sans-serif"),
    font_weight=600,
    pickable=False,
)

def fit_view(lats, lons, width_px=340, height_px=460, fill=0.7):
    """A view that shows every city with some margin, for any number of
    cities. Web-Mercator maths on the bounding box (512 px world tiles, as in
    Mapbox/Carto vector maps), sized for a phone-width (~340 px) container so
    nothing is cropped there; on a wide screen the same view just has more
    margin. (pydeck's own compute_view assumes a different viewport and
    cropped San Diego and San Francisco out of the same view.)"""
    lat_span = max(max(lats) - min(lats), 0.5)
    lon_span = max(max(lons) - min(lons), 0.5)
    centre_lat = (max(lats) + min(lats)) / 2
    z_lon = math.log2(width_px * 360 * fill / (512 * lon_span))
    z_lat = math.log2(height_px * 360 * fill * math.cos(math.radians(centre_lat)) / (512 * lat_span))
    zoom = max(3.0, min(z_lon, z_lat, 9.0))
    return pdk.ViewState(latitude=centre_lat, longitude=(max(lons) + min(lons)) / 2, zoom=zoom)


view = fit_view(cities["lat"].tolist(), cities["lon"].tolist())

# Carto basemap: pydeck's own default style needs a Mapbox token; Carto's
# public styles don't. (Tile provider is still an open decision before
# deploying - see PLAN.md.)
deck = pdk.Deck(
    layers=[markers, labels],
    initial_view_state=view,
    map_provider="carto",
    map_style="light",
    tooltip={
        "html": "<b>{name}</b><br/>{blurb}",
        "style": {"backgroundColor": "#1c2b2a", "color": "white", "fontSize": "13px"},
    },
)

event = st.pydeck_chart(
    deck,
    on_select="rerun",
    selection_mode="single-object",
    key="macro_map",
    height=460,
)

picked = (event.selection.objects or {}).get("cities", []) if event else []
if picked:
    target = next((c for c in CITIES if c["name"] == picked[0].get("name")), None)
    if target:
        st.switch_page(target["page"])

st.caption("Or pick a city from the list:")
for city in CITIES:
    st.page_link(city["page"], label=f"**{city['name']}**")
    st.caption(city["blurb"])  # a caption wraps; a long page_link label is clipped on a phone
