"""Morioka heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.morioka.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Morioka Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Morioka")
render_city_title("Morioka")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/morioka/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Morioka")

# From the japan-city skill's template, Akita's and Ichinomiya's pages (the
# ministry's notifications and its points) (approved wording, pre-approved for
# this build, 2026-09-30); the withheld-entries bullet and the Yamada and
# Hanawa lines' bullet are proposals in
# docs/decisions_drafts/worktree-japan-regional-1.md (Ichinomiya's call 125
# with the city's own reason; call 86 in Fukushima's proposed form). The
# dates are the lists' own (config.SOURCE_AS_OF); MHLW's file states no date,
# so it is dated by download. 2,701 is the list's restaurants with an address
# (of 3,350; 649 withheld), 83.5% of e-Stat's 3,233 in force on 2025-03-31.
# The ring share, 50.0%, is step 3's (2,303 of 4,609, 2026-10-07).
st.markdown(
    """
**The lines**

- Five lines are drawn, each labeled on the map and in the legend: JR East's Tohoku, Tazawako,
  Yamada and Hanawa lines and the IGR Iwate Galaxy Railway Line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Morioka City get rings, because the business data covers the city alone:
  lines running on to Takizawa, Yahaba, Iwate, Hachimantai and Miyako are cut at the city line.
  The stations left out are listed below.
- The Shinkansen is not drawn (Morioka appears as a JR and IGR station).
- The JR Yamada and Hanawa lines are infrequent: the Yamada Line runs 10 trains a weekday each way
  between Morioka and Kami-Yonai and 3 each way beyond it, and the Hanawa Line 7 toward Odate and
  9 toward Morioka.

**The businesses**

- From Morioka City's list of food-business permits (as of August 31, 2026) and its registers of
  barbers, beauty salons and laundries (as of September 30, 2026).
- Morioka City leaves out of its food list the premises whose operators asked not to be listed,
  about one restaurant in five, so they are not on this map. The 2,701 restaurants it lists with
  an address are 83.5% of the 3,233 in the national count of March 2025; where the others are is
  not known.
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
- **About 50% of storefronts sit within a ring.**
"""
)

render_map_help("three business categories (Food shops, Food service and Personal services)")
render_excluded_stations("Morioka")
render_country_links("Morioka")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Morioka")
