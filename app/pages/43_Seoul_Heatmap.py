"""Seoul heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Hong Kong's page is its template.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.seoul.config import (  # noqa: E402
    HEATMAP_HTML, PROVENANCE_JSON, REGISTERS)
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Seoul Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Seoul")
render_city_title("Seoul")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/seoul/step3_map.py` to generate it.")


# The snapshot dates, read from outputs/seoul/provenance.json so they cannot go
# stale on the next fetch: the newest record update across the registers, and
# the OpenStreetMap extract's date.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _upd = max(((_prov.get(k) or {}).get("newest_update") or "")[:10] for k in REGISTERS)
        _osm = ((_prov.get("osm_rail") or {}).get("osm_base") or "")[:10]
        _bits = []
        if _upd:
            _bits.append(f"permit registers updated to **{_upd}** (Seoul Metropolitan "
                         f"Government, via Seoul Open Data Plaza)")
        if _osm:
            _bits.append(f"subway lines and stations as mapped in OpenStreetMap on **{_osm}**")
        if _bits:
            st.caption("Snapshot: " + "; ".join(_bits) + ".")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass


# Prose approved by the owner 2026-09-25, set as bullets 2026-10-01. The whole-city
# heat sentence added 2026-09-25 was removed 2026-09-27, when the layer came
# back (owner).
st.markdown(
    """
**The lines**

- Fifteen lines are drawn, each labeled on the map and in the legend in its operator's colors:
  **Lines 1 to 9, the Shinbundang Line, the Ui LRT and the Sillim Line, and three Korail lines
  signed as part of the subway: the Gyeongui–Jungang, Suin–Bundang and Gyeongchun lines**.
  Line 8's pink is darkened so it stays distinct from the Food service dots.
- Routes and stations come from OpenStreetMap, because Korea's national station dataset carries
  no line routes.
- Businesses are counted around stations inside Seoul only, since the permit registers cover
  Seoul only; the lines are still drawn to their ends beyond the city.
- Not drawn: AREX, GTX-A, the Seohae Line, the Gimpo Goldline and intercity trains. Every station
  they serve inside Seoul is also on a drawn line.

**The businesses**

- From the **Seoul Metropolitan Government's permit registers**, the national licensing records
  Seoul republishes for the whole city: restaurants, cafés and karaoke bars; hair, beauty and
  nail salons, barbers, laundries and public baths; and, for retail, bakeries, butchers, food
  shops, shops licensed to sell tobacco, department stores and marts, and health-food shops.
- Korea licenses these trades rather than retail in general, so a clothes shop, a bookshop or a
  phone shop needs no such permit and is absent: **the Retail category leans toward food and
  convenience stores**. Read the balance between categories as a fact about Korea's licensing,
  not about Seoul's streets.
- Convenience stores and confectioners that hold a café permit are counted as shops.
- A shop holding several permits is counted once per building.
- Each dot carries the name on the permit, in Korean, and its kind in English. Where a registered
  name is a bare personal name at what reads as a home address, the name is withheld.
"""
)

render_map_help("three business categories (Food service, Retail and Personal services)")
render_excluded_stations("Seoul")
render_country_links("Seoul")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
