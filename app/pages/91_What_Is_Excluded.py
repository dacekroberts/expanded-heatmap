"""What is counted, and what is not - renders docs/excluded_categories.md.

The companion to 90_About_the_Data.py, and the half that the map legends
actually need. A legend row reading "Retail - NAICS Code: 44/45" claims more
than any of these maps contain: nonstore retailers are excluded everywhere,
parking is excluded everywhere, and several cities exclude a catch-all code
that would otherwise put home-based sole traders on a public map. Until this
page is reachable, that legend is overstating its own contents.

IT COVERS TWO SCOPES, NOT ONE. Until 2026-09-23 this page was entirely about
businesses, while the other half of the same sentence - "density around
rail-transit stations" - was scoped just as deliberately and said nowhere a
reader would look. Every city page names its own network in its title, so a
reader on the San Francisco page is told it is a Muni Metro map; what none of
them said is that BART, Caltrain and commuter rail generally are excluded
everywhere, by a rule with two recorded judgment calls in it. The question that
prompted this was "is BART in the San Francisco build?" - asked by someone who
had read the site.

THE STATION TABLE IS COMPUTED, NOT WRITTEN. Its numbers come from the
committed `outputs/<city>/excluded_stations.csv` files at render time, so they
cannot drift from the pipeline the way a hand-kept count does - the denominator
here is open (it grows with every city) and this project has already been
bitten by writing one of those into prose. Adding a city adds its row with no
edit here.

It also carries the standing commitment that a removal request is honoured
rather than argued, which is the one thing on this site a reader might need to
act on.
"""

import re
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from cities import CITIES  # noqa: E402
from components import (  # noqa: E402
    ABOUT_DATA_PAGE,
    OVERVIEW_PAGE,
    SITE_NAME,
    render_site_notices,
    set_base_font,
)

ROOT = Path(__file__).parent.parent.parent
DOC = ROOT / "docs" / "excluded_categories.md"
OUTPUTS = ROOT / "outputs"

# Where the generated station table is spliced into the document: the table
# belongs at the end of the station half, and the document is rendered as one
# string. Missing, the whole document renders and the table follows it - a
# worse layout, never a crash. scripts/check_scope_disclosure.py asserts the
# marker is still there, because a silent fallback nobody checks is how this
# would rot.
BUSINESS_HEADING = "## Which businesses are counted"

PARENTHETICAL = re.compile(r"\s*\([^)]*\)")

st.set_page_config(page_title=f"What is excluded — {SITE_NAME}",
                   page_icon="\U0001f5fa️", layout="wide")
set_base_font()

with st.container(horizontal=True, gap="medium", vertical_alignment="center"):
    st.page_link(OVERVIEW_PAGE, label="← All cities (map)")
    st.page_link(ABOUT_DATA_PAGE, label="Where this data comes from")

st.title("What is counted, and what is not")

st.markdown(
    """
These maps answer a narrow question - how much walk-in commerce sits within a
few hundred metres of a rail-transit station - and they answer it by leaving
two different things out.

**Which stations.** Each map covers one rail network, the one named in that
city's page title. Commuter rail is excluded everywhere, stations in
neighbouring municipalities are dropped because no register covers them, and
where a light-rail line stops every other block its surface stops are thinned
so the rings stay readable.

**Which businesses.** The legends are broader than the maps. "Retail" does not
mean every retailer; "Food service" does not mean every kitchen. Some things
are **excluded** - a choice made here, and reversible: vending machines and
mail-order sellers are not storefronts, parking garages sit outside this
project's question, and a few catch-all licence codes were dropped because
sampling showed they were mostly home-based sole traders rather than shops.
Other things are **missing**, which is not a choice at all: Philadelphia and
Boston license no personal-service trade that publishes addresses, so those
cities have two categories rather than three, and no filter here could add a
hairdresser that no register records.

If you believe a specific listing should not be on these maps, the last section
says how that is handled. The short version: it comes down, and it is not
argued about.
"""
)


def _slug(entry):
    """Output-directory name for a city, from its page path.

    `pages/2_San_Francisco_Heatmap.py` -> `san_francisco`. Derived rather than
    stored because cities.py already treats the page path as the link between
    an entry and its city, and a second hand-maintained key is a second thing
    to get wrong. A rename that breaks this shows up as an empty row, so
    check_scope_disclosure.py asserts every slug resolves to a real directory.
    """
    stem = Path(entry["page"]).stem              # 2_San_Francisco_Heatmap
    stem = stem.split("_", 1)[1] if stem[0].isdigit() else stem
    return stem[: -len("_Heatmap")].lower() if stem.endswith("_Heatmap") \
        else stem.lower()


@st.cache_data(show_spinner=False)
def station_scope():
    """One row per city: network mapped, and stations left out by reason.

    Counts the committed excluded_stations.csv files rather than restating
    them. The files do not share a schema - some name the reason in a `reason`
    column, the rest encode it as a boundary column (`located_in`, `state`,
    `distance_outside_m`, `in_city_spatial`) - so both shapes are read, and
    anything matching neither is counted separately rather than folded into a
    bucket it might not belong in.
    """
    BOUNDARY_COLUMNS = {"located_in", "state", "distance_outside_m",
                        "in_city_spatial", "municipio_codes"}
    rows = []
    for entry in CITIES:
        path = OUTPUTS / _slug(entry) / "excluded_stations.csv"
        # The blurb names the network and then its lines; the lines are the
        # city page's job. Dropping the parenthetical keeps the parts that are
        # not line lists - New York's Staten Island Railway, Mexico City's
        # Tren Ligero - which cutting at the first bracket would have lost.
        network = PARENTHETICAL.sub(
            "", entry.get("blurb", "").split(" — ")[0]).strip().rstrip(",")
        if not path.exists():
            rows.append({"City": entry["name"], "Network mapped": network,
                         "Outside the city": None, "Stops thinned": None,
                         "Other": None})
            continue
        frame = pd.read_csv(path, encoding="utf-8-sig")
        outside = thinned = other = 0
        if "reason" in frame.columns:
            reasons = frame["reason"].fillna("").str.lower()
            thinned = int(reasons.str.contains("spacing").sum())
            outside = int(reasons.str.contains("outside").sum())
            other = int(len(frame) - thinned - outside)
        elif BOUNDARY_COLUMNS & set(frame.columns):
            outside = int(len(frame))
        else:
            other = int(len(frame))
        rows.append({"City": entry["name"], "Network mapped": network,
                     "Outside the city": outside, "Stops thinned": thinned,
                     "Other": other})
    return pd.DataFrame(rows)


def _table(frame):
    """The scope frame as a markdown table, blanks shown as an em dash."""
    columns = [c for c in frame.columns
               if c != "Other" or frame["Other"].fillna(0).sum()]
    head = "| " + " | ".join(columns) + " |"
    rule = "|" + "|".join(["---" if i < 2 else "--:"
                           for i, _ in enumerate(columns)]) + "|"
    lines = [head, rule]
    for row in frame[columns].itertuples(index=False):
        # Counts arrive as floats when any city has no file at all (pandas
        # widens an int column to hold the NaN), so they are formatted as the
        # integers they are rather than printed as "16.0".
        cells = [("—" if pd.isna(v) else f"{int(v):,}"
                  if isinstance(v, (int, float)) else str(v)) for v in row]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


scope = station_scope()
totals = scope[["Outside the city", "Stops thinned", "Other"]].sum()

if DOC.exists():
    text = DOC.read_text(encoding="utf-8")
    head, marker, tail = text.partition(BUSINESS_HEADING)
    st.markdown(head)

    st.markdown(
        f"""
**{int(totals.sum()):,} stations are left out across these maps** -
{int(totals["Outside the city"]):,} for sitting outside the city whose register
the map is built from, and {int(totals["Stops thinned"]):,} thinned out of
street-running stretches where the stops are closer together than the rings.
Every one of them is named in its city's `excluded_stations.csv`.
"""
    )
    # A MARKDOWN TABLE, NOT st.dataframe. The grid widget renders collapsed
    # here - 52 px wide with no canvas at all, measured 2026-09-23 in the lean
    # venv - and even working it would be the only interactive element on a
    # page that is otherwise a document: no sorting worth doing on 20 rows, and
    # its contents would not appear in the page text.
    st.markdown(_table(scope))
    st.caption(
        "A dash is a city with no excluded-stations file: every station of "
        "its network is on its map."
    )

    st.markdown(marker + tail)
else:
    st.warning(f"{DOC.name} is missing from this checkout.")

render_site_notices(show_links=False)
