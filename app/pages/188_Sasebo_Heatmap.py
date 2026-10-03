"""Sasebo heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.sasebo.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Sasebo Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Sasebo")
render_city_title("Sasebo")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/sasebo/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Sasebo")

# From the japan-city skill's template and Kitakyushu's and Okayama's pages
# (approved wording, pre-approved for this build, 2026-09-30); the sentences
# no template covers are proposals in docs/decisions_drafts/japan-wave2.md
# (the Matsuura Railway's two pieces, why there are no personal services).
# The as-of dates are the lists' own (config.SOURCE_AS_OF); MHLW's file states
# none, so it is dated by download. One restaurant in five withholds its
# address in MHLW's file (530 of 2,332 open restaurant permits, 22.7%,
# 2026-10-03). The ring share, 69.3%, is step 3's.
st.markdown(
    """
**The lines**

- Three lines are drawn, each labeled on the map and in the legend: the Matsuura Railway's
  Nishi-Kyushu Line, and JR Kyushu's Sasebo and Omura lines.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Sasebo City get rings, because the business data covers the city alone:
  lines running on to Hirado, Matsuura, Arita and Kawatana are cut at the city line.
- The Matsuura Railway leaves the city through Saza and comes back into it; its four stations in
  Saza have no rings and are listed below.

**The businesses**

- **This map shows food businesses only.**
- Sasebo City publishes no lists of barbers, beauty salons or laundries, so personal services are
  not on this map.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear either.
- From two food lists. Sasebo City's own list holds food-business permits granted before June 2021
  (as of April 30, 2026), shown where still in term at the end of August 2026.
- Permits since then are filed through the Ministry of Health, Labour and Welfare's system, whose
  open data is the second list (downloaded October 2, 2026). A premises in both lists appears once.
- The Food shops layer is food retail only, and it is partial: shops that only notify rather than
  hold a permit, such as supermarkets, convenience stores and greengrocers, appear only where they
  chose to publish in the ministry's list.
- The lists may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- About one restaurant in five in Sasebo chose not to publish its address in the national filing
  system and is not on this map. Where they are is not known.
- The rest are matched to MLIT's address reference data, which places most at their street block;
  where that fails for a ministry filing, the dot sits at the ministry's own coordinates.
- The city's list names an operator only where it is a company, and the ministry's list does not
  say who the operator is, so a trade name that is a sole trader's own name cannot be checked here.
- Names and permit types are shown in Japanese, as the lists record them.
- **About 69% of storefronts sit within a ring.**
"""
)

render_map_help("two business categories (Food shops and Food service)")
render_excluded_stations("Sasebo")
render_country_links("Sasebo")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Sasebo")
