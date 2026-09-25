"""New York heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.

NOTE FOR ANY EDIT TO THE PROSE BELOW: MTA's transit-data terms state "You will
not state or imply that the data you provide through your Application is
accurate, complete, or timely", and WMATA §6 carries the identical clause for
Washington D.C. This page previously said its restaurant coverage was "close to
fully covered" and that Retail was "less complete ... than in the other
cities"; both were reworded on 2026-09-21, the second because it implied the
OTHER eight cities were complete. Describe what a register recorded on a date,
never how much of reality it captures.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.new_york.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="New York Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("New York")

st.title("New York: commercial density around MTA rail station areas")

st.markdown(
    """
Every MTA rail station in the five boroughs is included, and none was excluded
for lying outside the city: the network does not leave it. What is drawn is **lines, not services**: the 4, 5 and 6 are
one physical line up Lexington Avenue, so they appear once, grouped the way the
MTA's own map colours them. Each of the eleven — the numbered Manhattan trunks,
the lettered Brooklyn and Queens lines, the three shuttles and the Staten Island
Railway — is labelled directly on the map and in the legend, and a trunk's
branches are drawn wherever its services diverge.

**The station rings are smaller here.** Stations sit a median 480 m apart, so
the 0.6-mile rings most cities here use would reach past the next two stations in
every direction and merge into one wash over Manhattan. These rings run to
0.3 mi instead. Like every city on this site they start switched off, and they
read most clearly around the outer-borough and Staten Island stations — turn
them on from the layer control at the top left, along with the three business
categories.

**Four registries, because New York has no general business licence.** Food
service comes from the Health Department's restaurant permits, grocery and
bodega retail from the State's retail food store licences, salons and barbers
from the State's appearance-enhancement licences, and a narrow slice of
regulated retail from the city's own Consumer and Worker Protection licences.
Most cities here need only one.

That has a consequence worth stating plainly: **the Retail category here covers
less of the trade than it does in the other cities on this site.** A clothing
shop or a bookshop needs no licence from any of these four registries, so it is
simply absent, while restaurants appear because the city inspects them. Read
the balance between categories as a fact about New York's licensing, not about
its high streets. Where one business appears in two
registries it is counted once, matched on address and name; a spelling
difference between two registries can leave it counted twice.

When categories are enabled, density shows as numbered circles that sum areas
when zoomed out. Zooming in reveals individual dots; hover over one for its
details.

Top right: a **Cities** menu and a **Global View** button for moving between
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

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES.
render_site_notices()
