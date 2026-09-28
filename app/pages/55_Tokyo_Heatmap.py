"""Tokyo heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Kyoto's page, with one addition: the table of
each ward's share of the official restaurant count, READ from the build's
outputs/tokyo/official_shares.json and the roster's notes, never typed (owner
2026-09-28: a share the page states must be the one the build measured).
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.tokyo.config import HEATMAP_HTML, OUTPUTS  # noqa: E402
from pipeline.tokyo.wards import WARDS  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Tokyo Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Tokyo")

st.title("Tokyo: commercial density around rail stations")

# Prose approved by the owner 2026-09-28.
st.markdown(
    """
Fifty-two lines are drawn, each marked on the map by its operator's line code (JY, G, A…) and
named in full in the legend: JR East's Yamanote, Keihin-Tohoku, Chuo Rapid, Chuo-Sobu,
Yokosuka / Sobu Rapid, Keiyo, Joban, Saikyo and Utsunomiya / Takasaki lines; Tokyo Metro's nine
lines; Toei's four subway lines, the Tokyo Sakura Tram and the Nippori-Toneri Liner; and the
lines of Tokyu, Keio, Odakyu, Seibu, Tobu, Keisei and Keikyu, the Hokuso Line, the Tsukuba
Express, the Rinkai Line, the Yurikamome and the Tokyo Monorail. JR East's lines are drawn as the
services riders use, so where two share track, one is drawn over the other; the Tokaido and
Shonan-Shinjuku lines run in the wards only on track drawn here, and are not drawn separately.
Lines and stations come from MLIT's national railway data (国土数値情報); station names in English
are from OpenStreetMap, spelled as on the operators' signs. Only stations inside the 23 special
wards count, because the business data covers the wards alone: lines running on into Saitama,
Chiba, Kanagawa and the Tama area are cut at the ward line. The Shinkansen is not drawn, nor are
the Narita Sky Access and the Saitama Railway, each with a single station in the wards that other
lines serve. Line colours are this project's own, not the operators'.

Each of the 23 special wards runs its own health centre and publishes its own list of
food-business permits, or none. Eight publish a list usable here: Chuo, Minato, Shinjuku, Taito,
Koto, Meguro, Setagaya and Shibuya. The other fifteen publish no usable list: some only on
request or for viewing in person, some only as PDFs under terms that bar reuse, some only new
permits or an out-of-date list, and some none at all. Their stations are drawn hollow, without
rings, and a business near a ward edge is counted to the nearest station in a ward with data.

**The eight lists differ in how complete they are.** Each ward's list, against the official count
of restaurant permits in that ward:
"""
)

shares = OUTPUTS / "official_shares.json"
if shares.exists():
    by_code = {c: w for c, w in WARDS.items()}
    rows = sorted(json.loads(shares.read_text(encoding="utf-8")), key=lambda r: -r["share_pct"])
    table = ["| Ward | Restaurant permits in the list | Official count | Share | The list |",
             "|---|---:|---:|---:|---|"]
    for r in rows:
        w = by_code[r["code"]]
        table.append(f"| {w['en']} | {r['rows']:,} | {r['official']:,} | {r['share_pct']:.1f}% | {w['share_note']} |")
    st.markdown("\n".join(table))
    st.caption(f"Official count: {rows[0]['source']}.")

st.markdown(
    """
For Chuo, Minato, Shinjuku and Koto, the national online filing system's open data is added; it
holds only filings whose applicants agreed to publish them, and adds 0.1 to 3.1 points. A premises
in both lists is shown once.

The lists' dates differ: Shibuya's runs to 2 September 2026, Minato's to 31 July 2026, Meguro's is
as of 1 April 2026, Taito's and Setagaya's 31 March 2026, and Shinjuku's 1 January 2023; Chuo's
and Koto's hold only permits of 2021 and 2022. A dot means a permit on file, not a business open
today.

Barbers, beauty salons and laundries come from the registers of Minato, Taito, Meguro and Shibuya.
Seven more wards publish such registers, but a ward without a food list stays hollow, because food
is most of what a station counts. Japan has no general business licence, so shops other than food
shops do not appear. The Retail layer is food retail only, by permit type: bakeries and
confectioners, delis, butchers and fishmongers. Shops selling only packaged food have filed a
notification rather than a permit since 2021, and appear only where a list includes
notifications. Food trucks, stalls and temporary permits are left out.

The lists give an address but no location. Each address is matched to MLIT's address reference
data, which places 99.7% at their street block; where only the town can be found, the dot sits at
its centre, and a national filing that does not match is placed at its own coordinates. Where a
trade name is its operator's own name, the dot shows its permit type instead. Most of the lists
name only companies, and two wards withhold individual operators' names themselves, so this check
covers only the lists that name their operators. Names and permit types are shown in Japanese, as
the wards record them.

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
    st.info("No map yet. Run `python pipeline/tokyo/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
