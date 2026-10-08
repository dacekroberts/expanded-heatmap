"""Fuchū (Tokyo) heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py, in the
city-page format of 2026-10-01 (owner): title, map, captions, bullets, map help,
country links, notices.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.fuchu_tokyo.config import HEATMAP_HTML  # noqa: E402
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

st.set_page_config(page_title="Fuchū (Tokyo) Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Fuchū (Tokyo)")
render_city_title("Fuchū (Tokyo)")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/fuchu_tokyo/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Fuchū (Tokyo)")

# The shares the page states are the build's own (step 2 writes them to
# outputs/fuchu_tokyo/official_shares.json; never retyped, Tokyo's rule):
# at the yearbook's date, the end of March 2025 (calls 187-189).
_SHARES = {}
_SHARES_JSON = HEATMAP_HTML.parent / "official_shares.json"
if _SHARES_JSON.exists():
    _SHARES = {s["kind"]: s for s in json.loads(_SHARES_JSON.read_text(encoding="utf-8"))}


def _share(kind):
    s = _SHARES.get(kind)
    return f"{s['rows_at_date']:,} of {s['official']:,} ({s['share_at_date_pct']:.0f}%)" if s else "(not measured)"


# From the japan-city skill's template and Sasebo's and Tokyo's pages
# (approved wording, pre-approved for this build); the sentences no template
# covers (the ledgers' window and opt-outs, the shares at the yearbook's date) are proposals in
# docs/decisions_drafts/worktree-japan-east-1.md. The ring share, 88.9% (2,300 of 2,586), is step 3's.
st.markdown(
    """
**The lines**

- Five lines are drawn, each labeled on the map and in the legend: the Keio Line and Keio Keibajo
  Line, JR East's Nambu and Musashino lines, and the Seibu Tamagawa Line.
- Lines and stations come from MLIT's national railway data (国土数値情報); station names in
  English are from OpenStreetMap. Line colors are this project's own, not the operators'.
- Only stations inside Fuchū City get rings, because the business data covers the city alone: lines
  running on to Chofu, Tama, Kunitachi, Inagi, Kokubunji and Koganei are cut at the city line. The
  stations left out are listed below.

**The businesses**

- From the Tokyo Metropolitan Government's ledgers of food-business permits and notifications,
  barbers, beauty salons and laundries for the Tama area (as of August 31, 2026), and the Ministry
  of Health, Labour and Welfare's open data for the premises the ledgers lack (downloaded October
  6, 2026). A premises in both lists appears once.
- The ledgers hold new permits only since August 2019 and leave out premises whose operators asked
  not to be published, so they are not complete. Against Tokyo's official counts for the end of
  March 2025, they hold """
    + _share("restaurants") + """ of the city's restaurants, """ + _share("barber") + """ of its
  barbers, """ + _share("beauty") + """ of its beauty salons and """ + _share("laundry") + """ of
  its laundries.
- Japan has no general business license, so shops other than food shops (clothing, electronics,
  pharmacies) do not appear: the Food shops layer is food retail only (bakeries and confectioners,
  delis, butchers and fishmongers).
- Shops that only notify rather than hold a permit, such as supermarkets, convenience stores and
  greengrocers, appear where they notified since June 2021, so that part of the layer is partial.
- The lists may include premises that have closed, so a dot means a permit on file, not a business
  open today.

**Reading the map**

- The lists give an address but no location. Each address is matched to MLIT's address reference
  data, which places most at their street block; where only the district can be found, the dot
  sits at the district's center.
- Where a business's trade name is its operator's own name, the dot shows its permit type instead.
- Names and permit types are shown in Japanese, as the lists record them.
- **About 89% of storefronts sit within a ring.**
"""
)

render_map_help("three business categories (Food shops, Food service and Personal services)")
render_excluded_stations("Fuchū (Tokyo)")
render_country_links("Fuchū (Tokyo)")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Fuchū (Tokyo)")
