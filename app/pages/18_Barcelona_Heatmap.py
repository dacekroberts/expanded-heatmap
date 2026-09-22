"""Barcelona heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.barcelona.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Barcelona Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Barcelona")

st.title("Barcelona: commercial density around Barcelona Metro station areas")

st.markdown(
    """
**The businesses are a premises census, not a licence register, and that
changes what the map means.** Most cities here are built from business
licences - a record of who registered. Barcelona is built from the
Ajuntament's *Cens de locals en planta baixa*, a field survey of the
ground-floor units on the street and the signs above their doors. That is the
same shape as Madrid's and Montréal's, and **not comparable** with the
licence-register cities, where what is counted is a registration rather than a
shopfront.

**The survey is from 2022, and this map says so deliberately.** The city
publishes one file per survey year rather than revisions of a single file. The
2024 file covers the centre but barely half of several outer districts - Sant
Andreu is 83% short of 2022, Nou Barris 76%, Horta-Guinardó 69%, while Ciutat
Vella is within 5%. A map built on it would show the periphery as commercially
dead, which is roughly what a reader half expects, so nothing would look
wrong. The 2022 survey is complete, and it is four years old. That is the
trade, and naming the year is part of making it.

**One ground-floor unit in nine is empty.** A tenth of the premises surveyed
are recorded as having no economic activity - vacant, for sale or to let - and
they are excluded here. Most registers make vacancy something you infer;
Barcelona states it outright, so this is one of the few cities on this site
where empty shopfronts can be taken out rather than silently counted as
businesses.

**Nearly every storefront sits near a station, which limits what the rings can
show.** Barcelona fits its whole metro network into about 101 km², and almost
no storefront in the city falls outside the outer ring. In Los Angeles or
Miami the rings separate what the network reaches from what it does not; here
they mostly do not. Read this map as *where commerce concentrates* rather than
as *what the Metro reaches*.

**The network spans two operators, and comes from OpenStreetMap.** TMB runs
L1-L5, L9-L11 and the Montjuïc funicular; Ferrocarrils de la Generalitat de
Catalunya runs L6-L8, L12 and the Vallvidrera funicular. TMB publishes a feed
behind a free account, and taking it would still have left three more feeds to
stitch together, so the lines are drawn from OpenStreetMap - where every one of
them carries its own name and colour. **L9 and L10 are each drawn as two
separate segments**, because that is how they run: the northern and southern
halves do not meet.

**Stations outside the city are not mapped.** Around a third of the network's
stations lie in L'Hospitalet, Cornellà, Sant Boi, El Prat, Badalona and Santa
Coloma - several of them only metres past the boundary. The lines are drawn in
full, but mapping those stations would need each municipality's own premises
data. They are listed in `outputs/barcelona/excluded_stations.csv`.

**What is counted, and what is not.** Retail, food service and personal
services, as the census's own four-level activity classification defines them.
**Hotels, hostals and pensions are excluded** - they are accommodation rather
than food service, even though the census files them in the same group as
restaurants and bars. So are offices, health, education, finance, repair,
storage and construction. Premises *inside* shopping centres, galleries and
municipal markets **are** counted: the census flags them and this map
deliberately does not use those flags, because a mall beside a station is
commercial density a rider can reach.

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
    st.info("No map yet. Run `python pipeline/barcelona/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
