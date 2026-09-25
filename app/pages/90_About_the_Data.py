"""Where this data comes from - renders docs/data_sources.md in the app.

WHY THIS PAGE EXISTS, AND WHY IT BLOCKS PUBLISHING. Three separate obligations
converge on it:

  * New York City's Technical Standards Manual reserves the right to require a
    third party to "explicitly identify the source, version, and modifications
    made to a public data set" when re-publishing it. `data_sources.md` is the
    source and the version (endpoint plus retrieval date per dataset); its
    sibling page is the modifications.
  * Chicago's, SFMTA's, LA Metro's and MassDOT's notices have to appear where
    the SITE is accessed, not on one city page. They render on every page from
    `components.render_site_notices()`, and this page is where the reasoning
    behind each one can actually be read.
  * The map legends are deliberately broad - "Retail - NAICS Code: 44/45"
    overstates what the maps contain - so the exclusions must be reachable
    from them, and provenance without exclusions is half an answer.

The document is rendered as committed rather than re-written for the web: it
was written to be published as-is, and a hand-maintained web copy would drift
from the file the pipeline's authors actually read.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from components import (  # noqa: E402
    EXCLUSIONS_PAGE,
    OVERVIEW_PAGE,
    SITE_NAME,
    render_site_notices,
    set_base_font,
)

DOC = Path(__file__).parent.parent.parent / "docs" / "data_sources.md"

st.set_page_config(page_title=f"Where this data comes from — {SITE_NAME}",
                   page_icon="\U0001f5fa️", layout="wide")
set_base_font()

with st.container(horizontal=True, gap="medium", vertical_alignment="center"):
    st.page_link(OVERVIEW_PAGE, label="← Global View")
    st.page_link(EXCLUSIONS_PAGE, label="What is counted, and what is not")

st.title("Where this data comes from")

st.markdown(
    """
Every dataset behind these maps is a public register, and this page is the
project's own provenance record: the exact endpoint each one was fetched from,
the filter applied at download, the date it was retrieved, and the licence or
terms it carries. It is reproduced here exactly as it is kept in the
repository.

It is long, and deliberately so. Three things in it are worth knowing before
reading any map: **a government open-data portal is not evidence of permissive
terms** (Los Angeles' business registry is CC0 while its transit feed forbids
modifying the data); **several sources say nothing at all about reuse**, which
is recorded as unresolved rather than read generously; and **every retrieval
date is a statement about staleness**, because a register only ever describes
the day it was pulled.
"""
)

if DOC.exists():
    st.markdown(DOC.read_text(encoding="utf-8"))
else:
    st.warning(f"{DOC.name} is missing from this checkout.")

render_site_notices(show_links=False)
