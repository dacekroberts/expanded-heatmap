"""Taichung heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Seoul's page is its template.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.taichung.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Taichung Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Taichung")

st.title("Taichung: commercial density around metro stations")

# Approved by the owner 2026-09-25.
st.markdown(
    """
One line is drawn — **Taichung Metro's Green Line**, from Beitun Main Station to HSR Taichung
Station — labelled on the map and in the legend. Its stations and their names come from Taichung
Metro's own station table, and its route from OpenStreetMap, because the station table carries no
route. Neither source gives the line a colour, so it is drawn in a green of this project's
choosing. Every station is inside the city. Taiwan Railway and high-speed rail services are not
drawn.

Businesses come from Taiwan's **national business tax register** (Fiscal Information Agency),
which lists every trading location — a company's branches as their own rows — with an address and
an industry code. Shops, food service and personal services are read from the code; online sellers
are left out. A company head office registered on an upper floor or in a numbered room is usually
an office rather than a shop, so those rows are left out, except in buildings that hold many
storefronts, such as markets and malls. Brands trading inside a department store are generally
not registered at its address, so a department store tends to appear as a single point. One line
crosses a large city, so most of Taichung's storefronts lie outside the station rings; the
whole-city heat layer shows them all.

The register gives an address but no location. Each address is matched to Taichung's own
door-plate file, which gives every door plate its coordinates; addresses with no door plate — most
often market stalls, stalls in front of a building, and rural addresses — cannot be placed and are
left off. Where a sole proprietor's registered name is not clearly a trade name, the dot shows its
line of business instead: in Taiwan a small business is often registered under its owner's own
name, and the Fiscal Information Agency itself declines to publish owners' names. Names and lines
of business are shown in Chinese, as the register records them.

Concentric ring boundaries and the three business categories (Food service, Retail and Personal
services) are toggleable via the layer control in the top left. When enabled, business density
will display as numbered circles summing areas when zoomed out. Zooming in will show individual
dots; hover over those to see further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a statistical density
estimate, so read the colour as "roughly where things cluster."
"""
)

# The snapshot dates, read from outputs/taichung/provenance.json so they cannot
# go stale on the next fetch: the register's own data date, the door-plate
# file's edition, and the OpenStreetMap extract's date.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _reg = (_prov.get("fia_register") or {}).get("data_date") or ""
        _plates = (_prov.get("doorplates") or {}).get("edition") or ""
        _osm = ((_prov.get("osm_rail") or {}).get("osm_base") or "")[:10]
        _bits = []
        if _reg:
            _bits.append(f"tax register dated **{_reg}** (Fiscal Information Agency)")
        if _plates:
            _bits.append(f"door plates from **{_plates}** (Taichung City Government)")
        if _osm:
            _bits.append(f"the Green Line's route as mapped in OpenStreetMap on **{_osm}**")
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
    st.info("No map yet. Run `python pipeline/taichung/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
