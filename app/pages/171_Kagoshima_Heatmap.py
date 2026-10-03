"""Kagoshima heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.kagoshima.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Kagoshima Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Kagoshima")
render_city_title("Kagoshima")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/kagoshima/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Kagoshima")

# From the japan-city skill's template and Hiroshima's and Fukuoka's pages
# (approved wording, pre-approved for this build, 2026-09-30); the sentences
# it does not cover are proposals in the batch's drafts file. The as-of date is
# the city list's own (config.SOURCE_AS_OF); MHLW's file states none, so it is
# dated by download. One restaurant in four withholds its address in MHLW's
# file (1,397 of 5,914 open permits, 2026-10-02). The stops' median, 272 m,
# and the ring share, 60.4%, are steps 1 and 3's (2026-10-02).
st.markdown(
    """
**The lines**

- Four lines are drawn, each labeled on the map and in the legend: the Kagoshima City Tram; and JR
  Kyushu's Ibusuki Makurazaki, Kagoshima Main and Nippo Main lines.
- The city tram's two routes are drawn as one line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Kagoshima City get rings, because the business data covers the city alone: JR
  lines running on to Hioki, Aira and Ibusuki are cut at the city line. The stations left out are
  listed below.
- The Shinkansen is not drawn (Kagoshima-Chuo appears as a JR station).
- **Tram stops sit closer together than metro stations**, a median of 272 m here, so the rings are
  drawn at half the usual size (0.05 to 0.3 mi).

**The businesses**

- **This map shows food businesses only.**
- Kagoshima City publishes only its new barbers and beauty salons, a year at a time, and no list of
  laundries, so personal services are not on this map.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear either.
- The food businesses come from two lists. Kagoshima City's own list holds food-business permits
  granted before June 2021 and still held (as of 30 June 2026).
- Permits since then are filed through the Ministry of Health, Labour and Welfare's system, whose
  open data is the second list (downloaded 2 October 2026). A premises in both lists appears once.
- The Food shops layer is food retail only, and it is partial: shops that only notify rather than
  hold a permit, such as supermarkets, convenience stores and greengrocers, appear only where they
  chose to publish in the ministry's list.
- The lists may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- About one restaurant in four in Kagoshima chose not to publish its address in the national
  filing system and is not on this map. Where they are is not known.
- The rest are matched to MLIT's address reference data, which places most at their street block;
  where that fails for a ministry filing, the dot sits at the ministry's own coordinates.
- In the city's own list, where a trade name is its operator's own name, the dot shows its permit
  type instead; the ministry's list does not say who the operator is, so this cannot be checked
  there.
- Names and permit types are shown in Japanese, as the lists record them.
- **About 60% of storefronts sit within a ring.**
"""
)

render_map_help("two business categories (Food shops and Food service)")
render_excluded_stations("Kagoshima")
render_country_links("Kagoshima")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Kagoshima")
