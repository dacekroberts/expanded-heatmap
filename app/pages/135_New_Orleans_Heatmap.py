"""New Orleans heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.new_orleans.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="New Orleans Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("New Orleans")
render_city_title('New Orleans')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/new_orleans/step3_map.py` to generate it.")

# The data dates, read from outputs/new_orleans/provenance.json so they cannot
# go stale: the register's own last update and the date the OSM file was taken.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _reg = (_prov.get("register") or {}).get("rows_updated") or ""
        _rail = ((_prov.get("files_utc") or {}).get("osm_rail.json") or "")[:10]
        if _reg and _rail:
            st.caption(f"Occupational licence data from the City of New Orleans, updated "
                       f"**{_reg}**; the streetcar lines and their stops from "
                       f"OpenStreetMap, fetched **{_rail}**.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# The tram-city skill's page-text template, approved by the owner word for
# word on 2026-09-30 (set as bullets 2026-10-01), filled from New Orleans's own
# step 1 and step 2 figures.
# The lines are the five RTA runs (owner, 2026-09-30, re-taken at build). No
# frequency sentence: the brief's figure was search-level and is unverified.
st.markdown(
    """
**The streetcars**

- Five RTA streetcar lines are drawn, **St. Charles (12), Loyola/Rampart (46), Canal–Cemeteries
  (47), Canal–City Park/Museum (48) and Riverfront (49)**, each labelled on the map and in the
  legend, redrawn from OpenStreetMap's route geometry.
- New Orleans has no metro: its streetcars are its rapid transit, as Riga's trams are, so every
  streetcar stop gets rings. Buses and ferries are not drawn.
- The map covers the **City of New Orleans**, which is Orleans Parish, as the US Census Bureau
  draws its limits. Every streetcar stop is inside it.
- **Tram stops sit closer together than metro stations**, a median of 186 m here, so the rings are
  drawn at half the usual size (0.05 to 0.3 mi).

**The businesses**

- Businesses come from the City's list of **active occupational licences**, each placed at the
  point the City records for it; about one in twenty-three has no point and cannot be placed.
- **The map shows the business name the licence gives, never the owner's**; where a licence gives
  no business name, or the name is only a person's, it shows the street address.
- Personal services are thin on this map: 219 of the pins near stations are salons, barbers and the
  like, against 941 shops and 980 food businesses, and the City's catch-all "Personal Services,
  Other" (249 licences) is left out because it does not say what a business does.

**Reading the density**

- **Read the density as a register, not a street survey.** A licence is issued to a business at an
  address, and the list does not say whether the address has a shop a passer-by could walk into.
- **About nine storefronts in twenty sit within a ring.** Streetcar stops here stand a block or two
  apart, so the rings join into a band along each line. Read them as distance from the line.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_country_links('New Orleans')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
