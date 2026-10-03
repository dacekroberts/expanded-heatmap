"""Himeji heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.himeji.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Himeji Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Himeji")
render_city_title("Himeji")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/himeji/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Himeji")

# From the japan-city skill's template and Kawasaki's and Kitakyushu's pages
# (approved wording, pre-approved for this build, 2026-09-30). The as-of dates
# are the lists' own (config.SOURCE_AS_OF). The ring share, 67.2%, is step 3's.
st.markdown(
    """
**The lines**

- Six lines are drawn, each labeled on the map and in the legend: JR West's Kobe, Sanyo, Bantan
  and Kishin lines and Sanyo Electric Railway's Main and Aboshi lines.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Himeji City get rings, because the business data covers the city alone:
  lines running on to Takasago, Tatsuno, Fukusaki and Kamikawa are cut at the city line.
- The Shinkansen is not drawn (Himeji appears as a JR station).

**The businesses**

- From Himeji City's list of food-business permits and its registers of barbers, beauty salons
  and laundries (all as of September 10, 2026).
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear: the Food shops layer is food retail only (bakeries and confectioners,
  delis, butchers and fishmongers).
- Food businesses that only notify the city rather than hold a permit, such as many convenience
  stores and greengrocers, are not in the list.
- The lists may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- The lists give an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where only the district can be found, the dot
  sits at the district's center.
- Where a business's trade name is its operator's own name, the dot shows its permit type
  instead.
- Names and permit types are shown in Japanese, as the city records them.
- **About 67% of storefronts sit within a ring.**
"""
)

render_map_help("three business categories (Food shops, Food service and Personal services)")
render_excluded_stations("Himeji")
render_country_links("Himeji")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Himeji")
