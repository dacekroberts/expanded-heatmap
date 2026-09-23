"""Lille (Regional) heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.

Named `24_Lille_Heatmap.py` rather than the scaffold's
`24_Lille_(Regional)_Heatmap.py`: app/station_scope.py derives a city's
outputs directory from this filename, and `lille_(regional)` resolves to
nothing. Guadalajara's page follows the same pattern for the same reason.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.lille.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Lille (Regional) Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Lille (Regional)")

st.title("Lille (Regional): commercial density around Métro and Tramway station areas")

st.markdown(
    """
Four ilévia lines are drawn — **Métro 1 and 2, and Tram R and T** — each
labelled on the map and in the legend.

**This map covers eleven communes, not one.** The métro and tram run well
beyond the city of Lille, out to Villeneuve-d'Ascq, Roubaix and Tourcoing, and
a map of the commune alone would keep fewer than half of Métro 2's stations and
only three of the tram's thirty-six. So it takes in every commune with a
station: Lille, Roubaix, Tourcoing, Villeneuve-d'Ascq, Marcq-en-Barœul,
Wasquehal, Croix, Mons-en-Barœul, La Madeleine, Mouvaux and Lambersart. Each is
listed with its stations in `outputs/lille/served_communes.csv`.

**The lines come from two sources.** Station locations and the tram's route are
published by the Métropole Européenne de Lille itself. No official source
publishes the métro's route, so its two lines are drawn from OpenStreetMap.
ilévia colours both trams alike; Tram T is shown here in a darker shade of the
same blue so the two can be told apart.

Businesses come from **SIRENE**, France's national register of établissements,
joined to INSEE's separate geolocation file, the same sources as the other
French cities. About one active establishment in six across these communes is
marked non-diffusible by INSEE, which withholds its name, address and
coordinates together, so those never reach this map.

**Read the density as a register, not a street survey.** SIRENE records where a
business is *registered*, and some registered establishments have no
customer-facing shopfront; nothing in the data says which. Against
OpenStreetMap's mapped restaurants in the same eleven communes, where the two
schemes mean nearly the same thing, this map carries about **1.5 times** as
many points, inside the range of the other French cities.

**About three storefronts in five sit within a station ring.** The category
toggles show every storefront; the rings show the share the four lines actually
reach.

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

# Licence Ouverte 2.0 asks for the producer AND « la date de dernière mise à
# jour ». MEL's layers carry no update date (tramway_lignes has only a
# metadata dateStamp, 2024-06-03), so the retrieval date is shown and the
# caption SAYS it is the retrieval date - the brief's instruction, and the
# honest reading of an obligation the source gives no way to meet literally.
# Read from outputs/lille/provenance.json so it cannot go stale on a re-fetch.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _taken = (_prov.get("fetched_utc") or "")[:10]
        if _taken:
            st.caption(
                "Station locations, tram routes and line colours © Métropole "
                "Européenne de Lille and Ilévia, Licence Ouverte 2.0, retrieved "
                f"**{_taken}**. MEL publishes no update date for these layers, "
                "so this is the date they were read. Métro routes © "
                "OpenStreetMap contributors.")
    except (ValueError, OSError):
        # A malformed provenance file must not take the page down.
        pass

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/lille/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
