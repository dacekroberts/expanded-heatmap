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
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Vancouver (Regional) Heatmap",
                   page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Vancouver (Regional)")

st.title("Vancouver and Surrey: commercial density around SkyTrain "
         "station areas")

st.markdown(
    """
**This map covers two cities, and that is the first thing to know.** SkyTrain
is regional and Surrey has no rail of its own, so a Vancouver-only map would
cut the network at a line no rider recognises. Of 54 stations, 20 are in
Vancouver and 4 in Surrey; the other 30 are in Burnaby, Richmond, New
Westminster, Coquitlam and Port Moody, whose own business registers would each
have to be sourced and verified separately.
`outputs/vancouver/station_municipalities.csv` records which kept station is
where, and `excluded_stations.csv` names every station left out with the
municipality it sits in.

**Three lines are drawn** from TransLink's own route geometry, each labelled
directly on the map and in the legend: the Expo Line, the Millennium Line and
the Canada Line, in TransLink's own colours. The West Coast Express is commuter
rail and the SeaBus is a passenger ferry; neither is included, matching every
other city here.

**The two cities are licensed by different authorities, so read them as two
measurements that share a map rather than one continuous surface.** Vancouver
records a single business type per licence; Surrey records several per licence
and states whether a business is home-based. Home occupations are excluded - a
home business is not a storefront - and in Surrey that is about half of the
register. Surrey's four stations also reach a far smaller share of its own
commerce than Vancouver's twenty do, because Surrey's shops sit along arterial
roads the SkyTrain does not follow.

**Where a licence carries no trade name, the pin shows the business type
instead of a name.** Vancouver leaves the trade name blank on about half of its
mappable licences and falls back to the legal name, which for a sole proprietor
is a person's own name - the City marks those by wrapping them in parentheses.
This project publishes public commercial information, not personal
information, so those labels are replaced rather than the pins removed.

**Known limitation.** Roughly half of Vancouver's current-year licences carry
no coordinates at all and cannot be placed. They are overwhelmingly categories
this map excludes anyway - long-term and short-term rentals, contractors,
consultancies - but a small remainder have a real street address and are simply
absent. Canada publishes no national geocoder, so there is no equivalent of the
address recovery used for the US cities.

Concentric ring boundaries and the three business categories (Retail, Food
service and Personal services) are toggleable via the layer control in the top
left. When enabled, business density will display as numbered circles summing
areas when zoomed out. Zooming in will show individual dots; hover over those
to see further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a
statistical density estimate, so read the colour as "roughly where things
cluster."
"""
)

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/vancouver/step3_map.py` to generate it.")

render_site_notices()
