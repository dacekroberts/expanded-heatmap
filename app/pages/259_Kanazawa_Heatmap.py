"""Kanazawa heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.kanazawa.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Kanazawa Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Kanazawa")
render_city_title("Kanazawa")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/kanazawa/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Kanazawa")

# From the japan-city skill's template, Hiroshima's one-bucket line, Toyama's
# name-rule bullet in the singular and Hamamatsu's own-coordinates sentence
# (approved wording, pre-approved for this build, 2026-09-30). Four sentences
# are proposals in docs/decisions_drafts/worktree-japan-regional-2.md: the
# Ishikawa Line's crossing of Nonoichi, the personal-services reason, the
# snapshot bullet and the expiry bullet (the owner sent the expiry sentence
# to review time, 2026-10-05). The date is config.FOOD_AS_OF; about four in
# ten is 3,360 of the 7,844 storefront rows past their 許可満了日 on
# 2026-10-11 (42.8%); the ring share, 38.4%, is step 3's (2,837 of 7,388).
st.markdown(
    """
**The lines**

- Three lines are drawn, each labeled on the map and in the legend: the Hokuriku Railroad's
  (Hokutetsu) Asanogawa and Ishikawa lines and the IR Ishikawa Railway Line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Kanazawa City get rings, because the business data covers the city alone:
  lines running on to Uchinada, Nonoichi, Hakusan and Tsubata are cut at the city line. The
  stations left out are listed below.
- The Hokutetsu Ishikawa Line leaves the city between Shin-Nishi-Kanazawa and Magae to cross
  Nonoichi: its track there is drawn, its three stations there have no rings.
- The Shinkansen is not drawn (Kanazawa appears as an IR Ishikawa Railway station).

**The businesses**

- **This map shows food businesses only.**
- Kanazawa City's lists of barbers, beauty salons and laundries are not open data, so personal
  services are not on this map.
- From Kanazawa City's list of food-business permits (as of April 2024). The city has not
  updated its open list since.
- About four in ten of these permits have reached their expiry date since April 2024; renewals
  are not in the list.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear either: the Food shops layer is food retail only (bakeries and
  confectioners, delis, butchers and fishmongers).
- Food businesses that only notify the city rather than hold a permit, such as many convenience
  stores and greengrocers, are not in the list.
- The list may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- Each address is matched to MLIT's address reference data, which places most at their street
  block; where only the district can be found, the dot sits at the city's own coordinates for
  the premises.
- Where a trade name is its operator's own name, the dot shows its permit type instead; the
  city's list names an operator only where it is a company, so this cannot be checked for the
  rest.
- Names and permit types are shown in Japanese, as the city records them.
- **About 38% of storefronts sit within a ring.**
"""
)

render_map_help("two business categories (Food shops and Food service)")
render_excluded_stations("Kanazawa")
render_country_links("Kanazawa")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Kanazawa")
