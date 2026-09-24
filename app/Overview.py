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

from cities import (
    CITIES,
    DEFAULT_REGION,
    elsewhere_counts,
    IN_DEFAULT_VIEW,
    MAP_ONLY_NAV,
    REGION_MEMBERS,
    REGIONS,
)
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
st.caption("Storefront commercial density around rapid-transit stations, "
           "city by city.")

_FOLLOW_UP = (
    'each city map has an "All cities" button to come back here.'
    if MAP_ONLY_NAV
    else "each city page also has a switcher to jump straight to another city."
)
st.markdown(
    f"""
This project maps commercial/business density around rapid-transit station
areas, one city at a time. Each city has its own independently scoped detail
map - its own map instance, its own data, its own viewport bounds - rather
than one shared map instance loading every city's business points at once.
**Click a city on the map to open its detail map**; {_FOLLOW_UP}
"""
)

st.subheader("Covered cities")

# The map opens on ONE region and re-centres on the others, rather than fitting
# every city at once - see cities.py's REGIONS block, and
# docs/scaling_thresholds.md for why a single fitted world view stops working
# somewhere around 12-15 cities. The radio is hidden entirely while there is
# only one region, so this costs nothing until a second country exists.
_region_names = [r["name"] for r in REGIONS]
_region_cities = {r["name"]: r["cities"] for r in REGIONS}
if len(REGIONS) > 1:
    region = st.radio(
        "Region",
        _region_names,
        index=_region_names.index(DEFAULT_REGION),
        format_func=lambda n: f"{n} ({len(_region_cities[n])})",
        horizontal=True,
        key="macro_region",
    )
else:
    region = DEFAULT_REGION

# CLEARING THE CHART'S STORED STATE IS THE WHOLE FIX, and without it the
# switcher silently does nothing. st.pydeck_chart(on_select="rerun") persists
# the viewer's current view under its widget key, and on a rerun Streamlit
# restores that stored view and IGNORES initial_view_state - so a new centre
# computed below would be discarded before it was ever drawn. Dropping the key
# forces the chart to re-initialise from initial_view_state on this run.
#
# Keying the chart per region (macro_map_<region>) was tried first and does not
# work: it creates a fresh widget, but Streamlit still restores the previous
# key's state when the viewer switches back, so the map returns to wherever
# they had dragged it rather than to the region's centre.
#
# WARNING FOR ANYONE EDITING THE VIEW BELOW: the same persistence makes a
# changed initial_view_state invisible in a browser session that has already
# rendered this page, across server restarts included. Test in a fresh session
# (a new query string is enough) or you will debug correct code.
if st.session_state.get("_macro_region_shown") != region:
    st.session_state["_macro_region_shown"] = region
    st.session_state.pop("macro_map", None)

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


def _offset(value):
    """A city's (anchor, dx, dy), or the default when it declares none.

    `v is None` IS NOT ENOUGH, and assuming it was took the whole Overview page
    down from 2026-09-22 (commit 0fa3e55) until it was caught: `pd.DataFrame`
    fills a key that some dicts omit with **float('nan')**, not None, and
    `nan is None` is False - so `tuple(nan)` raised `TypeError: 'float' object
    is not iterable` and every load showed a traceback instead of the map, the
    city list, the caption and the site notices.

    It survived because the crash needs a city with NO `label_offset` at all,
    and for fifteen cities every entry happened to have one. Mexico City was
    the first without. So this is scalar-safe rather than None-safe.
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return DEFAULT_OFFSET
    return tuple(value)


offsets = offsets.map(_offset)
cities["anchor"] = offsets.map(lambda o: o[0])
cities["dx"] = offsets.map(lambda o: o[1])
cities["dy"] = offsets.map(lambda o: o[2])

# A LEAF REGION LABELS ONLY ITS OWN CITIES; THE COMPOSITE LABELS EVERY ONE.
# Owner's decision 2026-09-22, taking the narrow of two options.
#
# Every city is DRAWN in every region - the view is centred, never filtered -
# which is what makes the caption's "every city is on the map" true, and that
# does not change here: the markers layer below still gets the whole frame and
# a non-member's dot stays visible and clickable. What is dropped is the
# NAME PILL of a city the reader has just switched away from.
#
# It was a correctness fix before it was a tidiness one. A non-member sits at
# the frame edge at a zoom its offsets were never measured at, and collides
# there: "Los Angeles" covered San Diego's marker and overlapped its pill by
# 20.5 x 11.3 px in United States East, where NEITHER is a member, and
# "Philadelphia" hung 2.1 px below the canvas in Canada East. Tuning offsets
# to fix that is unbounded work - each of the six regions would constrain
# every city's single pixel offset - and the label being removed is one a
# reader of that region has no use for.
#
# THE COMPOSITE USED TO BE EXEMPT. It no longer is, and the reason is that the
# trade it was exempted on INVERTED as the map went international.
#
# The old rule kept every label on "United States" because that is the landing
# view, and suppressing non-members there "would take seven labels off it to
# close one 1.1 px abutment". Measured again on 2026-09-23, when Marseille
# became the 22nd city:
#
#   labels shown that are NOT the region's own      13
#   collisions in that view                          3
#   ...of which involve a non-member             3 of 3
#   non-member labels drawn OFF CANVAS at 375px  6 of 13
#
# So it is now thirteen labels against three collisions, EVERY collision is
# caused by a non-member, and at phone and tablet width nearly half of those
# labels are off-screen anyway - they cannot be serving the first impression
# they were kept for. The cost also grows with each international city, which
# is the part that matters: every one arrives needing its offsets tuned against
# a view it does not belong to, which `Overview.py` already calls "unbounded
# work" three paragraphs above.
#
# The rule is now simply: A REGION LABELS ITS OWN CITIES. No exception, so a
# future composite needs no decision. Markers are untouched - every city's dot
# stays visible and clickable in every view, which is what makes the caption's
# "every city is on the map" true - and `elsewhere_counts` still names the
# regions a reader has not opened.
_members = {c["name"] for c in _region_cities[region]}
label_cities = cities[cities["name"].isin(_members)]

markers = pdk.Layer(
    "ScatterplotLayer",
    id="cities",
    data=cities,
    get_position="[lon, lat]",
    # 4 px with a 1 px ring, reduced from 6 px with a 2 px ring on 2026-09-21.
    #
    # WHY THE DOTS ARE SMALL: at the fitted continental zoom the eastern cities
    # are a few pixels apart, and at 16 px outer diameter they merged into one
    # teal blob. Measured separations: New York/Philadelphia 6.0 px,
    # Philadelphia/Washington D.C. 9.0 px, New York/Boston 14.4 px, New
    # York/D.C. 15.0 px, San Diego/Los Angeles 7.7 px. Those numbers are the
    # same at 340 px and 1200 px, because fit_view pins the zoom to a 320 px
    # reference and spends extra width as margin.
    #
    # At 10 px outer this separates New York/Boston and New York/D.C. outright
    # and cuts the worst overlap from 10 px to 4 px, so the cluster reads as
    # distinct dots. 3 px was tried and rejected: it separates one more pair
    # but the dots stop working as position indicators, reading as specks for
    # the isolated cities.
    #
    # DO NOT TRY TO FIX THIS BY MOVING THE MARKERS. At this zoom 1 px is about
    # 21.7 km at New York's latitude, so separating New York from Philadelphia
    # would take **217 km** of displacement - New York's dot would land west of
    # Pittsburgh. Displacement was considered and is arithmetically dead. The
    # remaining overlap is cosmetic only: since the name pills became pickable,
    # clicking no longer depends on hitting a dot.
    get_radius=4,
    # pdk.types.String, not a bare str: pydeck would serialize "pixels" as the
    # expression "@@=pixels" (an undefined variable) and break the radius.
    radius_units=pdk.types.String("pixels"),
    get_fill_color=TEAL,
    get_line_color=OUTLINE,
    stroked=True,
    line_width_min_pixels=1,
    pickable=True,
    auto_highlight=True,
    highlight_color=HIGHLIGHT,
)
# Permanent city-name labels (not hover-only), consistent with the per-city
# maps' rule that things a reader needs to identify are always visible.
labels = pdk.Layer(
    "TextLayer",
    id="city-labels",
    # Not `cities`: a leaf region labels only its own - see label_cities above.
    data=label_cities,
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
    # WITHOUT THIS, "Montréal" RENDERS AS "Montr al". deck.gl builds the
    # TextLayer's font atlas from an ASCII-only character set by default, so
    # any accented glyph is silently dropped to a blank - not a missing-glyph
    # box, just a gap, which is why it reads as a spacing bug rather than an
    # encoding one. "auto" makes deck.gl build the atlas from the actual data,
    # so it covers whatever the city names contain.
    #
    # pdk.types.String() for the same reason as radius_units above: a bare
    # "auto" is serialized as the expression "@@=auto" and evaluates to
    # undefined, which silently restores the ASCII default.
    character_set=pdk.types.String("auto"),
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


# FITTED TO THE DEFAULT-VIEW CITIES ONLY, not to every city on the map.
# See cities.IN_DEFAULT_VIEW for why: fitting all of them made each new
# non-US city re-zoom the map and re-tighten the east-coast cluster, so every
# label offset in cities.py would have needed re-measuring per city. Framing
# the US set pins the zoom at 1.4525 permanently. Cities outside the frame are
# still drawn - they are simply found by zooming out, and they are all in the
# link list below.
#
# EACH REGION IS FITTED TO ITS OWN CITIES, which SUPERSEDES the 2026-09-22
# decision that the switcher must "re-centre and never re-zoom".
#
# That rule existed to protect the pixel `label_offset` values in cities.py,
# which were measured at the United States zoom of 1.4525 - the worry being
# that a different zoom would change the pixel distance between cities and
# invalidate all of them at once. Measured before changing it, and the worry
# only runs one way: zooming IN spreads cities apart, so collisions get BETTER,
# not worse. At each region's own fitted zoom - Canada West 3.868, Canada East
# 4.596, Mexico 5.060 - there are zero label collisions and zero pills covering
# their own marker. Zooming OUT would still be dangerous, and nothing here
# does that.
#
# The United States view is UNCHANGED, and by construction rather than by
# luck: IN_DEFAULT_VIEW is exactly the set of cities tagged "United States", so
# fitting that region reproduces zoom 1.4525 and the same centre.
#
# Why it changed: re-centring alone left Canada and Mexico drawn at continental
# zoom, which showed the same near-empty frame as the United States view and
# gave a reader almost nothing. Vancouver to Montréal is ~3,300 km - wider than
# the contiguous United States - which is also why Canada is split west/east.
_here = _region_cities[region]
view = fit_view([c["lat"] for c in _here], [c["lon"] for c in _here])

# RE-CENTRE ON THE REGION'S OWN MIDPOINT, KEEPING THE FITTED ZOOM. The heading
# on this block used to read "RE-CENTRE, NEVER RE-ZOOM", which stopped being
# true when the line above started fitting each region; `view.zoom` is now that
# region's own fitted zoom, not the pinned 1.4525, and this block preserves it.
#
# WHAT IT ACTUALLY DOES is drop fit_view's `west_pad` from the centre, because
# that padding lives in the fitted longitude and recomputing the midpoint
# discards it - so a region sits about 12 px east of its fitted frame. That
# reads like a bug and was removed on 2026-09-22; REMOVING IT MADE THINGS
# WORSE and it was restored, measured rather than argued:
#
#   phone-width (343 px canvas) label clipping, total across all regions
#     with this block:     137.4 px   (Vancouver 89.9 W, San Diego 16.9 E,
#                                      Edmonton 14.5 E, Guadalajara 9.8 W,
#                                      Montréal 6.3 E)
#     without it:          159.5 px   (Guadalajara fixed, every east-edge
#                                      label worse, and a NEW 7.9 px clip on
#                                      Boston in United States East)
#
# The west pad only ever helps a label running WEST off its dot, and in four
# of the five regions the label at risk runs EAST. So the 12 px eastward shift
# is doing real work here by accident, and the honest fix is to say so rather
# than to tidy the block away.
#
# FITTING THE BOX TO THE LABELS was the other candidate and is arithmetically
# dead: padding the longitude box by each edge label's pixel width drops Canada
# West from zoom 3.868 to the 1.0 floor, United States East from 3.085 to
# 1.273, and the composite from 1.4525 to 1.0 - it removes every clip by
# throwing away the per-region zoom the clipping is a side effect of. This is
# cities.py's standing rule ("do NOT solve a label overflow by padding
# fit_view's bounding box") holding in a second place.
#
# The residual clipping is the SAME accepted trade-off cities.py already
# documents for the composite at phone width, where Washington D.C. is 39%
# clipped and Philadelphia 28%, with the full text-link list beneath the map as
# the navigation guarantee. Every clipped pill stays clickable.
#
# A NEW ViewState rather than `view.zoom = ...`: pydeck does not serialise
# attributes mutated after construction, so the assignment form silently ships
# the old view.
if region != DEFAULT_REGION:
    _here = _region_cities[region]
    view = pdk.ViewState(
        latitude=(max(c["lat"] for c in _here) + min(c["lat"] for c in _here)) / 2,
        longitude=(max(c["lon"] for c in _here) + min(c["lon"] for c in _here)) / 2,
        zoom=view.zoom,
    )

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

# Deliberately does NOT say cities are "outside the view": the frame is
# computed for a 320 px reference and spends extra width as margin, so at
# 854 px the canvas covers far more latitude than the US box and Vancouver's
# dot is visible near the top. Whether a given city falls just inside or just
# beyond the edge depends on the container width, so the wording covers both
# and the list below is named as the guarantee.
# NAMES THE OTHER REGIONS RATHER THAN SAYING "SOME CITIES ARE ELSEWHERE".
# docs/scaling_thresholds.md's failure mode is a default that silently hides
# most of the site, and a reader cannot tell a deliberate frame from a broken
# one unless the counts are stated. Every city is drawn at every region - the
# view is centred, not filtered - so the wording is about where the view sits.
if len(REGIONS) > 1:
    # NOT "every region except this one": REGIONS holds composites and
    # their halves, so that counted the same cities twice. See
    # cities.elsewhere_counts().
    _elsewhere = ", ".join(
        f"{n_cities} in {n}" for n, n_cities in elsewhere_counts(region)
    )
    st.caption(
        f"Showing {len(_region_cities[region])} cities in {region} — "
        f"{_elsewhere} elsewhere. Every city is on the map: switch region "
        "above to re-centre, or use the list below, which always has all of "
        "them."
    )

st.caption("Or pick a city from the list:")
for city in CITIES:
    st.page_link(city["page"], label=f"**{city['name']}**")
    st.caption(city["blurb"])  # a caption wraps; a long page_link label is clipped on a phone

# Site-level notices, required on every page - see components._NOTICES.
render_site_notices()
