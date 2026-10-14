"""Naha heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.naha.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Naha Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Naha")
render_city_title("Naha")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/naha/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Naha")

# From the japan-city skill's template and Kyoto's page (the rebuilt register
# and its upper-bound sentences; approved wording, pre-approved for this
# build); the sentences neither covers are proposals in
# docs/decisions_drafts/worktree-japan-naha.md. The restaurant figure, 8,785
# against 8,530, is step 2's (outputs/naha/official_shares.json); the ring
# share, 84.7%, is step 3's (8,598 of 10,153).
st.markdown(
    """
**The lines**

- One line is drawn, labeled on the map and in the legend: the Yui Rail, Okinawa's monorail.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Naha City get rings, because the business data covers the city alone: the
  line running on to Urasoe is cut at the city line. The stations left out are listed below.

**The businesses**

- Naha publishes no complete list of food-business permits, only each month's new permits and,
  until May 2021, each month's renewals. The food businesses here are therefore rebuilt: every
  monthly list from April 2015 to August 2026, keeping each permit still within its term on
  August 31, 2026, the last date the newest monthly list covers.
- The city does not publish closures, so a business that closed before its permit ran out is still
  counted. The map shows an upper bound: the rebuilt list holds 8,785 restaurant permits, against
  8,530 in force in the national count of March 2025. A dot means a permit on file, not a business
  open today.
- Barbers and beauty salons come from the city's registers as of September 4, 2026. The city
  publishes no list of laundries, so the Personal services layer has none.
- Stalls licensed for the whole city (769) and vehicles licensed across the prefecture (171) have
  no fixed address and are left out.
- Bars with hostess service are left out where the permit names its form of business, which about
  one restaurant permit in five does.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear. The Food shops layer is food retail only, by permit type: bakeries
  and confectioners, delis, butchers and fishmongers.
- Shops selling only packaged food have filed a notification rather than a permit since 2021 and
  are not in the lists.

**Reading the map**

- The lists give an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where only the district can be found, the dot
  sits at the district's center.
- A street block is one point on the map, so dense blocks stack many dots on one spot. The densest
  is the Sakaemachi market block in Asato, with about 250.
- Where a business's trade name is its operator's own name, the dot shows its permit type instead.
- Names and permit types are shown in Japanese, as the city records them.
- **About 85% of storefronts sit within a ring.**
"""
)

render_map_help("three business categories (Food shops, Food service and Personal services)", search='naha')
render_excluded_stations("Naha")
render_country_links("Naha")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Naha")
