"""Houston heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.houston.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Houston Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Houston")
render_city_title('Houston')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/houston/step4_map.py` to generate it.")

# The fetch date, read from outputs/houston/provenance.json so it cannot go
# stale: permits count if the outlet had begun trading by it (config.AS_OF_DATE).
# as_of_date, not the file's UTC timestamp: the fetch ran on the evening of
# 2026-09-29 in Houston, after midnight UTC, and the timestamp read 2026-09-30
# while step 2 applied 2026-09-29 (deploy-verify, 2026-09-29).
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _files = _prov.get("files_utc") or {}
        _taken = (_prov.get("as_of_date")
                  or (_files.get("sales_tax_permits_houston.csv") or "")[:10])
        if _taken:
            st.caption(f"Sales tax permits fetched **{_taken}**.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# Pre-approved by the owner 2026-09-29 ("same with the eventual write-ups").
# The in-ring share is stated on the page (owner, 2026-09-29: build as scoped
# and say so).
st.markdown(
    """
METRORail's **Red Line**, **Green Line** and **Purple Line** are drawn. Each is
labelled on the map and in the legend, and redrawn from OpenStreetMap's route
geometry in this map's own colours. The Red Line runs every 6 minutes through the
day, and the Green and Purple Lines every 12. All 40 stations are inside the City
of Houston, so none is left out. Downtown the Green and Purple Lines run one way
on Capitol and Rusk Streets, so Central Station's two stops a block apart are
shown as one station.

The map covers the **City of Houston**, as the US Census Bureau draws its limits:
about 1,740 km² from Kingwood to Clear Lake. Three light-rail lines serve its
core, so **only about one storefront in thirteen sits within a station ring**,
far fewer than in most cities on this map. The toggle for all of Houston shows
the rest.

Businesses come from the Texas Comptroller's list of **active sales tax permit
holders**: every outlet selling taxable goods in the state, with its industry
code. Only outlets in Houston are used, and a permit counts only if the outlet
had begun trading by the date it was fetched. The list gives an address but no
location, so each storefront is placed at the matching point in the City of
Houston's own address file, or by the US Census Bureau's geocoder where there is
no match. It is kept only if the point falls inside the city, because a Houston
postal address also covers other towns and unincorporated land. About one address
in twenty-five could not be placed.

**Where the permit holder is a person rather than a company, the map shows the
street address instead of a name.** That covers sole owners and partnerships of
individuals. Such a business is left off altogether where the City's address
file records the point as residential, and so is any business at an apartment or
trailer address, as a home.

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

render_map_help('three business categories (Retail, Food service and Personal services)')
render_country_links('Houston')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
