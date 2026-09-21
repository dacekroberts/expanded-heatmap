"""Boston heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.

This page carries more caveats than any other, on purpose: Boston licenses
food and alcohol and almost nothing else, so what the map can and cannot show
is unusually far from what a reader would assume.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.boston.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Boston Heatmap", page_icon="\U0001f5fa️",
                   layout="wide")
set_base_font()

render_city_nav("Boston")

st.title("Boston: commercial density around MBTA rapid-transit station areas")

st.markdown(
    """
**Read this map as food-and-drink density, not general commercial density.**
That is the most important thing to know about it, and it is a fact about
Boston's licensing rather than about Boston's high streets. The city licenses
food and alcohol and essentially no other trade, so those are the businesses
that can be mapped here.

**Personal services is absent, not thin.** There is no hairdresser, barber or
nail salon on this map, and that is not a filter — no such licence exists as
data at any level of government. Massachusetts licenses cosmetology and
barbering at *state* level, through a register that is a per-licence lookup
with no bulk export and no addresses. Boston is the second city here with a
whole category missing for this reason; Philadelphia is the other.

**Retail is narrow.** What is here is retail *food* — groceries, convenience
stores, bodegas — plus package stores and cannabis dispensaries. A clothes
shop, a bookshop or a hardware store needs no licence from any of the three
registries behind this map, so it is simply absent. Read the balance between
the two categories accordingly.

**Three lines of data, assembled.** Food service and retail food come from
Inspectional Services' food-establishment records; package stores come from the
Licensing Board; cannabis dispensaries from its cannabis register. A premises
holding licences from more than one of them is counted once — 27 did, which is
mostly package stores that also hold a food licence.

**Five lines are drawn**, each labelled directly on the map and in the legend:
the Red, Orange, Blue and Green Lines and the Mattapan Trolley. Regional Rail
is a separate system and is not included, as commuter rail is excluded in every
city here.

**Two different kinds of station are missing, and both are listed in
`outputs/boston/excluded_stations.csv` with the reason for each.** 43 stations
were dropped for being in another municipality — the network is regional,
reaching Newton, Brookline, Cambridge, Somerville, Milton, Quincy, Medford,
Revere, Malden and Braintree — and 25 Green Line surface stops were thinned
out. The Green Line is a central subway plus four street-running branches whose
stops sit a block or two apart, so keeping all of them would have merged the
rings into one wash; the central subway stations, each branch's terminals and
every interchange are always kept. The Red, Orange and Blue Lines and the
Mattapan Trolley keep every in-city station.

**One limitation of the privacy screening, stated rather than glossed.** This
project checks whether a published name could be a person's name at their own
home. Boston's addresses carry no apartment or suite designators at all, so
that check has nothing to read here and reports a clean zero — which is a gap
in the measurement, not a proven result. What actually limits the exposure is
the sources: a food-service licence and a package-store licence both require
commercial premises, so a home cannot hold one.

Concentric ring boundaries and the business categories are toggleable via the
layer control in the top left. When enabled, business density displays as
numbered circles summing areas when zoomed out. Zooming in shows individual
dots; hover over those for further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a
statistical density estimate, so read the colour as "roughly where things
cluster."

Rail alignment data provided by MassDOT/MBTA.
"""
)

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/boston/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES.
render_site_notices()
