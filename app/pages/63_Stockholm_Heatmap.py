"""Stockholm heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.stockholm.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Stockholm Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Stockholm")

st.title("Stockholm: food businesses around Tunnelbana stations")

# Approved by the owner 2026-09-29.
st.markdown(
    """
Three lines are drawn: the Tunnelbana's **Gröna linjen** (routes T17, T18 and
T19), **Röda linjen** (T13 and T14) and **Blå linjen** (T10 and T11), redrawn
from OpenStreetMap. Each line is labelled once, and the legend names its
routes. Pendeltåg commuter trains, Roslagsbanan, Saltsjöbanan and the trams
are not drawn.

The map covers **Stockholms kommun**, the City of Stockholm. The lines' outer
stations in Solna, Sundbyberg, Danderyd, Huddinge and Botkyrka lie outside it
and are not drawn.

**This map shows food businesses only.** They come from the City of
Stockholm's food inspection register (Livsmedelstillsyn), published by its
Environment and Health Administration. The register lists every premises the
city's food control inspects: restaurants, cafés and bars, and food shops from
kiosks to supermarkets. No open register of other shops or of personal
services covers Stockholm, so **clothes shops, hairdressers and the like are
not on this map**. Kitchens in preschools, schools, care homes and workplaces
are left out by name, and so are pharmacies, wholesalers and food producers.
A few office canteens registered under a company name remain.

**The register stopped updating in October 2025.** Its latest inspection is
dated 21 October 2025 and nothing has been added since, so a business that
opened or closed after then is not reflected. Each premises is shown as it
stood at its latest inspection. The register began recording a premises' type
in 2024. Premises last inspected in 2022 or 2023 carry no type, and those
whose name identifies a restaurant or a food shop are shown, their pins marked
"classified from its name". About one storefront in twenty-five has no map
position and is not shown.

**About nine storefronts in ten sit within a station ring.**

Concentric ring boundaries and the business categories (Food service and Food
shops) are toggleable via the layer control in the top left. When enabled,
business density will display as numbered circles summing areas when zoomed
out. Zooming in will show individual dots; hover over those to see further
details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a
statistical density estimate, so read the colour as "roughly where things
cluster."
"""
)

# The register's own last-edit date, read from outputs/stockholm/provenance.json
# so it cannot go stale on the next fetch.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _date = _prov.get("register_last_edited")
        if _date:
            st.caption(f"Snapshot: the register as last edited on **{_date}** "
                       f"(Stockholms stad, miljöförvaltningen).")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/stockholm/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices()
