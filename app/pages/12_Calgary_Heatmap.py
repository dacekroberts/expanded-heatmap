"""Calgary heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern for every city's
detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.calgary.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Calgary Heatmap",
                   page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Calgary")

st.title("Calgary: commercial density around CTrain station areas")

st.markdown(
    """
**Calgary's licence register says which businesses have premises, and no other
city's does.** Its own categories are suffixed with the distinction every other
map here has to infer — `RETAIL DEALER - PREMISES` against `RETAIL DEALER - NO
PREMISES`, and `(MOBILE)`, `(HOME BASED)`, `(MAIL ORDER)` and `(DIRECT SALES)`
alongside them. So the City did most of the classifying, and about two-thirds
of its active licences are storefronts, against roughly a quarter in a typical
register.

**Every CTrain station is inside Calgary**, which makes this the only map on
this site where nothing was excluded for lying in another municipality.
Compare San Diego, which loses 16 of 63 stations, or Washington D.C., which
loses 58 of 98. `outputs/calgary/excluded_stations.csv` exists and is empty.

**Two lines are drawn** from Calgary Transit's own route geometry, in its own
colours: the Red Line and the Blue Line. They share the downtown 7 Avenue
trunk, where eight stations are served by both.

**Read the balance between Food service and Retail with care here.** Food
service is the larger category on this map, which is unusual — and it is a
consequence of how Calgary licenses rather than of what is on the street.
About two in five active licences carry more than one category, most often a
premises licence plus its alcohol or patio endorsements, and where a single
premises is licensed for both retail and food this map counts it as food. A
convenience store with a hot counter lands in Food service.

**Alcohol and patio licences are not counted as businesses.** A restaurant
holding `FOOD SERVICE - PREMISES`, `ALCOHOL BEVERAGE SALES (RESTAURANT)` and
`OUTDOOR PATIO` is one restaurant, not three. Those endorsements are the main
reason so many licences carry several categories.

**A small number of categories are excluded on grounds beyond scope**, and
they are listed with the reasoning on the "What is counted, and what is not"
page — chiefly body rub centres and escort agencies, which are licensed
commercial premises but are left off because mapping them adds exposure for
the people working there without answering the question this project asks.

**Known limitation.** Calgary publishes no usable home-business flag: the
register's `homeoccind` field reads `N` on every single row, so unlike Surrey
or Edmonton the City does not tell us which licences are home-based, and no
inference is attempted. The `(HOME BASED)` and `(MOBILE)` category suffixes
catch the cases the City does mark.

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
    st.info("No map yet. Run `python pipeline/calgary/step3_map.py` to generate it.")

render_site_notices()
