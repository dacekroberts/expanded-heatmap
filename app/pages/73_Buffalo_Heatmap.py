"""Buffalo heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.buffalo.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Buffalo Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Buffalo")
render_city_title('Buffalo')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/buffalo/step3_map.py` to generate it.")

# The fetch date, read from outputs/buffalo/provenance.json so it cannot go
# stale: the City's licences are counted if unexpired on it (config.AS_OF_DATE).
if PROVENANCE_JSON.exists():
    try:
        _files = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8")).get("files_utc") or {}
        _taken = (_files.get("city_licences.csv") or "")[:10]
        if _taken:
            st.caption(f"Business licences fetched **{_taken}** and counted if "
                       f"unexpired on that date.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# Approved by the owner 2026-09-29; set as bullets 2026-10-01. Open Data Buffalo's disclaimer (the
# licence read): the pins are never called the City's official records.
st.markdown(
    """
**The line**

- **NFTA Metro Rail**, Buffalo's one light-rail line, is drawn from DL&W, by the waterfront, to
  University. It is labelled on the map and in the legend, and redrawn from OpenStreetMap's route
  geometry in the colour OpenStreetMap records for it.
- All fourteen stations are inside the city, and none is left out.
- The line runs on the surface through the downtown transit mall and mostly in tunnel beyond it.
- **Trains run about every 20 minutes** through the day and evening, by NFTA's published
  timetable, less often than most lines on this site.

**The businesses**

- **Three registers, because Buffalo has no general business licence.** Restaurants, laundries and
  a slice of regulated retail (butchers, used-car and second-hand dealers, pawnbrokers, pet shops,
  tobacco sellers) come from the City's own business licences.
- Grocery, deli and convenience stores come from New York State's retail food store licences, and
  salons and barbers from the State's appearance-enhancement and barber business licences.
- So **the Retail category covers less of the trade than in most cities here**: a clothing shop or
  a bookshop needs none of these licences and is simply absent. Read the balance between categories
  as a fact about Buffalo's licensing, not about its high streets.
- Every licence in the City's file is marked active, including many that expired years ago, so **a
  City licence is counted only if it has not passed its expiry date**.
- The State's two files are placed at their own points and kept only inside the city limits.
- Where one business appears in two registers it is counted once; a grocer that both the City and
  the State license is matched on its street address. A business listed differently in two
  registers can still be counted twice.
- The State's food-store list carries no dates of its own and was last refreshed by the State on
  30 September 2025.
- **A salon licensed under a person's own name shows its licence type instead** (for example
  "Barber shop"), and a salon at an apartment address is left off, as a home.

**Reading the map**

- **About one storefront in four sits within a station ring.** The line runs up Main Street through
  a city of 105 km², and most of the city is beyond walking distance of it.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Buffalo")
render_country_links('Buffalo')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
