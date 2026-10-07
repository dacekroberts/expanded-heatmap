"""Ichinomiya heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.ichinomiya.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Ichinomiya Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Ichinomiya")
render_city_title("Ichinomiya")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/ichinomiya/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Ichinomiya")

# From the japan-city skill's template, Matsuyama's page (the ministry's
# notifications and its points) and Maebashi's (approved wording,
# pre-approved for this build, 2026-09-30); the dated first bullet and the
# coverage bullet are proposals in
# docs/decisions_drafts/worktree-japan-regional-1.md (the owner's call 125:
# the food share stated on the page). The dates are the lists' own
# (config.SOURCE_AS_OF); about two in three is the March list's 2,164
# restaurants of e-Stat's 3,292 in force (65.7%; 67.0% with the months); the
# ring share, 46.9%, is step 3's.
st.markdown(
    """
**The lines**

- Three lines are drawn, each labeled on the map and in the legend: Meitetsu's Nagoya Main and
  Bisai lines and JR Central's Tokaido Line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Ichinomiya City get rings, because the business data covers the city alone:
  lines running on to Inazawa and Gifu Prefecture are cut at the city line. The stations left out
  are listed below.
- The Shinkansen is not drawn.

**The businesses**

- From Ichinomiya City's list of food-business permits and its registers of barbers, beauty salons
  and laundries, all as of March 31, 2026, with the new permits and registrations it has listed
  each month since, to August 31, 2026.
- The city's food list leaves out vending-machine, vehicle, stall and temporary permits, entries
  containing personal information and operators who asked not to be listed, so it holds about two
  restaurants in three of the official count.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear: the Food shops layer is food retail only (bakeries and confectioners,
  delis, butchers and fishmongers).
- Shops that only notify rather than hold a permit, such as supermarkets, convenience stores and
  greengrocers, appear only where they chose to publish in the Ministry of Health, Labour and
  Welfare's open data (downloaded October 6, 2026), so that part of the Food shops layer is partial.
- The lists may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- The lists give an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where that fails, the dot sits at the ministry's
  own coordinates for the same premises, or else at its district's center.
- Where a trade name is its operator's own name, the dot shows its permit type instead.
- Names and permit types are shown in Japanese, as the lists record them.
- **About 47% of storefronts sit within a ring.**
"""
)

render_map_help("three business categories (Food shops, Food service and Personal services)")
render_excluded_stations("Ichinomiya")
render_country_links("Ichinomiya")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Ichinomiya")
