"""Sakai heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.sakai.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Sakai Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Sakai")
render_city_title("Sakai")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/sakai/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Sakai")

# From the japan-city skill's template and Hiroshima's and Kyoto's pages
# (approved wording, pre-approved for this build, 2026-09-30); the sentences
# they do not cover are proposals in docs/decisions_drafts/japan-batch.md. The
# rebuild's dates are config.SOURCE_AS_OF and config.AS_OF; MHLW's file states
# none, so it is dated by download.
st.markdown(
    """
**The lines**

- Six lines are drawn, each labeled on the map and in the legend: the Hankai Line, a tram; Osaka
  Metro's Midōsuji Line; Nankai's Main, Kōya and Semboku lines; and JR West's Hanwa Line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Sakai City get rings, because the business data covers the city alone:
  lines running on to Osaka, Takaishi, Izumi and Osakasayama are cut at the city line.

**The businesses**

- **This map shows food businesses only.**
- Sakai City publishes its lists of barbers, beauty salons and laundries only as PDF documents,
  outside its open data, so personal services are not on this map.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear either.
- The food businesses are rebuilt from Sakai City's list of food-business permits as of 1 April
  2026 and its monthly lists of new permits and closures since, keeping each permit still within
  its term on 31 August 2026, the last date the newest monthly lists cover.
- Shops that only notify rather than hold a permit, such as supermarkets, convenience stores and
  greengrocers, appear only where they chose to publish in the Ministry of Health, Labour and
  Welfare's open data (downloaded 2 October 2026), so that part of the Food shops layer is partial.
- The lists may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- The lists give an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where that fails for a ministry filing, the dot
  sits at the ministry's own coordinates, and otherwise at its district's center.
- In the city's own list, where a trade name is its operator's own name, the dot shows its permit
  type instead; the ministry's list does not say who the operator is, so this cannot be checked
  there.
- Names and permit types are shown in Japanese, as the lists record them.
- **About three-quarters of storefronts sit within a ring.**
"""
)

render_map_help("two business categories (Food shops and Food service)")
render_excluded_stations("Sakai")
render_country_links("Sakai")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
