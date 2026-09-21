"""Miami heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.

The name carries "(Regional)" because this is the one map here that is not a
single municipality - it must match the `name` in app/cities.py, which
render_city_nav() looks up.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.miami.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Miami (Regional) Heatmap",
                   page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Miami (Regional)")

st.title("Miami-Dade: commercial density around Metrorail and Metromover "
         "station areas")

st.markdown(
    """
**This is the only regional map here, and deliberately so.** Metrorail leaves
the City of Miami — its stations reach Hialeah, Medley, Coral Gables, South
Miami and unincorporated Miami-Dade — and everywhere else in this project that
would end the discussion, because mapping a neighbouring city means sourcing
its business data separately. Miami is the exception: Miami-Dade County
licenses business tax receipts for all 34 of its municipalities in a single
file, so covering the whole line cost nothing extra. Six municipalities hold
stations, every station is on the map, and
`outputs/miami/station_municipalities.csv` records which station is where.

**Three lines are drawn**, each labelled directly on the map and in the legend:
Metrorail, and the Metromover's Inner and Omni/Brickell loops. Metrorail
appears once even though Miami-Dade Transit signs it as two lines, Green and
Orange — its GTFS publishes a single route for both, and inventing a split the
feed does not contain would be worse than using the name every station sign
carries. The MIA Airport People Mover is left out because it runs terminal to
rental-car centre with no surrounding commerce to measure, and Tri-Rail is
commuter rail, excluded here as in every other city. The line colours are this
project's own rather than the agency's: Miami-Dade's own orange and two greens
collide with the business-category colours and with each other.

**The rings are worth turning on selectively here.** They start switched off,
as they do on every city on this site. Metrorail's stations are far apart — a
median 1.1 km — so their rings read cleanly. The Metromover's nineteen sit a
median 235 m apart, and every one of them falls inside a neighbour's outer
ring, so switching the rings on makes downtown one indistinguishable wash while
the Metrorail corridor stays legible. Each business is assigned to its nearest
station either way, so nothing is double-counted.

**The classification is the county's own, because its NAICS column is empty.**
The file carries a `BUSNAICSCD` field and it is null on all 194,099 rows, so
the categories here come from Miami-Dade's `CATGRYNAME` instead — all 150
values of it given an explicit verdict. What that leaves out is worth knowing.
The single largest category in the file, `SERVICE BUSINESS`, is 28,010 rows of
mostly offices, consultancies and agencies, and it is excluded; it does also
contain some genuine trade repair, so **this map undercounts small repair and
service premises in Miami.** Professional practice, apartments, contracting and
wholesale are out for the same reason. The full list and the reasoning are in
`docs/excluded_categories.md`.

One premises can hold several licences at once — a restaurant with an
entertainment permit and a retail licence is three rows in the raw file — so
rows are collapsed to one per premises on name and address, and the more
specific category wins over general retail. Roughly two thousand premises
needed that.

Concentric ring boundaries and the three business categories (Retail, Food
service and Personal services) are toggleable via the layer control in the top
left. When enabled, business density displays as numbered circles summing areas
when zoomed out. Zooming in shows individual dots; hover over those for further
details.

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
    st.info("No map yet. Run `python pipeline/miami/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES.
render_site_notices()
