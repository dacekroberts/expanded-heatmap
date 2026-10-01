"""Buenos Aires heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.buenos_aires.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_data_age,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Buenos Aires Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Buenos Aires")
render_city_title('Buenos Aires')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/buenos_aires/step3_map.py` to generate it.")

render_data_age('Buenos Aires')

# Approved by the owner 2026-09-28; set as bullets 2026-10-01.
st.markdown(
    """
**The lines**

- Six lines are drawn — Subte **Líneas A, B, C, D, E and H** — each labelled on the map and
  in the legend, from the station and track records of SBASE, the city company that owns the
  Subte, in the operator's line colours.
- The Premetro, a surface light-rail line from Línea E's southern end, is not drawn, and
  neither are the commuter railways.
- Every Subte station lies inside the Ciudad Autónoma, so none is left out.

**The businesses**

- The businesses come from the **city's land-use survey of 2022 to 2024**, in which
  surveyors walked every block and recorded the use of every ground floor.
- It records what a premises is used for, not who runs it, so **no business names are shown:
  each dot shows its street address and its kind of business**.
- Shops inside malls and arcades are not itemised in the survey and are left out, as are
  shopfronts whose use the surveyors could not identify (about one in fourteen) and homes
  with a business inside.

**Reading the map**

- **Read the density as a survey, not a register.** Each block was surveyed once, in 2022,
  2023 or 2024, so a shop that has opened or closed since is shown as the surveyors found it.
- The survey gives no map points: each business is placed at the centre of its land parcel,
  so businesses in one building share a point.
- **About two storefronts in three sit within a station ring.**
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_country_links('Buenos Aires')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
