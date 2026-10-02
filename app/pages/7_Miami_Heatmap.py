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
    render_city_title,
    render_country_links,
    render_data_age,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Miami (Regional) Heatmap",
                   page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Miami (Regional)")
render_city_title('Miami (Regional)')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/miami/step3_map.py` to generate it.")

render_data_age('Miami (Regional)')

st.markdown(
    """
**The lines**

- **This is a regional map, the site's first.** Metrorail leaves the City of Miami: its stations
  reach Hialeah, Medley, Coral Gables, South Miami and unincorporated Miami-Dade.
- Miami-Dade County licenses business tax receipts for all 34 of its municipalities in a single
  file, so covering the whole line cost nothing extra. Six municipalities hold stations, and every
  station is on the map.
- **Three lines are drawn**, each labeled directly on the map and in the legend: Metrorail, and the
  Metromover's Inner and Omni/Brickell loops.
- Metrorail appears once even though Miami-Dade Transit signs it as two lines, Green and Orange:
  its timetable feed publishes a single route for both, so the map uses the name every station
  sign carries rather than invent a split the feed does not contain.
- The MIA Airport People Mover is left out because it runs terminal to rental-car center with no
  surrounding commerce to measure, and Tri-Rail is commuter rail, left out here as on most maps on
  this site.
- The line colors are this project's own rather than the agency's: Miami-Dade's own orange and two
  greens collide with the business-category colors and with each other.

**The businesses**

- **Businesses are sorted by the county's own categories, because its industry-code (NAICS) column
  is empty.**
- The largest category in the file, "SERVICE BUSINESS" (28,010 rows, mostly offices,
  consultancies and agencies), is excluded. It also holds some genuine trade repair, so **this map
  undercounts small repair and service premises in Miami.** The full list and the reasoning are on
  the "What is counted, and what is not" page.
- One premises can hold several licenses at once (a restaurant with an entertainment permit and a
  retail license is three rows in the raw file), so each premises is counted once, matched on name
  and address, with the more specific category winning over general retail. Roughly two thousand
  premises were merged this way.

**Reading the map**

- **The rings are worth turning on selectively here.** They start switched off, as they do on every
  city on this site.
- Metrorail's stations are far apart, a median 1.1 km, so their rings read cleanly. The
  Metromover's nineteen sit a median 235 m apart, and every one of them falls inside a neighbor's
  outer ring, so switching the rings on makes downtown one indistinguishable wash while the
  Metrorail corridor stays legible.
- Each business is assigned to its nearest station either way, so nothing is double-counted.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Miami (Regional)")
render_country_links('Miami (Regional)')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES.
render_site_notices()
