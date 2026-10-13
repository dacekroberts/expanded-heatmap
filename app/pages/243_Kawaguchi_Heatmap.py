"""Kawaguchi heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.kawaguchi.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Kawaguchi Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Kawaguchi")
render_city_title("Kawaguchi")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/kawaguchi/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Kawaguchi")

# From the japan-city skill's template and Hiroshima's and Koshigaya's pages
# (approved wording, pre-approved for this build, 2026-09-30); the sentences
# no template covers (the dated first bullet with the missing June entries,
# the withheld addresses, the trains that pass without stopping) are
# proposals in docs/decisions_drafts/worktree-japan-east-2.md. The dates are
# the list's own (config.SOURCE_AS_OF); about one in six is the 1,316 entries
# of 8,364 whose address the city withholds; the ring share, 56.1% (2,980 of
# 5,312), is step 3's.
st.markdown(
    """
**The lines**

- Three lines are drawn, each labeled on the map and in the legend: the Saitama Rapid Railway Line
  and JR East's Keihin-Tohoku and Musashino lines.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Kawaguchi City get rings, because the business data covers the city alone:
  lines running on to Saitama City, Warabi, Koshigaya and Tokyo's Kita Ward are cut at the city
  line. The stations left out are listed below.
- JR's Utsunomiya, Takasaki and Shonan-Shinjuku line trains pass through the city without
  stopping and are not drawn.

**The businesses**

- **This map shows food businesses only.**
- Kawaguchi City's lists of barbers, beauty salons and laundries are not open data, so personal
  services are not on this map.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear either.
- From Kawaguchi City's list of food-business permits and notifications (as of March 31, 2026,
  with the new premises it listed for April, May and July 2026; the list has no entries for June).
- The Food shops layer is food retail only (bakeries and confectioners, delis, butchers and
  fishmongers, and the shops that notify the city, such as supermarkets, convenience stores and
  greengrocers).
- The list may include premises that have closed, so a dot means a permit on file, not a business
  open today.

**Reading the map**

- The city withholds the address of about one entry in six in its list, and those are not on this
  map. Where they are is not known.
- The rest are matched to MLIT's address reference data, which places most at their street block;
  where only the district can be found, the dot sits at the district's center.
- Where the city masks a trade name, or a trade name is its operator's own name, the dot shows its
  permit type instead.
- Names and permit types are shown in Japanese, as the list records them.
- **About 56% of storefronts sit within a ring.**
"""
)

render_map_help("two business categories (Food shops and Food service)", search='kawaguchi')
render_excluded_stations("Kawaguchi")
render_country_links("Kawaguchi")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Kawaguchi")
