"""Kitchener–Waterloo (Regional) heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.kitchener_waterloo.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Kitchener–Waterloo (Regional) Heatmap", page_icon="\U0001f5fa️",
                   layout="wide")
set_base_font()

render_city_nav("Kitchener–Waterloo (Regional)")
render_city_title('Kitchener–Waterloo (Regional)')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/kitchener_waterloo/step3_map.py` to generate it.")

# The zips' own date, read from outputs/kitchener_waterloo/provenance.json so
# it cannot go stale on the next fetch (Houston's lesson: as_of_date, not a
# file timestamp).
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _date = _prov.get("as_of_date")
        if _date:
            st.caption(f"Snapshot: Region of Waterloo Public Health's inspection data as "
                       f"published on **{_date}**.")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

# Written under the owner's pre-approval of this build's prose (2026-09-30);
# set as bullets 2026-10-01.
st.markdown(
    """
**The line**

- **Two cities, one map.** ION, the Region of Waterloo's light rail (Grand River Transit
  route 301), runs from Conestoga in north Waterloo to Fairway in south Kitchener, redrawn
  from OpenStreetMap with all 19 of its stops: 8 in Waterloo and 11 in Kitchener.
- Through both downtowns the two directions run on parallel streets, so both are drawn, and
  a stop on each side counts as its own.
- ION's bus extension to Cambridge is a bus, and is not drawn.
- Either city alone would be a short map, so this page shows them together; Cambridge and
  the townships are left out.

**The businesses**

- **This map shows food businesses and personal services.** Both come from Region of
  Waterloo Public Health's inspection data, which types every premises it inspects.
- Restaurants, take-outs, bars and snack bars are one layer; food shops (supermarkets,
  convenience stores, bakeries, butchers and produce sellers) are another; hair salons,
  barbers, aesthetics, nail, tattoo, piercing and similar studios are a third.
- The Region publishes no register of other shops, so clothes shops, hardware stores and the
  like are not on this map.
- A premises is shown when Public Health inspected it in the two years before the data's
  date; the data records no closings, so an inspection is the only sign that a place still
  trades. A few premises opened after the data's date and have no type yet; they are shown as
  restaurants, or as personal services.
- Kitchens in schools, daycares, care homes, churches, community centers and workplaces are
  left out by type, and so are caterers without a shop, banquet halls and food warehouses.
- Campus and hospital outlets, arena and stadium stands, clubs, cinemas and other venues,
  hotels, pharmacies, mobile units and the Kitchener Market's Saturday stalls are left out
  by name; a name rule is imperfect.
- Where a personal-services studio is registered under what reads as a person's own name,
  its type is shown instead.
- Inspection results are not shown, and a pin is not a rating.

**Reading the map**

- **About two in five of these premises sit within a station ring.** ION runs along the
  spine of both cities, through both downtowns and past both universities, whose campus
  outlets are not counted.
"""
)

render_map_help('three business layers (Restaurants and bars, Food shops and Personal services)')
render_excluded_stations("Kitchener–Waterloo (Regional)")
render_country_links('Kitchener–Waterloo (Regional)')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices("Kitchener–Waterloo (Regional)")
