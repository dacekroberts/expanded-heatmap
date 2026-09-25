"""Rotterdam heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Amsterdam's page is its template.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.rotterdam.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Rotterdam Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Rotterdam")

st.title("Rotterdam: commercial density around metro and tram stations")

# Approved by the owner 2026-09-24, with the first paragraph revised the same
# evening once trams 14 and 18 were found to be temporary works services.
st.markdown(
    """
Fourteen lines are drawn — **RET's metro lines A to E and its nine tram lines** — each
labelled on the map and in the legend, redrawn from RET's timetable data as published in the
national feed OVapi compiles, in RET's own colours. Trams 1 and 11, which RET gives one colour,
are shown a shade apart. Trams stop every few hundred metres, so on each tram line's outer
stretches only about one stop per half mile is drawn as a station; metro stations, interchanges
and each line's last stop inside the city are always drawn. Trams 4, 6 and 8 are drawn on their
usual routes: until 22 November they are shortened for works, and temporary trams 14 and 18,
which fill the gap, are not drawn. Tram 12, which runs only on match and event days, ferries and
national-rail (NS) trains are not drawn either.

The map covers the **municipality of Rotterdam**, Hoek van Holland and the port included. The
52 stops outside it, in Schiedam, Vlaardingen, Maassluis, Capelle aan den IJssel, Spijkenisse,
Barendrecht and Albrandswaard and along metro E to The Hague, are left out: the lines that run
on into those places are drawn whole but counted only inside the city, and metro E keeps twelve
of its twenty-three stations.

Businesses come from two sources, which is why this map has two categories rather than three.
**Food service is rebuilt from the city's published decisions.** Rotterdam publishes no register
of hospitality premises, but it announces every hospitality operating permit it grants in its
official gazette, with a point on the map, and a permit runs for five years. So a place is shown
if it was granted one in the five years before this map was made (a coffeeshop, whose permit
runs a year, in the last year). Tested on Amsterdam, which does publish a register, the same
method finds almost every premises and counts about one in seven too many, because a place that
closes stays on until its permit would have run out. These dots carry no name. **Shops and
services** comes from the national buildings register (BAG): every unit whose registered use is
a shop and which is in use. The BAG records what a unit is for, not who is in it, so these dots
show an address rather than a name, and a hairdresser looks the same as a clothes shop. A shop
unit that is also registered as a home is left off, and where a permit and a shop unit are a few
metres apart, the permit is kept.

**Read both layers as upper bounds.** Food service still includes places that have closed since
their permit was granted, and hotels and sports-club canteens hold the same permit and cannot be
told apart. About one Rotterdam shop unit in fourteen was registered as vacant at the start of
2025, by the national statistics office's count, and no open source says which. Takeaways that
need no hospitality permit are thin on the map.

**More than nine storefronts in ten sit within a station ring**, because the trams put a stop
near most streets in the city.

Concentric ring boundaries and the two business categories (Shops and services, and Food
service) are toggleable via the layer control in the top left. When enabled, business density
will display as numbered circles summing areas when zoomed out. Zooming in will show individual
dots; hover over those to see further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a statistical density
estimate, so read the colour as "roughly where things cluster."
"""
)

# The snapshot dates, read from outputs/rotterdam/provenance.json so they cannot
# go stale on the next fetch: the day the permit notices and the BAG units were
# retrieved (both serve their current state), and the window OVapi's national
# feed declares for itself.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _gtfs = _prov.get("gtfs_feed_info") or {}
        _start, _end = _gtfs.get("feed_start_date", ""), _gtfs.get("feed_end_date", "")
        _notices = ((_prov.get("notices") or {}).get("retrieved") or "")[:10]
        _bag = ((_prov.get("bag_units") or {}).get("retrieved") or "")[:10]
        _bits = []
        if _notices:
            _bits.append(f"permit notices published to **{_notices}** (the official gazette, via KOOP)")
        if _bag:
            _bits.append(f"shop units as registered on **{_bag}** (BAG, via PDOK)")
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
    st.info("No map yet. Run `python pipeline/rotterdam/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
