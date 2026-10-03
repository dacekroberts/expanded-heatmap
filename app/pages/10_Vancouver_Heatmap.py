"""Vancouver (Regional) heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.

The page name here must match the `name` in app/cities.py
("Vancouver (Regional)"), which render_city_nav() looks up.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.vancouver.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_data_age,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Vancouver (Regional) Heatmap",
                   page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Vancouver (Regional)")
render_city_title('Vancouver (Regional)')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/vancouver/step3_map.py` to generate it.")

render_data_age('Vancouver (Regional)')

st.markdown(
    """
**The lines**

- **This map covers two cities, Vancouver and Surrey.** SkyTrain is regional and Surrey has
  no rail of its own, so a Vancouver-only map would cut the network at a line no rider
  recognizes.
- Of 54 stations, 20 are in Vancouver and 4 in Surrey. The other 30 are in Burnaby,
  Richmond, New Westminster, Coquitlam and Port Moody. They are left out because each of those
  cities' business registers would have to be sourced and verified separately; all 30 are
  listed below.
- **Three lines are drawn** from TransLink's own route geometry, each labeled directly on
  the map and in the legend: the Expo Line, the Millennium Line and the Canada Line, in
  TransLink's own colors.
- The West Coast Express is commuter rail and the SeaBus is a passenger ferry; neither is
  included.

**The businesses**

- Home occupations are excluded - a home business is not a storefront - and in Surrey that
  is about half of the register.
- **Where a license carries no trade name, the pin shows the business type instead of a
  name.** Vancouver leaves the trade name blank on about half of its mappable licenses and
  shows the legal name instead, in parentheses; for a sole proprietor that is a person's own
  name.
- This project publishes public commercial information, not personal information, so those
  labels are replaced rather than the pins removed.
- **Surrey's annual business table carries no dates,** so its rows cannot be dated more
  closely than the year the table covers.

**Reading the map**

- **The two cities are licensed by different authorities, so read them as two measurements
  that share a map rather than one continuous surface.**
- Surrey's four stations reach a far smaller share of its own commerce than Vancouver's
  twenty do, because Surrey's shops sit along arterial roads the SkyTrain does not follow.
- **Known limitation.** Roughly half of Vancouver's current-year licenses carry no
  coordinates at all and cannot be placed. Nearly all are in categories this map excludes
  anyway, but a few have a real street address and are missing.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Vancouver (Regional)")
render_country_links('Vancouver (Regional)')

render_site_notices("Vancouver (Regional)")
