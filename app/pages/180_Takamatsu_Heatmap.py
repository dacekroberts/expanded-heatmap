"""Takamatsu heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.takamatsu.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Takamatsu Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Takamatsu")
render_city_title("Takamatsu")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/takamatsu/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Takamatsu")

# From the japan-city skill's template and Matsuyama's and Kitakyushu's pages
# (approved wording, pre-approved for this build, 2026-09-30); the sentences
# they do not cover are proposals in docs/decisions_drafts/japan-wave2.md. The
# as-of dates are the lists' own (config.SOURCE_AS_OF). The ring share, 71.7%,
# is step 3's.
st.markdown(
    """
**The lines**

- Five lines are drawn, each labeled on the map and in the legend: Kotoden's Kotohira, Nagao and
  Shido lines and JR Shikoku's Yosan and Kotoku lines.
- The Nagao Line's trains run on to Takamatsu-Chikko over the Kotohira Line's track, and it is
  drawn along it.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap and the railway's own station list. Line colors are this
  project's own, not the operators'.
- Only stations inside Takamatsu City get rings, because the business data covers the city alone:
  lines running on to Ayagawa, Miki, Sanuki and Sakaide are cut at the city line.
- The Yakuri cable car, which is a sightseeing line, is not drawn.

**The businesses**

- From Takamatsu City's list of food-business permits and its registers of barbers, beauty
  salons and laundries, all as of August 31, 2026.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear: the Food shops layer is food retail only (bakeries and confectioners,
  delis, butchers and fishmongers).
- Shops that only notify rather than hold a permit, such as supermarkets, convenience stores and
  greengrocers, appear only where they chose to publish in the Ministry of Health, Labour and
  Welfare's open data (downloaded October 2, 2026), so that part of the Food shops layer is partial.
- The lists may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- The lists give an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where that fails for a ministry filing, the dot
  sits at the ministry's own coordinates, and otherwise at its district's center.
- In the city's own lists, where a trade name is its operator's own name, the dot shows its permit
  type instead; the ministry's list does not say who the operator is, so this cannot be checked
  there.
- Names and permit types are shown in Japanese, as the lists record them.
- **About 72% of storefronts sit within a ring.**
"""
)

render_map_help("three business categories (Food shops, Food service and Personal services)")
render_excluded_stations("Takamatsu")
render_country_links("Takamatsu")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Takamatsu")
