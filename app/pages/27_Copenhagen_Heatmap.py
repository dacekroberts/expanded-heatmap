"""Copenhagen (Regional) heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.copenhagen.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
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

st.set_page_config(page_title="Copenhagen (Regional) Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Copenhagen (Regional)")
render_city_title('Copenhagen (Regional)')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/copenhagen/step3_map.py` to generate it.")

# The snapshot dates, read from outputs/copenhagen/provenance.json so they
# cannot go stale: the CVR weekly generation the join was built on (the six
# entities are one generation; Virksomhed carries Datafordeler's generation
# time) and the date the OSM address-point file was taken (Aarhus's caption).
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _times = sorted(v.get("generation_time") or ""
                        for k, v in (_prov.get("datafordeler") or {}).items()
                        if k.startswith("cvr/") and v.get("generation_time"))
        _points = (((_prov.get("osm") or {}).get("address_points") or {})
                   .get("file_utc") or "")[:10]
        if _times and _points:
            render_caption(f"Business and address data from Datafordeler's weekly "
                       f"extracts, generated **{_times[0][:10]}**; address points "
                       f"from OpenStreetMap, fetched **{_points}**.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# Approved by the owner 2026-09-24, with the partnership and catch-all
# clauses matching the two calls taken that day (DECISIONS.md); set as bullets
# 2026-10-01. Extended 2026-10-07 to the Letbane's eight kommuner and OSM's
# address points (owner); the new sentences are drafts proposals for review
# time (docs/decisions_drafts/worktree-abroad-batch.md).
st.markdown(
    """
**The lines**

- Twelve lines are drawn, **Metro lines M1 to M4, S-tog lines A, B, Bx, C, E, F and H, and
  Hovedstadens Letbane**, the light rail around the city's western suburbs, each labeled on the
  map and in the legend, redrawn from OpenStreetMap's route geometry in the operators' own
  colors. Two S-tog lines, A and F, and the Letbane are shown a shade lighter so they stay
  distinct from the Metro lines whose colors they nearly share.
- S-tog is Copenhagen's suburban rail network, and most maps on this site leave that kind of line
  out. It is drawn here because it runs like a metro, every ten minutes on its own tracks, and
  reaches many districts the Metro does not. Line Bx is the exception: it runs only at peak
  hours, every twenty minutes.
- The map covers the **municipalities of Copenhagen and Frederiksberg** and the **eight suburban
  municipalities the Letbane serves**: Lyngby-Taarbæk, Gladsaxe, Herlev, Rødovre, Glostrup,
  Brøndby, Vallensbæk and Ishøj. Frederiksberg is a separate municipality entirely surrounded by
  Copenhagen, with seven Metro stations of its own, so leaving it out would leave a hole in the
  middle of the map.
- The S-tog lines run further still, out to Køge, Hillerød and Frederikssund. Their stations out
  there are drawn on the line but get no ring, and their businesses are not counted; the same goes
  for the Metro's two airport stations in Tårnby. They are listed below.
- Rødovre has one Letbane stop, at its northwest edge, so only about one of its storefronts in four
  sits within a ring.

**The businesses**

- Businesses come from Denmark's **Central Business Register** (Det Centrale
  Virksomhedsregister, CVR), and specifically from its production units: each place where a
  business operates, recorded at that place's own address rather than its company's.
- Each is placed at its address in Denmark's official address register, Danmarks
  Adresseregister, using the address points OpenStreetMap carries for it. OpenStreetMap lacks
  a few of the register's points, so about one storefront in 600 in Copenhagen and Frederiksberg
  cannot be placed and is missing from the map.
- **Where a business is owned personally (a sole proprietorship, a partnership or any business
  whose registered name marks it as one person's), the map shows its address instead of its
  name**, because such businesses are usually registered under the owners' own names. So does a
  supermarket registered under its franchisee's own name.
- One broad category, *other personal services*, is left out, because most of it is people
  working from their own premises; it also holds the area's tattoo studios, which are therefore
  missing from the map.
- **About nine storefronts in ten sit within a station ring**: nineteen in twenty in Copenhagen
  and Frederiksberg, about two in three in the eight suburban municipalities.

**Reading the density**

- **Read the density as a register, not a street survey.** Some premises are newly registered and
  may not have opened yet.
- Denmark's classification files a web shop under the goods it sells, so some dots are businesses
  with no shop a passer-by could walk into, and nothing in the data says which.
- Against OpenStreetMap's mapped restaurants, cafés and takeaways in Copenhagen and Frederiksberg,
  the register carries about **1.1 times** as many.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Copenhagen (Regional)")
render_country_links('Copenhagen (Regional)')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Copenhagen (Regional)")
