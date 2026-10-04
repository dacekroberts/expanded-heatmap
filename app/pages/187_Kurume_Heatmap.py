"""Kurume heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.kurume.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Kurume Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Kurume")
render_city_title("Kurume")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/kurume/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Kurume")

# From the japan-city skill's template and Okayama's page (approved wording,
# pre-approved for this build, 2026-09-30); MHLW's name-rule bullet covers the
# whole page (Okayama's precedent, owner 2026-10-02). The sentence no template
# covers is a proposal in docs/decisions_drafts/japan-wave2.md (why there are
# no personal services). MHLW's file states no date, so it is dated by
# download. One restaurant in five withholds its address (867 of 3,900 open
# restaurant permits, 22.2%, 2026-10-03). The ring share, 63.2%, is step 3's.
st.markdown(
    """
**The lines**

- Four lines are drawn, each labeled on the map and in the legend: Nishitetsu's Tenjin Omuta and
  Amagi lines, and JR Kyushu's Kagoshima Main and Kyudai Main lines.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Kurume City get rings, because the business data covers the city alone:
  lines running on to Ogori, Tachiarai, Oki, Chikugo, Ukiha and Tosu are cut at the city line.
- The Shinkansen is not drawn (Kurume appears as a JR station).

**The businesses**

- **This map shows food businesses only.**
- Kurume City publishes only monthly lists of newly opened barbers and beauty salons, not a full
  register, and no list of laundries, so personal services are not on this map.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear either.
- The food businesses come from the Ministry of Health, Labour and Welfare's filing system, whose
  open data holds the permits and notifications Kurume City has recorded since June 2021
  (downloaded October 2, 2026). Permits granted before then and still in force are not in it.
- The Food shops layer is food retail only, and it is partial: shops that only notify rather than
  hold a permit, such as supermarkets, convenience stores and greengrocers, appear only where they
  chose to publish in the ministry's list.
- The list may include premises that have closed, so a dot means a permit on file, not a business
  open today.

**Reading the map**

- About one restaurant in five in Kurume chose not to publish its address in the national filing
  system and is not on this map. Where they are is not known.
- The rest are matched to MLIT's address reference data, which places most at their street block;
  where that fails, the dot sits at the ministry's own coordinates.
- The ministry's list does not say who the operator is, so a trade name that is its operator's own
  name cannot be checked here.
- Names and permit types are shown in Japanese, as the list records them.
- **About 63% of storefronts sit within a ring.**
"""
)

render_map_help("two business categories (Food shops and Food service)")
render_excluded_stations("Kurume")
render_country_links("Kurume")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Kurume")
