"""Washington D.C. heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page.

NOTE FOR ANY EDIT TO THE PROSE BELOW: WMATA's Transit Data Terms of Use §6
forbids stating or implying that the data this application provides "is
accurate, complete, or timely", and forbids stating or implying affiliation,
sponsorship or endorsement. MTA's terms carry the identical accuracy clause for
New York. So this page deliberately avoids "accurate", "complete", "current",
"up to date" and "official" - see PLAN.md's deploy gate, which sweeps every
page for the same words.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.washington_dc.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Washington D.C. Heatmap", page_icon="\U0001f5fa️",
                   layout="wide")
set_base_font()

render_city_nav("Washington D.C.")
render_city_title('Washington D.C.')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/washington_dc/step4_map.py` to "
            "generate it.")

render_data_age('Washington D.C.')

st.markdown(
    """
**The businesses**

- **All three categories come from one register here**, which is unusual in this project.
  Washington's Basic Business License register licenses restaurants, shops and salons alike, so
  unlike Boston and Philadelphia, where a whole category had no source at all, this map shows
  retail, food service and personal services from a single file.
- **Most of that register is not a business.** Of the 61,329 active licences inside the District,
  37,195 are residential rentals, and a further 11,074 are "General Business", Washington's default
  category for offices. Both are excluded, leaving about 6,500 licences at roughly 5,200 premises.
  A raw licence count for this city would describe its housing stock, not its high streets.
- **One licence category is genuinely ambiguous, and it is a large one.** Washington issues a
  "Delicatessen" licence to sandwich shops and cafés, and also to corner shops and convenience
  stores. It is counted as food service, which fits most of them, but about 180 premises here hold
  it with no other descriptive licence and could honestly read either way. That is a fact about
  Washington's licence categories, not about its shops.
- **Some pins were placed from their address rather than the register.** The published latitude
  and longitude are unusable (literally 39 and -77 on every row), and the register's real
  coordinates are missing on about 7% of these premises.
- Those were located from their street addresses with the Census Bureau's geocoder: 387 premises,
  each checked to fall inside the District's boundary. 64 could not be placed and are absent.
- **One limitation of the privacy screening, stated rather than glossed.** This project checks
  whether a published name could be a person's name at their own home. Washington's addresses carry
  almost no apartment or suite designators, so that check has little to read and reports zero, a
  gap in the measurement, not a proven result.
- What this city has instead is the register's own record of legal form: 14 pins, 0.36% of the
  map, are a sole proprietorship displaying what reads as a person's name, and each holds a licence
  that requires commercial premises.

**The lines**

- **Six lines are drawn**, each labelled directly on the map and in the legend: the Red, Blue,
  Green, Yellow, Orange and Silver Lines, in the colours WMATA's own schedule data gives them.
- **This is the District, not the Metrorail network.** 58 of Metrorail's 98 stations lie outside
  it (32 in Virginia, 26 in Maryland), each listed with its state below.
- A station in Arlington or Silver Spring would need Virginia's or Maryland's own business data,
  sourced separately.
- All six lines keep a substantial presence inside the District, so none drops out of the map, and
  every in-District station is kept: Metrorail is grade-separated throughout with its stations a
  median 962 m apart, so nothing here needs the thinning Boston's Green Line takes.

Rail alignment data from WMATA's Metrorail GTFS feed.
"""
)

render_map_help('business categories')
render_excluded_stations("Washington D.C.")
render_country_links('Washington D.C.')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES.
render_site_notices()
