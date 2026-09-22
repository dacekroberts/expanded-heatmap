"""Toronto heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.toronto.config import HEATMAP_HTML  # noqa: E402
from components import render_city_nav, set_base_font  # noqa: E402

st.set_page_config(page_title="Toronto Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Toronto")

st.title("Toronto: commercial density around TTC subway and LRT station areas")

st.markdown(
    """
**Toronto licenses food and trades, but not general retail — and that is the
one thing to know before reading this map.** There is no grocer, clothing shop,
pharmacy or hardware store here, because the City requires no licence for any
of them, so none appears in any register to map. What the Retail category holds
instead is the *regulated* slice: second-hand shops, pawn shops, precious-metal
buyers, smoke and vape shops, pet shops and fireworks vendors — the trades a
city licenses because it wants to watch them. **Read the balance between the
three categories as a fact about Toronto's licensing, not about its high
streets.** Food service is close to fully covered; Retail is a narrow slice of
what is actually on the street.

**This register has no coordinates at all — not one row.** Toronto is the only
city on this site whose addresses had to be matched against a separate
address-point layer to be placed on a map, because Canada has no national
geocoding service the way the United States does. The City's own One Address
Repository supplied the coordinates, and about one storefront in sixteen could
not be matched — mostly plazas and malls the repository does not carry as a
single address, so a few shopping centres are under-counted rather than any
district being missed.

**Five lines are drawn** from the TTC's own route geometry: Lines 1, 2 and 4 of
the subway, and Lines 5 and 6, which are light rail. Four of the five use the
TTC's own colours; Line 2's green was darkened because the agency's green is
almost exactly the green used for Personal services pins, and the two were
indistinguishable where a line ran under its own stations. **The 18 streetcar
routes are not included** — they run in traffic every block or two, and adding
them would quadruple the station count and change what this map is about.

**Two stations are missing on purpose.** Line 1 continues past the city limit
into York Region, so Highway 407 and Vaughan Metropolitan Centre sit outside
Toronto and outside this map; they are listed in
`outputs/toronto/excluded_stations.csv`. Everything else the TTC signs as a
rapid-transit station is here.

**Cancelled licences are excluded, and most of the register is cancelled.**
This is a licence history going back two decades rather than a snapshot, so
roughly three rows in four record a licence that has already ended. Only
current ones are mapped.

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
    st.info("No map yet. Run `python pipeline/toronto/step4_map.py` to generate it.")
