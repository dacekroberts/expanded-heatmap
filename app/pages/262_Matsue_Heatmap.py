"""Matsue heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.matsue.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Matsue Heatmap | Global Transit-Business Atlas", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Matsue")
render_city_title("Matsue")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/matsue/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Matsue")

# From the japan-city skill's template, Yokohama's one-bucket line, Kakogawa's
# coordinates bullet with both shares (owner's call 183) and Aomori's
# low-frequency bullet (approved wording, pre-approved for this build,
# 2026-09-30). Four bullets adapt an approved sentence of another page or are
# new, and are listed as proposals in
# docs/decisions_drafts/worktree-japan-regional-2.md: the Kisuki Line's
# frequency, the food bullet, the source bullet with its closure sentence, and
# the rural towns' sentence. The date is config.REGISTERS_AS_OF; the tiers are
# step 2's (776 and 158 of 948 rows); the ring share, 32.5%, is step 3's (299
# of 919).
st.markdown(
    """
**The lines**

- Three lines are drawn, each labeled on the map and in the legend: JR West's San'in and Kisuki
  lines and the Ichibata Electric Railway's Kita-Matsue Line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Matsue City get rings, because the business data covers the city alone:
  lines running on to Izumo, Yasugi and Unnan are cut at the city line. The stations left out are
  listed below.
- The JR Kisuki Line is infrequent: 10 trains a weekday run toward Kisuki and 11 toward Shinji.

**The businesses**

- **This map shows personal services only: barbers, beauty salons and laundries.**
- Restaurants, cafés and shops are not on this map: Matsue City's own list of food businesses is
  not open data, and the national list holds only about 2% of the city's restaurants.
- From Matsue City's registers of barbers, beauty salons and laundries (as of August 31, 2026).
- The registers may include premises that have closed, so a dot is a premises on the registers,
  not necessarily one open today.

**Reading the map**

- The registers give an address but no location. Each address is matched to MLIT's address
  reference data: about 82% reach their street block, and about 17%, where only the district can
  be found, sit at the district's center.
- MLIT's data holds almost no street blocks in the rural towns that joined the city in 2005
  (Kashima, Shimane, Mihonoseki, Yakumo and Yatsuka), so the 90 premises there sit at the center
  of a district that can be large.
- Where a business's trade name is its operator's own name, the dot shows its register type
  instead.
- Names and types are shown in Japanese, as the city records them.
- **About 33% of the premises sit within a ring.**
"""
)

render_map_help("business layer", search='matsue')
render_excluded_stations("Matsue")
render_country_links("Matsue")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Matsue")
