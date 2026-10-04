"""Mendoza heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py, in the
city-page format of 2026-10-01 (owner): title, map, captions, bullets, map help,
country links, notices.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.mendoza.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_caption,
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Mendoza Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Mendoza")
render_city_title("Mendoza")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/mendoza/step3_map.py` to generate it.")

# The caption from provenance.json: the register with its own date and portal,
# then the rail's fetch date (the tram-city caption's shape).
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _reg = (_prov.get("register") or {}).get("data_date") or ""
        _rail = ((_prov.get("files_utc") or {}).get("osm.json") or "")[:10]
        if _reg and _rail:
            render_caption(f"Commercial accounts from the Municipalidad de la Ciudad de Mendoza "
                       f"(datos.ciudaddemendoza.gob.ar), open at **{_reg}**; the Metrotranvía "
                       f"and its stations from OpenStreetMap, fetched **{_rail}**.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# Bullets on the scaffold's headings, filled from Mendoza's own step 1 and
# step 2 figures, with the tram-city template's sentences for a line drawn past
# the city. The frequency, business and confiteria bullets were proposals,
# approved shortened (owner, 2026-10-04; DECISIONS.md).
st.markdown(
    """
**The line**

- One light-rail line is drawn, the **Metrotranvía**, labeled on the map and in the legend,
  redrawn from OpenStreetMap's route geometry, in a darker red than its own, to stay clear of the
  dot colors.
- Trains run about every 10 minutes at weekday peaks and every 13 minutes at midday.
- Buses are not drawn.
- The map covers the **Ciudad de Mendoza**, the capital department. The Metrotranvía runs on into
  Godoy Cruz, Maipú and Las Heras, so its 18 stations there are left out.
- The line is still drawn to its ends, but those stations get no ring and their businesses are not
  counted. They are listed below.
- **Stations in the capital sit close together**, a median of 412 m here, so the rings are drawn
  at half the usual size (0.05 to 0.3 mi).

**The businesses**

- Businesses come from the capital's **list of open commercial accounts**, each placed at the
  point the city records for it.
- Each business counts once. One with several types goes in the first of Food service, Retail
  and Personal services that fits.
- **Where a business's name is written as a person's own, the map shows its type of business
  instead.**
- **The list dates from June 2025.** Businesses that opened since then are missing, and any that
  closed may still be shown.
- **About one storefront in seven sits within a ring.**

**Reading the density**

- **Read the density as a register, not a street survey.** An open account is a business
  registered at an address, and the list does not say whether it has a shop a passer-by could
  walk into.
- Confiterías count as cafés, not shops: here they have sidewalk tables and serve alcohol.
"""
)

render_map_help("three business categories (Retail, Food service and Personal services)")
render_excluded_stations("Mendoza")
render_country_links("Mendoza")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Mendoza")
