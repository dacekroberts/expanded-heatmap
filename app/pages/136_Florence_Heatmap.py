"""Florence heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.florence.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Florence Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Florence")
render_city_title('Florence')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/florence/step3_map.py` to generate it.")

# The fetch dates, read from outputs/florence/provenance.json so they cannot
# go stale: the Comune's layers are updated daily, so the fetch is the date.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _files = _prov.get("files_utc") or {}
        _reg = (_files.get("pubblici_esercizi_od.json") or "")[:10]
        _rail = (_files.get("osm_rail.json") or "")[:10]
        if _reg and _rail:
            st.caption(f"Premises data from the Comune di Firenze (CC BY 4.0), fetched "
                       f"**{_reg}**; the tram lines and their stops from OpenStreetMap, "
                       f"fetched **{_rail}**.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# The tram-city skill's page-text template, approved by the owner word for
# word on 2026-09-30, filled from Florence's own step 1 and step 2 figures;
# set as bullets 2026-10-01. The business paragraphs follow Milan's, the
# template city for a Comune's own registers. No frequency sentence: no
# timetable was read for it.
st.markdown(
    """
**The trams**

- Two tram lines are drawn, **T1 Leonardo and T2 Vespucci**, each labeled on the map and in the
  legend, redrawn from OpenStreetMap's route geometry, in OpenStreetMap's own colors.
- Florence has no metro, so its trams are its rapid transit, as in Riga. Every tram stop here gets
  rings.
- Lines T3 and T4 are under construction and are not drawn. Buses and trains are not drawn.
- **Tram stops sit closer together than metro stations**, a median of 323 m here, so the rings are
  drawn at half the usual size (0.05 to 0.3 mi).
- The map covers the **Comune di Firenze**. T1 runs on into Scandicci, so its 4 stops there are
  left out.
- The line is still drawn to its end, but those stops get no ring and their businesses are not
  counted. They are listed below.

**The businesses**

- **The premises come from four of the Comune's own registers**: shops, food and drink premises,
  hair and beauty businesses, and laundries, each placed at the point the Comune records for it.
- **No register carries a name or an address**, so each dot shows only what kind of business it
  is.
- Several premises often share one building, and each is counted.
- Private clubs, staff shops, online and vending sellers, caterers and restaurants inside hotels
  are left out.

**Reading the density**

- **Read the density as a register, not a street survey.** The food register includes premises
  the regional law exempts from the Comune's requirements, and some of them are not open to the
  public; the register does not say which, so they remain.
- **About three storefronts in eight sit within a ring.**
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Florence")
render_country_links('Florence')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
