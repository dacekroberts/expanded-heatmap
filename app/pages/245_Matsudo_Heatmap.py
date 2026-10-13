"""Matsudo heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.matsudo.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Matsudo Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Matsudo")
render_city_title("Matsudo")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/matsudo/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Matsudo")

# From the japan-city skill's template and Yokohama's and Kōchi's pages
# (approved wording, pre-approved for this build, 2026-09-30); the two-date
# source sentence, the upper-bound sentence and the Sky Access bullet are
# proposals in docs/decisions_drafts/worktree-japan-east-2.md. The dates are
# the lists' own (chiba_pref.SOURCE_AS_OF); the ring share, 79.8% (1,000 of
# 1,253), is step 3's.
st.markdown(
    """
**The lines**

- Seven lines are drawn, each labeled on the map and in the legend: the Keisei Matsudo Line, JR
  East's Joban and Musashino lines, the Hokuso Line, the Ryutetsu Nagareyama Line, the Keisei
  Narita Sky Access Line and the Tobu Urban Park Line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Matsudo City get rings, because the business data is cut to the city alone:
  lines running on to Kamagaya, Kashiwa, Nagareyama, Ichikawa, Funabashi, Shiroi, Misato and
  Tokyo's Katsushika Ward are cut at the city line. The stations left out are listed below.
- The Narita Sky Access Line shares the Hokuso Line's track and stops only at Higashi-Matsudo in
  the city.

**The businesses**

- **This map shows personal services only: barbers, beauty salons and laundries.**
- From Chiba Prefecture's open-data registers of barbers (as of March 31, 2025) and of beauty
  salons and laundries (as of March 31, 2026, with openings to August 31, 2026), which list only
  premises whose operators agreed to publication.
- The prefecture publishes openings but not closures, so a dot is a premises on the register, not
  necessarily one open today.
- Restaurants, cafés and shops are not on this map: the national food-permit filings publish too
  few addresses here to place them.

**Reading the map**

- The registers give an address but no location. Each address is matched to MLIT's address
  reference data, which places almost all at their street block; where only the district can be
  found, the dot sits at the district's center.
- Where a business's trade name is its operator's own name, the dot shows its register type
  instead.
- Names and register types are shown in Japanese, as the prefecture records them.
- **About 80% of storefronts sit within a ring.**
"""
)

render_map_help("business layer", search='matsudo')
render_excluded_stations("Matsudo")
render_country_links("Matsudo")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Matsudo")
