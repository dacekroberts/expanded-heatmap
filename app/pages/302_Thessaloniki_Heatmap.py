"""Thessaloniki heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.thessaloniki.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_caption,
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Thessaloniki Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Thessaloniki")
render_city_title("Thessaloniki")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/thessaloniki/step3_map.py` to generate it.")

# The licence layer's retrieval date and the rail's OSM date, read from
# outputs/thessaloniki/provenance.json so they cannot go stale on the next
# fetch. The layer publishes no date of its own (owner, 2026-10-04: the page
# gives the retrieval date and never calls the data current or complete).
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _lic = ((_prov.get("licences") or {}).get("retrieved") or "")[:10]
        _rail = ((_prov.get("osm") or {}).get("osm_base") or "")[:10]
        if _lic and _rail:
            render_caption(f"Shop-license data from the City of Thessaloniki (CC BY 4.0), retrieved "
                           f"**{_lic}**; the layer publishes no date of its own. The metro line and "
                           f"its stations from OpenStreetMap, fetched **{_rail}**.")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

# Matsuyama's page shape (three layers, food shops as a partial Retail layer),
# filled from Thessaloniki's own step 1 to step 3 figures. Sentences no template
# covers are proposals in docs/decisions_drafts/worktree-abroad-batch.md, for
# review time: the color clause, the branch bullet, the frequency bullet and
# the license-layer bullets.
st.markdown(
    """
**The lines**

- One line is drawn, **Line 1** of the Thessaloniki Metro, labeled on the map and in the legend.
- The line and its stations come from OpenStreetMap. The line's color is OpenStreetMap's, not the
  operator's.
- Only the 13 stations inside the Municipality of Thessaloniki get rings, because the business
  data covers the city alone. The Kalamaria branch is cut at the city line; its five stations,
  Nomarchia to Mikra, are listed below.
- Trains run about every 3 minutes between New Railway Station and 25th Martiou for most of the
  day, and about every 9 minutes on to Nea Elvetia.

**The businesses**

- From the City of Thessaloniki's register of shops holding an active license, retrieved October
  4, 2026. The layer publishes no date of its own, so a dot means a license on file, not a
  business open today.
- The register licenses food premises, hairdressers and beauty salons, so shops other than food
  shops (clothing, electronics, pharmacies) do not appear: the Food shops layer is food retail
  only.
- Convenience stores, patisseries, and bread shops and coffee roasters selling coffee to go count
  as Food shops; canteens inside offices, schools and other premises are left out.

**Reading the map**

- A dot shows the type of business, never its name: the register carries no names. The licensed
  activity is shown in Greek as the register records it.
- **Nearly nine storefronts in ten sit within a ring.**
"""
)

render_map_help("three business categories (Food shops, Food service and Personal services)")
render_excluded_stations("Thessaloniki")
render_country_links("Thessaloniki")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices("Thessaloniki")
