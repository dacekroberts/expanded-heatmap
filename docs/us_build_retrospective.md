# Retrospective: the US build, nine cities to first deploy

Written 2026-09-21, at the point where nine US cities are built, the site is
live, and the next city is Vancouver — the first outside the US.

**Scope note.** This file sits in `docs/`, which `session_roles.md` assigns to
the staging session. It was written by the build session at the owner's
request, as a cross-cutting retrospective rather than staging research output.
Flagged rather than filed silently.

**Claim labels**, per `session_roles.md`: **MEASURED** carries a number and the
command or query that produced it; **ASSERTED** is plausible and unverified.
Almost everything below is MEASURED, because the recurring lesson of this
project is that the asserted version was wrong about a third of the time.

---

## 1. What exists now

MEASURED — from each city's step output on 2026-09-21, after the rings-off
re-render:

| City | Within ring | Available | Stations | Notable |
|---|---|---|---|---|
| New York | 44,360 | 62,441 | 496 | 4 registries; 0.3 mi rings |
| Los Angeles | 14,019 | 58,173 | 56 | geocoding step; 9% corrupt coords |
| San Francisco | 12,376 | 17,837 | 49 | own palette; street-running thinning |
| Chicago | 11,796 | 20,686 | 123 | own licence taxonomy |
| Philadelphia | 4,954 | 8,504 | 94 | two buckets; two station rules |
| Washington D.C. | 3,860 | 5,230 | 40 | all three buckets, one registry |
| Miami (Regional) | 3,775 | 29,878 | 42 | first regional city, 6 municipalities |
| San Diego | 2,577 | 10,955 | 47 | first city; 16 stations out of scope |
| Boston | 2,410 | 3,164 | 57 | three registries, two buckets |

Nine cities, five taxonomy modules beyond NAICS, five mandatory source
notices displayed, one live site, one licence question still open.

---

## 2. Chronology of the final session

Seventeen commits, `38d4bd0..7e2082d`, 72 files, +20,920/−11,690. Ten were the
build session's, seven the staging session's once the two split.

1. **`d9e7f4f` Washington D.C.** — ninth city. First registry here covering all
   three buckets alone; first feed behind an API key; first feed with a
   validity window (ten days); second city needing a geocoding step.
2. **`47d893a` The pre-deploy gate** — the five required notices put on every
   page, two documentation pages added, accuracy sweep, MIT licence with a
   data carve-out, project renamed, entry point renamed.
3. **`48f6e29` The live URL** recorded after deploying to Streamlit Cloud.
4. **`7368255` Rings off by default** on every city.
5. **`688645c` The 1 px script frame** that was painting a visible dash.
6. **`e99551d` The three licence questions read** — two closed, one got worse.
7. **`7fc8dbb`–`114a8c0` Philadelphia** — reasoned interim position, drafted
   request, corrected addressing, sent, follow-up scheduled.
8. **`d6d30a0` Macro-map markers shrunk**, closing the deferred polish pass.

Interleaved, the staging session screened Canada (`3488f11`), generalised it
into an `add-country` skill (`c66e638`), and split the sessions by role and
path (`3f19031`).

---

## 3. What went wrong, grouped by the lesson

This is the part worth keeping. Each item is a real correction, not a
hypothetical.

### 3.1 A percentage is only as good as its denominator

Step 0 for D.C. recorded "trade name missing on 49% of storefront rows … the
Los Angeles trap at half LA's severity". MEASURED on the rows that actually
reach the map: **26.9%**, of which 85.6% carry a company-shaped legal name, and
the person-like residual is **14 pins, 0.36%**. The 49% had been measured
before the category exclusions, and `General Business` — 11,074 office rows,
mostly with no trade name — was most of it.

The same probe got two more numbers wrong the same way: the office catch-all
was recorded at 14,770 (it is 11,074 once scoped to active and in-District),
and `MAR_ID` was expected to recover the rows missing coordinates when they are
*the same rows*.

**Rule:** never record a percentage without naming the set it was measured on,
and re-measure on the set that reaches the output.

### 3.2 A licence is not one document — follow every pointer

Three separate corrections, all from opening a page an earlier review had
merely cited:

- **NYC** (earlier session): the nyc.gov footer's "All Rights Reserved" covers
  the website; Local Law 11 *forbids* the City from licensing its open data.
- **SEPTA** (this session): the "non-commercial" wording that made a portfolio
  site look prohibited lives in the *Web Contents* section of a Copyright
  Notice governing septa.org's own pages. The datasets carry an express grant
  to "use, reproduce and redistribute". And the Trademark Notice the licence
  points at claims exactly one thing: "The SEPTA Logo". Line names and route
  colours are not claimed anywhere.
- **Philadelphia** (this session): the dataset page incorporates
  `phila.gov/terms-of-use` **by reference**, and those terms prohibit
  "distribution or republication in any other form … and any modification
  whatsoever" without written permission. That inverted the position from
  "silence" to "prohibition".

And one correction in the other direction: Miami-Dade was recorded as "the only
one of the three where no agency document exists to read". One does —
`opendata.miamidade.gov/pages/terms-of-use`, two clicks from the portal footer.
It contains only an accuracy disclaimer, which turns "we found nothing" into
"the County's own terms impose no restriction": a stronger position, reached by
reading rather than asking.

**Rule:** a dataset's terms are not the publisher's website terms, and neither
is necessarily the whole instrument. Chase every reference before calling a
position established.

### 3.3 Measure in the environment the user actually sees

I measured WMATA's grey Silver Line against the **light** basemap, found it the
weakest colour in the project (ΔE 22.0 from OSM's track fill), recommended
darkening it, and the owner approved on those numbers. The map **opens in dark
mode**, where line strokes are brightened rather than inverted while the tiles
are inverted underneath. Both sides of the comparison move, oppositely:

| | dark (default) | light (toggle) |
|---|---|---|
| `#919D9D` official | 75.4 | 22.0 |
| `#5F6A6A` darkened | 47.2 | 41.0 |
| for scale, Blue | 81.7 | 54.3 |

Darkening made it the worst-contrast line in the city *in the mode every reader
sees first*, and in the render it was untraceable. Reversed to the published
colour.

**Rule:** identify the default state before measuring anything visual, and
measure every mode a reader can reach.

### 3.4 A check that cannot fail is not a check

`scripts/check_map_labels.js` reported "legend does not collapse" on **every**
city. It read the legend's height as found, called that the open height, then
collapsed it and compared. At narrow widths the legend renders **closed** on
load (37 px, no `open` attribute) — so it compared 37 against 37. Every map had
been "failing" that assertion invisibly, and the surrounding checks were
passing vacuously alongside it.

**Rule:** when a check fails everywhere, suspect the check. When it passes
everywhere, make it fail on purpose once.

### 3.5 Required notices behind a toggle are not displayed

I first put the five mandatory source notices inside a collapsed
`st.expander`. Streamlit keeps a collapsed expander's contents **out of the
DOM** — so the notices were absent until a reader clicked, not merely small.
Chicago's terms require its paragraph "at the site where the software
application … can be accessed", and this project's own rule for the OSM
attribution is that it must not sit "beneath UI, behind toggles, or
off-screen".

Caught by probing the rendered DOM for each notice's text rather than looking
at the page.

### 3.6 Geometry beats intuition, in both directions

- **Boston's Mattapan Trolley** was not thinned, against the obvious guess: its
  stops are a median 518 m apart, comparable to New York's 482 m and nowhere
  near San Francisco's 134 m.
- **Boston College** is in Newton, 6.6 m outside Boston — two independent
  boundary layers agreed, overturning a Step 0 assertion that it was "really a
  Boston station". *Naming beat measuring.*
- **Macro-map marker displacement** is arithmetically dead: at the fitted zoom
  1 px ≈ 21.7 km, so separating New York from Philadelphia needs **217 km** of
  displacement. Worth computing once to kill an idea permanently.
- **Padding `fit_view` to make room for labels is counterproductive**: the view
  is longitude-bound, so widening the box lowers the zoom and pulls the cluster
  *tighter*.

### 3.7 Operational mistakes, listed because they were avoidable

- **A broad `pkill -f "streamlit run"`** was run in a shared environment. It
  matched no Windows process by luck, but the pattern was wide enough to hit
  another project's dev server — and that server did stop during the session.
  Cause not established. Kill by PID, or by a path-scoped filter, never by a
  tool name.
- **Heredoc quoting broke twice more**, after the project had already learned to
  write scripts to files. The lesson does not stick unless it is the default.
- **A stale view was misdiagnosed as a failed change**: Streamlit serves a
  cached copy of an imported module across reruns, so edits to `cities.py`
  appeared not to apply. Restart the server when editing an imported module.
- **`drift_check.py` regenerates `outputs/`**, which churns every
  `heatmap.html` with fresh random Folium element IDs. Discard with
  `git checkout -- outputs/` rather than committing 6,000 lines of noise.

---

## 4. Skills and subagents worth building

Each tied to an incident above rather than invented.

### 4.1 `read-licence` (skill) — highest value

The three corrections in §3.2 would all have been caught by one checklist:

1. Fetch the dataset's declared licence field *and* any named licence document.
2. **Follow every pointer** the licence makes — "see our X notice", "subject to
   our terms of use", "accompanying conditions".
3. Search the dataset page for incorporation language: *"constitutes
   acceptance"*, *"subject to"*, *"agree to be bound"*. Read whatever it names.
4. Separate **website terms** from **dataset terms**. Ask explicitly: does this
   document's language describe web pages (printing, "as presented") or data?
5. Check whether the publishing portal is the publisher. A third-party
   catalogue's assertion is weaker — but check the publisher's own catalogue
   too, because it may say the same thing (Philadelphia's did).
6. Record which specific claims are MEASURED from the document text and quote
   them.

### 4.2 `verify-render` (skill, or extend `deploy-verify`)

Three lessons the current agent definition does not carry:

- On **hosted** Streamlit, DOM probes return an empty body while the page
  renders fine. Screenshot first; treat `innerText` as unavailable.
- **Identify the default theme before measuring colour**, and measure both.
- A **collapsed `st.expander` is not in the DOM** — so "is this text present?"
  and "can a reader see this text?" are different questions.

### 4.3 `contrast-check` (small script, not an agent)

Reusable: given a candidate colour, report CIE76 ΔE against the basemap fills
*in both modes* and against the three bucket colours, applying the dark-mode
CSS filter chain (`invert hue-rotate brightness contrast saturate` for tiles,
`brightness(1.55) saturate(0.9)` for strokes). Written ad hoc twice this
session; should be `scripts/check_colour_contrast.py`.

### 4.4 A batched browser-verification subagent

Running the label checker across nine cities meant re-sending a ~1,500-character
JS payload per city because navigation clears the page context. A subagent
given "run this file's contents against these nine URLs and report only the
`problems` arrays" would cut that to one dispatch. This is the single largest
token cost of the session that bought no new information.

### 4.5 `add-city` amendments

- **Step 0 must state the denominator** of every percentage it records.
- **Feed validity windows**: check `feed_info.txt` for `feed_end_date`; if the
  window is short, the fetch script must re-check it on every run, including
  runs that skip the download. WMATA's is ten days.
- **Keyed feeds**: read the key from the environment, never echo it — not even
  in an error message — and exit with instructions when absent.
- **The download boundary is the privacy control.** D.C.'s `outFields` list
  omits eight personal columns, so they never reach the machine. Stronger than
  filtering later, and step 2 asserts they stayed absent.

---

## 5. What the process got right

Worth recording so it is not accidentally dropped:

- **Step 0 before code.** Denver and San Jose both looked viable from dataset
  titles and had no usable data. The discipline paid for itself repeatedly.
- **`DECISIONS.md` as an append-only trail.** Every reversal in §3 was
  recoverable because the original reasoning was still there to contradict.
- **Taxonomy plurality.** Five local taxonomies coexist with NAICS and
  `map_common.py` names none of them, so a city with an unusual register needed
  no fork.
- **The privacy screening as a habit, not a gate.** It has no pass mark, which
  is why a 0.00% reading could be recorded as a *measurement gap* (Boston,
  D.C.) rather than a win.
- **Refusing to read licences generously.** The project recorded three
  questions as unresolved for days rather than assuming. One turned out to be a
  prohibition.
- **Verification finding real defects.** The final pass caught Boston's Blue
  Line label hidden under a map button at 854 px, and the checker bug in §3.4.

---

## 6. Open items

- **Philadelphia's permission request**, sent 2026-09-21; follow-up scheduled
  for the 28th. The map is live on a disclosed reasoned position, not a
  resolved permission.
- **Optional Carto API key.** Carto's basemaps now need one (free to 5M
  tiles/month); the macro map uses the undocumented keyless CDN. If withdrawn,
  that basemap goes blank while markers, pills and the link list keep working.
- **New Orleans and Seattle**, both deferred post-deploy. Seattle is the
  multi-municipality build and needs multi-polygon scope, per-jurisdiction
  provenance and cross-registry dedup.
- **Vancouver**, briefed by the staging session and not yet started — the first
  non-US city, so `add-country` applies and the brief's ASSERTED claims need
  verifying before anything is built on them.
