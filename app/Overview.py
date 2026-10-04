"""Entry page - project intro plus the macro map (the city picker).

This is the macro level of the hybrid architecture (see docs/project_context.md):
one lightweight map of every mapped city, then an independent detail map per
city. Click a city marker and the app jumps to that city's page.

Built with pydeck, which ships with Streamlit (no extra dependency), rather
than folium/streamlit-folium: this project keeps folium out of the deployed
runtime (see requirements.txt). st.pydeck_chart(on_select="rerun") returns the
clicked marker, and st.switch_page navigates without a full page reload. A
list of page links sits below the map as a fallback (keyboard access, and any
browser where the map doesn't load), one section per region, the selected
region's open.
"""

import base64
import json
import math
import sys
from pathlib import Path

import copy

import pandas as pd
import pydeck as pdk
import streamlit as st

from cities import (
    CITIES,
    DEFAULT_FRAME,
    DEFAULT_REGION,
    IN_DEFAULT_VIEW,
    MAP_ONLY_NAV,
    REGION_MEMBERS,
    REGION_ZOOM_WITHOUT,
    REGIONS,
    region_caption,
    SWITCHER_ORDER,
)
from label_competition import compete
from basemap import SECRET_NAME as BASEMAP_SECRET, carto_positron_style
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
    'each city map has a "Global View" button to come back here.'
    if MAP_ONLY_NAV
    else "each city page also has a switcher to jump straight to another city."
)
st.markdown(
    f"""
This project maps how densely shops, restaurants and personal services
cluster around rapid-transit stations, one city at a time. Each city has its
own detail map, with its own data and its own extent, rather than one shared
map loading every city's businesses at once.
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
# Storefront counts for the tooltip, generated from the pipeline's own data by
# scripts/check_macro_facts.py --write and checked by it before every push.
_FACTS = json.loads((Path(__file__).parent / "macro_facts.json").read_text(encoding="utf-8"))

# These are WebGL layer colours, so unlike every other colour in the app they
# CANNOT be restyled by CSS - the dark-mode filter deliberately hits only
# `.mapboxgl-canvas`, never `#deckgl-overlay`, so markers and labels keep
# whatever is baked in here. That is why the design gives each name its own
# opaque pill rather than relying on the basemap behind it: one set of colours
# has to read on both the light basemap and the inverted dark one.
#
# Derived from pipeline/theme.py rather than written as literals, so they
# cannot drift from the rest of the chrome. Alpha is appended per use.
TEAL = rgb_list(LIGHT["accent"], 235)      # the metro colour
# A DOT'S COLOUR IS ITS NETWORK, ITS FILL ITS COMPLETENESS (owner, 2026-09-29
# and 2026-09-30; this replaced colour-as-completeness from 2026-09-28).
#
# COLOUR = the highest-order mode the city's map draws (`mode` in cities.py:
# metro > light rail > tram). The three colours are the set validated for the
# completeness tiers, re-run 2026-09-30 with the dataviz skill's
# validate_palette.js on the light basemap and its filtered dark form: normal-
# vision floor 27.1, worst colour-blind pair 13.7 deutan / 17.0 tritan; below
# 3:1 only over water, as the teal always was, relieved by each dot's white
# ring, its name pill and the text legend. One set for both themes, because
# these are WebGL colours the dark-mode filter never reaches.
MODES = {
    "metro": ("Metro", TEAL),
    "light_rail": ("Light rail", [0x93, 0x33, 0xEA, 235]),
    "tram": ("Tram", [0xC2, 0x41, 0x0C, 235]),
}
# FILL decays with completeness (`coverage` in cities.py, which
# scripts/check_macro_facts.py holds to docs/map_inconsistencies.md): solid =
# full, the BOTTOM half = narrowed (a level, read as "partly full", not a pie
# read as shares), a hollow ring with a pale centre = one category. So colour
# never has to be decoded for completeness, nor fill for mode.
FILLS = {"full": "Full data", "narrowed": "Narrowed data", "one_bucket": "One category"}
DARK = rgb_list(LIGHT["text"], 255)        # label text, on the pill below
PILL = rgb_list(LIGHT["surface"], 235)     # the pill behind each name
OUTLINE = rgb_list(LIGHT["surface"], 255)  # ring around each marker
# Interaction feedback, deliberately outside the palette: it has to differ from
# every mode colour to read as "this one".
HIGHLIGHT = [251, 191, 36, 255]
# Drawn diameter of a dot, ring included. 10 px until 2026-09-30; a hollow ring
# at 10 px was too thin to see or tap, so 12. check_macro_labels.py's MARKER_R
# is half of this - change both together.
DOT_PX = 12
# In Global, the dots of cities that did not win a label (see the competition
# below) draw faded under the pills.
LOSER_DOT_OPACITY = 0.45


def _hex(rgb):
    return "#%02x%02x%02x" % tuple(rgb[:3])


def _dot_svg(colour, fill):
    """One dot as SVG in a 24-unit box (2 units = 1 px at DOT_PX): a 1 px ring
    in the surface color, then the mode color as a disc, a bottom-half level
    or a 2 px ring around a pale center."""
    c, pale = _hex(colour), _hex(OUTLINE)
    body = f'<circle cx="12" cy="12" r="12" fill="{pale}"/><circle cx="12" cy="12" r="10" fill="{c}"/>'
    if fill == "narrowed":
        # A 1.5 px ring with only the inner disc's TOP half pale, leaving the
        # lower half in colour. Painting a whole pale disc and a coloured half
        # over it left the pale disc's anti-aliased edge as a hairline round
        # the lower arc.
        body += f'<path d="M5 12 A7 7 0 0 1 19 12 Z" fill="{pale}"/>'
    elif fill == "one_bucket":
        body += f'<circle cx="12" cy="12" r="6" fill="{pale}"/>'
    return body


def _svg_uri(svg, w, h):
    head = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
    return "data:image/svg+xml;base64," + base64.b64encode((head + svg + "</svg>").encode()).decode()


# ONE SPRITE for all nine dots, drawn at 4x so it stays sharp on a phone's
# high-density screen; each row of the layer's data carries only a short key.
_CELL = 4 * DOT_PX
_ICON_KEYS = [(m, f) for m in MODES for f in FILLS]
ICON_ATLAS = _svg_uri("".join(
    f'<svg x="{i * _CELL}" y="0" width="{_CELL}" height="{_CELL}" viewBox="0 0 24 24">'
    f'{_dot_svg(MODES[m][1], f)}</svg>' for i, (m, f) in enumerate(_ICON_KEYS)),
    _CELL * len(_ICON_KEYS), _CELL)
# anchorY MUST be the centre: deck.gl's default is the icon's bottom edge, which
# would stand every dot 6 px north of its city.
ICON_MAPPING = {f"{m}-{f}": {"x": i * _CELL, "y": 0, "width": _CELL, "height": _CELL,
                             "anchorX": _CELL / 2, "anchorY": _CELL / 2, "mask": False}
                for i, (m, f) in enumerate(_ICON_KEYS)}

# Per-dot icon and tooltip text. A missing mode, tier or count falls back
# rather than raising: this page lists every city, and one city's absent fact
# must not take the whole Overview down (the label_offset NaN lesson, below).
_tier = cities["coverage"].where(cities["coverage"].isin(list(FILLS)), "full") \
    if "coverage" in cities else pd.Series(["full"] * len(cities), index=cities.index)
_mode = cities["mode"].where(cities["mode"].isin(list(MODES)), "metro") \
    if "mode" in cities else pd.Series(["metro"] * len(cities), index=cities.index)
cities["icon"] = _mode + "-" + _tier
cities["tier_label"] = _tier.map(FILLS.get)
cities["mode_label"] = _mode.map(lambda m: MODES[m][0])
_counts = _FACTS.get("storefronts", {})
cities["storefronts_text"] = cities["name"].map(
    lambda n: f"{_counts[n]:,} storefronts" if n in _counts else "storefront count pending")
for _col in ("placement", "data_age"):
    cities[_col] = cities[_col].fillna("not recorded") if _col in cities else "not recorded"

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
# A CITY MAY PLACE ITS LABEL DIFFERENTLY IN ONE REGION'S VIEW (owner, 2026-09-30:
# Buffalo south of its dot in United States East, where above it the pill read
# as Toronto's, while the landing view's East Coast cluster leaves no room
# below). `label_offset_by_region` maps a region name to (anchor, dx, dy);
# check_macro_labels.py scores the same override.
if "label_offset_by_region" in cities:
    _by_region = cities["label_offset_by_region"].map(
        lambda d: tuple(d[region]) if isinstance(d, dict) and region in d else None)
    offsets = pd.Series([b if b is not None else o for b, o in zip(_by_region, offsets)],
                        index=offsets.index)
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
#
# A MINOR CITY IS LABELLED ONLY IN ITS OWN REGION (the owner's label tiers,
# 2026-09-29; first applied 2026-09-30 to Tucson, Kansas City and New Orleans,
# whose pills met Monterrey's and Los Angeles's at the landing zoom). Its dot
# and tooltip stay in every view; `label_tier` in cities.py names it, and
# check_macro_labels.py applies the same rule.
_members = {c["name"] for c in _region_cities[region]
            if c.get("label_tier") != "minor" or c.get("region") == region}
# And another region's ANCHORS where this view is set to label them (East Asia
# names Seoul; owner, 2026-09-30) - see REGION_LABELS_ALSO in cities.py.
_also = getattr(sys.modules.get("cities"), "REGION_LABELS_ALSO", {}).get(region, ())
_members |= {c["name"] for c in CITIES if c.get("region") in _also
             and c.get("label_tier") != "minor"}
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
    #
    # SINCE 2026-09-30 THIS LAYER DRAWS NOTHING: the dots are the IconLayer
    # below (a half-filled circle is beyond a ScatterplotLayer). It stays for
    # picking and the amber hover highlight, at the icons' size, so the
    # selection code keys on the same "cities" id. Alpha 1, not 0: a fully
    # transparent fill is not something to rely on for picking.
    get_radius=DOT_PX / 2,
    # pdk.types.String, not a bare str: pydeck would serialize "pixels" as the
    # expression "@@=pixels" (an undefined variable) and break the radius.
    radius_units=pdk.types.String("pixels"),
    get_fill_color=[0, 0, 0, 1],
    stroked=False,
    pickable=True,
    auto_highlight=True,
    highlight_color=HIGHLIGHT,
)
# The visible dots: one sprite, nine cells (3 modes x 3 fills), keyed per city.
dots = pdk.Layer(
    "IconLayer",
    id="city-dots",
    data=cities,
    get_position="[lon, lat]",
    # pdk.types.String for the same reason as "pixels": a bare "data:..." string
    # is parsed as an expression and the page fails with "Unexpected ':'".
    icon_atlas=pdk.types.String(ICON_ATLAS),
    icon_mapping=ICON_MAPPING,
    get_icon="icon",
    get_size=DOT_PX,
    size_units=pdk.types.String("pixels"),
    pickable=False,
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
#
# GLOBAL, THE LANDING VIEW, BORROWS DEFAULT_FRAME'S FRAME (the United States):
# it labels every city but opens exactly where the United States view does.
# See DEFAULT_REGION in cities.py.
_frame_region = DEFAULT_FRAME if region == DEFAULT_REGION else region
_here = _region_cities[_frame_region]
# The ZOOM may leave out a region's outlier (cities.REGION_ZOOM_WITHOUT); the
# centre below still takes every city in the region.
_skip = REGION_ZOOM_WITHOUT.get(_frame_region, ())
_zoom_set = [c for c in _here if c["name"] not in _skip] or _here
view = fit_view([c["lat"] for c in _zoom_set], [c["lon"] for c in _zoom_set])
# A zoom set outright (cities.REGION_ZOOM: France North and South at 5.0). Read
# with getattr, NOT imported by name: Streamlit Cloud can serve a cached
# cities.py after a push until the app is rebooted, and a missing name in a
# `from cities import` takes the whole Overview down (2026-09-22). A stale
# module simply means no override.
_zoom_override = getattr(sys.modules.get("cities"), "REGION_ZOOM", {}).get(_frame_region)
if _zoom_override is not None:
    view = pdk.ViewState(latitude=view.latitude, longitude=view.longitude, zoom=_zoom_override)

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
# The United States frame is the one exception, as it always was: it is the
# landing frame (now Global's too) and its offsets were measured un-shifted.
if _frame_region != DEFAULT_FRAME:
    view = pdk.ViewState(
        latitude=(max(c["lat"] for c in _here) + min(c["lat"] for c in _here)) / 2,
        longitude=(max(c["lon"] for c in _here) + min(c["lon"] for c in _here)) / 2,
        zoom=view.zoom,
    )

# CARTO Positron basemap, with the project's CARTO key on every request
# (app/basemap.py says why it is a data: URL). No key, no basemap: keyless
# CARTO is outside its terms, so a checkout without the secret shows the
# warning and the dots on a blank ground rather than falling back.
_basemap_style = carto_positron_style()
if _basemap_style is None:
    st.warning(f"No basemap: the `{BASEMAP_SECRET}` secret is not set, and CARTO's "
               "terms allow its basemap only with a key.")
# GLOBAL'S LABELS ARE WON, NOT LISTED (owner, 2026-10-01): the cities compete
# for space at this view's zoom - trams and minor cities out, the rest ranked
# by mode, size and coverage, each trying its own offset and then four others -
# in app/label_competition.py, which check_macro_labels.py and
# check_deploy_imports.py score too. Europe had become a block of overlapping
# names, and hand-placing offsets against every neighbour did not scale.
if region == DEFAULT_REGION:
    _won = compete(CITIES, view.latitude, view.longitude, view.zoom,
                   _FACTS.get("storefronts", {}))
    _lab = cities[cities["name"].isin(_won)].copy()
    _lab["anchor"] = _lab["name"].map(lambda n: _won[n][0])
    _lab["dx"] = _lab["name"].map(lambda n: _won[n][1])
    _lab["dy"] = _lab["name"].map(lambda n: _won[n][2])
    labels.data = _lab
    # THE WINNERS ON TOP (owner, 2026-10-01). Every other city's dot draws
    # UNDER the pills and FADED: at world zoom a city that lost on space may
    # sit beneath a winner's pill, and reappears as the reader zooms in (pills
    # stay a fixed pixel size while the dots spread). The winners' dots draw at
    # full strength ABOVE the pills - the competition keeps every pill off its
    # own dot and off every winner's - so each name reads next to its city.
    # Opacity, not size or a coloured ring: a larger dot would crowd the
    # spacing the other views were tuned at, and a ring that reads on the
    # light basemap vanishes on the dark one. The invisible picking layer
    # splits the same way, so a pill's click is never caught by a dot under it.
    _is_won = cities["name"].isin(_won)

    def _part(layer, rows, suffix="", **props):
        part = copy.copy(layer)
        part.data = rows
        if suffix:
            part.id = layer.id + suffix
        for k, v in props.items():
            setattr(part, k, v)
        return part
    _layers = [_part(dots, cities[~_is_won], "-low", opacity=LOSER_DOT_OPACITY),
               _part(markers, cities[~_is_won], "-low"),
               labels,
               _part(dots, cities[_is_won]), _part(markers, cities[_is_won])]
else:
    _layers = [dots, markers, labels]

deck = pdk.Deck(
    # The invisible picking layer sits ABOVE the icons, so its amber hover
    # highlight covers the hovered dot; in a region view the name pills stay
    # on top of both (in Global, under them - above).
    layers=_layers,
    initial_view_state=view,
    # repeat=True draws the layers on EVERY copy of the world, not only the
    # primary one (-180..180). The basemap always repeats; without this, a
    # canvas wider than one world at the Global frame showed Asia on the left
    # with no cities on it - Seoul, Hong Kong and Taiwan appeared only past
    # Europe (owner, 2026-09-27). pydeck's default view is this same MapView
    # with controller=True, so nothing else changes. Zoomed far out a city can
    # appear twice, once per copy, both clickable - accepted by the owner.
    views=[pdk.View(type="MapView", controller=True, repeat=True)],
    # map_provider=None draws no basemap at all; Streamlit substitutes keyless
    # CARTO only when a style is missing and the provider is still set.
    map_provider="carto" if _basemap_style else None,
    **({"map_style": _basemap_style} if _basemap_style else {}),
    # Unlike the layers above this tooltip is an HTML overlay, so CSS CAN reach
    # it: the values here are the light-mode look, and components.py overrides
    # them under `body.dark-base` so it matches the city maps' tooltips instead
    # of staying this green-grey. A dark tooltip on the light basemap is
    # deliberate - it reads better than a pale one over map detail.
    tooltip={
        # The tier, storefront count, placement and data age (owner,
        # 2026-09-28): the facts a dot's size would have carried, without
        # letting big cities swallow their neighbours' dots and labels.
        "html": "<b>{name}</b><br/>{blurb}<br/>{mode_label} · {tier_label} · {storefronts_text}"
                "<br/>Placed by: {placement}<br/>Data: {data_age}",
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

# The two-key legend (owner, 2026-09-30): the mode colours as solid dots, then
# the three fills in a neutral grey, each with its words beside it, so neither
# key rests on colour alone (the dataviz rule; the colours sit under 3:1 over
# water). The swatches are the map's own dot drawings; the ink is the theme's
# text colour.
_GREY = rgb_list(LIGHT["muted"], 255)


def _legend_row(title, items):
    return (
        '<div style="display:flex;flex-wrap:wrap;align-items:center;gap:4px 16px;'
        'font-size:0.85rem;margin:2px 0">'
        f'<span style="font-weight:600">{title}</span>'
        + "".join(
            f'<span style="white-space:nowrap"><img src="{_svg_uri(_dot_svg(c, f), 24, 24)}" '
            f'width="{DOT_PX}" height="{DOT_PX}" alt="" style="margin-right:6px;'
            f'vertical-align:-1px">{label}</span>'
            for label, c, f in items)
        + "</div>")


st.markdown(
    '<div style="margin:2px 0 6px">'
    + _legend_row("Rail network", [(label, c, "full") for label, c in MODES.values()])
    + _legend_row("Business data", [(label, _GREY, f) for f, label in FILLS.items()])
    + "</div>",
    unsafe_allow_html=True,
)

# Either the dot or its name pill opens the city - see the labels layer above
# for why the pill matters more. Both layers carry the same `name`, so the
# lookup is identical; whichever layer deck.gl picked, the first hit wins.
objects = (event.selection.objects or {}) if event else {}
picked = (objects.get("cities", []) or objects.get("cities-low", [])
          or objects.get("city-labels", []))
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
# Global states the whole site's count (docs/scaling_thresholds.md's failure
# mode is a default that silently hides most of the site); a region view
# states only its own (owner, 2026-10-03: region views no longer name the
# other regions). Every city is drawn at every region - the view is centred,
# not filtered - so the wording is about where the view sits.
if region == DEFAULT_REGION:
    st.caption(
        f"All {len(CITIES)} cities are on the map, opening on the "
        f"{DEFAULT_FRAME}: drag or zoom out to reach the rest, pick a region "
        "above to jump there, or use the list below."
    )
elif len(REGIONS) > 1:
    # A region view states its own count only (owner, 2026-10-03): the
    # whole-map sentence belongs to Global, and the list below still holds
    # every city, its other regions closed. The sentence is cities.py's, which
    # check_macro_labels.py holds to the labels the view draws.
    st.caption(region_caption(region))

st.caption("Or pick a city from the list:")
# THE LIST FOLLOWS THE REGION SELECTOR (owner, 2026-10-01): one expander per
# leaf region, the same partition the caption above counts. The regions the
# selected view covers come first and open; every other region follows,
# closed, in menu order, so the list still holds
# every city in every view. Global opens none: 124 cities open ran to dozens
# of phone screens.
_leaves = [n for n in _region_names if n not in REGION_MEMBERS]
_open = [] if region == DEFAULT_REGION else [
    n for n in _leaves if n in REGION_MEMBERS.get(region, (region,))]
_by_name = cities.set_index("name")
for _leaf in _open + [n for n in _leaves if n not in _open]:
    _rows = [c for c in SWITCHER_ORDER if c["region"] == _leaf]   # grouped by country
    _multi = len({c["country"] for c in _rows}) > 1
    with st.expander(f"{_leaf} ({len(_rows)})", expanded=_leaf in _open):
        # Grouped by country where a region holds more than one, three cities
        # to a row; Streamlit stacks columns into one below 640 px.
        _groups = {}
        for city in _rows:
            _groups.setdefault(city["country"], []).append(city)
        for _country, _group in _groups.items():
            if _multi:
                st.caption(f"**{_country}**")
            for _i in range(0, len(_group), 3):
                for _col, city in zip(st.columns(3), _group[_i:_i + 3]):
                    with _col:
                        st.page_link(city["page"], label=f"**{city['name']}**")
                        # The tooltip's facts as well as the blurb: a touch
                        # screen has no hover, so on a phone this list is the
                        # only place they show. A caption wraps; a long
                        # page_link label is clipped on a phone.
                        _f = _by_name.loc[city["name"]]
                        st.caption(
                            f"{city['blurb']}  \n"
                            f"{_f['mode_label']} · {_f['tier_label']} · "
                            f"{_f['storefronts_text']}  \n"
                            f"Data: {_f['data_age']} · Placed by: {_f['placement']}")

# Site-level notices, required on every page - see components._NOTICES.
render_site_notices()
