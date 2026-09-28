"""Sapporo heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.sapporo.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Sapporo Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Sapporo")

st.title("Sapporo: commercial density around rail stations")

# Prose approved by the owner 2026-09-28. The as-of dates are the lists' own
# (config.FOOD_AS_OF, config.REGISTERS_AS_OF).
st.markdown(
    """
Seven lines are drawn, each labelled on the map and in the legend: the Sapporo Municipal Subway's
Namboku, Tōzai and Tōhō lines; the Sapporo Streetcar's loop; and JR Hokkaido's Hakodate Main,
Chitose and Gakuen Toshi lines. Lines and stations come from MLIT's national railway data
(国土数値情報); station names in English are from OpenStreetMap, written in one style with block
numbers as figures (Kita-18-Jo, Nishi-11-Chome). Only stations inside Sapporo City get rings,
because the business data covers the city alone: JR lines running on to Otaru, Ebetsu, Tōbetsu and
the airport are cut at the city line. Line colours are this project's own, not the operators'.

Businesses come from Sapporo City's list of food-business permits (as of 31 March 2026) and its
registers of barbers, beauty salons, laundries and coin laundries (as of 31 July 2026). Japan has
no general business licence, so shops other than food shops — clothing, electronics, pharmacies —
do not appear: the Retail layer is food retail only (bakeries and confectioners, delis, butchers
and fishmongers). Food businesses that only notify the city rather than hold a permit are not in
the list, nor are salons inside hospitals and care homes, which serve their residents rather than
the public. The list may include premises that have closed, so a dot means a permit on file, not a
business open today. Food trucks and stalls registered to trade anywhere in the city have no fixed
place and are left out.

The list gives an address but no location. Each address is matched to MLIT's address reference
data, which places most at their street block; where only the block group (条丁目) can be found,
the dot sits at its centre, which on Sapporo's grid is about one block. A handful of addresses
cannot be placed. Where a business's trade name is its operator's own name, the dot shows its
permit type instead. Names and permit types are shown in Japanese, as the city records them.

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
    st.info("No map yet. Run `python pipeline/sapporo/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
