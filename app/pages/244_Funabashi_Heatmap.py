"""Funabashi heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.funabashi.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Funabashi Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Funabashi")
render_city_title("Funabashi")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/funabashi/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Funabashi")

# From the japan-city skill's template and Yokohama's page (approved wording,
# pre-approved for this build, 2026-09-30); the source sentence with its
# reason for no food layer is the brief's proposal, recorded in
# docs/decisions_drafts/worktree-japan-east-2.md. The dates are the lists' own
# (config.SOURCE_AS_OF); the ring share, 83.8% (1,234 of 1,473), is step 3's.
st.markdown(
    """
**The lines**

- Ten lines are drawn, each labeled on the map and in the legend: the Keisei Main and Matsudo
  lines, JR East's Chuo-Sobu, Yokosuka / Sobu Rapid, Musashino and Keiyo lines, the Tozai Line, the
  Toyo Rapid Railway Line, the Tobu Urban Park Line and the Hokuso Line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Funabashi City get rings, because the business data covers the city alone:
  lines running on to Ichikawa, Narashino, Kamagaya, Yachiyo, Shiroi and Chiba are cut at the city
  line. The stations left out are listed below.

**The businesses**

- **This map shows personal services only: barbers, beauty salons and laundries.**
- From Funabashi City's registers of barbers and beauty salons (as of August 1, 2026) and of
  laundries (as of July 1, 2026). Restaurants, cafés and shops are not on this map: the national
  food-permit filings publish too few addresses here to place them.
- The registers record no closures, so a dot is a premises on the register then, not necessarily
  one open today.

**Reading the map**

- The registers give an address but no location. Each address is matched to MLIT's address
  reference data, which places almost all at their street block; where only the district can be
  found, the dot sits at the district's center.
- Where a business's trade name is its operator's own name, the dot shows its register type
  instead.
- Names and register types are shown in Japanese, as the city records them.
- **About 84% of storefronts sit within a ring.**
"""
)

render_map_help("business layer")
render_excluded_stations("Funabashi")
render_country_links("Funabashi")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Funabashi")
