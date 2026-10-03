"""Sacramento heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.sacramento.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Sacramento Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Sacramento")
render_city_title('Sacramento')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/sacramento/step4_map.py` to generate it.")

# The fetch date, read from outputs/sacramento/provenance.json so it cannot go
# stale: licences are counted if unexpired on it (config.AS_OF_DATE).
if PROVENANCE_JSON.exists():
    try:
        _files = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8")).get("files_utc") or {}
        _taken = (_files.get("business_operation_tax_active.csv") or "")[:10]
        if _taken:
            st.caption(f"Business licenses fetched **{_taken}** and counted if "
                       f"unexpired on that date.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# Approved by the owner 2026-09-29; set as bullets 2026-10-01. The Green Line sentence follows the
# closed-for-works rule (docs/category_rules.md, "Station scope"): name the
# closure and when it is due back.
st.markdown(
    """
**The lines**

- SacRT's **Blue Line** and **Gold Line** are drawn. Each is labeled on the map and in the legend,
  and redrawn from OpenStreetMap's route geometry in the colors OpenStreetMap records for it.
- Both run every 15 minutes through the day and every 30 in the evening, by SacRT's timetables.
- The **Green Line is not drawn**: SacRT suspended it in June 2025 for construction in the
  Railyards and expects it back by mid-October 2026. Its one station of its own, 7th &
  Richards/Township 9, is closed for works until then; its other stops are Blue or Gold stations and
  are on the map.
- The map covers the **City of Sacramento**. The Gold Line runs on to Rancho Cordova and Folsom,
  and both lines reach stops in unincorporated Sacramento County. Those stations are drawn on the
  line but get no ring, and are listed below.
- Downtown the lines run one way on 7th and 8th Streets, so three pairs of stops a block apart, at
  Capitol, County Center and K Street, are each shown as one station.
- Dos Rios, which opened on September 28, 2026 and is not yet in OpenStreetMap, is placed from
  Wikidata.

**The businesses**

- Businesses come from the City's **Business Operation Tax** register, which covers every business
  operating in the city. A license is counted only if it is active and has not passed its expiry
  date.
- The register gives an address but no location, so each storefront is placed by the US Census
  Bureau's geocoder. It is kept only if the point falls inside the city, because a Sacramento
  postal address also covers parts of the unincorporated county. About one address in fifty could
  not be placed.
- Businesses whose address the City withholds ("on file") cannot be placed at all; most are run
  from home.
- **Where a business name reads as a person's, the map shows the kind of business instead** (for
  example "Restaurants"). The register cannot tell a sole proprietor's own name from a trade name,
  so some real trade names are shown that way too.
- A business at an apartment address is left off, as a home.

**Reading the map**

- **About two storefronts in five sit within a station ring.**
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Sacramento")
render_country_links('Sacramento')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Sacramento")
