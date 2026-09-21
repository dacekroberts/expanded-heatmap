# Midnight slate — a dark theme for `expanded-heatmap`

Status: **received into this project 2026-09-21** and acted on — the decision
to keep Streamlit and implement this as one palette (page + map together) is in
`DECISIONS.md`, and the build steps are in `PLAN.md`. The status line below this
one described its former home before it was handed over; kept for provenance.

> Originally: drafted, held locally in `.claude/handoffs/` (gitignored). Pass to
> `expanded-heatmap` only when the user asks, after confirming the path.

**Two corrections made on receipt**, from measuring against this project rather
than from preference:

- `#4A5A78` for `--dm-disabled-text` measures **2.7:1** on the page and 2.5:1
  on the surface — below the 3:1 non-text floor. It is one of the four values
  marked "(suggested)" below rather than designed, so the file's own caveat
  flagged the right one. Use something ≥3:1; `#5A6B8C` was used in the preview.
- Every other contrast figure in this file was recomputed and **matched to the
  stated decimal**, which is why the rest of the untested palette was trusted.

Also note: three of the "Implementation notes" are already closed in this
project — the `st.components.v1.html` migration, the unbounded `streamlit>=`
pin (now `>=1.64,<2`), and the light-map-on-a-dark-page problem (the maps carry
their own theme and share one `localStorage` key).

**The palette below was never rendered.** It was designed in
`link-station-commercial` (which shipped a different dark theme, commit
`e2b8034`) and exists only as a static mockup plus the notes here. Treat the
hex values as a starting point to verify on a real page, not a tested result.
Everything under "Implementation notes" *is* tested — those come from
actually shipping a dark theme and finding what broke.

## The palette

Cool blue-navy page chrome, leaving the data colours to carry the accent.

| Role | Hex | Contrast vs page `#0B1220` |
|---|---|---|
| Page background | `#0B1220` | — |
| Surface (sidebar, widgets, cards) | `#131C2E` | — |
| Border | `#23304A` | 1.4:1 (decorative only) |
| Body text | `#E6EDF7` | 15.9:1 (14.5 on surface) |
| Muted text | `#8B9AB5` | 6.6:1 (6.0 on surface) |
| Link | `#7CB7FF` | 9.0:1 (8.2 on surface) |
| Accent (mockup) | `#4C9AFF` | 6.6:1; white text on it is only 2.9:1, so use dark text |

WCAG ratios, computed rather than estimated. All pass AA for text.

## Use your own accent, not the mockup's blue

`#4C9AFF` is a placeholder and reads as another project's look. Your current
accent is teal (`#0d9488` on a light theme), which only reaches 5.0:1 on
slate. Lightened versions work: **`#2dd4bf` (10.1:1)** or `#5eead4` (12.7:1).

Slate chrome plus your own teal keeps the identity yours while getting the
cool neutral background. A cool background also sits naturally beside the
dark map tiles, which come out blue-grey under an invert + hue-rotate filter.

## Draft `.streamlit/config.toml`

```toml
[theme]
base = "dark"
primaryColor = "#2dd4bf"            # your teal, lightened for dark
backgroundColor = "#0B1220"
secondaryBackgroundColor = "#131C2E"
textColor = "#E6EDF7"
linkColor = "#7CB7FF"               # or the teal above
borderColor = "#23304A"
```

## Implementation notes

These are the things that actually cost time.

1. **An explicit `[theme]` removes Streamlit's built-in light/dark toggle**,
   making the site dark-only. Your current `config.toml` comment says
   visitors can still switch via the hamburger menu — **that becomes false
   the moment you add a theme block.** Fix the comment at the same time.
   Adding separate `[theme.light]` and `[theme.dark]` blocks **does** bring
   the toggle back — since confirmed by testing, not assumed. Decide
   deliberately: dark-only is simplest, but you lose the light look the site
   has today.
2. **Hardcoded colours outside `config.toml` are the real work.** Measured
   examples from doing this once: a sidebar label at **1.01:1** contrast
   against the new background (invisible, and nobody noticed by eye), social
   icons at **2.77:1** (below the 3:1 non-text minimum), and an embedded
   iframe that stayed dark on a light page. Grep `app/components.py` and the
   pages for hex, `rgba`, `white`, `#fff` and `background` before calling it
   done, and check contrast numerically rather than by eye.
3. **`st.dataframe` is canvas-rendered.** Header styling cannot be set from
   CSS; it follows the theme's own colours only.
4. **Embedded map iframes are separate documents.** A light Folium map on a
   slate page is a white box. Either default the map to dark, or use the
   CSS-filter dark mode from `dark_mode_handoff.md` with the `--dm-*` values
   below so the map chrome matches the page.
5. **Consider having the map follow the visitor's system theme** rather than
   picking for them: `window.matchMedia('(prefers-color-scheme: dark)')` for
   the initial state, plus a `change` listener, with a manual toggle that
   wins once used. This pattern is implemented and verified end to end,
   including live mid-session OS switches. One trap: browser dev-tools
   colour-scheme emulation updates `matchMedia().matches` **without**
   dispatching the `change` event inside an iframe, so the listener cannot be
   tested that way — it needs a real OS theme switch in an ordinary browser.
6. **Streamlit version matters.** `borderColor`, fonts, radii and chart
   palettes are version-dependent; these notes come from 1.64. Also check
   for deprecated calls while you are in there — `st.components.v1.html` and
   `use_container_width` both have announced removal dates that have already
   passed, and an unbounded `streamlit>=` pin means a future rebuild can
   break the site with no code change.
7. **A theme change needs no new dependency.** Do not add one;
   Streamlit Cloud installs from `requirements.txt`.

## Map dark palette, if it should match slate

Substitute these for the `--dm-*` variables in `dark_mode_handoff.md`:

| Variable | Slate value |
|---|---|
| `--dm-page` | `#0B1220` |
| `--dm-surface` | `#131C2E` |
| `--dm-surface-hover` | `#1A2740` (suggested; not in the mockup) |
| `--dm-surface-disabled` | `#0F1626` (suggested) |
| `--dm-border` | `#23304A` |
| `--dm-text` | `#E6EDF7` |
| `--dm-muted` | `#8B9AB5` |
| `--dm-disabled-text` | `#4A5A78` (suggested) |
| `--dm-accent` | `#7CB7FF`, or your teal |
| `--dm-ring` | `#C9D6EA` (suggested) |

For a light/dark switch thumb: accent colour for the active thumb, a darker
variant when inactive, keeping 3:1+ between the icon and the thumb it sits on.

## Verifying it

- Run the `deploy-verify` agent against the lean venv, and check **every**
  page, not just the home page.
- Prefer DOM and computed-style checks over screenshots for colour claims;
  screenshots at pane resolution hide small mismatches, and a 1.01:1 label
  looks like empty space rather than a bug.
- Look specifically for: white-flash iframes, unstyled hardcoded text,
  low-contrast muted text, chart and legend fills that stayed light, and the
  page's own link colours.
- Beware measurements taken mid-transition or in a hidden browser pane —
  CSS transitions freeze at frame 0 when a pane is not rendering, which
  produces readings that look like real failures.
- Log the choice, and any rejected alternative with its reason, in
  `DECISIONS.md` — at this repository's root, not under `docs/`. Draft
  user-facing wording in chat first per this project's `CLAUDE.md`.

## Not covered

This file has not read `expanded-heatmap`'s source, so it cannot name that
project's specific hardcoded colours, chart usage, fonts or pinned Streamlit
version. And the palette itself has never been rendered on a live page —
verify it before trusting the hex values.
