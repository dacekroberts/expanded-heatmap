"""Milan heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.milan.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Milan Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Milan")

st.title("Milan: commercial density around Metropolitana di Milano station areas")

st.markdown(
    """
The map covers the **Comune di Milano** and draws the five metro lines -
**M1 (linea rossa)**, **M2 (linea verde)**, **M3 (linea gialla)**,
**M4 (linea blu)** and **M5 (linea lilla)** - each labelled on the map and in
the legend, in ATM's own colours. Milan's 17 tram routes are **not** drawn:
they are a dense street-running network whose stops sit a block or two apart,
which needs different treatment from a metro, and the agency publishes no
colour for any of them. Twenty-one metro stations lie outside the comune - the
ends of M1 at Rho and Sesto, M2 at Gessate and Cologno, M4 at Linate - and are
listed in `outputs/milan/excluded_stations.csv`.

**The premises come from six separate registers, and they are not merged.**
Milan licenses neighbourhood shops, bakers, artisan food makers, bars and
restaurants (in and out of the commercial plan) and personal services each in
its own register, and a premises appears in whichever one licenses what it
does. Because a single Milan address routinely holds many separate premises,
merging the registers on address would delete real businesses - so they are
kept apart. Where one business holds two licences it is counted twice; that is
the deliberate direction to err in, and it is why the counts read slightly
high rather than slightly low.

**About a fifth of the pins carry a shop sign; the rest carry an address.**
Milan records an *insegna* - the sign over the door - on only some rows, and
three of the six registers have no name field at all. Where a sign exists it is
shown, and where it does not the address is. No register carries an owner's
name, so nothing here can be a person.

One limitation worth stating: the register of premises licensed **outside** the
commercial plan includes staff canteens, private clubs and parish halls
alongside ordinary bars. Those that identify themselves are filtered out, but
the register does not mark them reliably, so some remain.

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
    st.info("No map yet. Run `python pipeline/milan/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
