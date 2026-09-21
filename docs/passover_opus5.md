# Passover for Opus 5: what this project is, and what to verify

Written by Claude Sonnet 5 on 2026-09-21, at the end of a long working session,
from the repository state at commit `520c165` (branch `master`, in sync with
`origin/master`, working tree clean before this file was added). **This file can
be wrong.** It is a map and a set of claims to test, not a source of truth: the
repository and running code are. Where this file says "verified", it says how;
where it says "not verified", believe that too.

## 1. Your task

The user wants a fresh, independent pair of eyes to **check and verify the whole
project: the codebase and its structural integrity**, and to say what is broken,
fragile, inconsistent or unproven. Concretely:

1. Read the project (section 12 gives an order), then work through the
   verification plan in section 9.
2. **Run the publishability check of the generated map HTML early** (section 9G).
   The committed `outputs/<city>/heatmap.html` files embed each business's name and
   coordinates from public registries, and the name fallbacks may expose
   individuals' names. This check **gates any public deployment** and has not been
   done. Give it its own verdict per city in your report.
3. **Default to read-only.** Report findings first. Change nothing until the user
   approves a fix, except throwaway scratch files. (The user's standing preference:
   a recommendation and its trade-off in chat, then wait for a "yes".)
4. Deliver a **findings report** (format in section 13) in chat. Publish or commit
   nothing unless asked.

Do not spend effort re-deriving settled decisions (section 5). Do spend it on the
publishability check and on trying to break the claims in section 8 (what has and has not been verified).

## 2. What the project is

A multi-city map of **commercial (storefront) density around rail-transit
stations**. For each city, a station-centred heatmap shows where retail,
food-service and personal-service businesses cluster relative to the transit
lines: toggleable distance rings (0-0.1, 0.1-0.2, 0.2-0.3, 0.3-0.6 mi), heat
layers, clustered per-category pins, and every transit line drawn from real GTFS
geometry with a permanent on-map label (its real public name) and a legend entry.
A **macro map** on the home page lists the cities; clicking a marker opens that
city's page. The audience is portfolio viewers; the priority is coverage and
working functionality, **not analysis**. Ridership and interpretive analysis are
explicitly out of scope until the user asks.

It was generalized from an earlier single-city prototype (see
`docs/project_context.md`). Nothing here depends on that prototype. **Do not
read or modify any other project on this machine**; the user has asked that
separate projects stay separate (no junctions or symlinks between them, checked
2026-09-19).

## 3. Current state (commit `520c165`)

| City | Rail system (lines drawn) | Stations in city | Businesses mapped | Taxonomy | Distinctive |
|---|---|---|---|---|---|
| San Diego | MTS Trolley (5) | 47 of 63 | 12,886 | `naics` | Data ships pre-geocoded; city filter by spatial join against a regional municipal layer |
| San Francisco | Muni Metro (6) | 49 (thinned) | 20,067 | `naics` | Central subway plus surface offshoots: uses the sub-transit-line filters; ~37% of rows carry a NAICS code |
| Los Angeles | Metro Rail (6) | 56 of 110 | 101,309 | `naics` | ~9% of registry coordinates were corrupt; recovered by Census geocoding (matched 98.9% of the rows that needed it, 9,066 of 9,166); in-city rows identified by `council_district` not `city`; largest map (5.6 MB) |
| Chicago | CTA 'L' (7; Yellow dropped) | 123 of 141 | 20,686 | `chicago_license` (local, not NAICS) | First local-taxonomy city: catch-all license types classified by `business_activity`; one row per site (account + site) with a license-priority order; source is a license-term history filtered to unexpired licenses (snapshot 2026-09-20); Metra deliberately out of scope |

Row-count baselines per step live in `DECISIONS.md` (search the city's entry).
Not started, in ease order (`PLAN.md`, `docs/city_shortlist.md`): New York,
Philadelphia, Boston, Washington D.C.; Dallas (marginal); San Jose, Denver, Austin,
Charlotte, Fort Worth ruled out on live-verified evidence.

## 4. Repository map (66 tracked files at `520c165`)

```
CLAUDE.md                     project conventions + invariants (read first)
README.md                     first draft, for outside readers
PLAN.md                       open work only
DECISIONS.md                  append-only reasoning trail, newest first, ~1,100 lines
requirements.txt              DEPLOY set: streamlit>=1.64,<2 ; pandas>=2.2  (lean on purpose)
requirements-pipeline.txt     pipeline set: pandas, geopandas, shapely, pyproj, folium, requests
.streamlit/config.toml        light theme, teal accent (#0d9488)
.gitattributes                * text=auto eol=lf   (repo stores LF; Windows checkouts may show CRLF warnings)
docs/                         project_context.md (stable briefing), city_shortlist.md,
                              sub_transit_line_filters.md, navigation_sidebar_and_city_links.md,
                              dark_mode_handoff.md (partly historical), this file
.claude/skills/               add-city, scaffold-city, pipeline-drift-check, decisions-entry
.claude/agents/               deploy-verify (browser-driven verification of the app)
scripts/                      scaffold_city.py (generates a new city's shared skeleton),
                              check_map_labels.js (browser check run on each map)
pipeline/
  map_common.py               SHARED renderer, 779 lines: render_heatmap(), label layout,
                              legend, dark-mode + navigation button JS/CSS (embedded strings)
  drift_check.py              re-runs every city's pipeline, diffs outputs/ against git HEAD
  census_geocoder.py          Census bulk geocoder with a content-hash cache (used by LA)
  taxonomies/                 __init__ (buckets, registry, filter_to_storefront), naics (complete),
                              chicago_license (complete), nyc_dca + phl_licensetype (SKELETONS)
  <city>/                     config.py, step1_stations.py, step2_clean_businesses.py, map step
                              (SD/SF/Chicago: step3_map.py; LA: step3_geocode.py + step4_map.py)
outputs/<city>/               COMMITTED: heatmap.html (1.0-5.6 MB, pre-rendered Folium)
                              + excluded_stations.csv (audit of stations left out)
app/
  Overview_&_Introduction.py  home page: pydeck macro map (click -> st.switch_page), fallback link list
  cities.py                   the city list (single source) + MAP_ONLY_NAV flag
  components.py               render_city_nav, render_macro_map_theme (dark mode), set_base_font
  pages/N_<City>_Heatmap.py   one per city: st.iframe(HEATMAP_HTML, width=1000, height=650)
data/<city>/{raw,processed}/  GITIGNORED downloads and intermediates (present locally only)
```

## 5. Architecture and settled decisions (do not relitigate; each has reasoning in `DECISIONS.md`)

- **Pipeline/app split.** An offline geopandas pipeline writes `outputs/<city>/`;
  the deployed app only reads those files and never runs the pipeline. The app's
  dependencies stay minimal (`streamlit`, `pandas`; `pydeck` ships with Streamlit)
  because Streamlit Community Cloud installs from `requirements.txt` and a geo
  stack there breaks the deploy. **No folium/geopandas/shapely/pyproj import may
  appear under `app/`** (checked: none at `520c165`).
- **Maps are pre-rendered static HTML** embedded with `st.iframe` (migrated from
  the deprecated `st.components.v1.html` on 2026-09-20), not `streamlit-folium`.
  The map is a **fixed 1000x650**: a Leaflet.heat bug throws on init if the
  container size is unresolved, silently killing every later layer. So the map is
  wider than Streamlit's column and scrolls inside its iframe; all overlay
  controls (legend, dark-mode/"All cities"/"Cities" buttons) use
  `position: fixed` so they stay in the visible frame.
- **Never buffer or measure distance in EPSG:4326.** Project to the city's own UTM
  zone, do the geometry, project back. The projected CRS is per city (checked in
  each `config.py`: SD and LA EPSG:32611, SF EPSG:32610, Chicago EPSG:32616).
- **Classification is pluggable.** Every taxonomy maps into three shared buckets
  (Retail, Food service, Personal services) via a module exposing `classify`,
  `FIELD_LABEL`, `VALUE_COLUMN`, `legend_label`, and optionally `EXTRA_COLUMNS`
  (a second field some values are classified by; used by Chicago). `naics` is the
  default; NAICS is not required. Step 2 filters with `filter_to_storefront()`,
  never NAICS prefixes directly. `map_common.py` never names a taxonomy.
- **One agency's rail system per city** (SD Trolley without Coaster; Muni Metro
  without BART/Caltrain; LA Metro Rail without Metrolink; CTA without Metra).
- **Every drawn transit line gets BOTH a permanent label with its real public name
  AND a legend entry.** Labels are placed automatically at each line's tail end
  (farthest from the other lines, on the in-city stretch), dispersing along the
  line when several would collide; the default view is fitted to stations plus
  labels (no hand-picked centre/zoom).
- **The project is never named after a city.** "Expanded Heatmap" is a placeholder.
- **Live-verify a city's data schema before writing pipeline code for it** (Denver
  and San Jose looked viable from titles and were not).
- **Both light and dark modes exist** on every city map and the macro map,
  sharing one `localStorage` key (`expanded-heatmap-theme`). The surrounding
  Streamlit page stays light (deferred; a custom theme may replace it).
- **Navigation is in a pilot:** `MAP_ONLY_NAV = True` in `app/cities.py` hides the
  sidebar page list and the city switcher, so the macro map is the only way in;
  each city map has an "All cities" button and a "Cities" dropdown (native
  `<select>`) that click hidden page links rendered by `render_city_nav()`. The
  old sidebar/switcher code is kept; one line restores it. Details and the
  reasoning: `docs/navigation_sidebar_and_city_links.md`. **The final go/no-go is
  the user's** (open in `PLAN.md`); the fallback link list under the macro map is
  kept on purpose.
- **Scaffolding.** `scripts/scaffold_city.py` writes the shared shape of a new
  city; steps 1 and 2 are deliberately not generated (copy the nearest built
  city). It has been tested only against a scratch copy of the repo structure,
  never by building a real city with it.
- **Drift check.** After any pipeline change, `python pipeline/drift_check.py
  [city]` re-runs the pipelines from local raw data and diffs against git HEAD,
  normalizing Folium's random element ids and CRLF/LF. Baseline at `520c165`:
  **zero drift on all four cities.**

## 6. Working rules and the user's preferences

Read `CLAUDE.md` for the project rules. Beyond it:

- **Recommend, then confirm.** For judgment calls (scope, classification, UI
  choices), give a recommendation and its main trade-off in chat and wait for a
  short yes before writing. For UI choices the user liked a **visual side-by-side**
  (a comparison page rendered in the Browser pane) before deciding.
- **Log every judgment call** in `DECISIONS.md` (append-only; use the
  `decisions-entry` skill). Never edit an old entry; add a new one. Include the
  numbers that were true and what was rejected.
- **Commits.** Commit after each green step; push to `origin master` after
  committing. Never amend unless asked; never force-push; **never touch git
  config** (pass identity per command:
  `git -c user.name=dacekroberts -c user.email=49654908+dacekroberts@users.noreply.github.com commit ...`).
  The commit trailer comes from the harness's attribution instruction for your
  session; follow that. **Stage files by name and read `git status` first:**
  the previous session once swept an unreviewed stray file into a public commit
  with a broad `git add docs`.
- **Pacing.** Check usage before proposing big work
  (`mcp__ccd_session_mgmt__get_usage`, load via ToolSearch). The user holds work
  when a limit is close rather than leaving half-built state; the 5-hour limit is
  the usual constraint. Give effort estimates as relative guesses, not measurements.
  As of 2026-09-21: Pro plan with a 5-hour and a weekly window; the weekly window
  resets **Sundays about 19:00 UTC** (next: 2026-09-27); extra usage is **disabled**,
  so reaching 100% stops work instead of billing. (The previous session's two saved
  memory notes, on pacing and on recommend-then-confirm, are fully reflected in this
  section; there is no need to import them.)
- **Servers.** Start test servers with `mcp__Claude_Browser__preview_start`
  (`streamlit-app-lean` on 8812, `heatmap-static` on 8813, defined in the
  gitignored `.claude/launch.json`); stop them when asked and confirm the ports
  are free. Never leave one running unasked.
- **Be honest about slips.** The user values a plain account of mistakes and of
  what was and was not verified. Keep summaries short.
- The user develops on Windows (desktop, Opera GX browser, no phone testing;
  Remote Control is enabled for occasional use away from the desk).

## 7. Environment and tooling gotchas (these cost real time)

- Two Python environments. **Pipeline:** the global Python 3.14 (geopandas 1.1.4,
  folium 0.20, pandas 3.0.6), run as `python3`. **App:** `.venv-lean`
  (streamlit 1.64.0, pydeck 0.9.3). Always verify the app from `.venv-lean`.
- **A running Streamlit serves an edited shared module (`app/components.py`) from
  cache.** Clear `__pycache__` under `app/` and `pipeline/` and restart the server
  before trusting a check.
- Bash-tool heredocs with mixed quotes have failed to parse as a whole (nothing
  ran). Write scripts to files with the Write tool and run them. In PowerShell,
  `"$port:"` is parsed as a drive; use `${port}`.
- Browser screenshots are scaled and can be a frame behind; prefer DOM/JS
  measurements (`javascript_tool`) and confirm visually second. The map's fixed
  controls are measured inside the iframe (`f.contentDocument`), which is
  same-origin.
- The repository stores LF (`.gitattributes`); a Windows working copy may show
  "CRLF will be replaced by LF" warnings once; harmless.
- Raw data in `data/` is a **dated local snapshot** (Chicago: 2026-09-20; LA
  geocoding uses a hash-keyed cache under `data/los_angeles/raw/`). A fresh clone
  has no `data/`, so the pipelines and the drift check cannot run there; each
  city's `config.py` records the exact download commands.

## 8. What has and has not been verified (the honest ledger)

**Verified, and how**
- Zero drift on all four cities at `520c165` (`pipeline/drift_check.py`).
- Behaviour of the app in the Claude desktop app's built-in Browser pane
  (Chromium), Streamlit 1.64.0, desktop and a 375 px emulation, by driving the
  page and reading the DOM: macro map and marker clicks, the four city pages,
  dark mode both ways and its persistence between maps, the "All cities" button
  (navigates in place; verified the window object survives), the "Cities"
  dropdown, the sidebar hidden, no console errors, no server deprecation warning.
- `scripts/check_map_labels.js` passes on all four standalone maps: every line
  label in view, none overlapping each other, the legend or the buttons; legend
  collapses.
- The scaffold script against a scratch copy (dry run, re-run, reused and new
  taxonomies, generated files compile and import).
- `requirements.txt` set installs and runs the app (the lean venv is built from it).

**The independent `deploy-verify` agent** (`.claude/agents/deploy-verify.md`)
**last ran on commit `c29d7fb` (all six checks passed).** These later changes were
verified only by the session's own browser checks, not by the agent: the
`st.iframe` migration (`0602c84`), the "All cities" button and map-only pilot
(`8c59cb4`), and the "Cities" dropdown (`520c165`). Running it is a good first move.

**Never done: treat as unknown**
- **A real deploy** to Streamlit Community Cloud. In particular: whether the
  `localStorage` sharing between the app page and the srcdoc map iframes behaves
  the same when the app is served from `*.streamlit.app` (possibly inside a
  wrapper frame, and with browser storage partitioning), and whether `st.iframe`'s
  same-origin sandbox and the parent-DOM access the buttons rely on still work
  there.
- Any browser other than Chromium in the built-in pane (Opera GX, Firefox, Safari);
  a real phone; a keyboard-only and screen-reader pass; the appearance of the
  *open* native dropdown list; performance of the 5.6 MB Los Angeles page.
- Upgrading Streamlit. The navigation and theme scripts depend on internals:
  `data-testid="stDeckGlJsonChart"`, the `.st-key-map-only-nav` container class,
  page-link anchors, and same-origin `window.parent` access.
- Rebuilding any city from freshly downloaded raw data (the drift check re-runs
  the pipelines on the *existing* local raw files).
- Building a real city with the scaffold; the dataset licences and terms of use for
  the four business registries and the transit feeds; the OpenStreetMap and Carto
  tile usage terms for a public site (open in `PLAN.md`).

## 9. Verification plan: run these, report the results

### A. Repository hygiene
1. `git status`, `git log origin/master..HEAD`, `git stash list` are empty; 32
   commits, 66 tracked files at `520c165` (67 if this file is committed).
2. `git ls-files --eol` shows `i/lf` throughout.
3. Secrets and stray references: `git grep -nIiE "api[_-]?key|secret|passw|bearer "`
   excluding `outputs/` should find nothing (the generated HTML contains business
   names that can false-match). `git grep -niE "seattle|link-station"` outside
   `DECISIONS.md` should hit only `docs/project_context.md:21` and one comment in
   `pipeline/taxonomies/naics.py`; anything else is a finding.
4. `data/` and `.venv-lean/` are ignored and not tracked; `outputs/<city>/` is.

### B. Structural integrity
5. Every city in `app/cities.py` has a page file whose name matches its `page`
   path, a `pipeline/<slug>/config.py` exporting `HEATMAP_HTML` and the names the
   page imports, and `outputs/<slug>/heatmap.html` + `excluded_stations.csv`.
   Page files must keep the `<Name>_Heatmap` naming: the "Cities" dropdown derives
   the current city from the URL. Check the four cities and the scaffold template
   against each other.
6. `python -m compileall -q app pipeline scripts` clean; `python -W error -c` on
   `map_common.py`, `components.py`, `Overview_&_Introduction.py`, `cities.py`
   reports no invalid escape sequences (JS lives inside Python strings and has
   produced such warnings before).
7. Invariants by grep: no `folium|geopandas|shapely|pyproj` import under `app/`;
   `pipeline/*/config.py` import only `pathlib` (the app imports them);
   distances/buffers are computed in a projected CRS (`nearest_station_and_ring`
   and any `.buffer(`); no NAICS prefixes in any `step2_clean_businesses.py`
   (they must call `filter_to_storefront`).
8. `MAP_ONLY_NAV`: with it `True` the sidebar and switcher are hidden and the
   hidden link container exists on every city page; with it `False` the sidebar
   and switcher return and the buttons still work. Test both.

### C. Pipeline reproducibility (on the machine that has `data/`)
9. `python pipeline/drift_check.py` prints `RESULT: zero drift` for all four cities.
   Read what it normalizes (Folium ids regex, CRLF) and confirm it cannot hide a
   real change.
10. For each city, re-read the step 2 filter sequence and compare its printed row
    counts with the baselines in `DECISIONS.md`; look for any filter that drops
    more than a few percent without an explanation (the project's own rule).
11. Chicago: confirm the dedupe-by-site logic and `LICENSE_PRIORITY`, that
    `AS_OF_DATE` makes a re-run deterministic, and that the 108 storefront rows
    without coordinates (0.4%) are as described. Los Angeles: confirm the geocode
    cache makes re-runs deterministic and coordinates outside the city bounds are
    rejected.

### D. Code review targets (highest risk first)
12. `pipeline/map_common.py`: the label-layout search (`_layout_labels`,
    `_choose_view`, `_label_candidates`: it assumes a legend size of
    `178 + 19*n_lines` px by 274 px, so a legend markup change can silently
    regress placement); `THEME_TOGGLE_HTML` (about 150 lines of CSS and JS in a
    Python string: escaping, `hidden` handling, `window.parent` use, timers);
    `load_line_shapes`; the duplicated bucket classification here versus step 2.
13. `pipeline/taxonomies/`: `filter_to_storefront` and `map_common` both handle
    `EXTRA_COLUMNS`; check they stay consistent. `chicago_license.classify` rules
    against the approved rules in `DECISIONS.md` ("catch-all license types" and
    "Chicago built"). `nyc_dca` / `phl_licensetype` are skeletons and must stay
    clearly marked as such.
14. `app/components.py` and `app/Overview_&_Introduction.py`: the injected CSS/JS,
    the `MutationObserver`, the 1 px `st.iframe` script frame, `fit_view` (west
    padding), label sides, the `MAP_ONLY_NAV` branches.
15. `pipeline/drift_check.py` and `pipeline/census_geocoder.py`: correctness of the
    diff and of the cache key.

### E. App runtime
16. Clear `__pycache__`, then start `streamlit-app-lean` and run the
    **`deploy-verify` agent** end to end. Also run `scripts/check_map_labels.js`
    on each standalone map with `localStorage['expanded-heatmap-theme']` set to
    `light` first. Watch the server log for warnings.
17. Try to break navigation: deep-link to a city page by URL, browser back/forward,
    a hard reload on a city page and then "All cities", dark mode set on one map
    then another, `localStorage` blocked (private window), a page loaded with
    JavaScript slow to render the hidden links.

### F. Documentation consistency
18. Known stale items to confirm and list (not necessarily fix):
    - `DECISIONS.md` header says all dates are from 2026-09-18; entries now run to
      2026-09-21.
    - `.claude/skills/add-city/SKILL.md` line 8 says "the three cities actually
      built"; there are four.
    - `docs/dark_mode_handoff.md` opens with a correct status banner but its Scope
      and mechanism sections still describe a different (base-layer) design and an
      undecided toggle placement; it is historical.
    - `README.md` does not mention dark mode, the map-only navigation or the
      scaffold script.
    - `PLAN.md` "Data quality follow-ups" says catch-all classification hand-samples
      are "not yet done for either built city"; there are four cities.
    Then check every numeric or behavioural claim in `docs/project_context.md`
    and `README.md` against the code.

### G. Publishability of the generated HTML (run early; it gates any public deployment)

**Why.** The four `outputs/<city>/heatmap.html` files are committed to a public
repository and are meant to be served publicly. Each embeds business-level
records from public registries. Whether that is acceptable, and under what
terms, has **not been reviewed**.

**What each map embeds** (verified from `pipeline/map_common.py:add_pin_layer` and
the generated files): one pin per business that lies within a station ring, as a
6-field row `[latitude, longitude, business_name, classification, nearest_station,
ring_band]`, in three `var data = [[...]]` blocks per map (one per category), plus
the latitude/longitude of **all** mapped businesses for the whole-city heat layer
(no names there). Pin counts equal the within-ring counts in `DECISIONS.md`
(2,971 San Diego; 13,874 San Francisco; 23,839 Los Angeles; 11,796 Chicago).
Coordinate precision differs: Chicago pins carry about 10 decimal places, Los
Angeles 4 (the source rounds), the others whatever their source provides.

**Where `business_name` comes from, and the fallbacks** (from each
`step2_clean_businesses.py`): trade name (`dba_name`, or Chicago's
`doing_business_as_name`), and **when there is no trade name it falls back to a
registrant or owner name**: San Diego `business_owner_name`, San Francisco
`ownership_name`, Los Angeles the registry's `business_name` (registrant), Chicago
`legal_name`. For sole proprietors those fallbacks are the likeliest source of
**individuals' personal names** in a public map, next to their premises location.
Chicago also excludes activities marked "(Home Based Business)"; whether the other
registries mark or exclude home-based businesses was not checked.

**Extract the pins** (read-only, local files only):

```python
import html, json, re
text = open("outputs/chicago/heatmap.html", encoding="utf-8").read()
blocks = re.findall(r"var data = (\[\[.*?\]\]);", text, re.S)
rows = [r for b in blocks for r in json.loads(b)]      # [lat, lon, name, class, station, ring]
names = [html.unescape(r[2]) for r in rows]
```

(Tested on all four maps: 3 blocks each, 6 fields per row, counts as above.)

**Checks to run and report per city**
1. **Fallback-name share.** Count pins whose name came from the fallback. Use
   `data/<city>/processed/businesses_clean.csv` where it kept the owner column, else
   the raw file under `data/<city>/raw/` (Chicago's clean CSV drops `legal_name`;
   its raw file `business_licenses_active.csv` has it). Each step 2 also prints
   "Filling N blank dba_name(s) from ..." when it re-runs.
2. **Personal-name sample.** Read a random sample of about 200 pins per city and
   classify each name as a business name or a personal name; report the rate and a
   few examples (counts matter more than a list of names in chat).
3. **Residential exposure.** For sole proprietors and any home-based businesses,
   the pin is the premises coordinate, which may be a home. Check which registries
   flag home-based businesses and whether those are already excluded, and sample
   for unit or apartment indicators in the raw address.
4. **Coordinate precision.** Rounding to 5 or 6 decimal places (about 1 m or 10 cm)
   changes nothing visible at ring scale; state whether it would help and where.
5. **Terms of use.** Read the stated licence or terms of each business registry
   (the portals are named in each city's `config.py` and in `DECISIONS.md`) and each
   transit feed: is redistribution of a derived map that lists business names and
   locations permitted, and is attribution required? Also the OpenStreetMap and Carto
   tile terms for a public site (open in `PLAN.md`), and whether the app currently
   shows the attribution each requires (the maps show their tile attribution; the app
   has no credits section).
6. **Verdict per city**, one of: publishable as is; publishable after named
   mitigations; do not publish. Give the evidence (counts, terms quoted or linked).

**Mitigation candidates to propose (do not apply without approval):** drop the owner
or registrant fallback (show only the classification for those rows, or omit them);
omit names from tooltips entirely; round coordinates; drop rows flagged home-based.
For each, say what it costs in accuracy or map value.

**Guardrails.** Do not alter `outputs/`, the pipelines or the map renderer during
this check, and do not publish, upload or share the HTML. The regenerated outputs
would need a drift-check baseline and a `DECISIONS.md` entry if the user later
approves a change.

### H. Deploy readiness (open items already in `PLAN.md`)
20. Tile provider (OSM raster tiles on city maps, Carto vector basemap on the macro
    map); Streamlit Cloud main-file path (fixed at app creation, so settle it
    first); project name; README finish; the 5.6 MB Los Angeles map; the missing
    caveats on city pages (Los Angeles ~9% rows without NAICS; San Francisco ~37%
    with NAICS; San Diego undercounts neighbourhoods recorded under their own name,
    La Jolla foremost).

## 10. Known limitations already documented (do not report as new)

Chicago: Metra excluded; Yellow Line not drawn; 108 storefront rows without
coordinates dropped (bias not analyzed); buckets are only approximately
comparable with the NAICS cities. Los Angeles and San Diego markers touch at phone
width (the fallback link list is the safety net). The map scrolls inside its
iframe on narrow screens (the Leaflet.heat workaround). Brown/Purple lines in dark
mode are brightened, not re-coloured. The macro map's page chrome is light.
`deploy-verify` and the scaffold are as described in section 8.

## 11. Open work (`PLAN.md`)

Next city (start at `add-city` Step 0, then the scaffold; that build is the
scaffold's first real test); the map-only pilot's go/no-go; page-level dark mode;
the two remaining taxonomy skeletons; the before-deploy items; data-quality
follow-ups; macro-map grouping at scale.

## 12. Suggested reading order

1. `CLAUDE.md`, 2. `docs/project_context.md`, 3. `PLAN.md`, 4. this file's
sections 8-9, 5. `DECISIONS.md` (skim headings, then the Chicago, Dark Mode,
`st.iframe` and navigation entries), 6. `pipeline/map_common.py`,
`pipeline/taxonomies/__init__.py`, `app/components.py`, one full city
(`pipeline/chicago/` is the newest), 7. `.claude/skills/*` and
`.claude/agents/deploy-verify.md`, 8. `docs/navigation_sidebar_and_city_links.md`.

## 13. What to hand back

A findings report in chat, ordered by severity, each item with **evidence** (a
command and its output, or a `file:line`), a **why it matters**, and a
**proposed fix** kept separate from any change made. Include the **per-city publishability verdict** (9G) as its own short section. Then:
what you checked and found sound; what you could not check and why; and any claim in this file that
turned out to be wrong. Keep it concise; the user reads the summary first.
