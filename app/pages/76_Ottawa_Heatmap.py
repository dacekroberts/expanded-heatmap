"""Ottawa heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.ottawa.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Ottawa Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Ottawa")
render_city_title('Ottawa')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/ottawa/step3_map.py` to generate it.")

# The feed's own date, read from outputs/ottawa/provenance.json so it cannot go
# stale on the next fetch (Houston's lesson: as_of_date, not a file timestamp).
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _date = _prov.get("as_of_date")
        if _date:
            st.caption(f"Snapshot: Ottawa Public Health's inspection data as published on "
                       f"**{_date}**.")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

# Written under the owner's pre-approval of this build's prose (2026-09-29);
# set as bullets 2026-10-01.
st.markdown(
    """
**The lines**

- Three lines are drawn: OC Transpo's **O-Train Line 1** (Blair to Tunney's Pasture),
  **Line 2** (Bayview to Limebank) and **Line 4** (South Keys to the Airport), redrawn from
  OpenStreetMap, with all 25 of their stations.
- Every station is inside the City of Ottawa. Buses are not drawn.

**The businesses**

- **This map shows food businesses only.** They come from Ottawa Public Health's food-safety
  inspection data, which lists every premises the health unit inspects.
- The data carries no type for a premises, so **restaurants, cafés, bars and take-outs share
  one layer with food shops**: grocers, convenience stores, bakeries, butchers and pharmacies
  that sell food.
- No open register of other shops or of personal services covers Ottawa, so clothes shops,
  hairdressers and the like are not on this map.
- A premises is shown when the health unit inspected it in the two years before the data's
  date; the data records no closings, so an inspection is the only sign that a place still
  trades.
- Kitchens in schools, daycares, hospitals, care homes, churches, community centres and
  workplaces are left out by name, and so are caterers without a shop, clubs, arenas,
  hotels, food trucks and event vendors. A name rule is imperfect, and a few such kitchens
  may remain.
- Inspection results are not shown.

**Reading the map**

- **About a third of these premises sit within a station ring.** The city is large and
  mostly rural beyond the Greenbelt, and the O-Train serves its core.
"""
)

render_map_help('business layer')
render_excluded_stations("Ottawa")
render_country_links('Ottawa')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices()
