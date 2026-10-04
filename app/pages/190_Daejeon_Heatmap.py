"""Daejeon heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.daejeon.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Daejeon Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Daejeon")
render_city_title("Daejeon")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/daejeon/step3_map.py` to generate it.")

# The register's edition, read from outputs/daejeon/provenance.json so it
# cannot go stale on the next fetch.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _ed = (_prov.get("semas") or {}).get("edition")
        if _ed:
            st.caption(f"Snapshot: the Small Enterprise and Market Service's storefront "
                       f"register, edition of **{_ed}**.")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

# Bucheon's text (approved by the owner 2026-09-29), with Daejeon's line; written
# under the owner's pre-approval of this build's prose (2026-09-30). The
# not-drawn bullet was a proposal, approved (owner, 2026-10-04; DECISIONS.md).
st.markdown(
    """
**The lines**

- One line is drawn, labeled on the map and in the legend in the operator's color:
  **Line 1** of the Daejeon Metro.
- Routes and stations come from OpenStreetMap.
- Every station of Line 1 is inside Daejeon.
- Not drawn: Line 2, a tram still under construction, and Korail's intercity lines.

**The businesses**

- From the **Small Enterprise and Market Service's commercial-district register**
  (소상공인시장진흥공단 상가(상권)정보), a national record of trading storefronts with a map
  position for every one: restaurants, cafés and bars; shops of every kind, from convenience
  stores and supermarkets to clothing, phones and pharmacies; and hair, nail and skin-care
  salons, laundries, bathhouses and massage.
- This national register is a different kind of record from the city license data behind
  Seoul's, Daegu's and Busan's maps, which count only licensed trades. So **Daejeon's Retail
  category is complete where those cities' is thin**, and density is not directly comparable
  between them.
- Each dot carries the storefront's name, in Korean, with its branch where it has one, and its
  kind in English. Where a registered name is a bare personal name at what reads as a home
  address, the name is withheld.
- The whole city is included; storefronts beyond walking distance of a station add to the
  all-city layer and nothing to the rings.
"""
)

render_map_help('three business categories (Food service, Retail and Personal services)')
render_excluded_stations("Daejeon")
render_country_links('Daejeon')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices("Daejeon")
