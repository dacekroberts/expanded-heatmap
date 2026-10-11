"""Uji heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.uji.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Uji Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Uji")
render_city_title("Uji")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/uji/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Uji")

# From the japan-city skill's template and Kurume's page (approved wording,
# pre-approved for this build); the sentences it does not cover (the
# prefecture's file cut by address, the withheld share measured
# prefecture-wide, the Tōzai Line left out) are proposals in
# docs/decisions_drafts/worktree-japan-kansai-1.md. The withheld share is the
# brief's (1,007 of 7,151 fixed open restaurants outside Kyoto City publish no
# address); the ring share, 56.4%, is step 3's (723 of 1,281, on the halved
# rings).
st.markdown(
    """
**The lines**

- Three lines are drawn, each labeled on the map and in the legend: JR West's Nara Line, Keihan's
  Uji Line and Kintetsu's Kyoto Line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Uji City get rings, because the business data covers the city alone: lines
  running on to Kyoto and Joyo are cut at the city line. The stations left out are
  listed below.
- The Kyoto Municipal Subway's Tōzai Line, which ends at Rokujizo, is not drawn: Rokujizo keeps its
  rings through the JR Nara Line.
- **Stations sit close together here**, a median of 505 m apart, so the rings are drawn at half
  the usual size (0.05 to 0.3 mi).

**The businesses**

- **This map shows food businesses only.**
- Kyoto Prefecture publishes its lists of barbers, beauty salons and laundries only as documents
  whose reuse needs its permission, so personal services are not on this map.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear either.
- The food businesses come from the Ministry of Health, Labour and Welfare's filing system, whose
  open data holds the permits and notifications Kyoto Prefecture has recorded since June 2021
  (downloaded October 6, 2026); each is placed in Uji by its address. Permits granted before then
  and still in force are not in it.
- The Food shops layer is food retail only, and it is partial: shops that only notify rather than
  hold a permit, such as supermarkets, convenience stores and greengrocers, appear only where they
  chose to publish in the ministry's list.
- The list may include premises that have closed, so a dot means a permit on file, not a business
  open today.

**Reading the map**

- About one restaurant in seven in Kyoto Prefecture's filings (outside Kyoto City) chose not to
  publish its address in the national filing system, so some in Uji are not on this map. Where
  they are is not known.
- The rest are matched to MLIT's address reference data, which places most at their street block;
  where that fails, the dot sits at the ministry's own coordinates.
- Where a business's trade name is its operator's own name, the dot shows its permit type instead.
- Names and permit types are shown in Japanese, as the list records them.
- **About 56% of storefronts sit within a ring.**
"""
)

render_map_help("two business categories (Food shops and Food service)")
render_excluded_stations("Uji")
render_country_links("Uji")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Uji")
