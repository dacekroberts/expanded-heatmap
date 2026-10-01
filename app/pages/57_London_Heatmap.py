"""London heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.london.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="London Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("London")
render_city_title('London')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/london/step3_map.py` to generate it.")

# The snapshot dates, read from outputs/london/provenance.json so they cannot
# go stale on the next fetch: the range of the 33 boroughs' own extract dates
# (the FSA's condition: say when the information was updated).
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _lo, _hi = (_prov.get("fsa_extract_range") or ["", ""])[:2]
        if _lo and _hi:
            st.caption(f"Snapshot: food businesses as extracted by each borough between "
                       f"**{_lo}** and **{_hi}** (Food Standards Agency).")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

# Approved by the owner 2026-09-28; set as bullets 2026-10-01.
st.markdown(
    """
**The lines**

- Nineteen lines are drawn — the **Underground's eleven**, the **DLR**, the **Elizabeth line** and
  the **six London Overground lines** — each labelled on the map, with its full name in the legend,
  redrawn from OpenStreetMap.
- The colours are close to TfL's but not the same: some of TfL's colours are too close to the dot
  colours, so the Piccadilly line appears in mauve and the Northern in grey.
- Tramlink, National Rail services and river buses are not drawn.
- The map covers **Greater London**. Lines that run on beyond it are cut at the boundary, and their
  32 stations outside it are left out.

**The businesses**

- **This map shows food businesses only.** They come from the **Food Standards Agency's food
  hygiene register**, which lists every premises a borough inspects: restaurants, cafés,
  takeaways, pubs and bars, and food shops from corner shops to supermarkets.
- No open register of other shops or of personal services covers London, so **clothes shops,
  hairdressers and the like are not on this map**.
- Caterers working from home, mobile traders, and kitchens in schools, hospitals and care homes
  are left out; a workplace canteen registered as a restaurant or café cannot be told apart and
  may appear.
- Names are shown as registered; where a business is registered "trading as" another name, the
  name on the shop is shown.

**Reading the map**

- **Read the density as a register, not a street survey.** A premises stays listed until the
  borough removes it.
- Most premises sit at the register's own map point. Where it gives none, a business with a full
  postcode is placed at the centre of its postcode, usually within a few dozen metres of its door.
- About one food storefront in twenty has neither and is not shown, mostly in outer boroughs. A
  business run from a private address, or registered at a flat, is never placed.
- **About three storefronts in four sit within a station ring.**
"""
)

render_map_help('business categories (Food service and Food shops)')
render_excluded_stations("London")
render_country_links('London')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
