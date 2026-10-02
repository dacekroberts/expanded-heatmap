"""Dublin heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.dublin.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Dublin Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Dublin")
render_city_title('Dublin')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/dublin/step3_map.py` to generate it.")

render_data_age('Dublin')

st.markdown(
    """
**The lines**

- Three lines are drawn: the **Luas Red Line**, the **Luas Green Line** and the **DART**, each
  labeled on the map and in the legend.
- Commuter and InterCity trains are not drawn. Iarnrod Eireann runs them over the same tracks,
  but they are not urban rail, and most maps on this site leave commuter rail out.
- The map covers **four local authorities** - Dublin City, Fingal, South Dublin and Dun
  Laoghaire-Rathdown - rather than the city alone, because the Luas and the DART run through all
  four.
- Two DART stations, Bray Daly and Greystones, lie in County Wicklow outside all four authorities -
  they and the reason are listed below.

**The businesses**

- **The pins carry addresses, not business names.** Ireland's rateable valuation register,
  published by Tailte Eireann, records *premises* rather than occupiers - it has no trade-name
  column, no occupier column and no owner column.
- Each pin therefore shows the address a valuation is filed against and the use recorded against
  it, which is all the source knows.
- Categories are the register's own recorded uses, grouped into three. Where a premises carries
  more than one use (a shop with offices above it, a salon behind a shopfront), the more specific
  trading use is shown.
- **The valuation list keeps vacant commercial premises on it, filed under their last use,
  so some pins may be empty units.** Only the 117 or so marked vacant are left out, and the
  list does not say which of the others are open.

**Reading the map**

- **Large parts of this map have no rail near them, and showing that is deliberate.** Much of
  Fingal and South Dublin lies beyond every drawn line.
- Swords, Fingal's largest town, has no rail station of any kind, and Clondalkin and Lucan are
  reached only by commuter services this map does not draw.
- Read the empty stretches as a fact about where Dublin built rail, not about where Dublin has
  shops.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Dublin")
render_country_links('Dublin')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
