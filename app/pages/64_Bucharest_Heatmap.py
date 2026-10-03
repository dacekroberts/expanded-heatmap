"""Bucharest heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.bucharest.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Bucharest Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Bucharest")
render_city_title('Bucharest')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/bucharest/step3_map.py` to generate it.")

# The registers' own date, read from outputs/bucharest/provenance.json so it
# cannot go stale on the next fetch.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _date = _prov.get("register_date")
        if _date:
            st.caption(f"Snapshot: DSVSA București's registers as published on **{_date}**.")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

# Approved by the owner 2026-09-29; set as bullets 2026-10-01.
st.markdown(
    """
**The lines**

- Five lines are drawn: Metrorex's **M1** to **M5**, redrawn from OpenStreetMap, each labeled
  with its code, with its termini in the legend.
- M5's two branches, to Valea Ialomiței and to Râul Doamnei, are one line.
- The map covers the **Municipality of Bucharest**, its six sectors; every metro station lies
  inside it.
- Suburban trains and trams are not drawn.

**The businesses**

- **This map shows food businesses only.** They come from the registers of Bucharest's
  Sanitary-Veterinary and Food Safety Directorate (DSVSA București), which records every food unit
  it registers: restaurants, cafés, bars and fast food, and food shops from butchers and bakeries
  to supermarkets.
- No open register of other shops or of personal services covers Romania, so **clothes shops,
  hairdressers and the like are not on this map**.
- Registrations the Directorate has canceled are left out, as are canteens, catering, pastry
  labs, mobile units, kiosk carts and vending machines.
- A premises with several registrations (a supermarket's butcher and bakery counters) is shown
  once.
- Names are the operating company's, without its legal form; a sole trader is shown by category
  only.

**Reading the map**

- **About one storefront in four cannot be placed.** The register gives an address but no map
  position. Each premises is placed by matching its street and house number to OpenStreetMap's
  address points in its own sector.
- Where OpenStreetMap lacks the house number, spells the street differently, or has the same
  number in two places, the premises is left off rather than guessed.
- The share placed is about the same in all six sectors, and lowest for fishmongers, many of
  which trade inside markets.
- **About seven placed storefronts in ten sit within a station ring.**
"""
)

render_map_help('business categories (Food service and Food shops)')
render_excluded_stations("Bucharest")
render_country_links('Bucharest')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices("Bucharest")
