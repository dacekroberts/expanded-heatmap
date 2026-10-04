"""Liverpool (Regional) heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.liverpool.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Liverpool (Regional) Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Liverpool (Regional)")
render_city_title("Liverpool (Regional)")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/liverpool/step3_map.py` to generate it.")

# The snapshot dates, read from outputs/liverpool/provenance.json so they
# cannot go stale on the next fetch: the four councils' own extract dates (the
# FSA's condition: say when the information was updated), then the rail's
# fetch date.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _lo, _hi = (_prov.get("fsa_extract_range") or ["", ""])[:2]
        _osm = (_prov.get("osm_fetched_utc") or "")[:10]
        if _lo and _hi:
            _when = f"on **{_lo}**" if _lo == _hi else f"between **{_lo}** and **{_hi}**"
            _rail = f"; the Merseyrail lines and stations from OpenStreetMap, fetched **{_osm}**" if _osm else ""
            st.caption(f"Snapshot: food businesses as extracted by each council {_when} "
                       f"(Food Standards Agency){_rail}.")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

# Bullets from the approved templates (the UK six's FSA bullets, London's
# colors bullet), 2026-10-04. The commuter-rail, evening and City Line
# bullets were proposals, approved shortened (owner, 2026-10-04; DECISIONS.md).
st.markdown(
    """
**The lines**

- Two Merseyrail lines are drawn, the **Northern Line** (Southport, Ormskirk and Headbolt Lane
  to Hunts Cross) and the **Wirral Line** (West Kirby, New Brighton, Chester and Ellesmere Port
  to the loop under Liverpool's center), each labeled on the map and in the legend, redrawn from
  OpenStreetMap.
- The colors are close to Merseyrail's but not the same: both are adjusted to stay clear of the
  dot colors.
- Merseyrail is suburban rail run like a metro: by day every station has a train at least every
  15 minutes, so all are shown.
- In the evening and on Sundays most stations have a train every 30 minutes.
- Northern's City Line from Lime Street runs too seldom to be drawn. Other national rail, buses
  and the Mersey Ferries are not drawn either.
- The map covers the four council areas Merseyrail serves: **Liverpool, Sefton, Knowsley and
  Wirral**. The lines run on to Ormskirk, Chester and Ellesmere Port, and the 10 stations beyond
  the four are listed below.

**The businesses**

- **This map shows food businesses only.** They come from the **Food Standards Agency's food
  hygiene register**, which lists every premises a council inspects: restaurants, cafés,
  takeaways, pubs and bars, and food shops from corner shops to supermarkets.
- No open register of other shops or of personal services covers these council areas, so
  **clothes shops, hairdressers and the like are not on this map**.
- Caterers working from home, mobile traders, and kitchens in schools, hospitals and care homes
  are left out; a workplace canteen registered as a restaurant or café cannot be told apart and
  may appear.
- Names are shown as registered; where a business is registered "trading as" another name, the
  name on the shop is shown.

**Reading the map**

- **Read the density as a register, not a street survey.** A premises stays listed until the
  council removes it.
- Most premises sit at the register's own map point. Where it gives none, a business with a full
  postcode is placed at the center of its postcode, usually within a few dozen meters of its door.
- About one food storefront in thirty has neither and is not shown. A business run from a
  private address, or registered at a flat, is never placed.
- **About half of the storefronts sit within a ring.**
"""
)

render_map_help('business categories (Food service and Food shops)')
render_excluded_stations("Liverpool (Regional)")
render_country_links("Liverpool (Regional)")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Liverpool (Regional)")
