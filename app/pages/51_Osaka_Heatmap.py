"""Osaka heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.osaka.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_data_age,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Osaka Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Osaka")
render_city_title('Osaka')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/osaka/step3_map.py` to generate it.")

render_data_age('Osaka')

# Prose approved by the owner 2026-09-28; set as bullets 2026-10-01. The 70%
# bullets are the owner's wording of 2026-09-24 (docs/build_briefs/osaka.md),
# verbatim. The as-of dates are the lists' own (config.FOOD_AS_OF,
# config.REGISTERS_AS_OF).
st.markdown(
    """
**The lines**

- Thirty-four lines are drawn, each labeled on the map and in the legend: Osaka Metro's Midōsuji,
  Tanimachi, Yotsubashi, Chūō, Sennichimae, Sakaisuji, Nagahori Tsurumi-ryokuchi and Imazatosuji
  lines and the New Tram; JR West's Osaka Loop, JR Kyoto, JR Kobe, JR Tōzai, JR Gakkentoshi, Osaka
  Higashi, JR Yumesaki, JR Yamatoji and JR Hanwa lines; Hankyu's Kobe, Takarazuka, Kyoto and Senri
  lines; Hanshin's Main and Namba lines; Keihan's Main and Nakanoshima lines; Kintetsu's Namba,
  Osaka and Minami-Osaka lines; Nankai's Main, Kōya and Shiomibashi lines; and the Hankai tram's
  Hankai and Uemachi lines.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'; with
  this many lines, a few labels stand a little off their line.
- Only stations inside Osaka City get rings, because the business data covers the city alone: lines
  running on to Sakai, Higashiōsaka, Suita, Yao, Moriguchi and beyond are cut at the city line. The
  stations left out are listed below.
- The Shinkansen is not drawn (Shin-Osaka appears as a JR and Metro station), nor is the track
  from Osaka Station's Umekita platforms to Fukushima, which only limited expresses use.

**The businesses**

- From Osaka City's list of food-business permits (as of 30 June 2026) and its registers of
  barbers, beauty salons and laundries (as of 31 March 2026).
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear: the Food shops layer is food retail only (bakeries and confectioners,
  delis, butchers and fishmongers).
- Food businesses that only notify the city rather than hold a permit, such as many convenience
  stores and greengrocers, are not in the list.
- The list may include premises that have closed, so a dot means a permit on file, not a business
  open today.
- Osaka City's published list holds about 70% of the restaurant permits Osaka reports to national
  statistics.
- Most of the difference appears to be expired permits still counted nationally; the rest, about
  a tenth of the count, are permits the city counts but does not list, some of them short-lived
  event permits. The city has not confirmed either.

**Reading the map**

- The list gives an address but no location. Each address is matched to MLIT's address reference
  data, which places nearly all at their street block; where only the district can be found, the
  dot sits at the district's center.
- Where a business's trade name is its operator's own name, the dot shows its permit type instead.
- Names and permit types are shown in Japanese, as the city records them.
"""
)

render_map_help('three business categories (Food shops, Food service and Personal services)')
render_excluded_stations("Osaka")
render_country_links('Osaka')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Osaka")
