"""Gifu heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py, in the
city-page format of 2026-10-01 (owner): title, map, captions, bullets, map help,
country links, notices.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.gifu.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_data_age,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Gifu Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Gifu")
render_city_title("Gifu")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/gifu/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Gifu")

# From the japan-city skill's template, Yokkaichi's notification sentence and
# Kitakyushu's laundry sentence (approved wording, pre-approved for this
# build, 2026-09-30); the coverage bullet is a proposal in
# docs/decisions_drafts/worktree-japan-regional-1.md (the owner's call 125,
# Ichinomiya's precedent: the food share stated on the page). The dates are
# the lists' own (config.SOURCE_AS_OF); about two in three is the permit
# list's 3,382 restaurants and cafes of e-Stat's 5,070 in force on
# 2025-03-31 (66.7%); the ring share, 30.7%, is step 3's on the standard
# rings (the ring call is with the owner: halved rings would make it 15.3%).
st.markdown(
    """
**The lines**

- Five lines are drawn, each labeled on the map and in the legend: Meitetsu's Nagoya Main,
  Kakamigahara and Takehana lines and JR Central's Tokaido and Takayama lines.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Gifu City get rings, because the business data covers the city alone:
  lines running on to Mizuho, Kakamigahara, Ginan, Kasamatsu, Hashima and Ichinomiya are cut at
  the city line. The stations left out are listed below.

**The businesses**

- From Gifu City's lists of food-business permits and food-business notifications (as of June 1,
  2025) and its registers of barbers and beauty salons (as of March 31, 2025).
- The city publishes no list of laundries, so laundries are not on this map.
- The city's food lists leave out vending-machine, vehicle, stall and temporary businesses, so
  they hold about two restaurants in three of the official count.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear: the Food shops layer is food retail only.
- Food shops that only notify the city rather than hold a permit, such as convenience stores,
  supermarkets and greengrocers, are included: the city publishes its list of notifications too.
- The lists may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- The lists give an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where only the district can be found, the dot
  sits at the district's center.
- Where a business's trade name is its operator's own name, the dot shows its permit type
  instead.
- Names and permit types are shown in Japanese, as the city records them.
- **About 31% of storefronts sit within a ring.**
"""
)

render_map_help("three business categories (Food shops, Food service and Personal services)")
render_excluded_stations("Gifu")
render_country_links("Gifu")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Gifu")
