"""Toyama heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.toyama.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Toyama Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Toyama")
render_city_title("Toyama")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/toyama/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Toyama")

# From the japan-city skill's template and Matsuyama's and Hiroshima's pages
# (approved wording, pre-approved for this build, 2026-09-30); the sentences
# it does not cover are proposals in the Japan batch's drafts file. The as-of
# dates are the lists' own (config.SOURCE_AS_OF). The median, 443 m, is step
# 1's (2026-10-02).
st.markdown(
    """
**The lines**

- Eight lines are drawn, each labeled on the map and in the legend: Chitetsu's city tram and its
  Toyamako Line (Portram), its Main, Fujikoshi, Kamidaki and Tateyama lines, the Ainokaze Toyama
  Railway and JR West's Takayama Line.
- The city tram's routes share most of their track, so the tram is drawn as one line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap and the tram operator's own line map. Line colors are this
  project's own, not the operators'.
- Only stations inside Toyama City get rings, because the business data covers the city alone:
  lines running on to Imizu, Funahashi, Namerikawa, Kamiichi and Tateyama are cut at the city
  line.
- JR Central's part of the Takayama Line, whose only station in the city is Inotani, a station of
  JR West's line, is not drawn.
- The Shinkansen is not drawn (Toyama appears as a station of the lines above).
- **Tram stops sit closer together than metro stations**, a median of 443 m here, so the rings are
  drawn at half the usual size (0.05 to 0.3 mi).

**The businesses**

- From Toyama City's list of food-business permits (as of June 30, 2026) and its registers of
  barbers, beauty salons and laundries (as of March 2026).
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear: the Food shops layer is food retail only (bakeries and confectioners,
  delis, butchers and fishmongers).
- Food businesses that only notify the city rather than hold a permit, such as many convenience
  stores and greengrocers, are not in the list.
- The lists may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- The lists give an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where that fails, the dot sits at the ministry's
  own coordinates for the same premises, or else at its district's center.
- Where a trade name is its operator's own name, the dot shows its permit type instead; the city's
  lists name an operator only where it is a company, so this cannot be checked for the rest.
- Names and permit types are shown in Japanese, as the lists record them.
- **About half of storefronts sit within a ring.**
"""
)

render_map_help("three business categories (Food shops, Food service and Personal services)")
render_excluded_stations("Toyama")
render_country_links("Toyama")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Toyama")
