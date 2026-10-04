"""Brussels heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.brussels.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Brussels Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Brussels")
render_city_title("Brussels")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/brussels/step3_map.py` to generate it.")

# The dates: the survey's own (one survey, every row dated 2025-10-17), and the
# day STIB's feed was fetched, read from outputs/brussels/provenance.json so it
# cannot go stale.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _feed = ((_prov.get("gtfs") or {}).get("file_utc") or "")[:10]
        if _feed:
            st.caption("Shops, restaurants and services from hub.brussels's survey for the City "
                       "of Brussels, dated **2025-10-17**; the metro and tram lines and their "
                       f"stations from STIB-MIVB's open data, fetched **{_feed}**.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# The scaffold's bullets filled in for the City; sentences outside the template
# are flagged in docs/decisions_drafts/belgium.md (the several-types sentence,
# the color sentence, the premetro sentence).
st.markdown(
    """
**The lines**

- STIB's four metro lines, **Metro 1, 2, 5 and 6**, and the fifteen tram lines that run into the
  City, **trams 4, 7, 8, 9, 10, 19, 25, 35, 51, 55, 62, 81, 82, 92 and 93**, are drawn, each
  labeled on the map and in the legend, redrawn from STIB-MIVB's open data in STIB's own colors.
  Five trams are shown a shade lighter or darker, so no two lines look alike.
- Every underground metro and premetro station in the City gets rings, including Anneessens,
  Bourse and Lemonnier, which only trams serve.
- Tram stops sit a few hundred meters apart, so they are thinned to about one per half mile along
  each line; stops shared by two lines, and each line's ends, are kept. The thinned stops are
  listed below.
- **Stations sit close together here**, a median of 377 m among those drawn with rings, so the
  rings are drawn at half the usual size (0.05 to 0.3 mi).
- The map covers the **City of Brussels**, one of the Brussels-Capital Region's 19 communes: the
  Pentagon, the European quarter, Laeken, Neder-Over-Heembeek, Haren and the Avenue Louise.
  Stations in the other 18 communes get no ring and their businesses are not counted; they are
  listed below. The lines are still drawn to their ends.
- Buses and national-rail (SNCB) trains are not drawn.

**The businesses**

- Businesses come from hub.brussels's survey of the City's ground-floor shops, published by the
  City of Brussels: every shop, restaurant, café and salon its field agents recorded, under the
  name on its sign.
- **The survey is dated October 17, 2025**, so shops that opened or closed since then may be
  missing or still shown.
- Empty shop units, hotels, offices, banks, repair shops, gyms, cinemas and the like are left out.
- A shop recorded under several types, a bakery that is also a café for instance, is shown once,
  as Food service if any of its types is, else as Retail, else as Personal services.
- **More than nine storefronts in ten sit within a ring.**
"""
)

render_map_help("three business categories (Retail, Food service and Personal services)")
render_excluded_stations("Brussels")
render_country_links("Brussels")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Brussels")
