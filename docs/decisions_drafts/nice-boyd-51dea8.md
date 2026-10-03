# DECISIONS drafts - nice-boyd-51dea8 (`claude/nice-boyd-51dea8`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-02 - Required notices: each city's own on its page, six on every page, all on a new page (owner)

- **The call (owner, 2026-10-02):** stop rendering every required notice on
  every page.
  - **Each city page** shows its own notices first, in full and inline, at
    body size rather than caption size. That keeps TransLink's legend (11)
    prominent on Vancouver (Regional), CRTM's (20) on Madrid, and the three
    Ordnance Survey statements legible on each of the eight UK pages that
    carry them.
  - **Every page** keeps OpenStreetMap's basemap line (1), Chicago (2), LA
    Metro (4), INEGI (8), Barcelona (21) and Kansas City (80), plus
    `_AS_RECORDED`, `_NON_AFFILIATION`, `_UNSETTLED_TERMS` (unchanged) and a
    link, "All required source notices".
  - **A new page, Required notices** (`app/pages/Required_Notices.py`,
    `components.NOTICES_PAGE`), lists every notice verbatim in
    `data_sources.md`'s number order, under the footer's existing intro.
- **Why these six stay on every page.** Cleanup's read of 2026-10-02 sorted
  the 114 notices by where their terms put them. Each class's deciding words
  were checked against the record.

  | Class | Notices | Where | Deciding words |
  |---|---|---|---|
  | SITE | 2 Chicago, 80 Kansas City | every page | "at the site where the software application ... can be accessed" (`data_sources.md`, items 2 and 80) |
  | UNCLEAR | 4 LA Metro | every page | acknowledgement "as set forth in the Web Services Developer Guidelines", which could not be read |
  | WORK, reaching the Overview | 8 INEGI, 21 Barcelona | every page | INEGI §1(g), notify "al usuario final de cualquier análisis o transformación"; Barcelona, changes "identified as such at the time of their distribution" |
  | PROMINENT | 1 OSM, 11 TransLink, 20 CRTM | OSM on every page and every map; 11 and 20 at body size on their pages | ODbL "not beneath UI, behind toggles, or off-screen"; TransLink "prominently displayed"; CRTM "Debe quedar claramente la indicación" |
  | WORK, one city | 3, 15, 24, 25, 26, 69, 70, 71, 77 | their pages | a notice carried with the derived work, which is the city's page |
  | ANY | 89 others | their pages | a credit with no place prescribed |
  | Ordnance Survey | 59, 63, 85, 88, 90, 92, 94, 96 | their pages, in full | the OGL's "including or linking to": all three statements on each UK page, and every page links to the full list |

  - New York (5) stays undisplayed, as before. It is a conditional duty met by
    About the Data and What Is Excluded, and is now named in
    `check_provenance.py`'s `NOT_DISPLAYED`.
- **The structure.** Each `_NOTICES` entry is a `Notice(number, heading,
  text, verbatim, cities, every_page)`. Notices that cover several cities name
  them through module-level groups: `_MEXICO`, `_NORWAY`, `_DENMARK`,
  `_CZECHIA`, `_BRAZIL`, `_KOREA_SEMAS`, `_UK_SIX` and `_OSM_RAIL` (the 52
  cities the rail-geometry sentence names). No verbatim string changed. The
  basemap line, hard-coded in the renderer until now, is a `Notice(1, ...)`
  of its own with the same text.
- **The checks.**
  - `check_provenance.py` C now matches each entry by number, not heading
    alone, and runs in reverse: a numbered notice displayed nowhere fails.
  - New check N fails four things: a city name not in `app/cities.py`; a
    city page that does not pass its own name to `render_site_notices()`; an
    every-page set other than {1, 2, 4, 8, 21, 80}; and any notice whose text
    is missing from the notices page or from a city it names. The last is
    checked by rendering against a stand-in for streamlit. Negative-tested on
    a bad city name, an empty notices page and a dropped Ordnance Survey line.
  - `check_deploy_imports.py` now wants `render_site_notices("<name>")` on
    each city page.
  - `rendered_surfaces.py` lists the new page.
- **Pages.** All 144 city pages changed one line, the call. The scaffold and
  France templates match it. The 21 French pages were regenerated with
  `france_page.py --write` and differ from the template by that line only.
- **Measured** (local lean server, pages in exact-size iframes):
  - **Edmonton at 375 px: 31,466 px before** (the brief's 31,443 by a
    slightly different measure) **and 6,408 px after.**
  - Other pages at 375 px: the Overview is 5,066; Chicago 4,900; Vancouver
    (Regional) 6,075; Madrid 6,397; London 6,294; Manchester (Regional)
    6,643; Mexico City 7,637; Seattle (Regional) 6,777; Montpellier 6,259.
  - The Required notices page is 51,508 px at 375 and 18,371 at 1200.
  - No page overflowed sideways at 375 or 1200. A city's own notices render
    at 16 px, the every-page set at 12.8 px.
- **For review time:** the new page's browser title, "Required notices",
  and heading, "Required source notices", reuse the footer's existing
  wording. No other reader-facing sentence was written.
