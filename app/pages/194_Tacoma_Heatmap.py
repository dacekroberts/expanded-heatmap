"""Tacoma heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py, in the
city-page format of 2026-10-01 (owner): title, map, captions, bullets, map help,
country links, notices.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.tacoma.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Tacoma Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Tacoma")
render_city_title("Tacoma")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/tacoma/step3_map.py` to generate it.")

# The tram-city caption from provenance.json: the register with its own date
# and the City's credit (cite data.tacoma.gov, the brief), then the rail's
# fetch date.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _reg = (_prov.get("register") or {}).get("data_last_edit") or ""
        _rail = ((_prov.get("files_utc") or {}).get("osm_rail.json") or "")[:10]
        if _reg and _rail:
            st.caption(f"Business license accounts from the City of Tacoma, Tax & License "
                       f"(data.tacoma.gov), last updated **{_reg}**; the tram line and its stops "
                       f"from OpenStreetMap, fetched **{_rail}**.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# The tram-city skill's page-text template, approved by the owner word for
# word on 2026-09-30, filled from Tacoma's own step 1 and step 2 figures; the
# business bullets follow Kansas City's, the template city for a US register.
# The Sounder clause, the name-rule bullet and the account caveat are
# proposals, approved shortened (owner, 2026-10-04; DECISIONS.md).
st.markdown(
    """
**The tram**

- One Sound Transit tram line is drawn, the **T Line**, labeled on the map and in the legend,
  redrawn from OpenStreetMap's route geometry, in OpenStreetMap's own colors.
- Trams run about every 12 minutes by day; less often in the evenings and on Sundays.
- Buses and suburban trains are not drawn: Sounder's trains to Tacoma run mostly at rush hour.
- Tacoma has no metro, so its tram is its rapid transit, as in Riga. Every tram stop here gets
  rings.
- **Tram stops sit closer together than metro stations**, a median of 451 m here, so the rings
  are drawn at half the usual size (0.05 to 0.3 mi).
- The map covers the **City of Tacoma**, as the US Census Bureau draws its limits. Every stop is
  inside it.

**The businesses**

- Businesses come from the City's list of **active business license accounts**, each placed at
  the point the City records for it, in one of the city's five council districts.
- **Where an account's only name reads as a person's, the map shows its type of business
  instead.**
- A business at an apartment, trailer or mobile-home space is left off as a home.
- **About one storefront in six sits within a ring.**

**Reading the density**

- **Read the density as a register, not a street survey.** The City notes that an active account
  need not hold this year's license, and the list does not show which addresses have a shop front.
- The industry codes it uses file a web shop under the goods it sells, so some dots are businesses
  with no shop at all, and nothing in the data says which.
"""
)

render_map_help("three business categories (Retail, Food service and Personal services)")
render_excluded_stations("Tacoma")
render_country_links("Tacoma")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Tacoma")
