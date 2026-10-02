"""Odense heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.odense.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Odense Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Odense")
render_city_title('Odense')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/odense/step3_map.py` to generate it.")

# The snapshot dates, read from outputs/odense/provenance.json so they cannot
# go stale: the CVR weekly generation the join was built on (the national
# cache Copenhagen fetched), and the dates the OSM tram and address-point
# files were taken.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _times = sorted(v.get("generation_time") or ""
                        for k, v in (_prov.get("datafordeler") or {}).items()
                        if k.startswith("cvr/") and v.get("generation_time"))
        _osm = _prov.get("osm") or {}
        _points = ((_osm.get("address_points") or {}).get("file_utc") or "")[:10]
        _rail = ((_osm.get("rail") or {}).get("file_utc") or "")[:10]
        if _times and _points and _rail:
            st.caption(f"Business and address data from Datafordeler's weekly "
                       f"extracts, generated **{_times[0][:10]}**; address points "
                       f"from OpenStreetMap, fetched **{_points}**; the tram line "
                       f"and its stops from OpenStreetMap, fetched **{_rail}**.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# The tram-city skill's page-text template, approved by the owner word for
# word on 2026-09-30, filled from Odense's own step 1 and step 2 figures; the
# business paragraphs are Aarhus's, the template city for CVR; set as bullets
# 2026-10-01.
st.markdown(
    """
**The tram**

- One tram line is drawn, **Odense Letbane**, labelled on the map and in the legend, redrawn from
  OpenStreetMap's route geometry, in a colour this project chose, since the source records none.
- Buses and regional trains are not drawn.
- Odense has no metro, so its tram is its rapid transit, as in Riga. Every tram stop here gets
  rings.
- **Tram stops sit closer together than metro stations**, a median of 430 m here, so the rings are
  drawn at half the usual size (0.05 to 0.3 mi).
- The map covers the **municipality of Odense**.

**The businesses**

- Businesses come from Denmark's **Central Business Register** (Det Centrale
  Virksomhedsregister, CVR), and specifically from its production units: each place where a
  business operates, recorded at that place's own address rather than its company's.
- Each is placed at its address in Denmark's official address register, Danmarks
  Adresseregister, using the address points OpenStreetMap carries for it.
- **Where a business is owned personally (a sole proprietorship, a partnership or any business
  whose registered name marks it as one person's), the map shows its address instead of its
  name**, because such businesses are usually registered under the owners' own names. So does a
  supermarket registered under its franchisee's own name.
- One broad category, *other personal services*, is left out, because most of it is people
  working from their own premises; it also holds the city's tattoo studios, which are therefore
  missing from the map.
- **About two storefronts in five sit within a ring.**

**Reading the density**

- **Read the density as a register, not a street survey.** Some premises are newly registered and
  may not have opened yet.
- Denmark's classification files a web shop under the goods it sells, so some dots are businesses
  with no shop a passer-by could walk into, and nothing in the data says which.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Odense")
render_country_links('Odense')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
