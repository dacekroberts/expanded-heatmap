"""Riga heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Rotterdam's page is its template.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.riga.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Riga Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Riga")

st.title("Riga: commercial density around tram stops")

# Approved by the owner 2026-09-24.
st.markdown(
    """
Seven tram lines are drawn — **Rīgas satiksme's trams 1, 5, 7, 8, 10, 11 and 14** — each labelled
on the map and in the legend, redrawn from Rīgas satiksme's own timetable data. Rīgas satiksme
draws every tram line in the same red, so the colours here are this project's. Trams stop every
400 metres or so, so on each line only about one stop per half mile is drawn as a station;
interchanges and each line's ends are always drawn. Buses, trolleybuses and suburban trains are
not drawn: the suburban lines run every 15 to 30 minutes at best. The map covers the city of Riga,
all 58 neighbourhoods.

Businesses come from two sources, which is why this map has two categories rather than three.
**Food service** is from the State Revenue Service's register of premises licensed to sell alcohol
or tobacco — cafés, bars, restaurants and canteens — placed by address; a café that sells neither
is not in it, so read this layer as a lower bound. These dots show the kind of place and its
street address, never the licence holder. **Shops and services** is from the national cadastre:
every premises registered for trade whose name reads as a shop or a service, placed at its
building. The cadastre records what a premises is for, not who is in it, so a hairdresser and a
clothes shop are one category. Premises in buildings the city lists as degrading are left off.

**Read the shops layer as an upper bound.** The cadastre does not record whether a premises is in
use, and there is no citywide vacancy figure. The city's survey of street-front ground-floor
premises in the historic centre and its protection zone (August–November 2024) counted 20.4% of
2,324 vacant; its own headline for the same survey is that 73% are occupied. A 2025 count of the
Old Town alone found 15% (87 of 573). Vacancy has not been measured anywhere else in the city.

Concentric ring boundaries and the two business categories (Shops and services, and Food service)
are toggleable via the layer control in the top left. When enabled, business density will display
as numbered circles summing areas when zoomed out. Zooming in will show individual dots; hover
over those to see further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a statistical density
estimate, so read the colour as "roughly where things cluster."
"""
)

# The snapshot dates, read from outputs/riga/provenance.json so they cannot go
# stale on the next fetch: the portal's own last-modified date for the excise
# register and the cadastre, and which monthly tram timetable file was read.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _ex = ((_prov.get("excise") or {}).get("last_modified") or "")[:10]
        _pg = ((_prov.get("premise_groups") or {}).get("last_modified") or "")[:10]
        _gt = _prov.get("gtfs") or {}
        _bits = []
        if _ex:
            _bits.append(f"excise licences as published **{_ex}** (VID, via data.gov.lv)")
        if _pg:
            _bits.append(f"cadastre premise groups as published **{_pg}** (VZD, via data.gov.lv)")
        if _gt.get("last_modified"):
            _bits.append(f"tram timetable published **{_gt['last_modified'][:10]}** (Rīgas satiksme)")
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
    st.info("No map yet. Run `python pipeline/riga/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
