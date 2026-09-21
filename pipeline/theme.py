"""The project's theme palettes - the single source for every colour that is
part of the *chrome*, as opposed to the data.

Three places render a theme and they must agree:

  1. `.streamlit/config.toml`     the Streamlit page (TOML, cannot import -
                                  the one unavoidable duplicate; keep it in
                                  step and run scripts/check_theme_sync.py)
  2. `pipeline/map_common.py`     each city map's chrome (THEME_TOGGLE_HTML)
  3. `app/components.py`          the macro map's chrome (_MACRO_THEME_CSS)

Before 2026-09-21, 2 and 3 each carried their own literal copies of the same
hex values, so a reskin of one produced a navy city map beside a teal macro
map. Both now build their CSS from here.

**This module imports nothing.** `app/` is installed from the lean
`requirements.txt` (streamlit + pandas only), so anything it imports from
`pipeline/` must stay dependency-free - the same rule the city pages' config
imports follow.

What is deliberately NOT here: business-category colours
(`pipeline/taxonomies/__init__.py`) and transit line colours (each city's
config). Those are data, set from agency brand colours and category identity,
and they stay legible across both themes rather than changing with it. It is
also why a chrome reskin only moves about 15% of a city page's pixels - see
docs/theming.md.
"""

# --- Dark: "midnight slate" -------------------------------------------------
# Cool blue-navy, chosen to sit beside the maps' dark basemap, which is an
# invert + hue-rotate CSS filter and so renders blue-grey. Contrast figures are
# measured against DARK["page"], and every one was recomputed rather than taken
# on trust. See docs/theming.md for the full table.
DARK = {
    "page": "#0B1220",              # body behind the map
    "surface": "#131C2E",           # legend, controls, tooltip, buttons
    "surface_hover": "#1A2740",
    "surface_disabled": "#0F1626",
    "border": "#23304A",
    "text": "#E6EDF7",              # 15.9:1 on page
    "muted": "#8B9AB5",             # 6.6:1
    # NOT the #4A5A78 originally suggested: that measures 2.7:1 on page and
    # 2.5:1 on surface, below the 3:1 non-text floor.
    "disabled_text": "#5A6B8C",
    # The teal is kept rather than moving to the source palette's #4C9AFF,
    # which its own author called a placeholder that reads as another
    # project's look. 12.7:1 on page.
    "accent": "#5eead4",
    "ring": "#C9D6EA",              # concentric ring outlines
    "station": "#7cc0ff",           # station dots; already blue, suits slate
}

# --- Light (the default) ----------------------------------------------------
# White base, teal accent. Unlike the dark values these were literals scattered
# across the map and macro-map CSS until 2026-09-21; they are named here so a
# change to the light look is also a one-place edit.
LIGHT = {
    "page": "#ffffff",
    "surface": "#ffffff",
    "surface_hover": "#f1f5f4",
    "surface_disabled": "#f8fafa",
    "border": "#999999",
    "text": "#1c2b2a",
    "muted": "#5b6b6a",
    "disabled_text": "#9aa8a7",
    "accent": "#0d9488",
    "ring": "#2c3e50",
    "station": "#1a5490",
}

# Streamlit's page theme, for scripts/check_theme_sync.py to compare against
# `.streamlit/config.toml`. Keys are Streamlit's own config names.
STREAMLIT_LIGHT = {
    "primaryColor": LIGHT["accent"],
    "backgroundColor": LIGHT["page"],
    "secondaryBackgroundColor": "#f1f5f4",
    "textColor": LIGHT["text"],
}
STREAMLIT_DARK = {
    # #0d9488 reaches only 5.0:1 on the slate page; #2dd4bf reaches 10.1:1.
    "primaryColor": "#2dd4bf",
    "backgroundColor": DARK["page"],
    "secondaryBackgroundColor": DARK["surface"],
    "textColor": DARK["text"],
    "linkColor": "#7CB7FF",
    "borderColor": DARK["border"],
}


def css_vars(palette, prefix="dm"):
    """A palette as CSS custom-property declarations.

    >>> css_vars({"page": "#000"})
    '--dm-page: #000;'
    """
    return " ".join(
        f"--{prefix}-{name.replace('_', '-')}: {value};"
        for name, value in palette.items()
    )


def rgba(hex_color, alpha):
    """"#0B1220", 0.8 -> "rgba(11, 18, 32, 0.8)". For the one place a colour
    needs transparency (the map attribution strip), so the page colour is not
    re-typed as literal channel values the way it used to be."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"
