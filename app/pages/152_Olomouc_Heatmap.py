"""Olomouc heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py; the text
is the Czech tram template (czech-tram-city section 7), approved by the owner
2026-09-30 word for word, filled with this city's own figures.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.olomouc.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Olomouc Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Olomouc")
render_city_title('Olomouc')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/olomouc/step3_map.py` to generate it.")

# The snapshot dates, read from outputs/olomouc/provenance.json so they cannot
# go stale on the next fetch: ROS02's own snapshot date, and when the tram lines
# and stops were fetched from OpenStreetMap.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _snap = _prov.get("ros02_snapshot", "")
        _osm = (_prov.get("osm_fetched") or "")[:10]
        _bits = []
        if _snap:
            _bits.append(f"establishments as of **{_snap}** (ROS02)")
        if _osm:
            _bits.append(f"tram lines and stops from OpenStreetMap, fetched **{_osm}**")
        if _bits:
            st.caption("Snapshot: " + "; ".join(_bits) + ".")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# The Czech tram template, approved by the owner 2026-09-30; set as bullets
# 2026-10-01. Figures from this city's own build (2026-09-30): 7 lines; 36 stops
# at a 316 m median gap; 616 restaurants against OSM's 342 (1.80); 1,742 of 2,235
# storefronts in a ring.
st.markdown(
    """
**The trams**

- Seven tram lines are drawn, **DPMO's trams 1 to 7**, each labelled on the map and in the legend.
- The lines and stops are drawn from OpenStreetMap, and the colours are this project's, because
  none are published for reuse.
- Buses, trolleybuses and trains are not drawn.
- Olomouc has no metro, so its trams are its rapid transit, as in Riga. Every tram stop
  here gets rings.
- **Tram stops sit closer together than metro stations**, a median of 316 m here, so the rings are
  drawn at half the usual size (0.05 to 0.3 mi).
- The map covers the **city of Olomouc**.

**The businesses**

- Businesses come from the Czech **register of active business establishments** (ROS02), which
  records each place a business operates at that place's own address. The national address
  register (RÚIAN) puts each one on the map; Prague's map uses the same two sources.
- What each establishment does comes from the Czech Statistical Office's business register (RES).
  RES records one main activity per business, so every establishment inherits its owner's, and a
  chain's office or warehouse counts as the chain's trade.
- Businesses whose main activity is something else, such as a brewery's pub or a wholesaler's
  shop, are not shown, because no open source records what each establishment itself does.
- **Where a business belongs to a person trading in their own name, or to a partnership, the map
  shows its address instead of its name.** Where such an establishment is at the owner's own
  registered address, which is usually their home, it is left off the map altogether.
- **About 78% of storefronts sit within a ring.**

**Reading the density**

- **Read the density as a register, not a street survey.** Some establishments are newly
  registered and may not have opened yet.
- Czechia's classification files a web shop under the goods it sells, so some dots are businesses
  with no shop a passer-by could walk into.
- Against OpenStreetMap's mapped restaurants, cafés and takeaways in the city, the register carries
  about **1.8 times** as many.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Olomouc")
render_country_links('Olomouc')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices()
