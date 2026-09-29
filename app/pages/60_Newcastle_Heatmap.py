"""Newcastle (Regional) heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.newcastle.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Newcastle (Regional) Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Newcastle (Regional)")

st.title("Newcastle (Regional): food businesses around Tyne and Wear Metro stations")

# Approved by the owner 2026-09-28.
st.markdown(
    """
Two lines are drawn, the Tyne and Wear Metro's **Green line** (Airport to South
Hylton) and **Yellow line** (St James to South Shields, round the coast), each
labelled on the map and redrawn from OpenStreetMap. The colours are close to
Nexus's but not the same, so they stay distinct from the dot colours. Between
Pelaw and Sunderland the Green line runs on track shared with national rail
trains; its stations are all drawn, as the Metro serves them. Northern's
national rail trains are not drawn.

The map covers the five districts of **Tyne and Wear**: Newcastle upon Tyne,
Gateshead, North Tyneside, South Tyneside and Sunderland. Every Metro station
is inside them.

**This map shows food businesses only.** They come from the **Food Standards
Agency's food hygiene register**, which lists every premises a council
inspects: restaurants, cafés, takeaways, pubs and bars, and food shops from
corner shops to supermarkets. No open register of other shops or of personal
services covers Tyne and Wear, so **clothes shops, hairdressers and the like are
not on this map**. Caterers working from home, mobile traders, and kitchens in
schools, hospitals and workplaces are left out.

**Read the density as a register, not a street survey.** A premises stays
listed until the council removes it. Most premises sit at the register's own
map point. Where it gives none, a business with a full postcode is placed at the
centre of its postcode, usually within a few dozen metres of its door. About
one food storefront in fourteen has neither and is not shown. A business run
from a private address, or registered at a flat, is never placed. Names are
shown as registered; where a business is registered "trading as" another name,
the name on the shop is shown.

**About half the storefronts sit within a station ring.**

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

# The snapshot dates, read from outputs/newcastle/provenance.json so they
# cannot go stale on the next fetch: the range of the five councils' own
# extract dates (the FSA's condition: say when the information was updated).
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _lo, _hi = (_prov.get("fsa_extract_range") or ["", ""])[:2]
        if _lo and _hi:
            st.caption(f"Snapshot: food businesses as extracted by each council between "
                       f"**{_lo}** and **{_hi}** (Food Standards Agency).")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/newcastle/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices()
