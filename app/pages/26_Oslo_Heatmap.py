"""Oslo heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import base64
import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.oslo.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Oslo Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Oslo")

st.title("Oslo: commercial density around T-bane and tram station areas")

st.markdown(
    """
Eleven lines are drawn — **T-bane lines 1 to 5 and tram (trikk) lines 12, 13,
15, 17, 18 and 19** — each labelled on the map and in the legend, redrawn from
Ruter's published route geometry. Ruter's data gives every T-bane line one
colour and every tram line another, so the map uses the per-line colours from
Ruter's own network maps; two are shown a shade lighter so they stay distinct
from each other and from the business dots. Tram 15 runs most of line 12's
route while the Briskeby line is closed for rebuilding and has no published
colour of its own, so the map gives it one.

The map covers the **municipality of Oslo**. The T-bane's western branches run
on into Bærum, so twelve of their stations, out to Kolsås and Østerås, are
drawn on the line but get no ring, and their businesses are not counted. They
are listed in `outputs/oslo/excluded_stations.csv`. Bærum's businesses are in
the same national register this map reads, so leaving them out is a choice
rather than a limit of the data. Ferries are not drawn.

Businesses come from Norway's **Central Coordinating Register for Legal
Entities** (Enhetsregisteret), kept by the Brønnøysund Register Centre, and
specifically from its register of business premises, each recorded at the
address where it operates rather than where its company is registered. Each
premises is placed using Kartverket's official address register. **Where a
business belongs to a sole trader, the map shows its address instead of its
name**, because a sole trader's business is usually registered under the
owner's own name.

**Read the density as a register, not a street survey.** Some premises are
newly registered and may not have opened yet, and Norway's classification files
a web shop under the goods it sells, so some dots are businesses with no shop a
passer-by could walk into; nothing in the data says which. Against
OpenStreetMap's mapped restaurants in the same municipality, this map carries
about **3.3 times** as many, more than the French cities' 1.3 to 1.8. But
restaurants with registered employees alone outnumber OpenStreetMap's two to
one, so much of that gap is OpenStreetMap missing Oslo's restaurants rather
than the register inventing them.

**About three storefronts in four sit within a station ring.** The category
toggles show every storefront; the rings show the share the eleven lines
actually reach.

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

# The snapshot date, read from outputs/oslo/provenance.json so it cannot go
# stale on the next fetch. Entur's feed_info declares NO validity window -
# Toulouse's case, not Rennes' - so the fetch date is the only thing pinning
# the snapshot, and no window is stated because none is published.
if PROVENANCE_JSON.exists():
    try:
        _taken = (json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
                  .get("fetched_utc") or "")[:10]
        if _taken:
            st.caption(f"Transit data from Ruter via Entur, snapshot taken **{_taken}**.")
    except (ValueError, OSError):
        # A malformed provenance file must not take the page down.
        pass

# ENTUR'S SPECIFIED CREDIT, WITH ITS LOGO, beside the data it covers. Entur
# asks for "Data made available by Entur + (logo)"; the owner's call
# (2026-09-24) was to show the logo. The file is Entur's own, unaltered, from
# its RGB logo pack. Entur's rules: the primary (blue) logo on a light
# background, at least 20 px - so it sits on a white chip whatever the page
# theme, and the SVG's 800x400 canvas is drawn 56 px tall because the mark
# fills ~39% of it, putting the visible logo at ~22 px.
_ENTUR_LOGO = Path(__file__).parent.parent / "assets" / "entur" / "Enturlogo_Blue_RGB.svg"
if _ENTUR_LOGO.exists():
    _b64 = base64.b64encode(_ENTUR_LOGO.read_bytes()).decode("ascii")
    st.markdown(
        '<div style="display:flex;align-items:center;gap:10px;margin:0 0 0.6rem">'
        '<span style="background:#ffffff;border-radius:6px;display:inline-flex">'
        f'<img src="data:image/svg+xml;base64,{_b64}" alt="Entur" height="56"></span>'
        '<span style="font-size:0.85rem">Data made available by Entur, under the '
        '<a href="https://data.norge.no/nlod/en/2.0">NLOD</a>.</span></div>',
        unsafe_allow_html=True)

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/oslo/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
