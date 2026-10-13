"""Shizuoka heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.shizuoka.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Shizuoka Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Shizuoka")
render_city_title("Shizuoka")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/shizuoka/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Shizuoka")

# From the japan-city skill's template, Yokohama's one-bucket line and Kōchi's
# upper-bound sentences (approved wording, pre-approved for this build,
# 2026-09-30). The source bullet with each register's own date and the food
# bullet are proposals in docs/decisions_drafts/worktree-japan-regional-2.md
# (the owner asked for each list's date on the page, 2026-10-04). The dates
# are config.TRADE_AS_OF; the ring share, 44.2%, is step 3's (1,216 of 2,752).
st.markdown(
    """
**The lines**

- Two lines are drawn, each labeled on the map and in the legend: the Shizuoka Railway's
  Shizuoka-Shimizu Line and JR Central's Tokaido Line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Shizuoka City get rings, because the business data covers the city alone:
  lines running on to Fuji and Yaizu are cut at the city line. The stations left out are listed
  below.
- The Shinkansen is not drawn (Shizuoka appears as a JR Tokaido Line station).
- The Oigawa Railway's Ikawa Line, which is a sightseeing line, is not drawn.

**The businesses**

- **This map shows personal services only: barbers, beauty salons and laundries.**
- Restaurants, cafés and shops are not on this map: the national list of food businesses gives
  an address for only about six in ten of Shizuoka's restaurants.
- From Shizuoka City's registers of barbers, beauty salons and laundries: the complete lists as
  of March 31, 2026 and the new premises listed each month since, to August 31, 2026 for barbers
  and September 30, 2026 for beauty salons and laundries.
- The city lists new premises each month but not closures, so a premises that closed after March
  is still counted. The map shows an upper bound, and a dot is a premises on the lists, not
  necessarily one open today.

**Reading the map**

- The lists give an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where only the district can be found, the dot
  sits at the district's center.
- Where a business's trade name is its operator's own name, the dot shows its register type
  instead.
- Names and types are shown in Japanese, as the city records them.
- **About 44% of the premises sit within a ring.**
"""
)

render_map_help("business layer", search='shizuoka')
render_excluded_stations("Shizuoka")
render_country_links("Shizuoka")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Shizuoka")
