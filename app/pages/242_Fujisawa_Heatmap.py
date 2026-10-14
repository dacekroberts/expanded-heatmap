"""Fujisawa heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.fujisawa.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Fujisawa Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Fujisawa")
render_city_title("Fujisawa")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/fujisawa/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Fujisawa")

# From the japan-city skill's template and Ichinomiya's, Kawasaki's and
# Koshigaya's pages (approved wording, pre-approved for this build,
# 2026-09-30); the sentences no template covers (the dated first bullet, the
# estimate the owner's call 175 asks for, the closures) are proposals in
# docs/decisions_drafts/worktree-japan-east-2.md. The dates are the lists' own
# (config.SOURCE_AS_OF); 88% to 101% is the brief's estimate (3,790 restaurant
# permits per 1,495 census establishments, 2.54, against four Kanagawa cities'
# 2.52 to 2.87); the ring share, 77.2% (3,821 of 4,947), is step 3's.
st.markdown(
    """
**The lines**

- Five lines are drawn, each labeled on the map and in the legend: the Odakyu Enoshima Line, the
  Enoshima Electric Railway (Enoden), the JR Tokaido Line, the Shonan Monorail and the Sotetsu
  Izumino Line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Fujisawa City get rings, because the business data covers the city alone:
  lines running on to Kamakura, Yokohama, Yamato and Chigasaki are cut at the city line. The
  stations left out are listed below.
- Yokohama's Blue Line subway, which has only its terminus, Shonandai, in the city, is not drawn;
  Shonandai appears as a station of the Odakyu and Sotetsu lines.

**The businesses**

- From Fujisawa City's lists of food-business permits and of barbers, beauty salons and laundries,
  all as of June 30, 2026, with the new food permits it listed for July and August 2026.
- No official count of Fujisawa's restaurants is published. Measured against the 2021 census of
  restaurants at the rates of four other Kanagawa cities, the list is estimated to hold between
  88% and 101% of them.
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
- Where a trade name is its operator's own name, the dot shows its permit type instead; the food
  list names an operator only where it is a company, so this cannot be checked for the rest.
- Names and permit types are shown in Japanese, as the lists record them.
- **About 77% of storefronts sit within a ring.**
"""
)

render_map_help("three business categories (Food shops, Food service and Personal services)", search='fujisawa')
render_excluded_stations("Fujisawa")
render_country_links("Fujisawa")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Fujisawa")
