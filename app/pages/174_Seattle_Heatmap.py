"""Seattle (Regional) heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.seattle.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Seattle (Regional) Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Seattle (Regional)")
render_city_title("Seattle (Regional)")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/seattle/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Seattle (Regional)")
# The credits the sources require on the city's own page (notices 109-113):
# King County's two texts word for word, Snohomish County's in the owner's
# words, the Liquor Board's list date and its own note. Unconditional.
st.caption(
    "Food inspection data: Public Health – Seattle & King County. Data provided by "
    "permission of King County. Lynnwood and Mountlake Terrace food: Snohomish County, "
    "Food Service Establishments (2025). Shops licensed to sell alcohol: Washington State "
    "Liquor and Cannabis Board, off-premise licensee list of September 29, 2026, whose "
    "reports the Board says \"contain possible errors due to a known data transfer "
    "issue\". Business license data: City of Seattle; City of Bellevue. Rail: "
    "OpenStreetMap."
)

# The scaffold's bullets filled in for the city (2026-10-02); New York's
# multi-source bullets are the model for The businesses. Sentences beyond the
# template are flagged as proposals in docs/decisions_drafts/seattle-tbilisi.md.
st.markdown(
    """
**The lines**

- Two lines are drawn, each labeled on the map and in the legend: **the 1 Line** (Lynnwood City
  Center to Federal Way Downtown) and **the 2 Line** (Lynnwood City Center to Downtown Redmond),
  in colors close to Sound Transit's own. They share track from Lynnwood City Center to
  International District/Chinatown.
- Routes and stations come from OpenStreetMap. Pinehurst, opened on September 30, 2026, is
  placed from Sound Transit's own station page until OpenStreetMap carries it.
- Not drawn: the Seattle Streetcar, the T Line in Tacoma, Sounder trains and the airport's SEA
  Underground.
- All 39 stations are drawn, in 11 cities: Seattle, Bellevue, Redmond, Shoreline, SeaTac,
  Kent, Tukwila, Federal Way, Mercer Island, Lynnwood and Mountlake Terrace. Businesses are
  counted inside those cities and, where a ring crosses a city line, in the part of the ring
  beyond it.

**The businesses**

- **Each city's businesses come from whoever publishes them.** Seattle's and Bellevue's own
  business license registers; Public Health – Seattle & King County's food inspections for
  food in every King County city (in Seattle, for what the license register lacks); Snohomish
  County's 2025 list of food establishments for Lynnwood and Mountlake Terrace; and the
  Washington State Liquor and Cannabis Board's list of shops licensed to sell alcohol, outside
  Seattle and Bellevue.
- So **outside Seattle and Bellevue, Retail covers only food shops and shops licensed to sell
  alcohol, and no personal services are shown**: none of the other nine cities publishes them.
  Read the balance between cities as a fact about who publishes what, not about their main
  streets.
- Seattle licenses fall due each December 31, and a license not yet renewed is kept, so some
  shops shown may have closed. A lapsed restaurant license is kept only if King County
  inspected a business of the same name in 2025 or 2026.
- Bellevue's licenses never expire, so its shops and services are shown only from licenses
  issued since 2010. Bellevue's restaurants come from King County's inspections.
- Snohomish County's list dates from 2025 and may not be current.
- Where one business appears in two sources it is counted once, matched on address and name; a
  spelling difference between two sources can leave it counted twice.
- A business licensed under a person's own name shows its category instead of the name.
"""
)

render_map_help("three business categories (Retail, Food service and Personal services)")
render_excluded_stations("Seattle (Regional)")
render_country_links("Seattle (Regional)")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Seattle (Regional)")
