"""Kobe heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.kobe.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Kobe Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Kobe")
render_city_title('Kobe')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/kobe/step3_map.py` to generate it.")

render_data_age('Kobe')

# Prose approved by the owner 2026-09-27; set as bullets 2026-10-01. It restates
# no counts; the as-of date is the food list's own (config.FOOD_AS_OF).
st.markdown(
    """
**The lines**

- Fifteen lines are drawn, each labeled on the map and in the legend: Kobe Municipal Subway's
  Seishin-Yamate, Hokushin and Kaigan lines, the Port Liner and Rokkō Liner, JR West's JR Kobe,
  Wadamisaki and JR Takarazuka lines, the Hankyu Kobe Line, the Hanshin Main Line, the Sanyō Main
  Line, the Kobe Kōsoku Line, and Kobe Electric Railway's Arima, Sanda and Ao lines.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Kobe City get rings, because the business data covers the city alone: lines
  running on to Ashiya, Akashi, Sanda and Miki are cut at the city line. The stations left out are
  listed below.
- The Shinkansen is not drawn (Shin-Kobe appears as a subway station), nor are the Maya and Rokkō
  cable cars, sightseeing lines up the mountain.

**The businesses**

- From Kobe City's list of food-business permits (all permits in force at the end of March 2026)
  and its registers of barbers, beauty salons and laundries.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear: the Food shops layer is food retail only (bakeries and confectioners,
  delis, butchers and fishmongers).
- Food businesses that only notify the city rather than hold a permit, such as many convenience
  stores and greengrocers, are not in the list.
- The city notes that premises which have closed may still be listed, so a dot means a permit on
  file, not a business open today.

**Reading the map**

- The list gives an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where only the district can be found, the dot
  sits at the district's center.
- Where a business's trade name is its operator's own name, the dot shows its permit type instead.
- Names and permit types are shown in Japanese, as the city records them.
"""
)

render_map_help('three business categories (Food shops, Food service and Personal services)')
render_excluded_stations("Kobe")
render_country_links('Kobe')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Kobe")
