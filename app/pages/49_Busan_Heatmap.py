"""Busan heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Seoul's and Daegu's pages are its template.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.busan.config import (  # noqa: E402
    HEATMAP_HTML, PROVENANCE_JSON, REGISTERS)
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

st.set_page_config(page_title="Busan Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Busan")
render_city_title('Busan')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/busan/step3_map.py` to generate it.")

# The snapshot dates, read from outputs/busan/provenance.json so they cannot go
# stale on the next fetch: the newest record update across the permit types and
# the OpenStreetMap extract's date.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _upd = max(((_prov.get(k) or {}).get("newest_update") or "")[:10] for k in REGISTERS)
        _osm = ((_prov.get("osm_rail") or {}).get("osm_base") or "")[:10]
        _bits = []
        if _upd:
            _bits.append(f"permit records updated to **{_upd}** (Busan Metropolitan City, "
                         f"Big-데이터웨이브)")
        if _osm:
            _bits.append(f"subway lines and stations as mapped in OpenStreetMap on **{_osm}**")
        if _bits:
            render_caption("Snapshot: " + "; ".join(_bits) + ".")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# Approved by the owner 2026-09-27; set as bullets 2026-10-01.
st.markdown(
    """
**The lines**

- Five lines are drawn, each labeled on the map and in the legend in the operators' colors:
  **Busan Metro Lines 1 to 4 and the Busan–Gimhae LRT**. Line 4's blue is darkened so it stays
  distinct from the Retail dots, and Line 4 runs on rubber tires (a light metro).
- Routes and stations come from OpenStreetMap, because no transit feed is published.
- Businesses are counted around stations inside Busan only, since the permit data covers Busan
  only; Line 2 and the LRT are still drawn to their ends in Yangsan and Gimhae.
- Not drawn: the Donghae Line (동해선), a Korail commuter line whose stops in Busan are about
  2.3 km apart, and intercity trains. Ten stations served only by the Donghae Line, from Centum
  and Sinhaeundae up the coast to Gijang and Ilgwang, have no ring.

**The businesses**

- From **Busan Metropolitan City's permit data**, the national licensing records the city serves
  for all its districts and its county through its open-data portal: restaurants, cafés and
  karaoke bars; hair, beauty and nail salons, barbers, laundries and public baths; and, for
  retail, bakeries, butchers, food shops, shops licensed to sell tobacco, department stores and
  marts, and health-food shops.
- Korea licenses these trades rather than retail in general, so a clothes shop, a bookshop or a
  phone shop needs no such permit and is absent: **the Retail category leans toward food and
  convenience stores**. Read the balance between categories as a fact about Korea's licensing,
  not about Busan's streets.
- Convenience stores and confectioners that hold a café permit are counted as shops.
- **The data is a snapshot.** The city's feed stopped updating on April 15, 2026, when the
  national licensing data moved to a new service, so permits granted or closed after early April
  2026 are not shown. The snapshot line above gives the date.
- A shop holding several permits is counted once per building.
- Each dot carries the name on the permit, in Korean, and its kind in English. Where a registered
  name is a bare personal name at what reads as a home address, the name is withheld.
"""
)

render_map_help('three business categories (Food service, Retail and Personal services)')
render_excluded_stations("Busan")
render_country_links('Busan')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Busan")
