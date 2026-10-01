"""Minneapolis heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.minneapolis.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Minneapolis Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Minneapolis")
render_city_title('Minneapolis')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/minneapolis/step3_map.py` to generate it.")

# The fetch date, read from outputs/minneapolis/provenance.json so it cannot go
# stale on the next fetch (Houston's lesson: as_of_date, not a file timestamp).
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _date = _prov.get("as_of_date")
        if _date:
            st.caption(f"Snapshot: the City of Minneapolis's food inspection data as "
                       f"fetched on **{_date}**.")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

# Written under the owner's pre-approval of this build's prose (2026-09-29); set as
# bullets 2026-10-01.
st.markdown(
    """
**The lines**

- Two lines are drawn: Metro Transit's **METRO Blue Line** (Target Field to the Mall of America, by
  way of the airport) and **METRO Green Line** (Target Field to St. Paul's Union Depot), redrawn
  from OpenStreetMap.
- Rings are drawn only around the stations inside the City of Minneapolis, because the business
  data stops at the city line.
- The Green Line's stations in St. Paul and the Blue Line's at Fort Snelling, the airport and
  Bloomington are left out, and each is listed with its municipality below.
- Buses and the Northstar commuter line are not drawn.

**The businesses**

- **This map shows food businesses only.** They come from the City of Minneapolis's food inspection
  data, which lists every facility the City licenses and inspects for food.
- The map has two layers: **food service** (restaurants, cafés, bars) and **food shops** (grocers,
  convenience stores, butchers, and the one liquor store the data lists).
- No open register of other shops or of personal services covers the city, so clothes shops,
  hairdressers and the like are not on this map.
- A facility is shown when the City inspected it in the two years before the data was fetched; the
  data records no closings, so an inspection is the only sign that a place still trades.
- The data files some other kitchens with the restaurants and shops, so these are left out by name.
  A name rule is imperfect, and a few such kitchens may remain.
- A grocer licensed twice for one counter, once as a grocery and once as a meat market, is shown
  once.
- Inspection results are not shown.
"""
)

render_map_help('business layers')
render_excluded_stations("Minneapolis")
render_country_links('Minneapolis')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices()
