"""Nagasaki heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.nagasaki.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Nagasaki Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Nagasaki")
render_city_title("Nagasaki")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/nagasaki/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Nagasaki")

# From the japan-city skill's template and Hiroshima's and Matsuyama's pages
# (approved wording, pre-approved for this build, 2026-09-30); the sentences
# it does not cover are proposals in the Japan batch's drafts file. The as-of
# dates are dated from the lists' rows (config.SOURCE_AS_OF); MHLW's file
# states none, so it is dated by download (provenance.json). "One restaurant
# in four": 2,090 of 8,603 restaurant permits withhold their address (step 2's
# data, 2026-10-02). The median, 219 m, is step 1's.
st.markdown(
    """
**The lines**

- Two lines are drawn, each labeled on the map and in the legend: the Nagasaki Electric Tramway
  and JR Kyushu's Nagasaki Main Line.
- The tram's routes share most of their track, so the tram is drawn as one line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Nagasaki City get rings, because the business data covers the city alone: the
  line running on to Nagayo and Isahaya is cut at the city line. The stations left out are listed
  below.
- The Shinkansen is not drawn (Nagasaki appears as a station of the lines above).
- **Tram stops sit closer together than metro stations**, a median of 219 m here, so the rings are
  drawn at half the usual size (0.05 to 0.3 mi).

**The businesses**

- The food businesses come from two lists. Nagasaki City's own list is a snapshot of the
  food-business permits in force on 30 June 2023, the newest it publishes under an open license.
- Permits filed online go through the Ministry of Health, Labour and Welfare's system, whose open
  data is the second list (downloaded 2 October 2026) and carries the permits granted since. A
  premises in both lists appears once.
- The barbers, beauty salons and laundries come from the city's registers as of 31 March 2023;
  premises opened since then are not on this map.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear either.
- The Food shops layer is food retail only, and it is partial: shops that only notify rather than
  hold a permit, such as supermarkets, convenience stores and greengrocers, appear only where they
  chose to publish in the ministry's list.
- The lists may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- About one restaurant in four in Nagasaki chose not to publish its address in the national
  filing system and is not on this map. Where they are is not known.
- The rest are matched to MLIT's address reference data, which places most at their street block;
  where that fails for a ministry filing, the dot sits at the ministry's own coordinates.
- None of the lists says who a business's operator is, so where a trade name is its operator's own
  name, this cannot be checked here.
- Names and permit types are shown in Japanese, as the lists record them.
- **More than half of storefronts sit within a ring.**
"""
)

render_map_help("three business categories (Food shops, Food service and Personal services)")
render_excluded_stations("Nagasaki")
render_country_links("Nagasaki")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Nagasaki")
