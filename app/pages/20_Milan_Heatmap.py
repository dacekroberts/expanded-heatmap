"""Milan heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.milan.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_data_age,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Milan Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Milan")
render_city_title('Milan')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/milan/step3_map.py` to generate it.")

render_data_age('Milan')

# "One pin in seven" below is step 2's own "shop sign on" line (15.3% of every
# storefront, 15.4% of the within-ring pins, 2026-09-23). It read "a fifth"
# until then - the per-register rates (17.7% on the largest) were the only ones
# printed, and none of them is the rate across the map.
st.markdown(
    """
**The lines**

- The map covers the **Comune di Milano** and draws the five metro lines - **M1 (linea rossa)**,
  **M2 (linea verde)**, **M3 (linea gialla)**, **M4 (linea blu)** and **M5 (linea lilla)** - each
  labelled on the map and in the legend, in ATM's own colours.
- Milan's 17 tram routes are **not** drawn: they are a dense street-running network whose stops
  sit a block or two apart, which needs different treatment from a metro, and the agency publishes
  no colour for any of them.
- Twenty-one metro stations lie outside the comune - the ends of M1 at Rho and Sesto, M2 at
  Gessate and Cologno, M4 at Linate - and are listed on the What is counted page.

**The businesses**

- **The premises come from six separate registers, and they are not merged.** Milan licenses
  neighbourhood shops, bakers, artisan food makers, bars and restaurants (in and out of the
  commercial plan) and personal services each in its own register.
- A single Milan address routinely holds many separate premises, so merging the registers on
  address would delete real businesses. Where one business holds two licences it is counted twice;
  that is the deliberate direction to err in, and it is why the counts read slightly high rather
  than slightly low.
- **About one pin in seven carries a shop sign; the rest carry an address.** Milan records an
  *insegna* - the sign over the door - on only some rows, and three of the six registers have no
  name field at all.
- No register carries an owner's name, so nothing here can be a person.

**Reading the map**

- The register of premises licensed **outside** the commercial plan includes staff canteens,
  private clubs and parish halls alongside ordinary bars. Those that identify themselves are
  filtered out, but the register does not mark them reliably, so some remain.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_country_links('Milan')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
