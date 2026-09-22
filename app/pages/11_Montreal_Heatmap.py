"""Montréal heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern for every city's
detail page. Scaffolded by scripts/scaffold_city.py.

The page name here must match the `name` in app/cities.py ("Montréal"), which
render_city_nav() looks up. The FILENAME is ASCII on purpose: the display name
carries the accent, the filename does not, so nothing depends on an accented
path.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.montreal.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Montréal Heatmap",
                   page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Montréal")

st.title("Montréal: commercial density around Métro station areas")

st.markdown(
    """
**This is the only map here built from a field survey rather than a licence
register.** The Ville de Montréal walks its commercial streets each year and
records what occupies each unit, so it counts what is actually there rather
than who holds a permit. One consequence is worth knowing before reading the
colours: roughly **69% of surveyed units are storefronts**, against about 28%
in a licence-register city, so the balance between categories here reflects the
street more directly than it can elsewhere on this site.

**Vacant units are excluded.** The survey records them — about 3,500 of them —
and a licence register never can. An empty shopfront is premises rather than
commerce, so counting them would measure the supply of retail space instead.
That is a choice, and it is the one filter on this map that no other city here
needed.

**Four lines are drawn** from the Société de transport de Montréal's own
published geometry, each labelled directly on the map and in the legend, in the
STM's own colours: Ligne 1 (Verte), Ligne 2 (Orange), Ligne 4 (Jaune) and
Ligne 5 (Bleue).

**64 of the Métro's 68 stations are on the island** and are mapped. The other
four — Cartier, De la Concorde and Montmorency in Laval, and
Longueuil–Université-de-Sherbrooke — are excluded, because those cities'
commercial data would have to be sourced and verified separately. They are
listed in `outputs/montreal/excluded_stations.csv`.

**Known limitation.** The map is scoped to the agglomeration, which includes 15
related municipalities alongside the 19 boroughs, but only about a tenth of
surveyed units fall in those municipalities and two of them are not in the
survey at all. The Métro does not reach them, so this barely affects what is
drawn — but read the island's edges as thinner in the data, not necessarily on
the ground.

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
    st.info("No map yet. Run `python pipeline/montreal/step3_map.py` to generate it.")

render_site_notices()
