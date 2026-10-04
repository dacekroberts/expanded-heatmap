"""Tbilisi heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.tbilisi.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_caption,
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_data_age,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Tbilisi Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Tbilisi")
render_city_title("Tbilisi")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/tbilisi/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Tbilisi")
# The credit Geostat's terms require (notice 114), on the city's own page.
render_caption(
    "Business data: National Statistics Office of Georgia (Geostat), Statistical "
    "Business Register, retrieved 2026-10-02; processed by this project. Rail: "
    "OpenStreetMap."
)

# The scaffold's bullets filled in for the city (2026-10-02); Prague's and
# Taichung's national-register pages are the model for The businesses.
# Sentences beyond the template are flagged as proposals in
# docs/decisions_drafts/seattle-tbilisi.md.
st.markdown(
    """
**The lines**

- Two lines are drawn, each labeled on the map and in the legend: **the Akhmeteli-Varketili
  Line** (16 stations) and **the Saburtalo Line** (7), in colors close to the metro's own. They
  meet at Station Square, where the two lines' stations, Station Square-1 and Station
  Square-2, are drawn separately.
- Routes and stations come from OpenStreetMap.
- All 23 stations are drawn, and all are inside the city of Tbilisi, the area covered.

**The businesses**

- **One national source**: the National Statistics Office of Georgia's business register, read
  where each business says it operates rather than where it is registered.
- **A business, not a shop**: the register lists each business once, at one address, so a chain
  with several shops appears once.
- A business appears once Geostat counts it as active, so one opened in the last year or two may
  not be shown yet.
- **About one storefront in five is not shown**: some have no location, and some share a point
  that is the center of a district rather than an address, four of them beside metro stations.
- A company shows its registered name, in Georgian. A business registered to a person shows its
  category instead of a name.
"""
)

render_map_help("three business categories (Retail, Food service and Personal services)")
render_excluded_stations("Tbilisi")
render_country_links("Tbilisi")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Tbilisi")
