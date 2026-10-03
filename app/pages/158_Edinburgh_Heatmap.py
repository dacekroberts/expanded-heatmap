"""Edinburgh heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.edinburgh.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Edinburgh Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Edinburgh")
render_city_title("Edinburgh")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/edinburgh/step3_map.py` to generate it.")

# The snapshot dates, read from outputs/edinburgh/provenance.json so they
# cannot go stale on the next fetch: the council file's own extract date (the
# FSA's condition: say when the information was updated), then the rail's
# fetch date (the tram-city caption). Glasgow's FHIS credit.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _lo, _hi = (_prov.get("fsa_extract_range") or ["", ""])[:2]
        _osm = (_prov.get("osm_fetched_utc") or "")[:10]
        if _lo and _hi:
            _when = f"on **{_lo}**" if _lo == _hi else f"between **{_lo}** and **{_hi}**"
            _rail = f"; the tram line and its stops from OpenStreetMap, fetched **{_osm}**" if _osm else ""
            st.caption(f"Snapshot: food businesses as extracted by the City of Edinburgh Council "
                       f"{_when} (Food Standards Scotland, via the Food Standards Agency){_rail}.")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

# Bullets from the approved templates (Glasgow's FHIS bullets, Newcastle's
# placement bullets; the tram-city line bullets), 2026-10-02. The one-line
# form of the first tram bullet is a proposal (docs/decisions_drafts/uk-six.md).
st.markdown(
    """
**The tram**

- One tram line is drawn, **Edinburgh Trams** from Edinburgh Airport to Newhaven, labeled on the
  map and in the legend, redrawn from OpenStreetMap's route geometry, in a color this project
  chose, since the source records none.
- Trams run about every 7 minutes by day; less often in the evenings.
- Buses and suburban trains are not drawn.
- Edinburgh has no metro, so its trams are its rapid transit, as in Riga. Every tram stop here gets
  rings.
- The map covers the **City of Edinburgh**, the council area; every tram stop is inside it.

**The businesses**

- **This map shows food businesses only.** They come from the City of Edinburgh Council's entries
  in the **Food Hygiene Information Scheme**, Scotland's food hygiene register, run by Food
  Standards Scotland and published through the Food Standards Agency.
- It lists every premises the council inspects: restaurants, cafés, takeaways, pubs and bars, and
  food shops from corner shops to supermarkets.
- No open register of other shops or of personal services covers Edinburgh, so **clothes shops,
  hairdressers and the like are not on this map**.
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
- About one food storefront in twenty-two has neither and is not shown. A business run from a
  private address, or registered at a flat, is never placed.
- **About three storefronts in five sit within a station ring.**
"""
)

render_map_help('business categories (Food service and Food shops)')
render_excluded_stations("Edinburgh")
render_country_links("Edinburgh")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices("Edinburgh")
