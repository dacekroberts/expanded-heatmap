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
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Osaka Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Osaka")

st.title("Osaka: commercial density around rail stations")

# Prose approved by the owner 2026-09-28. The 70% paragraph is the owner's
# wording of 2026-09-24 (docs/build_briefs/osaka.md), verbatim. The as-of
# dates are the lists' own (config.FOOD_AS_OF, config.REGISTERS_AS_OF).
st.markdown(
    """
Thirty-four lines are drawn, each labelled on the map and in the legend: Osaka Metro's Midōsuji,
Tanimachi, Yotsubashi, Chūō, Sennichimae, Sakaisuji, Nagahori Tsurumi-ryokuchi and Imazatosuji
lines and the New Tram; JR West's Osaka Loop, JR Kyoto, JR Kobe, JR Tōzai, JR Gakkentoshi, Osaka
Higashi, JR Yumesaki, JR Yamatoji and JR Hanwa lines; Hankyu's Kobe, Takarazuka, Kyoto and Senri
lines; Hanshin's Main and Namba lines; Keihan's Main and Nakanoshima lines; Kintetsu's Namba, Osaka
and Minami-Osaka lines; Nankai's Main, Kōya and Shiomibashi lines; and the Hankai tram's Hankai and
Uemachi lines. Lines and stations come from MLIT's national railway data (国土数値情報); station
names in English are from OpenStreetMap, and two it lacks are the operators' own. Only stations
inside Osaka City get rings, because the business data covers the city alone: lines running on to
Sakai, Higashiōsaka, Suita, Yao, Moriguchi and beyond are cut at the city line. The Shinkansen is
not drawn (Shin-Osaka appears as a JR and Metro station), nor is the track from Osaka Station's
Umekita platforms to Fukushima, which only limited expresses use. Line colours are this project's
own, not the operators'; with this many lines, a few labels stand a little off their line.

Businesses come from Osaka City's list of food-business permits (as of 30 June 2026) and its
registers of barbers, beauty salons and laundries (as of 31 March 2026). Japan has no general
business licence, so shops other than food shops — clothing, electronics, pharmacies — do not
appear: the Food shops layer is food retail only (bakeries and confectioners, delis, butchers and
fishmongers). Food businesses that only notify the city rather than hold a permit, such as many
convenience stores and greengrocers, are not in the list, nor are linen-supply laundries, which
serve hotels and hospitals rather than the public. The list may include premises that have closed,
so a dot means a permit on file, not a business open today. Food trucks and stalls registered to
trade anywhere in the city have no fixed place and are left out.

Osaka City's published list holds about 70% of the restaurant permits Osaka reports to national
statistics. Most of the difference appears to be expired permits still counted nationally; the
rest, about a tenth of the count, are permits the city counts but does not list, some of them
short-lived event permits. The city has not confirmed either.

The list gives an address but no location. Each address is matched to MLIT's address reference
data, which places nearly all at their street block; where only the district can be found, the dot
sits at the district's centre. A handful of addresses cannot be placed. Where a business's trade
name is its operator's own name, the dot shows its permit type instead. Names and permit types are
shown in Japanese, as the city records them.

Concentric ring boundaries and the three business categories (Retail, Food
service and Personal services) are toggleable via the layer control in the top
left. When enabled, business density will display as numbered circles summing
areas when zoomed out. Zooming in will show individual dots; hover over those
to see further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a
statistical density estimate, so read the colour as "roughly where things
cluster."
"""
)

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/osaka/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
