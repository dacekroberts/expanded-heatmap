"""What is counted, and what is not - renders docs/excluded_categories.md.

The companion to 10_About_the_Data.py, and the half that the map legends
actually need. A legend row reading "Retail - NAICS Code: 44/45" claims more
than any of these maps contain: nonstore retailers are excluded everywhere,
parking is excluded everywhere, and several cities exclude a catch-all code
that would otherwise put home-based sole traders on a public map. Until this
page is reachable, that legend is overstating its own contents.

It also carries the standing commitment that a removal request is honoured
rather than argued, which is the one thing on this site a reader might need to
act on.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from components import (  # noqa: E402
    ABOUT_DATA_PAGE,
    OVERVIEW_PAGE,
    SITE_NAME,
    render_site_notices,
    set_base_font,
)

DOC = Path(__file__).parent.parent.parent / "docs" / "excluded_categories.md"

st.set_page_config(page_title=f"What is excluded — {SITE_NAME}",
                   page_icon="\U0001f5fa️", layout="wide")
set_base_font()

with st.container(horizontal=True, gap="medium", vertical_alignment="center"):
    st.page_link(OVERVIEW_PAGE, label="← All cities (map)")
    st.page_link(ABOUT_DATA_PAGE, label="Where this data comes from")

st.title("What is counted, and what is not")

st.markdown(
    """
The legends on these maps are broader than the maps themselves. "Retail" does
not mean every retailer; "Food service" does not mean every kitchen. This page
is the full list of what was left out of each city and why, reproduced exactly
as it is kept in the repository.

Two distinctions run through it. Some things are **excluded** - a choice made
here, and reversible: vending machines and mail-order sellers are not
storefronts, parking garages sit outside this project's question, and a few
catch-all licence codes were dropped because sampling showed they were mostly
home-based sole traders rather than shops. Other things are **missing**, which
is not a choice at all: Philadelphia and Boston license no personal-service
trade that publishes addresses, so those cities have two categories rather
than three, and no filter here could add a hairdresser that no register
records.

If you believe a specific listing should not be on these maps, the last
section says how that is handled. The short version: it comes down, and it is
not argued about.
"""
)

if DOC.exists():
    st.markdown(DOC.read_text(encoding="utf-8"))
else:
    st.warning(f"{DOC.name} is missing from this checkout.")

render_site_notices(show_links=False)
