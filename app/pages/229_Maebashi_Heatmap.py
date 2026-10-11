"""Maebashi heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.maebashi.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Maebashi Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Maebashi")
render_city_title("Maebashi")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/maebashi/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Maebashi")

# From the japan-city skill's template and Utsunomiya's page (approved
# wording, pre-approved for this build, 2026-09-30); the registers' rebuild
# and laundry-share bullets are proposals in
# docs/decisions_drafts/worktree-japan-regional-1.md. The dates are the lists'
# own (config.SOURCE_AS_OF); the laundry counts are step 2's and e-Stat's
# FY2024 table (the brief); one restaurant in 50 is MHLW's 38 of 1,850 open
# restaurant permits with no address; the ring share, 40.5%, is step 3's.
st.markdown(
    """
**The lines**

- Three lines are drawn, each labeled on the map and in the legend: the Jomo Electric Railway's
  Jomo Line and JR East's Ryomo and Joetsu lines.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Maebashi City get rings, because the business data covers the city alone:
  lines running on to Kiryu, Midori, Isesaki, Takasaki and Shibukawa are cut at the city line.
  The stations left out are listed below.

**The businesses**

- From two food lists and three registers. Maebashi City's own list holds food-business permits
  granted before April 2023 and still held (as of June 30, 2026).
- Permits since then are filed through the Ministry of Health, Labour and Welfare's system, whose
  open data is the second list (downloaded October 4, 2026). A premises in both lists appears once.
- Barbers, beauty salons and laundries come from the city's registers, brought up to August 31,
  2026 from its March list and its monthly lists of openings and closings.
- The laundry register lists 139 laundries, against 170 in the national count a year earlier. The
  city notes that some premises are left off at their operators' request.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear.
- The Food shops layer is food retail only, and it is partial: shops that only notify rather than
  hold a permit, such as supermarkets, convenience stores and greengrocers, appear only where they
  chose to publish in the ministry's list.
- The lists may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- About one restaurant in 50 in Maebashi chose not to publish its address in the national
  filing system and is not on this map. Where they are is not known.
- The rest are matched to MLIT's address reference data, which places most at their street block;
  where that fails for a ministry filing, the dot sits at the ministry's own coordinates, and
  otherwise at the district's center.
- Where a trade name is its operator's own name, the dot shows its permit type instead.
- Names and permit types are shown in Japanese, as the lists record them.
- **About 40% of storefronts sit within a ring.**
"""
)

render_map_help("three business categories (Food shops, Food service and Personal services)")
render_excluded_stations("Maebashi")
render_country_links("Maebashi")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Maebashi")
