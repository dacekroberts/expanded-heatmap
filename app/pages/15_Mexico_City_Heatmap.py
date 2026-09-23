"""Mexico City heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.mexico_city.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Mexico City Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Mexico City")

st.title("Mexico City: commercial density around Metro CDMX station areas")

# No counts in this prose, deliberately: add-city Step 8's rule is that a
# station count or a "twelve lines" in page text is literal and goes stale when
# the pipeline changes. Line names are safe - they are the operator's, not
# computed.
st.markdown(
    """
Metro CDMX runs twelve lines — Líneas 1 to 9, A, B and 12 — and this map draws
all of them alongside the STE Tren Ligero, which continues south from Tasqueña
to Xochimilco. Each line is labelled directly on the map in the name its riders
use, and appears in the legend.

Only stations inside Ciudad de México are mapped. Líneas A and B run north and
east into the State of Mexico, and those stations are left out because this map
has no business data for them — their rings would sit over blank ground. They
are listed in `outputs/mexico_city/excluded_stations.csv`.

**The line geometry here comes from OpenStreetMap, not from the operator.**
Every public host for the Mexico City government, for STC Metro and for the STE
is unreachable from where this was built, and the Metro's transit feed is
refused at its download location. So the alignments are OpenStreetMap
contributors' mapping of the network rather than the agency's own file — the one
city here whose rail geometry does not come from its operator. For the same
reason, the station count has not been checked against what STC Metro
publishes.

**The businesses are a census, not a licence register, and that changes what
the map means.** Most cities here are built from business licences: a record
of who registered. Mexico City is built from INEGI's DENUE, compiled by
surveying premises and recording the name on the shopfront. It is far more
complete than a licence register, so the density shown here is **not
comparable** with the licence-register cities' — read it as a fact about how
the data was collected as much as about Mexico City's streets.

Fixed premises only. DENUE separately records semi-fixed units — stalls and
street posts — and those are not shown, although street commerce is a real and
substantial part of the city's retail.

Unlike the other cities, this map has no whole-city layer: there is no option
to show every business in Mexico City at once, only those near a station. That
layer would have carried more than twice the points of the default one.

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

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/mexico_city/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. This page did not call it until
# 2026-09-22; the scaffold template omitted it.
render_site_notices()
