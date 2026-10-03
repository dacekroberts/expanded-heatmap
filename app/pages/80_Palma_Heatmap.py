"""Palma heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.palma.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Palma Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Palma")
render_city_title('Palma')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/palma/step3_map.py` to generate it.")

# The register's own last-update date, read from outputs/palma/provenance.json
# (GOIB's terms require it to be shown).
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _date = _prov.get("as_of_date")
        if _date:
            st.caption(f"Snapshot: the Consell de Mallorca's register as last updated on "
                       f"**{_date}**; Catastro's address points as accessed on "
                       f"**{_prov.get('files_utc', {}).get('A.ES.SDGC.AD.07040.zip', '')[:10]}**.")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

# Written under the owner's pre-approval of this build's prose (2026-09-30);
# set as bullets 2026-10-01.
st.markdown(
    """
**The line**

- One line is drawn: **Metro M1** of the Metro de Palma, run by Serveis Ferroviaris de Mallorca,
  from Plaça d'Espanya (the Estació Intermodal) to the university and ParcBit, redrawn from
  OpenStreetMap with all 10 of its stations, every one inside the municipality. Much of it runs in
  tunnel.
- **It is not a frequent service**: a train about every 20 minutes on weekdays in term time and
  every 30 to 40 minutes in the holidays, Saturdays until mid-afternoon, and none on Sundays.
- A second metro line to Marratxí no longer runs as a metro; SFM's trains to Inca and beyond, and
  buses, are not drawn.

**The businesses**

- **This map shows food businesses only.** They come from the Consell de Mallorca's register of
  restaurant and entertainment establishments: bars, cafés, restaurants, music bars and nightclubs.
- No open register of other shops or of personal services covers Palma, so clothes shops,
  hairdressers and the like are not on this map.
- A premises is shown when the register lists it as active.
- Caterers without premises of their own are left out, and so, by name, are sports, golf and
  sailing clubs, cinemas and bingo halls, parish and clinic bars, and hotels (a hotel's own named
  café or restaurant stays). A name rule is imperfect.

**Reading the map**

- **About one premises in five could not be placed.** The register gives coordinates for about one
  in eight; the rest are placed at their address, matched street and number to the Spanish land
  registry's address points, or at the nearest listed number on the same side of the street.
- Addresses with no street number, and streets the two sources spell differently, are left off
  the map.
- **About a third of the placed premises sit within a station ring.** The Metro runs north from
  the center; the old town, the seafront and the beaches of Playa de Palma are beyond its reach.
"""
)

render_map_help('business layer')
render_excluded_stations("Palma")
render_country_links('Palma')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices("Palma")
