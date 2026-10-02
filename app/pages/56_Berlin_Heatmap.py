"""Berlin heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.berlin.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Berlin Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Berlin")
render_city_title('Berlin')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/berlin/step3_map.py` to generate it.")

# The snapshot dates, read from outputs/berlin/provenance.json so they cannot
# go stale on the next fetch: the register's own monthly date (IHK's last
# commit of the file) and the window of VBB's calendar.txt (no feed_info.txt).
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _cal = _prov.get("gtfs_calendar") or {}
        _start, _end = _cal.get("start", ""), _cal.get("end", "")
        _snap = _prov.get("register_date", "")
        _bits = []
        if _snap:
            _bits.append(f"businesses as of **{_snap}** (IHK Berlin, monthly)")
        if _start and _end:
            _bits.append(f"timetable data valid **{_start[:4]}-{_start[4:6]}-{_start[6:]}** "
                         f"to **{_end[:4]}-{_end[4:6]}-{_end[6:]}** (VBB)")
        if _bits:
            st.caption("Snapshot: " + "; ".join(_bits) + ".")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# A courtesy credit, not a licence condition: CC0 asks for none (owner, 2026-09-28).
st.caption("Business data: IHK Berlin (CC0).")

# Approved by the owner 2026-09-28; set as bullets 2026-10-01.
st.markdown(
    """
**The lines**

- Twenty-five lines are drawn — **U-Bahn U1 to U9** and the **S-Bahn's sixteen lines**, the Ring
  (S41 and S42) among them — each labelled on the map and in the legend, redrawn from the
  Berlin-Brandenburg transport association's (VBB) own timetable geometry.
- The colours are close to the operators' but not the same: several S-Bahn lines share one colour
  on the official map, and each line here needs its own.
- **The U6 north of Kurt-Schumacher-Platz is closed for rebuilding** until about August 2027, so
  its five stations to Alt-Tegel are not drawn.
- Trams, regional trains and ferries are not drawn.
- The map covers the **Land of Berlin**. The S-Bahn runs on into Brandenburg; its 36 stations
  there are left out, since the business data stops at the city boundary.

**The businesses**

- Businesses come from the **Berlin Chamber of Industry and Commerce (IHK Berlin)**, which
  publishes its members' business premises as points, each with its economic activity.
- It publishes no names, so each dot is labelled with its kind of business.
- **Craft businesses belong to a different chamber and are not in it**: hairdressers, laundries
  and dry cleaners are almost entirely missing, and bakers and butchers are thin, so Personal
  services shows only part of what is on the street — beauty and nail salons, spas, saunas and
  massage.

**Reading the map**

- **Read the density as a register, not a street survey.** Closures and moves reach the register
  late, and a business can be registered where there is no shop — an office, a business centre or
  a home.
- General non-food retail, mostly traders selling online or at markets, is left off; a web shop
  that names what it sells cannot be told apart from a shop.
- Against OpenStreetMap at four station areas, the register carries about 1.2 to 1.5 times as
  many restaurants, cafés and bars.
- **About eight storefronts in ten sit within a station ring.**
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Berlin")
render_country_links('Berlin')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
