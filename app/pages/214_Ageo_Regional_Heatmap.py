"""Ageo (Regional) heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.ageo_regional.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Ageo (Regional) Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Ageo (Regional)")
render_city_title("Ageo (Regional)")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/ageo_regional/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Ageo (Regional)")

# From the japan-city skill's template and Shimonoseki's and Nishitōkyō's
# pages (approved wording, pre-approved for this build); the sentences no
# template covers (the two towns on one page, the old-law upper bound, the
# prefecture's withholding note with no share, call 173) are proposals in
# docs/decisions_drafts/worktree-japan-east-1.md. The ring share, 51.9%
# (1,367 of 2,633), is step 3's.
st.markdown(
    """
**The lines**

- Two lines are drawn, each labeled on the map and in the legend: the New Shuttle and JR East's
  Takasaki Line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Ageo City and Ina Town get rings, because the business data covers the two
  alone: the lines running on to Saitama City and Okegawa are cut at their line. The New Shuttle's
  five stations in Ina, its terminus Uchijuku among them, are drawn and ringed. The stations left
  out are listed below.
- The Shinkansen is not drawn.

**The businesses**

- From Saitama Prefecture's lists for Ageo City and Ina Town: its food-business permits and
  notifications (downloaded October 6, 2026), its list of permits under the old food law (as of
  March 31, 2026), and its barbers, beauty salons and laundries (as of March 31, 2026, with new
  premises to August 31, 2026).
- The old-law permits are shown while their term runs; closures since March are not seen, so
  that part of the map is an upper bound.
- The prefecture leaves out some premises at their operators' request, so the lists are not
  complete.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear: the Food shops layer is food retail only (bakeries and confectioners,
  delis, butchers and fishmongers, and the shops that notify the prefecture, such as supermarkets,
  convenience stores and greengrocers).
- The lists may include premises that have closed, so a dot means a permit on file, not a business
  open today.

**Reading the map**

- The lists give an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where that fails for a food business, the dot
  sits at the prefecture's own coordinates, and where only the district can be found, at the
  district's center.
- Where a business's trade name is its operator's own name, the dot shows its permit type instead.
- Names and permit types are shown in Japanese, as the lists record them.
- **About 52% of storefronts sit within a ring.**
"""
)
render_map_help("three business categories (Food shops, Food service and Personal services)")
render_excluded_stations("Ageo (Regional)")
render_country_links("Ageo (Regional)")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Ageo (Regional)")
