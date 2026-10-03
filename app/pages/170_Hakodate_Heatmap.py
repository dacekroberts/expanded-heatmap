"""Hakodate heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.hakodate.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Hakodate Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Hakodate")
render_city_title("Hakodate")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/hakodate/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Hakodate")

# From the japan-city skill's template and Yokohama's and Matsuyama's pages
# (approved wording, pre-approved for this build, 2026-09-30); the sentences
# they do not cover are proposals in docs/decisions_drafts/japan-batch.md. The
# as-of date is the registers' own (config.REGISTERS_AS_OF). The median is
# step 1's (2026-10-02).
st.markdown(
    """
**The lines**

- Three lines are drawn, each labeled on the map and in the legend: the Hakodate City Tram, JR
  Hokkaido's Hakodate Line and the South Hokkaido Railway.
- The city tram's routes share most of their track, so the tram is drawn as one line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Hakodate City get rings, because the business data covers the city alone:
  lines running on to Nanae and Hokuto are cut at the city line.
- **Tram stops sit closer together than metro stations**, a median of 363 m here, so the
  rings are drawn at half the usual size (0.05 to 0.3 mi).

**The businesses**

- **This map shows personal services only: barbers, beauty salons and laundries.**
- Hakodate City publishes its registers of these premises, but no register of food businesses or
  of other shops, so restaurants, cafés and shops are not on this map.
- The registers are as of 31 August 2026 and record no closures, so a dot is a premises on the
  register then, not necessarily one open today.

**Reading the map**

- The registers give an address but no location. Each address is matched to MLIT's address
  reference data, which places most at their street block; where only the district can be found,
  the dot sits at the district's center.
- Where a business's trade name is its operator's own name, the dot shows its register type
  instead.
- Names and types are shown in Japanese, as the city records them.
- **About three in ten of the premises sit within a ring.**
"""
)

render_map_help("business layer")
render_excluded_stations("Hakodate")
render_country_links("Hakodate")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Hakodate")
