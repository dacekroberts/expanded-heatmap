"""Brno heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py; the text
is the Czech tram template (czech-tram-city section 7), approved by the owner
2026-09-30 word for word, filled with Brno's own figures.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.brno.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Brno Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Brno")
render_city_title('Brno')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/brno/step3_map.py` to generate it.")

# The snapshot dates, read from outputs/brno/provenance.json so they cannot go
# stale on the next fetch: ROS02's own snapshot date, and the calendar window of
# KORDIS's feed, which ships no feed_info.txt (recorded by fetch_sources.py).
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _cal = _prov.get("gtfs_calendar") or {}
        _start, _end = _cal.get("calendar_start", ""), _cal.get("calendar_end", "")
        _snap = _prov.get("ros02_snapshot", "")
        _bits = []
        if _snap:
            _bits.append(f"establishments as of **{_snap}** (ROS02)")
        if _start and _end:
            _bits.append(f"tram timetable data valid **{_start[:4]}-{_start[4:6]}-{_start[6:]}** "
                         f"to **{_end[:4]}-{_end[4:6]}-{_end[6:]}** (KORDIS JMK)")
        if _bits:
            st.caption("Snapshot: " + "; ".join(_bits) + ".")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# The Czech tram template, approved by the owner 2026-09-30. Figures from Brno's
# own build (2026-09-30): 11 lines; 146 stops in the city at a 336 m median gap
# (step 1); the register's 2,110 restaurants against OSM's 1,315 restaurants,
# cafés and takeaways in the city (1.60); 5,932 of 7,200 storefronts in a ring.
st.markdown(
    """
Eleven tram lines are drawn, **DPMB's trams 1 to 10 and 12**, each labelled on
the map and in the legend. The stops come from the IDS JMK timetable data
published by KORDIS JMK, and the lines are shown in the operator's colours; their
routes are drawn from OpenStreetMap, because the timetable data carries none.
Brno has no metro: its trams are its rapid transit, as Riga's are, so every tram
stop gets rings. Buses, trolleybuses and trains are not drawn, nor the heritage
tram H4 or the event shuttle P1.

The map covers the **city of Brno**. Line 2's last two stops, in Modřice beyond
the city boundary, are left out.

Businesses come from the Czech **register of active business establishments**
(ROS02), which records each place where a business operates at that place's own
address, placed using the national address register (RÚIAN), the same sources as
Prague's map. What each establishment does comes from the Czech Statistical
Office's business register (RES). RES records one main activity per business, so
every establishment inherits its owner's, and a chain's office or warehouse
counts as the chain's trade. **Where a business belongs to a person trading in
their own name, or to a partnership, the map shows its address instead of its
name.** Where such an establishment is at the owner's own registered address,
which is usually their home, it is left off the map altogether.

**Read the density as a register, not a street survey.** Some establishments are
newly registered and may not have opened yet. Czechia's classification files a
web shop under the goods it sells, so some dots are businesses with no shop a
passer-by could walk into. Against OpenStreetMap's mapped restaurants, cafés and
takeaways in the city, the register carries about **1.6 times** as many.
Businesses whose main activity is something else, such as a brewery's pub or a
wholesaler's shop, are not shown, because no open source records what each
establishment itself does.

**Tram stops sit closer together than metro stations**, a median of 336 m here,
so the rings are drawn at half the usual size (0.05 to 0.3 mi). **About 82% of
storefronts sit within a ring.**

Concentric ring boundaries and the three business categories (Retail, Food
service and Personal services) are toggleable via the layer control in the top
left. When enabled, business density will display as numbered circles summing
areas when zoomed out. Zooming in will show individual dots; hover over those
to see further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a
statistical density estimate, so read the colour as "roughly where things
cluster."
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_country_links('Brno')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices()
