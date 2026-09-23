"""San Francisco heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided
pattern for every city's detail page.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.san_francisco.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="San Francisco Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("San Francisco")

st.title("San Francisco: commercial density around Muni Metro station areas")

st.markdown(
    """
Stations are represented by blue dots along Muni Metro's six lines (J
Church, K Ingleside, L Taraval, M Ocean View, N Judah, T Third Street -
each labeled directly on the map and in the legend). Every underground
subway station is shown; the street-running stretches of each line are
thinned to roughly one station per half mile (plus each line's terminals
and any transfer points) so the rings stay readable - the excluded
stations are documented in `outputs/san_francisco/excluded_stations.csv`.

**BART and Caltrain are not on this map.** Both are regional rail crossing
county lines, and commuter rail is left out of every city map on this site.
Where BART and Muni Metro share a station, the station is here as the Muni one
it also is — Embarcadero, Montgomery, Powell and Civic Center are all mapped,
as are the Balboa Park and Glen Park interchanges. The F Market heritage
streetcar and the cable cars are out too: a separately branded service, and a
different mode.

Concentric ring boundaries and NAICS-geocoded storefronts are toggleable
via the layer control in the top left. When enabled, business density
will display as numbered circles summing areas when zoomed out. Zooming
in will show individual dots; hover over those to see further details.

Top right: a **Cities** menu and an **All cities** button for moving
between maps, and a light/dark switch. The map opens in whichever mode
the page is using; once you pick one, it carries across the other city
maps.

The heat layer is illustrative. Leaflet applies a visual blur rather than
a statistical density estimate, so read the colour as "roughly where
things cluster."
"""
)

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/san_francisco/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES.
render_site_notices()
