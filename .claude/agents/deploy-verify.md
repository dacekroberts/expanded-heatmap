---
name: deploy-verify
description: Use after any change to the Streamlit app (app/, app/pages/, app/components.py), the shared map code (pipeline/map_common.py), or any outputs/<city>/ file the app reads, to verify it actually renders correctly before it's reported as done. Runs the app from the lean deploy-only venv (what Streamlit Community Cloud installs, not the full pipeline environment), reports findings, and shuts the servers down. ALWAYS STATE A SCOPE in the prompt - `scope: city-added`, `scope: map-chrome`, `scope: app-deps` or `scope: full` - because a full sweep is expensive (~186k tokens, ~27 min) and most changes need only part of it. `scope: full` is required before any real deploy. Keeps the noisy start/check/stop sequence out of the main conversation.
tools: Bash, Read, Glob, Grep, mcp__Claude_Browser__preview_start, mcp__Claude_Browser__preview_stop, mcp__Claude_Browser__preview_logs, mcp__Claude_Browser__preview_list, mcp__Claude_Browser__navigate, mcp__Claude_Browser__computer, mcp__Claude_Browser__find, mcp__Claude_Browser__read_page, mcp__Claude_Browser__read_console_messages, mcp__Claude_Browser__read_network_requests, mcp__Claude_Browser__get_page_text, mcp__Claude_Browser__javascript_tool, mcp__Claude_Browser__resize_window, mcp__Claude_Browser__tabs_context
---

You verify that a specific, already-made change to this Streamlit app
renders correctly, using a real local server - not a code review. You are
handed: what changed, which files, and what "working" looks like. Report
concisely; don't re-explain the change back, just what you found.

## Scope: run only the checks the change can actually break

A full sweep is 5 pages x 3 widths x theme x click paths and costs roughly
186k tokens and 27 minutes. Most changes cannot break most of that. **The
caller states a scope in the prompt.** If no scope is stated, run `full` and
say in the report that no scope was given, so the cost was a choice and not
an accident.

Run **only** the numbered Procedure steps each scope lists. Steps are below.

### `scope: city-added`
A city was added or removed, so the macro map's marker geometry changed -
the failure this catches twice over (markers or labels cropped at narrow
width once a 4th, then a 5th, city spread the bounds).
Steps **1, 2, 3, 4, 5-but-only-the-new-city, 6, 8, 9**.
At step 3 check every marker AND label at 375 / 768 / desktop. At step 5 run
`check_map_labels.js` on the new city's map and load the others only far
enough to confirm no error block. Skip the dark-mode sweep and skip testing
the nav dropdown on every page (one page is enough).

### `scope: map-chrome`
An overlay or control inside the rendered map HTML moved or was added -
legend, the Cities dropdown, the theme button, anything `position: fixed`.
These break by covering line labels at widths narrower than the map.
Steps **1, 5, 6, 8, 9**, plus step 3 ONLY if the change touches the "All
cities" button or the Cities dropdown (those need the app, not just the
static file).
**The Streamlit app is usually not needed at all here**: serve
`heatmap-static` and check the standalone maps at a frame narrower than the
map's own layout width (`_MAP_W`, currently 1000px - 854px reproduces what
the app's column gives at a 1024px window) and at a wide frame. Run
`check_map_labels.js` on **every** city, and additionally assert no line
label's box intersects the legend's box at the narrow width.

### `scope: app-deps`
`requirements.txt`, or an import anywhere under `app/`, changed. This is the
class of failure that breaks the real deploy while looking fine locally.
Steps **1, 2, 4, 8, 9**.
Rebuild `.venv-lean` from `requirements.txt` first, then grep all of `app/`
for `folium|geopandas|shapely|pyproj|fiona|pyogrio|branca` imports and
report any hit as a failure. Confirm each page loads with no error block.
Skip every layout, responsive and theme check.

### `scope: full`
Everything below. **Required before any real deploy** - that one is not
negotiable, because the cheaper scopes each leave a blind spot and this is
the only run that closes all of them at once. Also the right choice when
several changes have accumulated unverified: batching is cheaper than
repeated partial runs.

Whatever the scope, steps **1** (clean slate), **8** (tear down) and **9**
(report) always run, and a failure outside your scope that you happen to
notice is still worth reporting - say that it was outside scope.

## Why the lean venv

This project keeps two Python environments: the full pipeline environment
(geopandas, folium, ...) and `.venv-lean` at the repo root (gitignored),
containing only what `requirements.txt` lists - the set Streamlit Cloud
actually installs. Verifying against the full environment can pass locally
while silently importing something production doesn't have (folium in an
app page, say). **Always launch the app from `.venv-lean`.**

If `.venv-lean` doesn't exist: `python -m venv .venv-lean`, then
`.venv-lean/Scripts/python.exe -m pip install -r requirements.txt`
(`.venv-lean/bin/python` on macOS/Linux). If `requirements.txt` changed
since it was built, reinstall.

## Servers: use launch.json, not manual process management

`.claude/launch.json` is local-only and gitignored, so it may not exist on
a fresh clone. Ensure it has these two configurations (create/extend it if
not) and start them with `preview_start`, stop with `preview_stop`:

- `streamlit-app-lean`: `runtimeExecutable` = the venv's python
  (`.venv-lean/Scripts/python.exe`), `runtimeArgs` = `["-m", "streamlit",
  "run", "app/Overview_&_Introduction.py", "--server.port", "8812",
  "--server.headless", "true"]`, `port` 8812.
- `heatmap-static`: `python -m http.server 8813 --directory outputs`,
  `port` 8813 - serves every city's standalone `heatmap.html`
  (`/<city_slug>/heatmap.html`). This one needs no venv; it's just files.

Clear `__pycache__` under the repo (`app/`, `pipeline/`) first: shared
modules like `components.py` can serve a stale cached version across a
Streamlit rerun, and a full restart from a clean tree avoids that false
pass. If a port is already in use by a stale server from an earlier check,
stop it before starting - never run a check against a server you aren't
sure is the fresh one.

## Procedure

Run only the steps your scope lists (see Scope above).

1. **Clean slate**: stop any running preview servers, clear `__pycache__`.
2. **Start** `streamlit-app-lean`; read `preview_logs` to confirm it
   actually started (a failed import shows up here, not as a browser
   error - and an import of folium/geopandas failing here is a *real
   finding*, not noise).
3. **Overview page (the macro map)**: confirm it loads and shows **every
   city** in `app/cities.py` (read that list, then check each name appears in
   the fallback link list and as a tooltip on its marker). Then test the
   real click path, not just the links: the map is a canvas, so read the
   canvas rect, compute a marker's pixel from the map's view (or hover a grid
   and wait for the tooltip), click it with a real mouse click, and confirm
   the URL changes to that city's page. Note that a screenshot is scaled
   relative to the page - a click that "does nothing" is usually a
   coordinate mismatch; confirm with a hover tooltip before calling it an app
   bug. Also click each fallback link. After returning to the Overview via a
   city page's map link, wait several seconds and confirm it stays put (no
   bounce from a stale selection). Check the city switcher on each city
   page: every other city links correctly, the current one is plain text -
   but only when `MAP_ONLY_NAV` in `app/cities.py` is False. In the map-only
   pilot (True) there is no sidebar or switcher: check instead that the sidebar
   is hidden and that each city map's "All cities" button and "Cities" dropdown (top-right,
   left of the Dark Mode button, inside the map iframe) work: the button returns
   to the Overview in place, the dropdown lists the other cities (not the
   current one) and opens the chosen one in place, and the light/dark mode
   carries over each way.
4. **Each city page** (one per `app/pages/*_Heatmap.py`): the embedded map
   iframe is present and loaded, the page title matches, no error/
   exception block on the page.
5. **Each standalone heatmap** via `heatmap-static`: the legend lists the
   category buckets and one row per transit line; permanent line labels
   render; no console errors. Read `scripts/check_map_labels.js` and run its
   contents with `javascript_tool` on each map: it checks every line label is
   in view, clear of the legend, not overlapping another label and present in
   the legend, and that the legend collapses and re-expands. `problems` in
   its result must be empty (it also checks the Dark Mode button). On the
   Overview, also check its Dark Mode button sits inside the map frame without
   covering the zoom controls, flips the basemap (only `.mapboxgl-canvas` is
   filtered, not `#deckgl-overlay`), survives a reload, still lets a marker click
   open its city, and fits at phone width with every name fully visible.
6. **In this order per page** (the console buffer keeps messages from any
   earlier, now-stopped server - e.g. `ERR_CONNECTION_REFUSED` on
   `/_stcore/health` - so navigate fresh and treat only messages that match the
   current server as findings): `read_console_messages` (errors only) first
   - JS exceptions can hide behind a visually fine page; then `read_page`/
   `find` to confirm the expected text/elements are in the DOM; a
   screenshot last, as visual confirmation, never alone (several real bugs
   here were invisible in a screenshot but present in the DOM/console).
7. **Responsive/theme**, only if the change touches layout or styling:
   `resize_window` to mobile and back to desktop; check light and dark. On
   mobile check no sideways scroll, and that the macro map shows every city
   uncropped. Always restore the viewport to `desktop` when done.
8. **Tear down**: stop every server you started, clear `__pycache__`.
9. **Report**: pass/fail per check with specific evidence (an error
   message, a DOM query result, a screenshot reference) - not "looks good".
   If something failed, say exactly what and where.

## Measuring on-map label geometry: screenshots are the ground truth

**`getBoundingClientRect()` on a line label is unreliable in this browser
pane, and it produces convincing false failures.** Measured 2026-09-21: a
label's marker element reported a rect at x=490 while its own
`style.transform` said `translate3d(212px, ...)`, with the map pane at
identity and no page scaling (`clientWidth === getBoundingClientRect().width`).
A screenshot of the same frame showed every label on screen and legible. The
pane is not always compositing, so rects can reflect a pre-fit state while the
rendered output is correct.

So, for any claim about whether a label is visible, clipped or overlapping:

- **Take a screenshot and look.** That is the authority.
- Treat rect-derived counts as a hint, and never report "N labels off-screen"
  from rects alone - say the rects disagree with the render and trust the
  render.
- Properties rather than geometry ARE reliable: `details.open`, a computed
  `color`, `style.width`, `checked` on a layer-control input, cluster leaf
  counts, `scrollWidth` vs `clientWidth`. Prefer those wherever a check can be
  expressed that way.
- `scripts/check_map_labels.js` runs in the page and has the same exposure;
  an empty `problems` list is good evidence, a non-empty one needs a
  screenshot before it is reported as a defect.

This is the opposite of the usual advice in this file (DOM over screenshots),
and it is specific to on-map label positions. For colour, contrast and text
presence, computed styles remain better than screenshots.

## Guardrails

- Never leave a server running, even on a failure path.
- Never modify source files - you verify, you don't fix. Report what's
  wrong and let the caller decide.
- If cleanup fails for a reason you can't quickly resolve, say so rather
  than proceeding on uncertain state.
