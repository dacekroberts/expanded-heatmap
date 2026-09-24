"""Amsterdam heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.amsterdam.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Amsterdam Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Amsterdam")

st.title("Amsterdam: commercial density around metro and tram stops")

# Approved by the owner 2026-09-24.
st.markdown(
    """
Twenty-one lines are drawn — **GVB's metro lines 50 to 54 and its sixteen tram
lines** — each labelled on the map and in the legend, redrawn from GVB's
timetable data, as published in the national feed OVapi compiles, in GVB's own
colours. Five tram lines are shown a shade lighter or darker, because GVB gives
some lines the same colour (6 and 25, 19 and 29) and a few sit too close to a
metro line to tell apart. Trams stop every few hundred metres, so on each tram
line's outer stretches only about one stop per half mile is drawn as a station;
metro stations, interchanges and each line's last stop inside the city are
always drawn. Tram 3, which runs no service in this timetable period, the museum
tram, ferries and national-rail (NS) trains are not drawn.

The map covers the **municipality of Amsterdam**, Weesp included. The 22 stops
outside it, in Amstelveen, Diemen, Ouder-Amstel and Uithoorn, are left out: the
lines that run on into those places are drawn whole but counted only inside the
city, and tram 6 keeps five of its sixteen stops.

Businesses come from two of the city's own registers, which is why this map has
two categories rather than three. **Food service** is the city's register of
hospitality operating permits: every restaurant, café, lunchroom, snack bar,
coffeeshop and nightclub that holds one, under the name on its permit. **Shops
and services** comes from the national buildings register (BAG): every unit
whose registered use is a shop and which is in use. The BAG records what a unit
is for, not who is in it, so these dots show an address rather than a name, and
a hairdresser looks the same as a clothes shop — the split between retail and
personal services that other cities show is not available here. A shop unit that
is also registered as a home is left off. Where a permit and a shop unit share
an address, the permit is kept, because it names the business.

**Read the shop layer as space set aside for shops, not as open shops.** About
one Amsterdam shop unit in twenty stood empty at the start of 2026, by the city's
own statistics, and no open source says which. Takeaways that need no
hospitality permit are thin on the map, and cafés inside a sports club,
community centre, theatre or hotel are not shown.

**About nineteen storefronts in twenty sit within a station ring**, because the
trams put a stop near almost every street in the city.

Concentric ring boundaries and the two business categories (Shops and services,
and Food service) are toggleable via the layer control in the top left. When
enabled, business density will display as numbered circles summing areas when
zoomed out. Zooming in will show individual dots; hover over those to see
further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a
statistical density estimate, so read the colour as "roughly where things
cluster."
"""
)

# The snapshot dates, read from outputs/amsterdam/provenance.json so they cannot
# go stale on the next fetch: the day the two registers were retrieved (the
# city's API serves the current state, with no date of its own), and the window
# OVapi's national feed declares for itself.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _gtfs = _prov.get("gtfs_feed_info") or {}
        _start, _end = _gtfs.get("feed_start_date", ""), _gtfs.get("feed_end_date", "")
        _snap = _prov.get("permits_snapshot", "")
        _bits = []
        if _snap:
            _bits.append(f"permits and shop units as retrieved on **{_snap}** "
                         f"(city register, BAG)")
        if _start and _end:
            _bits.append(f"metro and tram timetable data valid "
                         f"**{_start[:4]}-{_start[4:6]}-{_start[6:]}** to "
                         f"**{_end[:4]}-{_end[4:6]}-{_end[6:]}** (OVapi)")
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
    st.info("No map yet. Run `python pipeline/amsterdam/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
