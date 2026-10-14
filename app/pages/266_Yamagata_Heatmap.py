"""Yamagata heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.yamagata.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Yamagata Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Yamagata")
render_city_title("Yamagata")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/yamagata/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Yamagata")

# From the japan-city skill's template, Hiroshima's one-bucket line and
# Okazaki's and Ichinomiya's pages (the ministry's notifications and its
# points; approved wording, pre-approved for this build, 2026-09-30). Four
# bullets are proposals in docs/decisions_drafts/worktree-japan-regional-2.md:
# the dated source bullet (Okazaki's), the personal-services lists (from
# Aomori's), the prefecture-wide permits (from Aomori's whole-city bullet)
# and the withheld restaurants (from Hiroshima's). The date is
# config.FOOD_AS_OF; about 270 is the list's 273 prefecture-wide restaurant
# permits; one in twelve is 222 of its 2,770 restaurant permits (8.0%); the
# ring share, 34.0%, is step 3's (1,114 of 3,280).
st.markdown(
    """
**The lines**

- Three lines are drawn, each labeled on the map and in the legend: JR East's Ou, Senzan and
  Aterazawa lines.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Yamagata City get rings, because the business data covers the city alone:
  lines running on to Kaminoyama, Tendō, Sendai, Yamanobe and Nakayama are cut at the city line.
  The stations left out are listed below.
- The Shinkansen is not drawn (Yamagata appears as a JR Ou Line station).

**The businesses**

- **This map shows food businesses only.**
- Yamagata City's lists of barbers, beauty salons and laundries hold only premises opened since
  April 2019, so personal services are not on this map.
- From Yamagata City's list of food-business permits (as of August 31, 2026).
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear: the Food shops layer is food retail only (bakeries and confectioners,
  delis, butchers and fishmongers).
- Shops that only notify rather than hold a permit, such as supermarkets, convenience stores and
  greengrocers, appear only where they chose to publish in the Ministry of Health, Labour and
  Welfare's open data (downloaded October 6, 2026), so that part of the Food shops layer is partial.
- About 270 restaurant permits are registered for the whole prefecture rather than an address,
  which are event stalls and food trucks; they are not on this map.
- The lists may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- The lists give an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where that fails, the dot sits at the ministry's
  own coordinates for the same premises, or else at its district's center.
- About one restaurant in twelve in Yamagata chose not to publish its name and address in the
  city's list and is not on this map. Where they are is not known.
- Where a trade name is its operator's own name, the dot shows its permit type instead.
- Names and permit types are shown in Japanese, as the lists record them.
- **About 34% of storefronts sit within a ring.**
"""
)

render_map_help("two business categories (Food shops and Food service)", search='yamagata')
render_excluded_stations("Yamagata")
render_country_links("Yamagata")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Yamagata")
