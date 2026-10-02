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
    render_city_title,
    render_country_links,
    render_data_age,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="San Francisco Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("San Francisco")
render_city_title('San Francisco')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/san_francisco/step3_map.py` to generate it.")

render_data_age('San Francisco')

# The F Market & Wharves added 2026-09-27 (the tram rescope), wording approved
# by the owner; set as bullets 2026-10-01.
st.markdown(
    """
**The lines**

- Stations are represented by blue dots along seven lines: Muni Metro's six (J Church, K Ingleside,
  L Taraval, M Ocean View, N Judah, T Third Street) and the F Market & Wharves streetcar, each
  labeled directly on the map and in the legend.
- Every underground subway station is shown. The street-running stretches of each line are thinned
  to roughly one station per half mile (plus each line's terminals and any transfer points) so the
  rings stay readable; the excluded stations are listed below.
- **BART and Caltrain are not on this map.** Both are regional rail crossing county lines, and
  commuter rail is left out here as on most maps on this site.
- Stations BART shares with Muni Metro are mapped as Muni stations: Embarcadero, Montgomery,
  Powell and Civic Center, and the Balboa Park and Glen Park interchanges.
- The cable cars are out, as a different mode.
- The F Market & Wharves streetcar is drawn, because it runs along the Embarcadero to Fisherman's
  Wharf, which no Muni Metro line reaches. Where it stops directly above a Muni Metro station, the
  two count as one station.

**The businesses**

- Where a business is registered under a person's name alone at an apartment or other dwelling
  unit, the map shows its street address instead of a name.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("San Francisco")
render_country_links('San Francisco')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES.
render_site_notices()
