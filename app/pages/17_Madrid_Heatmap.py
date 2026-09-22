"""Madrid heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.madrid.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Madrid Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Madrid")

st.title("Madrid: commercial density around Metro de Madrid station areas")

st.markdown(
    """
**The businesses are a premises census, not a licence register, and that
changes what the map means.** Most cities here are built from business
licences - a record of who registered. Madrid is built from the Ayuntamiento's
*Censo de locales*, which records the unit on the street and the sign above its
door. That is the same shape as Montréal's commercial survey, and the density
here is close to Montréal's for that reason. It is **not comparable** with the
licence-register cities, where what is counted is a registration rather than a
shopfront.

**About one storefront premises in eleven cannot be placed on this map.** The
register gives every premises a coordinate, but 9.2% of the ones in these three
categories carry a literal zero rather than a location. Those are left out
rather than guessed at. The loss is not even across the city - it falls hardest
on Barajas and the centre - but it falls hardest of all on tourist flats and
hostels, which this map does not show anyway.

**The rail network comes from CRTM's own published layers, not from a transit
feed.** A GTFS feed for the Metro exists and downloads cleanly, but CRTM
stopped refreshing it in May 2025 while continuing to maintain the network
layers this map is drawn from. Where Metro de Madrid publishes a figure, the
two reconcile: its 303 stations are 293 station-and-line records plus Metro
Ligero's line 1, which it also operates.

**Stations outside the city are not mapped.** Forty-nine of the network's 242
stations lie in Alcorcón, Getafe, Arganda del Rey and fifteen other
municipalities; lines 10 and 12 run well past the city and are drawn in full,
but mapping their stations would need each municipality's own business
register. They are listed in `outputs/madrid/excluded_stations.csv`.

**What is counted, and what is not.** Retail, food service and personal
services, as the register's own activity classification defines them. Hotels
and tourist flats are excluded - they are accommodation rather than food
service. So are wholesale, vehicle repair, and premises with no shopfront such
as online and vending sales.

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
    st.info("No map yet. Run `python pipeline/madrid/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
