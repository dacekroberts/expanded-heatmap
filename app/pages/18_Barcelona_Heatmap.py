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
    render_city_title,
    render_country_links,
    render_data_age,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Barcelona Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Barcelona")
render_city_title('Barcelona')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/barcelona/step3_map.py` to generate it.")

render_data_age('Barcelona')

st.markdown(
    """
**The lines**

- **The network spans two operators, and comes from OpenStreetMap**, where every line carries its
  own name and color. TMB runs L1-L5, L9-L11 and the Montjuïc funicular; Ferrocarrils de la
  Generalitat de Catalunya runs L6-L8, L12 and the Vallvidrera funicular.
- **L9 and L10 are each drawn as two separate segments**, because that is how they run: the
  northern and southern halves do not meet.
- **Stations outside the city are not mapped.** Around a third of the network's stations lie in
  L'Hospitalet, Cornellà, Sant Boi, El Prat, Badalona and Santa Coloma - several of them only
  meters past the boundary.
- The lines are drawn in full, but mapping those stations would need each municipality's own
  premises data. They are listed below.

**The businesses**

- **The businesses are a premises census, not a license register, and that changes what the map
  means.** Most cities here are built from business licenses - a record of who registered.
- Barcelona is built from the Ajuntament's *Cens de locals en planta baixa*, a field survey of the
  ground-floor units on the street and the signs above their doors: the same shape as Madrid's and
  Montréal's, and **not comparable** with the license-register cities, where what is counted is a
  registration rather than a shopfront.
- **The survey is from 2022, and this map says so deliberately.** The city publishes one file per
  survey year rather than revisions of a single file.
- The 2024 file covers the center but barely half of several outer districts. A map built on it
  would show the periphery as commercially dead, and since a reader half expects that, nothing
  would look wrong.
- So this map uses the 2022 survey: complete, but four years old.
- **One ground-floor unit in nine is empty.** A tenth of the premises surveyed are recorded as
  having no economic activity - vacant, for sale or to let - and they are excluded here.
- The map counts retail, food service and personal services as the census's own four-level
  activity classification defines them. **Hotels, hostals and pensions are excluded**, as
  accommodation rather than food service.
- Premises *inside* shopping centers, galleries and municipal markets **are** counted.

**Reading the map**

- **Nearly every storefront sits near a station, which limits what the rings can show.** Barcelona
  fits its whole metro network into about 101 km², and almost no storefront in the city falls
  outside the outer ring.
- In Los Angeles or Miami the rings separate what the network reaches from what it does not; here
  they mostly do not. Read this map as *where commerce concentrates* rather than as *what the
  Metro reaches*.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Barcelona")
render_country_links('Barcelona')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Barcelona")
