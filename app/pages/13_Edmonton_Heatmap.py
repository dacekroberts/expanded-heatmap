"""Edmonton heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.edmonton.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Edmonton Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Edmonton")

st.title("Edmonton: commercial density around ETS LRT station areas")

st.markdown(
    """
**Edmonton's licence register says whether a business runs from a home, and
the City removes the address when it does.** A single field separates
commercial premises from home-based trades, mobile operators, and licences
held by a person rather than a place — so this map needed none of the
inference that Vancouver's required, where the city says nothing and a parcel
join had to stand in. Where a licence belongs to an individual, Edmonton
replaces the street address with `<REDACTED FOR PRIVACY>` and takes the
coordinates away with it, so those records cannot be placed on a map at all.
The privacy work here was done upstream, by the publisher.

**Three of this system's apparent stations are not stations.** Every train
stops at two garage access points and a tail track, and at none of the three
can a passenger get on or off. In the schedule data they are indistinguishable
from real stations, and counting them is why this project's own earlier reading
of Edmonton came out too low per station. They are listed in
`outputs/edmonton/non_revenue_stops.csv`. Every remaining station is inside the
city, so nothing was dropped for lying in another municipality —
`outputs/edmonton/excluded_stations.csv` exists and is empty, as Calgary's is.

**Three lines are drawn** from Edmonton Transit Service's own route geometry:
the Capital Line, the Metro Line and the Valley Line. The colours are this
site's rather than the agency's. ETS signs Capital blue and Valley green, and
both sit too close to the Retail and Personal services pin colours to stay
readable on top of them, so each line keeps its hue and is darkened until it
separates. The Metro Line shares the Capital Line's track through the
south-west, where the two run together.

**Retail is the largest category here**, which is the reverse of Calgary's
balance and is again a fact about licensing rather than about streets.
Edmonton licenses general retail in several size bands plus a convenience-store
class, so ordinary shops are well covered — where a number of large US cities
license no general retail at all, and their maps show almost none of it.

**Personal services is overstated, by a knowable amount.** Edmonton's
accredited "Health Enhancement Centre" licence covers massage and spa
premises, which belong in this category, but also physiotherapy and
chiropractic clinics, which are regulated health care and do not. The register
does not distinguish them, and roughly a quarter of that licence class reads
as a clinic. It is counted anyway, so that Edmonton stays comparable with
Calgary, where massage premises count for the same underlying reason: Alberta
does not regulate massage therapy as a health profession, and British Columbia
does — which is why Vancouver's equivalent is excluded. Read this category as
slightly generous here.

**Adult services and body rub centres are left off**, as in Calgary, along
with several categories that merge a trade this map counts with one it does
not. What is excluded, and why, is on the "What is counted, and what is not"
page.

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
    st.info("No map yet. Run `python pipeline/edmonton/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. This page did not call it until
# 2026-09-22; the scaffold template omitted it.
render_site_notices()
