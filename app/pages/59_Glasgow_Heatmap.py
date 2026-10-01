"""Glasgow heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.glasgow.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Glasgow Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Glasgow")
render_city_title('Glasgow')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/glasgow/step3_map.py` to generate it.")

# The snapshot date, read from outputs/glasgow/provenance.json so it cannot go
# stale on the next fetch: the council file's own extract date (the FSA's
# condition: say when the information was updated).
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _date = _prov.get("fsa_extract_date")
        if _date:
            st.caption(f"Snapshot: food businesses as extracted by Glasgow City Council on "
                       f"**{_date}** (Food Standards Scotland, via the Food Standards Agency).")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

# Approved by the owner 2026-09-28.
st.markdown(
    """
One line is drawn: the **Glasgow Subway**, the 15-station loop through the city
centre, the West End and the south side, redrawn from OpenStreetMap in SPT's
orange. Its two tunnels, the Outer and Inner Circle, are drawn as one line.
Glasgow's suburban and national rail lines are not drawn.

The map covers **Glasgow City**, the council area; the Subway lies wholly
inside it.

**This map shows food businesses only.** They come from Glasgow City Council's
entries in the **Food Hygiene Information Scheme**, Scotland's food hygiene
register, run by Food Standards Scotland and published through the Food
Standards Agency. It lists every premises the council inspects: restaurants,
cafés, takeaways, pubs and bars, and food shops from corner shops to
supermarkets. No open register of other shops or of personal services covers
Glasgow, so **clothes shops, hairdressers and the like are not on this map**.
Caterers working from home, mobile traders, and kitchens in schools, hospitals
and care homes are left out; a workplace canteen registered as a restaurant or
café cannot be told apart and may appear.

**Read the density as a register, not a street survey.** A premises stays
listed until the council removes it. Every business shown sits at the
register's own map point; about one food storefront in a hundred has none and
is not shown. A business registered at a flat, where home bakers and cooks
register, is never placed, and neither is a childminder. Names are shown as
registered; where a business is registered "trading as" another name, the name
on the shop is shown.

**Only about two storefronts in five sit within a station ring.** One
15-station loop serves the centre and the West End; most of the city's food
businesses lie beyond it.

Concentric ring boundaries and the business categories (Food service and Food
shops) are toggleable via the layer control in the top left. When enabled,
business density will display as numbered circles summing areas when zoomed
out. Zooming in will show individual dots; hover over those to see further
details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a
statistical density estimate, so read the colour as "roughly where things
cluster."
"""
)

render_map_help('business categories (Food service and Food shops)')
render_country_links('Glasgow')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices()
