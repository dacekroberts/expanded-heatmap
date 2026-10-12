"""Tottori heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.tottori.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Tottori Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Tottori")
render_city_title("Tottori")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/tottori/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Tottori")

# From the japan-city skill's template, Uji's and Mito's pages (the
# ministry's filings as the food source, the share clause, the withheld
# addresses, the ministry's coordinates) and Hiroshima's one-bucket line
# (approved wording, pre-approved for this build, 2026-09-30). Six bullets
# adapt an approved sentence of another page or are new, and are listed as
# proposals in docs/decisions_drafts/worktree-japan-regional-2.md: the Inbi
# Line across Yazu (Kanazawa's Ishikawa Line bullet), its frequency (Aomori's
# Tsugaru Line bullet), the missing personal-services lists (Aomori's), the
# share's caveat, the four towns, and the area-wide permits (Aomori's).
# MHLW's file states no date, so it is dated by download. The food share:
# 1,573 restaurant permits at a fixed address in the city, 79.0% of e-Stat's
# 1,990. Withheld addresses: 34 of 2,065 open restaurant permits. The ring
# share, 50.5%, is step 3's (1,131 of 2,240, 2026-10-11).
st.markdown(
    """
**The lines**

- Two lines are drawn, each labeled on the map and in the legend: JR West's San'in and Inbi
  lines.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Tottori City get rings, because the business data covers the city alone:
  lines running on to Iwami, Yurihama, Yazu and Chizu are cut at the city line. The stations left
  out are listed below.
- The JR Inbi Line leaves the city between Tsunoi and Kunifusa to cross Yazu: its track there is
  drawn, its three stations there have no rings.
- The JR Inbi Line is infrequent south of Yazu: about 12 trains a day run from Tottori to
  Kunifusa, Takagari, Mochigase and Inaba-Yashiro.

**The businesses**

- **This map shows food businesses only.**
- Neither Tottori City nor Tottori Prefecture publishes a list of barbers, beauty salons or
  laundries, so personal services are not on this map.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear either.
- The food businesses come from the Ministry of Health, Labour and Welfare's filing system, whose
  open data holds the permits and notifications Tottori City's health center has recorded since
  June 2021 (downloaded October 6, 2026). Permits granted before then and still in force are not
  in it, so it holds about 8 in 10 of the restaurant permits in the official count. The true
  share may be higher, because the official count may include four neighboring towns.
- The health center also licenses those four towns (Iwami, Yazu, Wakasa and Chizu); their filings
  are left out by address.
- About 350 permits and filings are registered for the whole city or prefecture rather than an
  address, which are event stalls and food trucks; they are not on this map.
- The Food shops layer is food retail only, and it is partial: shops that only notify rather than
  hold a permit, such as supermarkets, convenience stores and greengrocers, appear only where they
  chose to publish in the ministry's list.
- The list may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- About one restaurant in 60 in the health center's filings chose not to publish its address in
  the national filing system and is not on this map. Where they are is not known.
- The rest are matched to MLIT's address reference data, which places most at their street block;
  where that fails, the dot sits at the ministry's own coordinates.
- Where a business's trade name is its operator's own name, the dot shows its permit type instead.
- Names and permit types are shown in Japanese, as the list records them.
- **About 50% of storefronts sit within a ring.**
"""
)

render_map_help("two business categories (Food shops and Food service)")
render_excluded_stations("Tottori")
render_country_links("Tottori")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Tottori")
