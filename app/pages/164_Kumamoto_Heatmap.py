"""Kumamoto heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.kumamoto.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Kumamoto Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Kumamoto")
render_city_title("Kumamoto")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/kumamoto/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Kumamoto")

# From the japan-city skill's template and Hiroshima's and Matsuyama's pages
# (approved wording, pre-approved for this build, 2026-09-30); the sentences
# it does not cover are proposals in the Japan batch's drafts file. The as-of
# dates are the lists' own (config.SOURCE_AS_OF); MHLW's file states none, so
# it is dated by download (provenance.json). "About three in four": the two
# lists hold 7,053 of the official 9,229 restaurants (76.4%,
# outputs/kumamoto/official_shares.json, step 2, 2026-10-02). "One restaurant
# in 180": 40 of 7,051 restaurant permits withhold their address (step 2's
# data, 2026-10-02). The median, 362 m, is step 1's.
st.markdown(
    """
**The lines**

- Five lines are drawn, each labeled on the map and in the legend: the Kumamoto City Tram;
  Kumamoto Electric Railway's Kikuchi and Fujisaki lines; and JR Kyushu's Kagoshima and Hohi main
  lines.
- The city tram's routes share most of their track, so the tram is drawn as one line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Kumamoto City get rings, because the business data covers the city alone:
  lines running on to Koshi, Kikuyo, Gyokuto and Uto are cut at the city line. The stations left out
  are listed below.
- The Shinkansen is not drawn (Kumamoto appears as a station of the lines above).
- **Tram stops sit closer together than metro stations**, a median of 362 m here, so the rings are
  drawn at half the usual size (0.05 to 0.3 mi).

**The businesses**

- The food businesses come from two lists. Kumamoto City's own list holds every restaurant permit
  applied for at a city counter and in force on March 31, 2026, except those whose operators asked
  not to be listed.
- Permits filed online go through the Ministry of Health, Labour and Welfare's system, whose open
  data is the second list (downloaded October 2, 2026). A premises in both lists appears once.
- Together the two lists hold about three in four of the restaurants licensed in the city; food
  trucks and event stalls, which the official count includes, are not in them.
- The barbers, beauty salons and laundries come from the city's registers as of March 31, 2026.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear either.
- The city's list holds restaurants only, so the Food shops layer comes from the ministry's list
  alone. It is food retail only, and it is partial: shops appear only where they chose to publish
  in the ministry's list.
- The lists may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- About one restaurant in 180 in Kumamoto chose not to publish its address in the national filing
  system and is not on this map. Where they are is not known.
- The rest are matched to MLIT's address reference data, which places most at their street block;
  where that fails for a ministry filing, the dot sits at the ministry's own coordinates.
- In the city's own lists, where a trade name is its operator's own name, the dot shows its permit
  type instead; the ministry's list does not say who the operator is, so this cannot be checked
  there.
- Names and permit types are shown in Japanese, as the lists record them.
- **About half of storefronts sit within a ring.**
"""
)

render_map_help("three business categories (Food shops, Food service and Personal services)")
render_excluded_stations("Kumamoto")
render_country_links("Kumamoto")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Kumamoto")
