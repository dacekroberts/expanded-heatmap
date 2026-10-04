"""Aarhus heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.aarhus.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
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

st.set_page_config(page_title="Aarhus Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Aarhus")
render_city_title('Aarhus')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/aarhus/step3_map.py` to generate it.")

# The snapshot dates, read from outputs/aarhus/provenance.json so they cannot
# go stale: the CVR weekly generation the join was built on (the national
# cache Copenhagen fetched; Virksomhed carries Datafordeler's generation time)
# and the date the OSM address-point file was taken.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _times = sorted(v.get("generation_time") or ""
                        for k, v in (_prov.get("datafordeler") or {}).items()
                        if k.startswith("cvr/") and v.get("generation_time"))
        _points = (((_prov.get("osm") or {}).get("address_points") or {})
                   .get("file_utc") or "")[:10]
        if _times and _points:
            render_caption(f"Business and address data from Datafordeler's weekly "
                       f"extracts, generated **{_times[0][:10]}**; address points "
                       f"from OpenStreetMap, fetched **{_points}**.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# Approved by the owner 2026-09-29 (Copenhagen's text, with Aarhus's network,
# its 15-minute light-rail test and the franchisee-name rule); set as bullets
# 2026-10-01.
st.markdown(
    """
**The Letbane**

- **Letbane line L2** is drawn on the stretch built as a city tramway: from Aarhus H through
  Nørreport, the university and Skejby to Lisbjerg and Lystrup, with its short branch to
  Lisbjergskolen.
- It is labeled on the map and in the legend, and redrawn from OpenStreetMap's route geometry in
  the color OpenStreetMap records for the Letbane.
- Line L1 shares its first stops, Aarhus H to Skolebakken, and also serves Lystrup.
- The Letbane also runs beyond the city tramway on two converted railway lines, south to Odder and
  north-east to Grenaa, and those are not drawn. Midttrafik's own timetables show trains there
  every 30 minutes by day, against every 7 to 8 minutes on the city tramway, and this site draws
  light rail only where it runs at least every 15 minutes.
- Their 19 stops inside the municipality and the 11 beyond it are listed below.
- **The station rings are smaller here.** The tramway's stops sit about 500 m apart, so the rings
  run to 0.3 mi instead of the 0.6 mi most cities here use.
- The map covers the **municipality of Aarhus**.

**The businesses**

- Businesses come from Denmark's **Central Business Register** (Det Centrale
  Virksomhedsregister, CVR), and specifically from its production units: each place where a
  business operates, recorded at that place's own address rather than its company's.
- Each is placed at its address in Denmark's official address register, Danmarks
  Adresseregister, using the address points OpenStreetMap carries for it.
- **Where a business is owned personally (a sole proprietorship, a partnership or any business
  whose registered name marks it as one person's), the map shows its address instead of its
  name**, because such businesses are usually registered under the owners' own names. So does a
  supermarket registered under its franchisee's own name.
- One broad category, *other personal services*, is left out, because most of it is people
  working from their own premises; it also holds the city's tattoo studios, which are therefore
  missing from the map.
- **About one storefront in four sits within a ring.**

**Reading the density**

- **Read the density as a register, not a street survey.** Some premises are newly registered and
  may not have opened yet.
- Denmark's classification files a web shop under the goods it sells, so some dots are businesses
  with no shop a passer-by could walk into, and nothing in the data says which.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Aarhus")
render_country_links('Aarhus')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Aarhus")
