"""Bergen heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.bergen.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Bergen Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Bergen")
render_city_title('Bergen')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/bergen/step3_map.py` to generate it.")

# The snapshot date, read from outputs/bergen/provenance.json so it cannot go
# stale on the next fetch. Entur's feed_info declares NO validity window -
# Toulouse's case, not Rennes' - so the fetch date is the only thing pinning
# the snapshot, and no window is stated because none is published. Bergen's
# feed and register were cached before this build ran, so the dates are each
# cached FILE's own (provenance "files_utc"), not the provenance run's.
if PROVENANCE_JSON.exists():
    try:
        _files = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8")).get("files_utc") or {}
        _taken = (_files.get("rb_sky-aggregated-gtfs.zip") or "")[:10]
        _register = (_files.get("underenheter.csv.gz") or "")[:10]
        if _taken and _register:
            st.caption(f"Transit data from Skyss via Entur, snapshot taken **{_taken}**; "
                       f"business register downloaded **{_register}**.")
    except (ValueError, OSError, AttributeError):
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

# Approved by the owner 2026-09-29 (Oslo's text, with Bergen's network); set as
# bullets 2026-10-01.
st.markdown(
    """
**The lines**

- Both lines of **Bybanen**, Bergen's light rail, are drawn, **Bybanen 1** (Byparken – Bergen
  Airport Flesland) and **Bybanen 2** (Kaigaten – Fyllingsdalen), each labeled on the map and in
  the legend, redrawn from Skyss's published route geometry.
- Neither Skyss's data nor OpenStreetMap gives the two lines different colors, so line 1 is shown
  in the color OpenStreetMap records for Bybanen and line 2 in a color chosen for this map.
- Ferries are not drawn.
- The map covers the **municipality of Bergen**, which holds every Bybanen stop, the airport
  included.
- Byparken and Kaigaten, the two lines' city-center termini a block apart, are shown as two stops.

**The businesses**

- Businesses come from Norway's **Central Coordinating Register for Legal Entities**
  (Enhetsregisteret), kept by the Brønnøysund Register Centre. They are taken from its register of
  business premises, each recorded at the address where it operates rather than where its company
  is registered.
- Each premises is placed using Kartverket's official address register.
- **Where a business belongs to a sole trader, the map shows its address instead of its name**,
  because a sole trader's business is usually registered under the owner's own name.
- **About three storefronts in five sit within a station ring.** Bybanen runs south from the
  center, and the municipality reaches north to Åsane, where there is no light rail.

**Reading the density**

- **Read the density as a register, not a street survey.** Some premises are newly registered and
  may not have opened yet.
- Norway's classification files a web shop under the goods it sells, so some dots are businesses
  with no shop a passer-by could walk into; nothing in the data says which.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Bergen")
render_country_links('Bergen')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
