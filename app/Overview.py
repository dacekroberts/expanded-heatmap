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

from cities import CITIES, MAP_ONLY_NAV
from components import (
    SITE_NAME,
    render_macro_map_theme,
    render_site_notices,
    set_base_font,
)
# components.py has already put the repo root on sys.path; pipeline/theme.py
# imports nothing, so it is safe under the lean deploy venv.
from pipeline.theme import DARK as DARK_PALETTE, LIGHT, rgb_list

st.set_page_config(page_title=SITE_NAME, page_icon="\U0001f5fa️", layout="wide")
set_base_font()
render_macro_map_theme()

# The public name lives in components.SITE_NAME; the repository keeps its own
# name (`expanded-heatmap`), which is a directory, not a title.
st.title(SITE_NAME)
st.caption("Storefront commercial density around rail-transit stations, "
           "city by city.")

_FOLLOW_UP = (
    'each city map has an "All cities" button to come back here.'
    if MAP_ONLY_NAV
    else "each city page also has a switcher to jump straight to another city."
)
st.markdown(
    f"""
This project maps commercial/business density around rail transit station
areas, one city at a time. Each city has its own independently scoped detail
map - its own map instance, its own data, its own viewport bounds - rather
than one shared map instance loading every city's business points at once.
**Click a city on the map to open its detail map**; {_FOLLOW_UP}
"""
)

st.subheader("Covered cities")

cities = pd.DataFrame(CITIES)

# These are WebGL layer colours, so unlike every other colour in the app they
# CANNOT be restyled by CSS - the dark-mode filter deliberately hits only
# `.mapboxgl-canvas`, never `#deckgl-overlay`, so markers and labels keep
# whatever is baked in here. That is why the design gives each name its own
# opaque pill rather than relying on the basemap behind it: one set of colours
# has to read on both the light basemap and the inverted dark one.
#
# Derived from pipeline/theme.py rather than written as literals, so they
# cannot drift from the rest of the chrome. Alpha is appended per use.
TEAL = rgb_list(LIGHT["accent"], 235)      # marker fill
DARK = rgb_list(LIGHT["text"], 255)        # label text, on the pill below
PILL = rgb_list(LIGHT["surface"], 235)     # the pill behind each name
OUTLINE = rgb_list(LIGHT["surface"], 255)  # ring around each marker
# Interaction feedback, deliberately outside the palette: it has to differ from
# both the teal marker and the category colours to read as "this one".
HIGHLIGHT = [251, 191, 36, 255]

# Where each name sits relative to its marker: an explicit (anchor, dx, dy) in
# pixels from cities.py's `label_offset`. See that file's docstring for why this
# is per-city rather than a three-sided enum, and for the rule that a label
# overflow is fixed by moving the label and never by padding fit_view's box.
DEFAULT_OFFSET = ("middle", 0, -22)
offsets = (cities["label_offset"] if "label_offset" in cities
           else pd.Series([None] * len(cities), index=cities.index))
offsets = offsets.map(lambda v: DEFAULT_OFFSET if v is None else tuple(v))
cities["anchor"] = offsets.map(lambda o: o[0])
cities["dx"] = offsets.map(lambda o: o[1])
cities["dy"] = offsets.map(lambda o: o[2])

markers = pdk.Layer(
    "ScatterplotLayer",
    id="cities",
    data=cities,
    get_position="[lon, lat]",
    get_radius=6,
    # pdk.types.String, not a bare str: pydeck would serialize "pixels" as the
    # expression "@@=pixels" (an undefined variable) and break the radius.
    radius_units=pdk.types.String("pixels"),
    get_fill_color=TEAL,
    get_line_color=OUTLINE,
    stroked=True,
    line_width_min_pixels=2,
    pickable=True,
    auto_highlight=True,
    highlight_color=HIGHLIGHT,
)
# Permanent city-name labels (not hover-only), consistent with the per-city
# maps' rule that things a reader needs to identify are always visible.
labels = pdk.Layer(
    "TextLayer",
    id="city-labels",
    data=cities,
    get_position="[lon, lat]",
    get_text="name",
    get_size=14,
    get_color=DARK,
    # An opaque pill behind each name so it reads on both the light basemap and
    # the dark-mode one (WebGL text can't be recoloured by CSS); a halo outline
    # smeared the letters at this size.
    background=True,
    get_background_color=PILL,
    background_padding=[5, 2],
    get_text_anchor="anchor",
    get_pixel_offset="[dx, dy]",
    # Same typeface as the rest of the app (components.set_base_font). String()
    # for the same reason as radius_units above.
    font_family=pdk.types.String("Space Grotesk, sans-serif"),
    font_weight=600,
    # PICKABLE, and that is the point rather than a nicety. This map is the
    # app's only navigation (MAP_ONLY_NAV), and the dots are a 12 px target
    # whose centres are 6.0 px apart for New York/Philadelphia and 9.0 px for
    # Philadelphia/Washington D.C. - they physically overlap, so a click there
    # cannot reliably say which city was meant. The name pill is 56-133 px
    # wide and, since the 2026-09-21 offsets, never overlaps another, so it is
    # an unambiguous target. The selection handler below reads BOTH layers.
    pickable=True,
    auto_highlight=True,
    highlight_color=HIGHLIGHT,
)

def fit_view(lats, lons, width_px=320, height_px=460, fill=0.7, west_pad=0.12):
    """A view that shows every city with some margin, for any number of
    cities. Web-Mercator maths on the bounding box (512 px world tiles, as in
    Mapbox/Carto vector maps), sized for a phone-width (~340 px) container so
    nothing is cropped there; on a wide screen the same view just has more
    margin. (pydeck's own compute_view assumes a different viewport and
    cropped San Diego and San Francisco out of the same view.) The zoom floor
    is low enough for cities a continent apart: at 3.0 a phone-width map
    cropped San Francisco and Chicago."""
    # The westernmost city's name sits to its left (cities.py `label`), so the
    # box is padded on the west by a fraction of its width; without it that
    # name was clipped at phone width.
    lon_min = min(lons) - west_pad * max(max(lons) - min(lons), 0.5)
    lat_span = max(max(lats) - min(lats), 0.5)
    lon_span = max(max(lons) - lon_min, 0.5)
    centre_lat = (max(lats) + min(lats)) / 2
    z_lon = math.log2(width_px * 360 * fill / (512 * lon_span))
    z_lat = math.log2(height_px * 360 * fill * math.cos(math.radians(centre_lat)) / (512 * lat_span))
    zoom = max(1.0, min(z_lon, z_lat, 9.0))
    return pdk.ViewState(latitude=centre_lat, longitude=(max(lons) + lon_min) / 2, zoom=zoom)


view = fit_view(cities["lat"].tolist(), cities["lon"].tolist())

# Carto basemap: pydeck's own default style needs a Mapbox token; Carto's
# public styles don't. (Tile provider is still an open decision before
# deploying - see PLAN.md.)
deck = pdk.Deck(
    layers=[markers, labels],
    initial_view_state=view,
    map_provider="carto",
    map_style="light",
    # Unlike the layers above this tooltip is an HTML overlay, so CSS CAN reach
    # it: the values here are the light-mode look, and components.py overrides
    # them under `body.dark-base` so it matches the city maps' tooltips instead
    # of staying this green-grey. A dark tooltip on the light basemap is
    # deliberate - it reads better than a pale one over map detail.
    tooltip={
        "html": "<b>{name}</b><br/>{blurb}",
        "style": {
            "backgroundColor": LIGHT["text"],
            "color": LIGHT["surface"],
            "fontSize": "13px",
        },
    },
)

event = st.pydeck_chart(
    deck,
    on_select="rerun",
    selection_mode="single-object",
    key="macro_map",
    height=460,
)

# Either the dot or its name pill opens the city - see the labels layer above
# for why the pill matters more. Both layers carry the same `name`, so the
# lookup is identical; whichever layer deck.gl picked, the first hit wins.
objects = (event.selection.objects or {}) if event else {}
picked = objects.get("cities", []) or objects.get("city-labels", [])
if picked:
    target = next((c for c in CITIES if c["name"] == picked[0].get("name")), None)
    if target:
        st.switch_page(target["page"])

st.caption("Or pick a city from the list:")
for city in CITIES:
    st.page_link(city["page"], label=f"**{city['name']}**")
    st.caption(city["blurb"])  # a caption wraps; a long page_link label is clipped on a phone

# Site-level notices, required on every page - see components._NOTICES.
render_site_notices()
