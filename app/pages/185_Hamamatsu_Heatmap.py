"""Hamamatsu heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py, in the
city-page format of 2026-10-01 (owner): title, map, captions, bullets, map help,
country links, notices.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.hamamatsu.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_data_age,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Hamamatsu Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Hamamatsu")
render_city_title("Hamamatsu")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/hamamatsu/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Hamamatsu")

# From the japan-city skill's template and Hakodate's, Okayama's and
# Kawasaki's pages (approved wording, pre-approved for this build,
# 2026-09-30); the sentences they do not cover are proposals in
# docs/decisions_drafts/japan-wave2.md. The date is the registers'
# publication date (config.REGISTERS_AS_OF). The ring share, 33.9%, is step
# 3's (1,080 of 3,187, 2026-10-03).
st.markdown(
    """
**The lines**

- Four lines are drawn, each labeled on the map and in the legend: the Enshu Railway Line, the
  Tenryu Hamanako Line, and JR Central's Tokaido and Iida lines.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Hamamatsu City get rings, because the business data covers the city alone:
  lines running on to Kosai and Iwata, and the Iida Line on into Aichi and Nagano, are cut at the
  city line.
- The city reaches from the coast far into the mountains: 32 of its 54 stations are on the Tenryu
  Hamanako Line and on the Iida Line's mountain stretch through Tenryu Ward.
- The Shinkansen is not drawn (Hamamatsu appears as a JR station).

**The businesses**

- **This map shows personal services only: barbers, beauty salons and laundries.**
- Hamamatsu City publishes its registers of these premises, but no register of food businesses or
  of other shops, so restaurants, cafés and shops are not on this map.
- The registers were published on 18 August 2026 and record no closures, so a dot is a premises on
  the register then, not necessarily one open today.

**Reading the map**

- The registers give an address but no location. Each address is matched to MLIT's address
  reference data, which places most at their street block; where only the district can be found,
  the dot sits at the city's own coordinates for the premises.
- The registers do not say who the operator is, so a trade name that is its operator's own name
  cannot be checked here.
- Names and types are shown in Japanese, as the city records them.
- **About a third of the premises sit within a ring.**
"""
)

render_map_help("business layer")
render_excluded_stations("Hamamatsu")
render_country_links("Hamamatsu")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Hamamatsu")
