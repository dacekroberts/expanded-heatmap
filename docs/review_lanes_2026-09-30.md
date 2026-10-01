# The mega-review in lanes (owner, 2026-09-30)

The owner's call: this review batch (every build since the second review, about
120 cities on the site) is verified by several sessions at once, each taking one
angle, instead of one `full` deploy-verify in one session. The cleanup session
prepared the batch as one branch and lands it; the lanes only look.

## The batch

`review-rehearsal` (local, cleanup's worktree): every queued branch merged in
landing order with each conflict resolved and git's rerere recording the
resolutions, then reconciled (master list, tram list, notices). `check_all`
passes 29 of 29 on it. In landing order:

- France: `france-build-2` (macro-france inside it), then `france-build-3`
  (Angers) - 21 cities, France North and South at zoom 5.0.
- Band B: Ottawa, Minneapolis, Pittsburgh, Kitchener–Waterloo (Regional),
  Palma, Yokohama, Hiroshima, Namyangju, Ansan, Uijeongbu, Anyang.
- Dallas.
- bergen-date, houston-caption, map-labels-madrid-oslo, continuity-calls,
  aarhus-baseline.
- Czech: `czech-build` - Brno, Plzeň, Olomouc, Ostrava, Liberec (Regional),
  Most (Regional); with Prague, a macro region of their own, **Czechia**.
- The misc tram session's three cities (added when they land).

**Held out:** `buffalo-label` (owner, until the batch has rendered).

**Notices, renumbered in landing order:** 69-71 France (TaM, M réso, LiA),
72 Ottawa, 73 Region of Waterloo, 74 Palma, 75 Yokohama, 76 Hiroshima,
77 Angers, 78 KORDIS (Brno), 79 PMDP (Plzeň); 68 (SEMAS) names every Korean
satellite. The misc cities' notices follow from 80.

## How the lanes work

- **One pinned commit.** Every lane checks out the same commit of
  `review-rehearsal` (cleanup names the SHA in each prompt) in its own
  worktree, detached, with `data/` linked to the shared folder (a junction,
  never a copy). A lane never commits, merges or pushes.
- **Look, don't fix.** A lane reports findings; cleanup fixes them on the
  rehearsal, and the lane that found a defect re-checks only that defect
  afterwards, at the narrow scope (deploy-verify's own rule: `full` is for a
  batch, not for a fix).
- **Its own ports.** Each worktree's `.claude/launch.json` keeps deploy-verify's
  configuration NAMES (`streamlit-app-lean`, `heatmap-static`) on the lane's
  ports below, and the lane tells deploy-verify to leave them as they are. Two
  lanes on one port stop each other's servers.

  | Lane | Streamlit | Static maps |
  |---|---|---|
  | 1 | 8831 | 8832 |
  | 2 | 8841 | 8842 |
  | 3 | 8851 | 8852 |
  | 4 | 8861 | 8862 (if it needs one) |

- **Memory.** A lane's app is about 0.2 GB; four fit easily. Nothing here is a
  heavy job, but a lane that runs a drift check or reads a raw register goes
  through `scripts/heavy_job.py` like any session.
- **Reports.** Each lane writes its report to its own session scratchpad and
  sends it to the cleanup session. Every finding has its page or file, the
  width and theme, what it shows, and whether it blocks the landing. Cleanup
  merges the reports into one review page for the owner.
- **Together the lanes cover `full`.** The rule that a real deploy needs a
  `full` sweep is met by the union: lanes 1 and 2 take every new city page,
  lane 3 every shared surface (all five fixed pages, the theme, the click
  paths, the macro map, the deploy dependencies), and lane 4 the prose
  `full` never reads.
- **Owner only:** the iPhone check, the reboot, and the calls each lane
  surfaces.

## Lane 1 - the French cities (21)

deploy-verify `scope: city-added` naming the 21 French batch cities:
Montpellier, Nice, Strasbourg, Bordeaux (Regional), Nantes (Regional), Grenoble
(Regional), Rouen (Regional), Saint-Étienne, Angers, Dijon, Tours, Le Havre,
Mulhouse, Reims, Caen, Brest, Besançon, Orléans, Le Mans, Avignon, Valenciennes
(Regional). Plus, for each page:
- `node scripts/check_map_labels.js` on its map; no error block on the page;
- the caption's dates match `outputs/<slug>/provenance.json`;
- its notice in the site notices (69-71, 77, or the shared SIRENE/INSEE ones),
  and **Angers mark-free**: the network brand appears nowhere the app shows
  (page, caption, macro label, notice);
- the macro views **France North** and **France South** at 375, 768 and 1200:
  every French dot and label, both themes.

## Lane 2 - Band B, Korea, Dallas, Czechia and the misc cities

deploy-verify `scope: city-added` naming: Ottawa, Minneapolis, Pittsburgh,
Kitchener–Waterloo (Regional), Palma, Yokohama, Hiroshima, Namyangju, Ansan,
Uijeongbu, Anyang, Dallas, Brno, Plzeň, Olomouc, Ostrava, Liberec (Regional),
Most (Regional), and the misc session's three. The same per-page checks as
lane 1, and:
- the one-category pages (Ottawa, Minneapolis, Pittsburgh, Hiroshima) say
  plainly what is missing; Yokohama says it is the first page not built on food;
- Dallas: the residential rule that cannot run and its two template departures
  are disclosed as written (owner's flags);
- the macro views **Seoul Capital Area** and **Czechia** (new: all seven Czech
  cities, Prague moved in) at three widths, both themes.

## Lane 3 - the shared surfaces and the deploy

deploy-verify `scope: map-chrome` across EVERY city's map (the re-rendered
Madrid, Oslo and Fukuoka included), plus `scope: app-deps`, plus full's
non-city steps:
- the five fixed pages, both themes, the nav and the Cities dropdown, the
  click paths;
- the macro map's **two-key legend** (colour = mode, fill = coverage) against
  `app/cities.py` for a sample from each tier, the tooltip text, and every
  region's frame at 375, 768 and 1200 (`check_macro_labels.py` scores the
  geometry; this looks at the rendered page);
- `node scripts/check_macro_attribution.mjs` at 375, 768 and 1200;
  `check_map_attribution.js` at 650, 768 and 812 on a sample of new maps;
- `python scripts/check_inline_arrays.py`: no map holds a JS array an iPhone
  cannot compile;
- the Overview's city list on a phone (about 39 screens at 106 cities): report
  its length at 120 for the owner's layout call, but don't change it.

## Lane 4 - prose, notices and records (no browser, or one render)

Reads, doesn't render:
- the site notices as `render_site_notices()` builds them against
  `docs/data_sources.md` notices 68-79 (+ the misc cities'): every MUST
  DISPLAY verbatim, every credit linked;
- the What Is Excluded page and `docs/excluded_categories.md` for every new
  city; `check_scope_disclosure.py`;
- captions: Houston (provenance's as_of_date) and Bergen (register 2026-09-24);
- each new city's `check_personal_exposure.py` verdict recorded (in DECISIONS
  or its drafts file);
- `docs/map_inconsistencies.md`: the themes the new cities make stale (4, 6,
  and the per-country lists in 1, 8 and 9) and Prague's stale table-B pins
  (6,027 / 5,464 / 6,122 against its map's 6,003 / 5,444 / 6,081);
- `python scripts/check_stale_claims.py` and `check_plan_done.py` (they report;
  list what the batch made stale);
- the drafts to fold into DECISIONS at landing (`docs/decisions_drafts/`):
  list each file and any entry that names a notice number from before the
  renumbering (yokohama.md says 69 for 75, hiroshima.md 69 for 76).

## After the lanes

Cleanup fixes the findings on the rehearsal, the finding lanes re-check their
defects, and the owner decides the calls. Then: `git fetch`, merge
`origin/master` into the rehearsal, `check_all`, `check_deploy_imports`, one
push to master, **one reboot**, one live check (`publish-city`'s gate), the
owner's iPhone check. Then the drafts are folded and the branches retired with
the owner's word.

## Later: the site-wide prose and UI pass

After this lands, the owner plans a second delegated review: every element of
the site except the maps themselves, made succinct and readable for a general
audience. It gets its own lane plan then; findings from lane 4 that are about
tone rather than correctness are kept for it, not fixed now.
