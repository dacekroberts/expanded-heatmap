"""Aomori heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.aomori.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Aomori Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Aomori")
render_city_title("Aomori")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/aomori/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Aomori")

# From the japan-city skill's template and Hiroshima's one-bucket line
# (approved wording, pre-approved for this build, 2026-09-30). Three bullets
# adapt an approved sentence of another page and are listed as proposals in
# docs/decisions_drafts/worktree-japan-regional-2.md: the Tsugaru Line's
# frequency (Akita's Uetsu Line bullet), the missing personal-services lists
# (Akita's laundries bullet) and the whole-city permits. The date is
# config.FOOD_AS_OF; the ring share, 34.9%, is step 3's (1,231 of 3,528).
st.markdown(
    """
**The lines**

- Three lines are drawn, each labeled on the map and in the legend: JR East's Ou and Tsugaru
  lines and the Aoimori Railway Line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Aomori City get rings, because the business data covers the city alone:
  lines running on to Yomogita, Fujisaki and Hiranai are cut at the city line. The stations left
  out are listed below.
- The Shinkansen is not drawn (Shin-Aomori appears as a JR Ou Line station).
- The JR Tsugaru Line is infrequent: 9 trains a weekday run toward Kanita and 8 toward Aomori.

**The businesses**

- **This map shows food businesses only.**
- Aomori City publishes no list of barbers, beauty salons or laundries, so personal services are
  not on this map.
- From Aomori City's list of food-business permits (as of August 31, 2026).
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear: the Food shops layer is food retail only (bakeries and confectioners,
  delis, butchers and fishmongers).
- Food businesses that only notify the city rather than hold a permit, such as many convenience
  stores and greengrocers, are not in the list.
- About 1,300 permits are registered for the whole city rather than an address, which are event
  stalls and food trucks; they are not on this map.
- The list may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- The list gives an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where only the district can be found, the dot
  sits at the district's center.
- Where a business's trade name is its operator's own name, the dot shows its permit type instead.
- Names and permit types are shown in Japanese, as the city records them.
- **About 35% of storefronts sit within a ring.**
"""
)

render_map_help("two business categories (Food shops and Food service)")
render_excluded_stations("Aomori")
render_country_links("Aomori")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Aomori")
