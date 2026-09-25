"""Hong Kong heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Rotterdam's page is its template.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.hong_kong.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Hong Kong Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Hong Kong")

st.title("Hong Kong: commercial density around MTR stations")

# Approved by the owner 2026-09-24; the third paragraph revised the same evening
# when placement moved from address lookups to FEHD's own points.
st.markdown(
    """
Nine lines are drawn — **MTR's Island, Tsuen Wan, Kwun Tong, Tseung Kwan O, South Island, Tung
Chung, Tuen Ma and East Rail lines, and the Light Rail** — each labelled on the map and in the
legend, in MTR's own colours. Their routes and stations come from OpenStreetMap, because MTR
publishes its stations as lists without locations; every line's station count matches MTR's own
list. The Light Rail's twelve routes share one network of track through Tuen Mun, Yuen Long and
Tin Shui Wai, so it is drawn as one line in a colour of this project's choosing, and its stops, a
few hundred metres apart, are thinned to about one per half mile; stops that are also MTR
stations, and each route's ends, are always kept. Not drawn: the Airport Express, the Disneyland
Resort Line, the high-speed rail to the mainland, the Peak Tram, and Hong Kong Tramways, which
runs within a few hundred metres of the Island Line for nearly all its length. Racecourse
station, open only on race days, is left out.

Businesses come from the **Food and Environmental Hygiene Department's licence registers**, which
cover restaurants and food shops but not general retail: a clothes shop, an electronics shop or a
hair salon needs no licence from FEHD. So **this map is mostly restaurants**, and its other two
categories are narrower than elsewhere: **Food shops** (fresh provisions, bakeries, and siu mei
and lo mei shops) and **Bathhouses**. Read the balance between categories as a fact about Hong
Kong's licensing, not about its streets. Food factories, cold stores, factory canteens, swimming
pools, cinemas, karaoke and the funeral trades are licensed too, and are left out. Each dot
carries the shop sign on its licence.

The registers give an address but no location. FEHD publishes the same registers with a location
for each licence on the Government's spatial data portal (CSDI), and this map uses FEHD's own
points, matched to the day's register by licence number; the few licences that have no point
there yet are left off. Premises on different floors of one building share one point, so a tower
of restaurants shows as a stack of dots in one place.

Concentric ring boundaries and the three business categories (Food service, Food shops and
Bathhouses) are toggleable via the layer control in the top left. When enabled, business density
will display as numbered circles summing areas when zoomed out. Zooming in will show individual
dots; hover over those to see further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a statistical density
estimate, so read the colour as "roughly where things cluster."
"""
)

# The snapshot dates, read from outputs/hong_kong/provenance.json so they cannot
# go stale on the next fetch: the registers' own generation date, the latest
# record update in FEHD's point layers, and the OpenStreetMap extract's date.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _gen = max((_prov.get(k) or {}).get("generation_date") or ""
                   for k in ("fehd_restaurants", "fehd_other_food", "fehd_non_food"))
        _pts = max((_prov.get(k) or {}).get("latest_record_update") or ""
                   for k in ("csdi_restaurants", "csdi_other_food", "csdi_non_food"))
        _osm = ((_prov.get("osm_rail") or {}).get("osm_base") or "")[:10]
        _bits = []
        if _gen:
            _bits.append(f"licence registers generated **{_gen}** (FEHD, via DATA.GOV.HK)")
        if _pts:
            _bits.append(f"licence locations updated to **{_pts}** (FEHD, via the CSDI Portal)")
        if _osm:
            _bits.append(f"MTR and Light Rail lines as mapped in OpenStreetMap on **{_osm}**")
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
    st.info("No map yet. Run `python pipeline/hong_kong/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
