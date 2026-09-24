"""Copenhagen heatmap page - embeds the pre-rendered Folium HTML.

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
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Copenhagen Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Copenhagen")

st.title("Copenhagen: commercial density around Metro and S-tog station areas")

# Approved by the owner 2026-09-24, with the partnership and catch-all
# clauses matching the two calls taken that day (DECISIONS.md).
st.markdown(
    """
Eleven lines are drawn — **Metro lines M1 to M4 and S-tog lines A, B, Bx, C, E,
F and H** — each labelled on the map and in the legend, redrawn from
OpenStreetMap's route geometry in the operators' own colours. Two S-tog lines, A
and F, are shown a shade lighter so they stay distinct from the Metro lines whose
colours they nearly share. S-tog is Copenhagen's suburban rail network, and most
maps on this site leave that kind of line out. It is drawn here because inside
the city it runs like a metro, every ten minutes on its own tracks, and reaches
many districts the Metro does not.

The map covers the **municipalities of Copenhagen and Frederiksberg**.
Frederiksberg is a separate municipality entirely surrounded by Copenhagen, with
seven Metro stations of its own, so leaving it out would leave a hole in the
middle of the map. The S-tog lines run far beyond both, out to Køge, Hillerød and
Frederikssund. Their stations out there are drawn on the line but get no ring,
and their businesses are not counted; the same goes for the Metro's two airport
stations in Tårnby. They are listed in `outputs/copenhagen/excluded_stations.csv`.

Businesses come from Denmark's **Central Business Register** (Det Centrale
Virksomhedsregister, CVR), and specifically from its production units: each place
where a business operates, recorded at that place's own address rather than its
company's. Each is placed using Denmark's official address register, Danmarks
Adresseregister. **Where a business is owned personally (a sole proprietorship, a
partnership or any business whose registered name marks it as one person's), the
map shows its address instead of its name**, because such businesses are usually
registered under the owners' own names.

**Read the density as a register, not a street survey.** Some premises are newly
registered and may not have opened yet. Denmark's classification files a web shop
under the goods it sells, so some dots are businesses with no shop a passer-by
could walk into, and nothing in the data says which. Against OpenStreetMap's
mapped restaurants, cafés and takeaways in the same two municipalities, the
register carries about **1.1 times** as many. One catch-all category, *other
personal services*, is left out, because most of it is people working from their
own premises; it also holds Copenhagen's tattoo studios, which are therefore
missing from the map. A small share of premises (under 2%) carry no official
address and cannot be placed.

**About nineteen storefronts in twenty sit within a station ring.**

Concentric ring boundaries and the three business categories (Retail, Food
service and Personal services) are toggleable via the layer control in the top
left. When enabled, business density will display as numbered circles summing
areas when zoomed out. Zooming in will show individual dots; hover over those
to see further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a
statistical density estimate, so read the colour as "roughly where things
cluster."
"""
)

# The snapshot date, read from outputs/copenhagen/provenance.json so it cannot
# go stale on the next fetch: the CVR weekly generation the join was built on.
# All six CVR entities are one generation (fetch_sources refuses a mix), so
# any of them dates it; Virksomhed carries Datafordeler's generation time.
if PROVENANCE_JSON.exists():
    try:
        _files = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8")).get("datafordeler", {})
        _times = sorted(v.get("generation_time") or "" for k, v in _files.items()
                        if k.startswith("cvr/") and v.get("generation_time"))
        if _times:
            st.caption(f"Business and address data from Datafordeler's weekly "
                       f"extracts, generated **{_times[0][:10]}**.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/copenhagen/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
