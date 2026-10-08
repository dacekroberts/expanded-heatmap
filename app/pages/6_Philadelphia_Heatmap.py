"""Philadelphia heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.

The prose below says TWO categories, not three, on purpose: Philadelphia has no
Personal services source at all (see pipeline/taxonomies/phl_licensetype.py),
and neither does Boston. This comment used to call Philadelphia "the only city
here" without one, which Boston falsified two cities later - so name the
comparison, never claim uniqueness. If that ever changes, this page and
docs/excluded_categories.md both need updating.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.philadelphia.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Philadelphia Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Philadelphia")
render_city_title('Philadelphia')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/philadelphia/step3_map.py` to generate it.")

render_data_age('Philadelphia')

# The 11th St sentence follows the closed-for-works rule
# (docs/category_rules.md, "Station scope"), in the wording of Sacramento's
# page: name the closure and when it is due back.
st.markdown(
    """
**The lines**

- Every open SEPTA Metro station inside Philadelphia is mapped, across four lines: the
  **Market–Frankford Line** and **Broad Street Line** (with its Ridge Spur), which run
  grade-separated, and the **Subway–Surface Trolleys** and **Girard Avenue Trolley**, which run in
  the street.
- Each is labeled directly on the map and in the legend, and the trolleys' five branches are drawn
  wherever they diverge.
- **11th St on the Market–Frankford Line is not drawn**: SEPTA closed it on September 5, 2026 to
  rebuild it with elevators and expects it back on August 30, 2027. Until then L trains run through
  it without stopping.
- **The two kinds of line are treated differently.** Market–Frankford and Broad Street stations sit
  a median 700 m apart, so every one inside the city is kept.
- The trolleys stop every 130 m or so, closer together than the innermost ring this map draws.
  So they are thinned to roughly one stop per half-mile measured along the track, keeping each
  branch's terminals, the Center City tunnel stations all five share, and every point where a
  trolley meets a subway line.
- Every stop cut this way is listed below, along with the six stations that
  lie outside the city in Upper Darby, Yeadon and Darby.
- Two SEPTA Metro lines are absent because they never enter Philadelphia: the Norristown High Speed
  Line and the Media–Sharon Hill trolleys both begin at 69th Street in Upper Darby.
- Regional Rail is left out as well. Like Metra in Chicago and the LIRR in New York it is commuter
  rail, and SEPTA brands it separately from SEPTA Metro.

**The businesses**

- **Two categories here, not three: Personal services is missing from the data, not just from the
  map.** Philadelphia licenses activities, not businesses, and has no salon, barber or nail license
  of any kind, so, as in Boston, this category has no source to draw on.
- Retail is narrow for a related reason. What the city licenses is food retail, so Retail here
  means bodegas, mini-markets and beer distributors, plus the big-box tier (Target, CVS, Dollar
  Tree, Ross), which appears only because those stores also sell packaged food.
- A clothing shop, bookshop or hardware store needs no license, so it is simply not here; pavement
  newsstands mostly are not either, since the register holds neither a coordinate nor an address
  for them.
- Read the balance between the two categories as a fact about Philadelphia's licensing, not about
  its high streets.
- Where one business holds several licenses (a restaurant with pavement seating holds two), it is
  counted once.
"""
)

render_map_help('two business categories (“Food shops, tire and precious-metal dealers” and Food service)')
render_excluded_stations("Philadelphia")
render_country_links('Philadelphia')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES.
render_site_notices("Philadelphia")
