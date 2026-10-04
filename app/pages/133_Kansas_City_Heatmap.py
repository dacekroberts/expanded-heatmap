"""Kansas City heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.kansas_city.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_caption,
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Kansas City Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Kansas City")
render_city_title('Kansas City')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/kansas_city/step3_map.py` to generate it.")

# The data dates, read from outputs/kansas_city/provenance.json so they cannot
# go stale: the register's own last update and the date the OSM streetcar file
# was taken.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _reg = (_prov.get("register") or {}).get("data_date") or ""
        _rail = ((_prov.get("files_utc") or {}).get("osm_rail.json") or "")[:10]
        if _reg and _rail:
            render_caption(f"Business license data from the City of Kansas City, Missouri, "
                       f"last updated **{_reg}**; the streetcar line and its stops from "
                       f"OpenStreetMap, fetched **{_rail}**.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# The tram-city skill's page-text template, approved by the owner word for
# word on 2026-09-30 (set as bullets 2026-10-01), filled from Kansas City's own
# step 1 and step 2 figures;
# the business paragraphs follow Houston's, the template city for a US register.
# The frequency is stated as a fact, never cited from RideKC's schedule (the
# brief: RideKC's terms restrict schedules).
st.markdown(
    """
**The streetcar**

- One streetcar line is drawn, the **KC Streetcar**, labeled on the map and in the legend,
  redrawn from OpenStreetMap's route geometry, in a color this project chose, since the source
  records none.
- Kansas City has no metro: its streetcar is its rapid transit, as Riga's trams are, so every stop
  gets rings.
- Streetcars run about every 10 minutes by day, seven days a week. Buses are not drawn.
- The map covers the **City of Kansas City, Missouri**, as the US Census Bureau draws its limits.
  Every streetcar stop is inside it.
- **Streetcar stops sit closer together than metro stations**, a median of 384 m here, so the rings
  are drawn at half the usual size (0.05 to 0.3 mi).

**The businesses**

- Businesses come from the City's list of **business license holders**, each placed at the point
  the City records for it, and kept only if that point falls inside the city.
- **Where the license holder is a person rather than a company, the map shows the street address
  instead of a name**, and so it does where a company trades under a person's own name. Elsewhere
  the map shows the name the business trades under.
- **The license data dates from January 15, 2026**, and holds licenses valid for 2025 and 2026.
  Businesses that opened since then are missing, and any that closed may still be shown.
- **About one storefront in eight sits within a ring.**

**Reading the density**

- **Read the density as a register, not a street survey.** A license is issued to a business at an
  address, and the list does not say whether the address has a shop a passer-by could walk into.
- The industry codes it uses file a web shop under the goods it sells, so some dots are businesses
  with no shop at all, and nothing in the data says which.
- **It holds few restaurants and bars**, about 175 across the whole city, so food service is far
  thinner here than on most maps.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Kansas City")
render_country_links('Kansas City')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Kansas City")
