"""Pittsburgh heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.pittsburgh.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_caption,
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Pittsburgh Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Pittsburgh")
render_city_title('Pittsburgh')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/pittsburgh/step3_map.py` to generate it.")

# The list's own date and the fetch date, read from outputs/pittsburgh/
# provenance.json so they cannot go stale on the next fetch.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _reg, _date = _prov.get("register_date"), _prov.get("as_of_date")
        if _reg and _date:
            render_caption(f"Snapshot: the Allegheny County Health Department's food facilities as "
                       f"updated on **{_reg}**, fetched on {_date}.")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

# Written under the owner's pre-approval of this build's prose (2026-09-30); set as
# bullets 2026-10-01.
st.markdown(
    """
**The lines**

- Three lines are drawn: Pittsburgh Regional Transit's light rail, the T - the **PRT Red Line**,
  **PRT Blue Line** and **PRT Silver Line** - redrawn from OpenStreetMap, from their shared
  downtown subway and North Shore stations out to the South Hills.
- The service is light rail, not a metro: the Red Line runs about every 20 minutes, and the Blue
  and Silver Lines for part of the day only.
- Rings are drawn only around the stations inside the City of Pittsburgh, because the business data
  used here stops at the city line; the stations in Dormont, Mount Lebanon, Castle Shannon, Bethel
  Park and South Park are left out, and each is listed with its municipality below.
- Stations here are close together, so the rings are half the usual size, reaching 0.3 miles.
- Buses and the inclines are not drawn.

**The businesses**

- **This map shows food businesses only.** They come from the Allegheny County Health Department's
  list of food facilities, which covers every place the department licenses to serve or sell food.
- The map has two layers: **food service** (restaurants and bars) and **food-selling shops**
  (supermarkets, convenience stores, bakeries and packaged-food shops, including dollar and
  discount stores that sell food).
- No open register of other shops or of personal services covers the city, so clothes shops,
  hairdressers and the like are not on this map, except where they also sell food.
- A facility is shown when the department lists it as active.
- The list files some other kitchens with the restaurants and shops, so these are left out by name.
  A name rule is imperfect, and a few such kitchens may remain.
- Inspection results are not shown.
"""
)

render_map_help('business layers')
render_excluded_stations("Pittsburgh")
render_country_links('Pittsburgh')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices("Pittsburgh")
