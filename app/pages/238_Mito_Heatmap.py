"""Mito heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.mito.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Mito Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Mito")
render_city_title("Mito")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/mito/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Mito")

# From the japan-city skill's template, Kurume's page (the ministry's filings
# as the food source, the withheld addresses) and Akita's and Ichinomiya's
# pages (the ministry's notifications and its points) (approved wording,
# pre-approved for this build, 2026-09-30); the two sentences no template
# covers are proposals in docs/decisions_drafts/worktree-japan-regional-1.md:
# Kairakuen's bullet (call 156) and the 91% clause (call 157, Ichinomiya's
# form). The registers' date is the lists' own (config.SOURCE_AS_OF); MHLW's
# file states no date, so it is dated by download. The food share: 2,892
# restaurant permits in term on 2026-08-31, 90.7% of e-Stat's 3,188; 469 of
# 2,542 on fixed premises (18.5%) withhold the address (2026-10-07). The ring
# share, 24.2%, is step 3's (977 of 4,040, 2026-10-07).
st.markdown(
    """
**The lines**

- Three lines are drawn, each labeled on the map and in the legend: JR East's Joban and Suigun
  lines and Kashima Rinkai's Oarai Kashima Line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Mito City get rings, because the business data covers the city alone:
  lines running on to Kasama, Hitachinaka, Naka and Oarai are cut at the city line. The stations
  left out are listed below.
- Kairakuen, a seasonal station on the JR Joban Line, has no train in the current timetable and is
  not shown.

**The businesses**

- From Mito City's registers of barbers, beauty salons and laundries (as of July 2, 2026).
- The food businesses come from the Ministry of Health, Labour and Welfare's filing system, whose
  open data holds the permits and notifications Mito City has recorded since June 2021
  (downloaded October 6, 2026). Permits granted before then and still in force are not in it, so
  it holds about 91% of the restaurant permits in the official count.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear: the Food shops layer is food retail only (bakeries and confectioners,
  delis, butchers and fishmongers).
- Shops that only notify rather than hold a permit, such as supermarkets, convenience stores and
  greengrocers, appear only where they chose to publish in the ministry's list, so that part of the
  Food shops layer is partial.
- The lists may include premises that have closed, so a dot means a permit on file, not a
  business open today.

**Reading the map**

- About one restaurant in five in Mito chose not to publish its address in the national filing
  system and is not on this map. Where they are is not known.
- The lists give an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where that fails, the dot sits at the ministry's
  own coordinates for the same premises, or else at its district's center.
- Where a trade name is its operator's own name, the dot shows its permit type instead.
- Names and permit types are shown in Japanese, as the lists record them.
- **About 24% of storefronts sit within a ring.**
"""
)

render_map_help("three business categories (Food shops, Food service and Personal services)")
render_excluded_stations("Mito")
render_country_links("Mito")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Mito")
