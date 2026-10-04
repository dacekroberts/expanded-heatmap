"""Yokkaichi heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.yokkaichi.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Yokkaichi Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Yokkaichi")
render_city_title("Yokkaichi")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/yokkaichi/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Yokkaichi")

# From the japan-city skill's template and Kawasaki's page (approved wording,
# pre-approved for this build, 2026-09-30); the sentences it does not cover are
# proposals in docs/decisions_drafts/japan-wave2.md: the notification bullet,
# which replaces the template's (the city publishes its notifications, and
# they count as Food shops). The as-of dates are the lists' own
# (config.SOURCE_AS_OF). The ring share, 73.9%, is step 3's.
st.markdown(
    """
**The lines**

- Seven lines are drawn, each labeled on the map and in the legend: Kintetsu's Nagoya and
  Yunoyama lines; the Yokkaichi Asunarou Railway's Utsube and Hachioji lines; the Sangi Line;
  JR's Kansai Line; and the Ise Railway's Ise Line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Yokkaichi City get rings, because the business data covers the city alone:
  lines running on to Kawagoe, Asahi, Komono, Inabe and Suzuka are cut at the city line.

**The businesses**

- From Yokkaichi City's lists of food-business permits and food-business notifications and its
  lists of barbers, beauty salons and laundries (all as of August 31, 2026).
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
- **About 74% of storefronts sit within a ring.**
"""
)

render_map_help("three business categories (Food shops, Food service and Personal services)")
render_excluded_stations("Yokkaichi")
render_country_links("Yokkaichi")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Yokkaichi")
