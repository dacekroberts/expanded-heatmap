"""New York heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview_&_Introduction.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.new_york.config import HEATMAP_HTML  # noqa: E402
from components import render_city_nav, set_base_font  # noqa: E402

st.set_page_config(page_title="New York Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("New York")

st.title("New York: commercial density around MTA rail station areas")

st.markdown(
    """
Every MTA rail station in the five boroughs is included, and none was excluded
for lying outside the city — unlike the other cities here, the network does not
leave its own city. What is drawn is **lines, not services**: the 4, 5 and 6 are
one physical line up Lexington Avenue, so they appear once, grouped the way the
MTA's own map colours them. Each of the eleven — the numbered Manhattan trunks,
the lettered Brooklyn and Queens lines, the three shuttles and the Staten Island
Railway — is labelled directly on the map and in the legend, and a trunk's
branches are drawn wherever its services diverge.

**The station rings are smaller here, and start switched off.** Stations sit a
median 480 m apart, so the half-mile rings used elsewhere would reach past the
next two stations in every direction and merge into one wash over Manhattan.
These rings run to 0.3 mi instead. They still read cleanly around the
outer-borough and Staten Island stations, so they remain available in the layer
control at the top left, along with the three business categories.

**Four registries, because New York has no general business licence.** Food
service comes from the Health Department's restaurant permits, grocery and
bodega retail from the State's retail food store licences, salons and barbers
from the State's appearance-enhancement licences, and a narrow slice of
regulated retail from the city's own Consumer and Worker Protection licences.
No other city here needed more than one source.

That has a consequence worth stating plainly: **the Retail category is less
complete in New York than in the other cities.** A clothing shop or a bookshop
needs no licence from any of these four registries, so it is simply absent,
while restaurants — which every one of which is inspected — are close to fully
covered. Read the balance between categories as a fact about New York's
licensing, not about its high streets. Where one business appears in two
registries it is counted once, matched on address and name; a spelling
difference between two registries can leave it counted twice.

When categories are enabled, density shows as numbered circles that sum areas
when zoomed out. Zooming in reveals individual dots; hover over one for its
details.

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
    st.info("No map yet. Run `python pipeline/new_york/step4_map.py` to generate it.")
