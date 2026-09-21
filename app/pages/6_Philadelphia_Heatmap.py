"""Philadelphia heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview_&_Introduction.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.

The prose below says TWO categories, not three, on purpose: Philadelphia is the
only city here with no Personal services source at all (see
pipeline/taxonomies/phl_licensetype.py). If that ever changes, this page and
docs/excluded_categories.md both need updating.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.philadelphia.config import HEATMAP_HTML  # noqa: E402
from components import render_city_nav, set_base_font  # noqa: E402

st.set_page_config(page_title="Philadelphia Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Philadelphia")

st.title("Philadelphia: commercial density around SEPTA Metro station areas")

st.markdown(
    """
Every SEPTA Metro station inside Philadelphia is mapped, across four lines: the
**Market–Frankford Line** and **Broad Street Line** (with its Ridge Spur),
which run grade-separated, and the **Subway–Surface Trolleys** and **Girard
Avenue Trolley**, which run in the street. Each is labelled directly on the map
and in the legend, and the trolleys' five branches are drawn wherever they
diverge.

**The two kinds of line are treated differently, because they are different
kinds of line.** Market–Frankford and Broad Street stations sit a median 700 m
apart, so every one inside the city is kept. The trolleys stop every 130 m or
so — closer together than the innermost ring this map draws — so they are
thinned to roughly one stop per half-mile measured along the track, keeping
each branch's terminals, the Center City tunnel stations all five share, and
every point where a trolley meets a subway line. Every stop cut this way is
listed in `outputs/philadelphia/excluded_stations.csv`, along with the six
stations that lie outside the city in Upper Darby, Yeadon and Darby.

Two SEPTA Metro lines are absent because they never enter Philadelphia: the
Norristown High Speed Line and the Media–Sharon Hill trolleys both begin at
69th Street in Upper Darby. Regional Rail is left out as well — like Metra in
Chicago and the LIRR in New York it is commuter rail, and SEPTA brands it
separately from SEPTA Metro.

**Two categories here, not three, and the missing one is missing from the data
rather than from the map.** Philadelphia licenses activities, not businesses,
and there is no salon, barber or nail licence of any kind; Pennsylvania
publishes its cosmetology licensees only as county totals with no addresses. So
**Personal services is absent entirely** — the only city here where a whole
category has no source to draw on.

Retail is narrow for a related reason. What the city licenses is food retail, so
Retail here means bodegas, mini-markets and beer distributors, plus the big-box
tier — Target, CVS, Dollar Tree, Ross — which appears only because those stores
also sell packaged food. A clothing shop, bookshop or hardware store needs no
licence, so it is simply not here; pavement newsstands mostly are not either,
since the register holds neither a coordinate nor an address for them. Read the
balance between the two categories as a fact about Philadelphia's licensing, not
about its high streets. Where one business holds several licences — a restaurant
with pavement seating holds two — it is counted once.

Ring boundaries and both business categories are toggleable via the layer
control at the top left. When categories are enabled, density shows as numbered
circles that sum areas when zoomed out; zooming in reveals individual dots, and
hovering over one gives its details.

Top right: a **Cities** menu and an **All cities** button for moving between
maps, and a light/dark switch. The map opens in whichever mode the page is
using; once you pick one, it carries across the other city maps.

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
    st.info("No map yet. Run `python pipeline/philadelphia/step3_map.py` to generate it.")
