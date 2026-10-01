"""Hiroshima heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.hiroshima.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Hiroshima Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Hiroshima")

st.title("Hiroshima: restaurants and food shops around rail and tram stops")

# Written under the owner's pre-approval of this build's prose (2026-09-30),
# from Fukuoka's page (the two-list Japanese template, approved 2026-09-28) and
# the tram template's ring sentence. The as-of dates are the lists' own
# (config.SOURCE_AS_OF); MHLW's file states none, so it is dated by download
# (provenance.json). "One restaurant in seven": 1,779 of 12,682 restaurant
# permits withhold their address (step 2's data, 2026-09-30).
st.markdown(
    """
Twelve lines are drawn, each labelled on the map and in the legend: the Astram Line; JR West's
Sanyo, Kabe, Geibi and Kure lines; and Hiroden's streetcar network, its Main, Ujina, Eba, Yokogawa,
Hakushima and Minami lines and the Miyajima Line out to the west. Lines and stations come from
MLIT's national railway data (国土数値情報), in its 2025 edition, which has the streetcars' new route
into Hiroshima Station; station names in English are from OpenStreetMap, written as the operators
sign them. Only stations inside Hiroshima City get rings, because the business data covers the
city alone: lines running on to Hatsukaichi, Fuchu, Kaita, Saka and Higashihiroshima are cut at
the city line. The Shinkansen is not drawn. Line colours are this project's own, not the
operators'.

**This map shows food businesses only.** Hiroshima City publishes no complete list of barbers,
beauty salons or laundries, only its new openings, so personal services are not on this map, and
Japan has no general business licence, so shops other than food shops (clothing, electronics,
pharmacies) do not appear either. The food businesses come from two lists. Hiroshima City's own
list holds every food-business permit applied for at a city counter and in force at the end of
March 2026. Permits filed online go through the Ministry of Health, Labour and Welfare's system,
whose open data is the second list (downloaded 30 September 2026). A premises in both lists appears
once. The Food shops layer is food retail only, and it is partial: shops that only notify rather
than hold a permit, such as supermarkets, convenience stores and greengrocers, appear only where
they chose to publish in the ministry's list. Food trucks, street and festival stalls, caterers,
school and hospital kitchens, staff canteens and snack bars are not included. The lists may
include premises that have closed, so a dot means a permit on file, not a business open today.

About one restaurant in seven in Hiroshima chose not to publish its address in the national filing
system and is not on this map. Where they are is not known. The rest are matched to MLIT's
address reference data, which places most at their street block; where that fails for a ministry
filing, the dot sits at the ministry's own coordinates. In the city's own list, where a trade name
is its operator's own name, the dot shows its permit type instead; the ministry's list does not
say who the operator is, so this cannot be checked there. Names and permit types are shown in
Japanese, as the lists record them.

**Tram stops sit closer together than metro stations**, a median of 357 m here, so the rings are
drawn at half the usual size (0.05 to 0.3 mi). **About two-thirds of storefronts sit within a
ring.**

Concentric ring boundaries and the two business categories (Retail and Food service) are
toggleable via the layer control in the top left. When enabled, business density will display as
numbered circles summing areas when zoomed out. Zooming in will show individual dots; hover over
those to see further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a
statistical density estimate, so read the colour as "roughly where things
cluster."
"""
)

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/hiroshima/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
