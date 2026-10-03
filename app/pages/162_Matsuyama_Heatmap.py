"""Matsuyama heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.matsuyama.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Matsuyama Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Matsuyama")
render_city_title("Matsuyama")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/matsuyama/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Matsuyama")

# From the japan-city skill's template and Hiroshima's page (approved wording,
# pre-approved for this build, 2026-09-30); the sentences it does not cover are
# proposals in docs/decisions_drafts/japan-batch.md. The as-of date is the
# lists' own (config.SOURCE_AS_OF); MHLW's file states none, so it is dated by
# download. The tram stops' median, 374 m, is step 1's (2026-10-02).
st.markdown(
    """
**The lines**

- Five lines are drawn, each labeled on the map and in the legend: Iyotetsu's city tram, its
  Takahama, Yokogawara and Gunchu lines, and JR Shikoku's Yosan Line.
- The city tram's routes share most of their track, so the tram is drawn as one line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Matsuyama City get rings, because the business data covers the city alone:
  lines running on to Toon and Masaki are cut at the city line. The stations left out are listed
  below.
- **Tram stops sit closer together than metro stations**, a median of 374 m here, so the rings are
  drawn at half the usual size (0.05 to 0.3 mi).

**The businesses**

- From Matsuyama City's lists of food-business permits and of barbers, beauty salons and
  laundries, all as of 31 March 2026.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear: the Food shops layer is food retail only (bakeries and confectioners,
  delis, butchers and fishmongers).
- Shops that only notify rather than hold a permit, such as supermarkets, convenience stores and
  greengrocers, appear only where they chose to publish in the Ministry of Health, Labour and
  Welfare's open data (downloaded 2 October 2026), so that part of the Food shops layer is partial.
- The lists may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- The lists give an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where that fails, the dot sits at the ministry's
  own coordinates for the same premises, or else at its district's center.
- In the city's own lists, where a trade name is its operator's own name, the dot shows its permit
  type instead; the ministry's list does not say who the operator is, so this cannot be checked
  there.
- Names and permit types are shown in Japanese, as the lists record them.
- **About half of storefronts sit within a ring.**
"""
)

render_map_help("three business categories (Food shops, Food service and Personal services)")
render_excluded_stations("Matsuyama")
render_country_links("Matsuyama")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Matsuyama")
