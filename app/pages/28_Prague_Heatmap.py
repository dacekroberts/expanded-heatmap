"""Prague heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.prague.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Prague Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Prague")

st.title("Prague: commercial density around metro station areas")

# Approved by the owner 2026-09-24.
st.markdown(
    """
Three lines are drawn — **Metro A, B and C** — each labelled on the map and in
the legend, redrawn from the Prague Integrated Transport system's (PID) own route
geometry in the operator's colours. Line A is shown a shade lighter so it stays
distinct from the green of the personal-services dots. **Flora station on line A
is closed for reconstruction** until about December 2026; it is drawn, since the
closure is temporary. Trams, the Petřín funicular, ferries and suburban trains
are not drawn.

The map covers the **City of Prague**, and every metro station lies inside it,
so none is left out.

Businesses come from the Czech **register of active business establishments**
(ROS02), which records each place where a business operates at that place's own
address, placed using the national address register (RÚIAN). What each
establishment does comes from the Czech Statistical Office's business register
(RES). RES records one main activity per business, so every establishment
inherits its owner's, and a chain's office or warehouse counts as the chain's
trade. **Where a business belongs to a person trading in their own name, or to a
partnership, the map shows its address instead of its name.** Where such an
establishment is at the owner's own registered address, which is usually their
home, it is left off the map altogether.

**Read the density as a register, not a street survey.** Some establishments are
newly registered and may not have opened yet. Czechia's classification files a
web shop under the goods it sells, so some dots are businesses with no shop a
passer-by could walk into. Against OpenStreetMap's mapped restaurants, cafés and
takeaways in the city, the register carries about **1.6 times** as many.
Businesses whose main activity is something else, such as a brewery's pub or a
wholesaler's shop, are not shown, because no open source records what each
establishment itself does.

**About seven storefronts in ten sit within a station ring.**

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

# The snapshot dates, read from outputs/prague/provenance.json so they cannot
# go stale on the next fetch: ROS02's own snapshot date, and the window PID's
# feed declares for itself (two weeks, so it moves with every refetch).
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _gtfs = _prov.get("gtfs_feed_info") or {}
        _start, _end = _gtfs.get("feed_start_date", ""), _gtfs.get("feed_end_date", "")
        _snap = _prov.get("ros02_snapshot", "")
        _bits = []
        if _snap:
            _bits.append(f"establishments as of **{_snap}** (ROS02)")
        if _start and _end:
            _bits.append(f"metro timetable data valid **{_start[:4]}-{_start[4:6]}-{_start[6:]}** "
                         f"to **{_end[:4]}-{_end[4:6]}-{_end[6:]}** (PID)")
        if _bits:
            st.caption("Snapshot: " + "; ".join(_bits) + ".")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/prague/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
