"""Dallas heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.dallas.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Dallas Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Dallas")

st.title("Dallas: commercial density around DART light rail stations")

# Houston's text (pre-approved by the owner 2026-09-29), with Dallas's facts;
# written under the owner's pre-approval of this build's prose (2026-09-30).
# Two sentences beyond Houston's template, flagged for review time: the
# timetable (the brief: purpose-built track, so frequency is disclosed) and the
# thin personal-services layer (owner, 2026-09-30: narrowed, and the page says
# why). The in-ring share is stated on the page, as Houston's is.
st.markdown(
    """
DART's four light-rail lines are drawn: the **Red Line**, **Blue Line**, **Green
Line** and **Orange Line**. Each is labelled on the map and in the legend, and
redrawn from OpenStreetMap's route geometry in this map's own colours. Each line
runs about every 20 minutes at peak and every 20 to 30 minutes at other times;
downtown, where all four share the transit mall, trains come more often. 44
stations are inside the City of Dallas; the 20 beyond it, in the suburbs and at
DFW Airport, are left out and the lines are drawn to their ends. The Dallas
Streetcar and the M-Line trolley are not drawn, and neither are the Silver Line
and the TRE, which are commuter rail.

The map covers the **City of Dallas**, as the US Census Bureau draws its limits:
about 990 km². Four light-rail lines radiate from downtown, so **about one
storefront in four sits within a station ring**. The toggle for all of Dallas
shows the rest.

Businesses come from the Texas Comptroller's list of **active sales tax permit
holders**: every outlet selling taxable goods in the state, with its industry
code. Only outlets in Dallas are used, and a permit counts only if the outlet
had begun trading by the date it was fetched. Texas taxes only some services, so
many personal-service businesses, such as hair salons and barbers, hold no permit
and do not appear. The list gives an address but no location, so each storefront
is placed at the matching point in the City of Dallas's own address points (or
the nearest listed number on the same side of the street), or by the US Census
Bureau's geocoder where there is no match. The placement is approximate, not
surveyed. It is kept only if the point falls inside the city, because a Dallas
postal address also covers other towns. About one address in forty could not be
placed.

**Where the permit holder is a person rather than a company, the map shows the
street address instead of a name.** That covers sole owners and partnerships of
individuals. A business at an apartment or trailer address is left off
altogether, as a home.

Online and mail-order sellers are left out by their industry code, as are
caterers, food trucks, contract canteens, parking, funeral services and the
catch-all "other personal services".

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

# The fetch date, read from outputs/dallas/provenance.json so it cannot go
# stale: permits count if the outlet had begun trading by it (config.AS_OF_DATE).
if PROVENANCE_JSON.exists():
    try:
        _files = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8")).get("files_utc") or {}
        _taken = (_files.get("sales_tax_permits_dallas.csv") or "")[:10]
        if _taken:
            st.caption(f"Sales tax permits fetched **{_taken}**.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/dallas/step4_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
