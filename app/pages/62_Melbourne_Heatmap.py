"""Melbourne heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.melbourne.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Melbourne Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Melbourne")
render_city_title('Melbourne')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/melbourne/step3_map.py` to generate it.")

# The census year, read from outputs/melbourne/provenance.json so it cannot go
# stale on the next fetch.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _year = _prov.get("clue_year")
        if _year:
            st.caption(f"Snapshot: the City of Melbourne's Census of Land Use and Employment, "
                       f"**{_year}**.")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

# Approved by the owner 2026-09-28; set as bullets 2026-10-01.
st.markdown(
    """
**The lines**

- Six lines are drawn, one for each of Metro Trains' line groups: **Burnley** (the Alamein,
  Belgrave, Glen Waverley and Lilydale lines), **Clifton Hill** (Hurstbridge and Mernda),
  **Northern** (Craigieburn and Upfield), **Cross City** (Werribee, Williamstown and Sandringham),
  **Frankston**, and the **Metro Tunnel** (Sunbury, Cranbourne and Pakenham).
- A group's lines share one track through the city, so each group is drawn once and labelled on
  the map, with its lines named in the legend.
- The colours are close to Metro Trains' but not the same, so they stay distinct from the dot
  colours.
- Metro Trains is suburban rail that runs as a metro through the City Loop and the Metro Tunnel;
  every station in the area is shown.
- **Trams are not drawn.** With them, nearly every storefront would sit within a ring, against 96%
  without them.
- The event-day Flemington Racecourse line, V/Line trains and the City Circle special service are
  not drawn either.

**The area**

- The map covers the **City of Melbourne** council area only: the CBD, Docklands, Southbank,
  Carlton, North Melbourne, Parkville, Kensington and East Melbourne.
- Neighbouring councils publish no comparable census, so they are not on the map.
- Lines are cut at the boundary, and the stations beyond it, Richmond among them, are left out.

**The businesses**

- **The businesses come from the City of Melbourne's Census of Land Use and Employment**, which
  records every business establishment in the area with its trading name and industry class. This
  map uses the **2024** census.
- Points are placed per property, so the shops in a shopping centre or an arcade share one point.
- Shops, food and personal services are all shown, including businesses on upper floors.
- **Nearly all storefronts sit within a station ring**, because the stations are close together
  across a small, dense area.
"""
)

render_map_help('business categories (Retail, Food service and Personal services)')
render_excluded_stations("Melbourne")
render_country_links('Melbourne')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices()
