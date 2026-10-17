"""Kurashiki heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.kurashiki.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Kurashiki Heatmap | Global Transit-Business Atlas", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Kurashiki")
render_city_title("Kurashiki")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/kurashiki/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Kurashiki")

# From the japan-city skill's template and Hiroshima's one-bucket line
# (approved wording, pre-approved for this build, 2026-09-30). Four bullets
# adapt an approved sentence of another page and are listed as proposals in
# docs/decisions_drafts/worktree-japan-regional-2.md: the personal-services
# lists (Okayama's bullet), the area-wide permits (Aomori's), the upper-bound
# bullet (Kyoto's and Shizuoka's) and the share at a district's center (call
# 145). No coverage sentence (owner, call 229). The date is
# config.FOOD_AS_OF; the ring share, 53.5%, is step 3's (2,574 of 4,815).
st.markdown(
    """
**The lines**

- Six lines are drawn, each labeled on the map and in the legend: the Mizushima Rinkai Railway's
  Mizushima Main Line, JR West's Sanyo, Seto-Ohashi, Hakubi and Uno Minato lines, and the Ibara
  Railway's Ibara Line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Kurashiki City get rings, because the business data covers the city alone:
  lines running on to Okayama, Hayashima, Soja, Yakage, Asakuchi, Tamano and Kagawa are cut at the
  city line. The stations left out are listed below.
- The Shinkansen is not drawn (Shin-Kurashiki appears as a JR Sanyo Line station).

**The businesses**

- **This map shows food businesses only.**
- Kurashiki City publishes its lists of barbers and beauty salons under terms that do not allow
  reuse, and no list of laundries, so personal services are not on this map.
- From Kurashiki City's list of food-business permits (as of March 31, 2026).
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear: the Food shops layer is food retail only (bakeries and confectioners,
  delis, butchers and fishmongers).
- Food businesses that only notify the city rather than hold a permit, such as many convenience
  stores and greengrocers, are not in the list.
- About 660 permits are registered for an area rather than an address, which are food trucks and
  stalls; they are not on this map.
- The city publishes the list once a year and no closures in between, so a business that closed
  after March 2026 is still counted. The map shows an upper bound, and a dot means a permit on
  file, not a business open today.

**Reading the map**

- The list gives an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where only the district can be found, the dot
  sits at the district's center. About one dot in eight sits at a district's center.
- Where a business's trade name is its operator's own name, the dot shows its permit type instead.
- Names and permit types are shown in Japanese, as the city records them.
- **About 53% of storefronts sit within a ring.**
"""
)

render_map_help("two business categories (Food shops and Food service)", search='kurashiki')
render_excluded_stations("Kurashiki")
render_country_links("Kurashiki")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Kurashiki")
