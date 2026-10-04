"""Kitakyushu heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.kitakyushu.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Kitakyushu Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Kitakyushu")
render_city_title("Kitakyushu")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/kitakyushu/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Kitakyushu")

# From the japan-city skill's template and Fukuoka's page (approved wording,
# pre-approved for this build, 2026-09-30); the sentences it does not cover are
# proposals in the batch's drafts file. The as-of dates are the lists' own
# (config.SOURCE_AS_OF); MHLW's file states none, so it is dated by download.
# One restaurant in seven withholds its address in MHLW's file (1,484 of
# 10,760 open permits, 2026-10-02). The ring share, 71.1%, is step 3's.
st.markdown(
    """
**The lines**

- Eight lines are drawn, each labeled on the map and in the legend: the Kitakyushu Monorail; the
  Chikuho Electric Railroad; and JR Kyushu's Kagoshima Main, Nippo Main, Hitahikosan, Wakamatsu,
  Fukuhoku Yutaka and Sanyo lines.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Kitakyushu City get rings, because the business data covers the city alone:
  JR and Chikuho lines running on to Nakama, Nogata, Mizumaki, Onga, Kurate, Kanda, Kawara and
  Shimonoseki are cut at the city line. The stations left out are listed below.
- The Shinkansen is not drawn (Kokura appears as a JR and Monorail station).
- The Sarakurayama cable car and the Mojiko Retro sightseeing train, which are sightseeing lines,
  are not drawn.
- Nishi-Kurosaki on the Chikuho line closed on July 31, 2026 and is not shown.

**The businesses**

- From two food lists and two registers. Kitakyushu City's own list holds food-business permits
  granted before June 2021 (as of March 31, 2026), shown where still in term at the end of August
  2026.
- Permits since then are filed through the Ministry of Health, Labour and Welfare's system, whose
  open data is the second list (downloaded October 2, 2026). A premises in both lists appears once.
- Barbers and beauty salons come from the city's registers as of August 31, 2026. The city publishes
  no list of laundries, so laundries are not on this map.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear.
- The Food shops layer is food retail only, and it is partial: shops that only notify rather than
  hold a permit, such as supermarkets, convenience stores and greengrocers, appear only where they
  chose to publish in the ministry's list.
- The lists may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- About one restaurant in seven in Kitakyushu chose not to publish its address in the national
  filing system and is not on this map. Where they are is not known.
- The rest are matched to MLIT's address reference data, which places most at their street block;
  where that fails for a ministry filing, the dot sits at the ministry's own coordinates.
- The city's lists name an operator only where it is a company, and the ministry's list does not
  say who the operator is, so a trade name that is a sole trader's own name cannot be checked here.
- Names and permit types are shown in Japanese, as the lists record them.
- **About 71% of storefronts sit within a ring.**
"""
)

render_map_help("three business categories (Food shops, Food service and Personal services)")
render_excluded_stations("Kitakyushu")
render_country_links("Kitakyushu")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Kitakyushu")
