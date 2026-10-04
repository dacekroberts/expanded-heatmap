"""Higashiōsaka heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.higashiosaka.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Higashiōsaka Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Higashiōsaka")
render_city_title("Higashiōsaka")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/higashiosaka/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Higashiōsaka")

# From the japan-city skill's template and Sakai's, Kyoto's and Kawasaki's
# pages (approved wording, pre-approved for this build, 2026-09-30); the
# sentences they do not cover are proposals in
# docs/decisions_drafts/japan-wave2.md. The dates are the rebuilt register's
# (config.SOURCE_AS_OF and AS_OF). The ring share, 90.4%, is step 3's (5,218
# of 5,775, 2026-10-03).
st.markdown(
    """
**The lines**

- Six lines are drawn, each labeled on the map and in the legend: Kintetsu's Nara, Osaka and
  Keihanna lines; Osaka Metro's Chuo Line; and JR West's Osaka Higashi and Gakkentoshi lines.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Higashiōsaka City get rings, because the business data covers the city
  alone: lines running on to Osaka, Yao, Daito and Ikoma are cut at the city line.

**The businesses**

- **This map shows food businesses only.**
- Higashiōsaka City publishes no list of barbers, beauty salons or laundries, so personal services
  are not on this map.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear either: the Food shops layer is food retail only (bakeries and
  confectioners, delis, butchers and fishmongers).
- The food businesses are rebuilt from Higashiōsaka City's list of food-business permits as of April
  1, 2026 and its monthly lists of new permits since, keeping each permit still within its term
  on August 31, 2026, the last date the newest monthly list covers.
- The city does not publish closures, so a business that closed before its permit ran out is still
  counted. The map shows an upper bound, and a dot means a permit on file, not a business open
  today.
- Food businesses that only notify the city rather than hold a permit, such as many convenience
  stores and greengrocers, are not in the list.

**Reading the map**

- The list gives an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where only the district can be found, the dot
  sits at the district's center.
- The list names an operator only where it is a company, so a trade name that is its operator's
  own name cannot be checked here.
- Names and permit types are shown in Japanese, as the city records them.
- **About nine in ten storefronts sit within a ring.**
"""
)

render_map_help("two business categories (Food shops and Food service)")
render_excluded_stations("Higashiōsaka")
render_country_links("Higashiōsaka")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Higashiōsaka")
