"""Moriguchi heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.moriguchi.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Moriguchi Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Moriguchi")
render_city_title("Moriguchi")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/moriguchi/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Moriguchi")

# From the japan-city skill's template and Kochi's page (approved wording: a
# full list plus monthly new premises, barbers and beauty salons only); the
# sentences they do not cover (the prefecture as publisher, no food list) are
# proposals in docs/decisions_drafts/worktree-japan-kansai-2.md. The as-of
# dates are the lists' own (config.SOURCE_AS_OF; the register pinned at
# config.REGISTERS_AS_OF). The ring share is step 3's (2026-10-11).
st.markdown(
    """
**The lines**

- Three lines are drawn, each labeled on the map and in the legend: the Keihan Main Line and
  Osaka Metro's Tanimachi Line and Imazatosuji Line, which has one station in the city, at
  Taishibashi-Imaichi.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Moriguchi City get rings, because the business data covers the city alone:
  lines running on to Osaka, Kadoma and Neyagawa are cut at the city line. The stations left out
  are listed below.
- The Osaka Monorail, which has one station in the city, is not drawn: Dainichi keeps its rings
  through the Tanimachi Line.
- **Stations sit close together here**, a median of 371 m apart, so the rings are drawn at half
  the usual size (0.05 to 0.3 mi).

**The businesses**

- **This map shows personal services only: barbers and beauty salons.**
- Osaka Prefecture, which licenses Moriguchi's premises, publishes no list of laundries, so they
  are not on this map.
- Restaurants, cafés and shops are not on this map either: neither the prefecture nor the city
  publishes a list of food-business permits for Moriguchi.
- Barbers and beauty salons come from Osaka Prefecture's complete lists as of March 31, 2026 and
  the new premises listed each month since, to August 31, 2026.
- The prefecture lists new premises each month but not closures, so a premises that closed after
  March is still counted. The map shows an upper bound, and a dot is a premises on the lists, not
  necessarily one open today.

**Reading the map**

- The lists give an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where only the district can be found, the dot
  sits at the district's center.
- Where a business's trade name is its operator's own name, the dot shows its register type
  instead.
- Names and types are shown in Japanese, as the prefecture records them.
- **About half of the premises sit within a ring.**
"""
)

render_map_help("business layer")
render_excluded_stations("Moriguchi")
render_country_links("Moriguchi")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Moriguchi")
