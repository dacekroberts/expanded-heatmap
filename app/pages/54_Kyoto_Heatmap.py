"""Kyoto heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.kyoto.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Kyoto Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Kyoto")
render_city_title('Kyoto')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/kyoto/step3_map.py` to generate it.")

render_data_age('Kyoto')

# Prose approved by the owner 2026-09-28; set as bullets 2026-10-01. The
# rebuild's date is config.AS_OF, the registers' config.REGISTERS_AS_OF.
st.markdown(
    """
**The lines**

- Eighteen lines are drawn, each labelled on the map and in the legend: the Kyoto Municipal
  Subway's Karasuma and Tōzai lines; JR West's Kyoto, Biwako, Sagano, Nara and Kosei lines;
  Keihan's Main, Ōtō, Uji and Keishin lines; Hankyu's Kyoto and Arashiyama lines; Kintetsu's Kyoto
  Line; the Randen's Arashiyama and Kitano lines; and Eiden's Eizan and Kurama lines.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colours are this project's own, not the operators'.
- Only stations inside Kyoto City get rings, because the business data covers the city alone:
  lines running on to Ōtsu, Uji, Mukō, Nagaokakyō and Yawata are cut at the city line.
- The Sagano Scenic Railway and the Eizan and Kurama cable cars, which are sightseeing lines, are
  not drawn.

**The businesses**

- Kyoto has published no complete list of food-business permits since 2021, only each month's new
  ones. The food businesses here are therefore rebuilt: the city's full list of March 2021 plus
  every monthly list since, keeping each permit still within its term on 31 July 2026, the last
  date the newest monthly list covers.
- The city does not publish closures, so a business that closed before its permit ran out is still
  counted. The map shows an upper bound, and a dot means a permit on file, not a business open
  today.
- Barbers, beauty salons and laundries come from the city's complete lists as of 31 March 2026 and
  the new premises listed each month since.
- Japan has no general business licence, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear. The Food shops layer is food retail only, by permit type: bakeries
  and confectioners, delis, butchers and fishmongers.
- Shops selling only packaged food have filed a notification rather than a permit since 2021 and
  are not in the lists.

**Reading the map**

- The lists give an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where only the town can be found, the dot sits
  at its centre.
- Kyoto's central addresses name the street corner before the town (河原町通三条上る下丸屋町),
  and the match reads past the corner to the town.
- Where a business's trade name is its operator's own name, the dot shows its permit type instead.
- Names and permit types are shown in Japanese, as the city records them.
"""
)

render_map_help('three business categories (Food shops, Food service and Personal services)')
render_excluded_stations("Kyoto")
render_country_links('Kyoto')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
