"""Required notices - every notice publishing these maps requires, verbatim,
in docs/data_sources.md's number order.

The fourth information page, beside About_the_Data.py, What_Is_Excluded.py
and Why_the_Maps_Differ.py. Until 2026-10-02 every page carried all of the
notices in its footer; the owner moved each to its own city's page and to
this page, which every page's footer links to (components.NOTICES_PAGE).
Only the notices whose terms reach every page stay in every footer; the
reasons are beside components._NOTICES. scripts/check_provenance.py check N
holds every notice to this page and to its own city's page.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from components import (  # noqa: E402
    ABOUT_DATA_PAGE,
    DIFFERENCES_PAGE,
    EXCLUSIONS_PAGE,
    OVERVIEW_PAGE,
    SITE_NAME,
    render_all_notices,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title=f"Required notices — {SITE_NAME}",
                   page_icon="\U0001f5fa️", layout="wide")
set_base_font()

with st.container(horizontal=True, gap="medium", vertical_alignment="center"):
    st.page_link(OVERVIEW_PAGE, label="← Global View")
    st.page_link(ABOUT_DATA_PAGE, label="Where this data comes from")
    st.page_link(EXCLUSIONS_PAGE, label="What is counted, and what is not")
    st.page_link(DIFFERENCES_PAGE, label="Why the maps differ")

st.title("Required source notices")

render_all_notices()

render_site_notices(show_links=False, lists_all=True)
