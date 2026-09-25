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

# --- Type -------------------------------------------------------------------
# One font stack, for the same reason there is one palette: before this, the
# city maps and the macro map each said `sans-serif` and nothing said what that
# resolved to.
#
# **The non-Latin fallbacks are the point.** A bare `sans-serif` leaves the
# browser to choose, which is fine for Latin text and unreliable for anything
# else - missing glyphs render as tofu boxes, and a substituted face changes
# the line metrics so a tooltip can outgrow its own box. The 2026-09-21 country
# screen found candidate cities whose business names are Japanese, Korean,
# Traditional Chinese, Greek, Hebrew, Latvian and Czech, so this stops being
# hypothetical the moment a non-Latin city is built.
#
# The order matters and is not arbitrary. Browsers fall through **per glyph**,
# not per string, so the Latin/Greek/Cyrillic faces come first and the CJK
# faces after: Segoe UI and Noto Sans carry no CJK glyphs, so a Japanese name
# falls past them to Yu Gothic or Hiragino rather than being rendered by a face
# that has the character but not the design. Putting a CJK face first would
# silently restyle every Latin name on the map.
#
# THE CJK ORDER DEPENDS ON THE MAP'S LANGUAGE, and a single order was wrong for
# every map but one script's. Han unification puts Chinese and Japanese on the
# same code points, so whichever CJK face comes first draws EVERY Han
# character: with Japanese first, Hong Kong's shop signs rendered in Japanese
# glyph forms (骨 and 直 are the classic cases). They were legible, and to a
# Hong Kong reader they looked foreign. Cantonese-only characters a Japanese
# face lacks (嘅, 冇, 啲) fell through to the next face, so one sign could mix
# two typefaces. Found by Hong Kong's deploy check, 2026-09-24.
#
# So font_stack(lang) puts the map's own script's faces first among the CJK
# ones, and the Latin faces stay ahead of all of them (the reason is above).
# FONT_STACK, the no-language default, is unchanged. A map declares its
# language through render_heatmap(lang=...), which also sets <html lang>.
_LATIN_FACES = '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", '  # Latin, Greek, Cyrillic, Hebrew
_CJK_FACES = {
    "ja": '"Hiragino Sans", "Yu Gothic", Meiryo, ',
    "ko": '"Apple SD Gothic Neo", "Malgun Gothic", ',
    "zh-HK": '"PingFang HK", "Noto Sans HK", ',        # Hong Kong forms where a face has them
    "zh-TW": '"PingFang TC", "Microsoft JhengHei", ',   # Traditional (Taiwan forms)
    "zh-CN": '"PingFang SC", "Microsoft YaHei", ',      # Simplified
}
# The fallback order after a map's own faces, per language. Hong Kong falls to
# the Traditional faces before anything else: Microsoft JhengHei, the only
# Traditional face Windows ships, is far closer to Hong Kong's forms than a
# Japanese or Simplified face.
_CJK_ORDER = {
    None:    ("ja", "ko", "zh-TW", "zh-CN"),            # the original order, unchanged
    "ja":    ("ja", "ko", "zh-TW", "zh-CN"),
    "ko":    ("ko", "ja", "zh-TW", "zh-CN"),
    "zh-HK": ("zh-HK", "zh-TW", "zh-CN", "ja", "ko"),
    "zh-TW": ("zh-TW", "zh-HK", "zh-CN", "ja", "ko"),
    "zh-CN": ("zh-CN", "zh-TW", "ja", "ko"),
}


def font_stack(lang=None):
    """The CSS font stack for a map in `lang` (None: no declared language)."""
    try:
        order = _CJK_ORDER[lang]
    except KeyError:
        raise ValueError(f"no font order for lang={lang!r}; add one to "
                         f"pipeline/theme.py _CJK_ORDER") from None
    return _LATIN_FACES + "".join(_CJK_FACES[k] for k in order) + "Arial, sans-serif"


FONT_STACK = font_stack()

# What the shared map CSS uses. A map that declares a language sets --hm-font
# on its root (render_heatmap), so every shared block stays byte-identical
# across maps and scripts/check_render_current.py can still compare them.
FONT_VAR = f"var(--hm-font, {FONT_STACK})"


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


# Shared JS: decide the theme a map should START in, when the visitor has not
# chosen one. Used by both the city maps (THEME_TOGGLE_HTML) and the macro map
# (_MACRO_THEME_JS), so the rule is written once.
#
# Why read a background colour rather than ask a framework. Streamlit exposes
# no theme signal at all - no `data-theme` on <html> or <body>, no CSS custom
# property (checked 2026-09-21). But whichever of System / Light / Dark the
# visitor picks, the page's own background reflects it, and a map iframe is
# same-origin with its host, so reading that background detects all three.
# `prefers-color-scheme` alone would only match the default System case and
# would be wrong the moment someone picks Light or Dark explicitly.
#
# A standalone map has no host to read - `window.parent === window` and its own
# background is the thing being decided - so it falls back to the OS
# preference.
#
# An explicit click always wins over this, and is remembered; see the callers.
AMBIENT_THEME_JS = """
    function ambientPrefersDark() {
        try {
            if (window.parent !== window) {
                var bg = window.parent.getComputedStyle(
                    window.parent.document.body).backgroundColor;
                var n = bg && bg.match(/[\\d.]+/g);
                if (n && n.length >= 3) {
                    var alpha = n.length > 3 ? parseFloat(n[3]) : 1;
                    if (alpha > 0.1) {          // transparent tells us nothing
                        // Perceived brightness, 0-255; a binary decision does
                        // not need full WCAG gamma expansion.
                        var b = 0.299 * +n[0] + 0.587 * +n[1] + 0.114 * +n[2];
                        return b < 128;
                    }
                }
            }
        } catch (e) { /* cross-origin or no parent: fall through */ }
        return !!(window.matchMedia
                  && window.matchMedia('(prefers-color-scheme: dark)').matches);
    }
"""


def css_vars(palette, prefix="dm"):
    """A palette as CSS custom-property declarations.

    >>> css_vars({"page": "#000"})
    '--dm-page: #000;'
    """
    return " ".join(
        f"--{prefix}-{name.replace('_', '-')}: {value};"
        for name, value in palette.items()
    )


def rgb_list(hex_color, alpha=255):
    """"#0d9488", 235 -> [13, 148, 136, 235]. For pydeck/WebGL layers, which
    take colour channels rather than CSS, and which CSS therefore cannot
    restyle - see the note in app/Overview.py."""
    h = hex_color.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)] + [alpha]


def rgba(hex_color, alpha):
    """"#0B1220", 0.8 -> "rgba(11, 18, 32, 0.8)". For the one place a colour
    needs transparency (the map attribution strip), so the page colour is not
    re-typed as literal channel values the way it used to be."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"
