"""Neyagawa heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.neyagawa.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Neyagawa Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Neyagawa")
render_city_title("Neyagawa")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/neyagawa/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Neyagawa")

# From the japan-city skill's template and Yokohama's page (approved wording:
# the one-bucket line with laundries); the sentence they do not cover (no
# food list) is a proposal in docs/decisions_drafts/worktree-japan-kansai-2.md.
# The as-of date is the lists' own (config.REGISTERS_AS_OF). The ring share is
# step 3's (2026-10-11).
st.markdown(
    """
**The lines**

- Two lines are drawn, each labeled on the map and in the legend: the Keihan Main Line and the JR
  Gakkentoshi Line, which has one station in the city, at Neyagawakoen.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Neyagawa City get rings, because the business data covers the city alone:
  lines running on to Hirakata, Kadoma, Katano, Shijōnawate and Daitō are cut at the city line.
  The stations left out are listed below.

**The businesses**

- **This map shows personal services only: barbers, beauty salons and laundries.**
- From Neyagawa City's registers of barbers, beauty salons and laundries (as of August 31, 2026).
- Restaurants, cafés and shops are not on this map: the city publishes no list of food-business
  permits.
- The lists may include premises that have closed, so a dot means a premises on the register, not
  a business open today.

**Reading the map**

- The lists give an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where only the district can be found, the dot
  sits at the district's center.
- Where a business's trade name is its operator's own name, the dot shows its register type
  instead.
- Names and types are shown in Japanese, as the city records them.
- **About seven in ten of the premises sit within a ring.**
"""
)

render_map_help("business layer", search='neyagawa')
render_excluded_stations("Neyagawa")
render_country_links("Neyagawa")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Neyagawa")
