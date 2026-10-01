"""Yokohama heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.yokohama.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_data_age,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Yokohama Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Yokohama")
render_city_title('Yokohama')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/yokohama/step3_map.py` to generate it.")

render_data_age('Yokohama')

# Written under the owner's pre-approval of this build's prose (2026-09-30),
# from Kobe's page (the Japanese template) and Palma's (a one-layer page). It
# restates no counts; the as-of date is the registers' own
# (config.REGISTERS_AS_OF). Set as bullets 2026-10-01.
st.markdown(
    """
**The lines**

- Twenty lines are drawn, each labelled on the map and in the legend: the Yokohama Municipal
  Subway's Blue and Green lines; JR East's Keihin-Tohoku / Negishi, Tokaido, Yokosuka, Yokohama,
  Nambu and Tsurumi lines and the Sotetsu-JR Link Line; the Keikyu Main and Zushi lines; Tokyu's
  Toyoko, Den-en-toshi, Kodomonokuni and Shin-yokohama lines; the Minatomirai Line; Sotetsu's
  Main, Izumino and Shin-yokohama lines; and the Kanazawa Seaside Line, an automated guideway.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colours are this project's own, not the operators'.
- Only stations inside Yokohama City get rings, because the business data covers the city alone:
  lines running on to Tokyo, Kawasaki, Machida, Yamato, Fujisawa, Kamakura, Zushi and Yokosuka are
  cut at the city line.
- Where JR services share track they are drawn over one another.
- The Shinkansen is not drawn (Shin-Yokohama appears as a station of the lines above).

**The businesses**

- **This map shows personal services only: barbers, beauty salons and laundries.**
- Yokohama City publishes its registers of these premises, but no list of food businesses or of
  other shops, so restaurants, cafés and shops are not on this map.
- The registers are as of 1 April 2026 and record no closures, so a dot is a premises on the
  register then, not necessarily one open today.

**Reading the map**

- The registers give an address but no location. Each address is matched to MLIT's address
  reference data, which places almost all at their street block; where only the district can be
  found, the dot sits at the district's centre.
- Where a business's trade name is its operator's own name, the dot shows its register type
  instead.
- Names and types are shown in Japanese, as the city records them.
- Most of the premises sit within a station ring: Yokohama's rail network reaches most of the
  city.
"""
)

render_map_help('business layer')
render_country_links('Yokohama')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
