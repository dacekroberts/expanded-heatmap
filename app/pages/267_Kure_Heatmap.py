"""Kure heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.kure.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Kure Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Kure")
render_city_title("Kure")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/kure/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Kure")

# From the japan-city skill's template, Kurume's and Tottori's pages (the
# ministry's filings as the food source, the withheld addresses, the
# ministry's coordinates), Soka's one-line bullets and Hiroshima's one-bucket
# line (approved wording, pre-approved for this build, 2026-09-30). Four
# bullets adapt an approved sentence of another page or are new, and are
# listed as proposals in docs/decisions_drafts/worktree-japan-regional-2.md:
# the missing personal-services lists (Aomori's), the food share (the owner's
# call 125, Ichinomiya's sentence shape), the withheld addresses as "three in
# ten", and the placement tiers (Kakogawa's, the owner's call 145). MHLW's
# file states no date, so it is dated by download. The food share: 1,022
# restaurant permits at a fixed, published address, 58.3% of e-Stat's 1,752.
# Withheld addresses: 487 of 1,543 open restaurant permits (31.6%). Tiers:
# 1,406 block (88.2%), 167 the ministry's point (10.5%, 134 on the islands),
# 22 a town center. The ring share, 58.6%, is step 3's (935 of 1,595,
# 2026-10-11).
st.markdown(
    """
**The lines**

- One line is drawn, labeled on the map and in the legend: JR West's Kure Line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Kure City get rings, because the business data covers the city alone: the
  line running on to Saka and Higashihiroshima is cut at the city line. The stations left out are
  listed below.

**The businesses**

- **This map shows food businesses only.**
- Kure City publishes no list of barbers, beauty salons or laundries, so personal services are
  not on this map.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear either.
- The food businesses come from the Ministry of Health, Labour and Welfare's filing system, whose
  open data holds the permits and notifications Kure City has recorded since June 2021
  (downloaded October 6, 2026). Permits granted before then and still in force are not in it.
- The map shows about half (46%) of the restaurants in the official count: the ministry's list
  holds permits granted since June 2021, vehicles and stalls are left out, and about three
  fixed restaurants in ten do not publish their address.
- The Food shops layer is food retail only, and it is partial: shops that only notify rather than
  hold a permit, such as supermarkets, convenience stores and greengrocers, appear only where they
  chose to publish in the ministry's list.
- The list may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- About three restaurants in ten in Kure chose not to publish their address in the national
  filing system and are not on this map. Where they are is not known.
- The rest are matched to MLIT's address reference data: about 88% reach their street block, and
  about 11%, most of them on the city's islands, sit at the ministry's own coordinates; 22 sit
  at their district's center.
- Where a business's trade name is its operator's own name, the dot shows its permit type instead.
- Names and permit types are shown in Japanese, as the list records them.
- **About 59% of storefronts sit within a ring.**
"""
)

render_map_help("two business categories (Food shops and Food service)")
render_excluded_stations("Kure")
render_country_links("Kure")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Kure")
