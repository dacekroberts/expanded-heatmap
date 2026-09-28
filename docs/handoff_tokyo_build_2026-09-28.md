# Handoff - the Tokyo build session (from "Fukuoka handoff", "Staging and build handoff" and "Tokyo sources research", 2026-09-28)

**The one handoff for the Tokyo build session.** It consolidates three
earlier ones: the Japan build session's Tokyo plan, the build role from
"Staging and build handoff", and Tokyo sources research's closing note. The
first and third files are deleted. The staging role keeps its own handoff
(`docs/handoff_staging_2026-09-28.md`). Read this once and follow the
pointers. **When a section is done, delete it rather than adding an
addendum.**

This session builds Tokyo, then carries the BUILD role (section 7).

## 1. Read first, in this order

1. **The `japan-city` skill**, then **the `tokyo-ward` skill**, which covers
   only what a ward adds. Between them they are the manual.
2. **`docs/build_briefs/tokyo.md`**, especially "Ward cards" (all 23 wards
   settled 2026-09-28) and "Rail". Run `python scripts/brief_check.py tokyo`
   before any code.
3. **`pipeline/tokyo/wards.py`**: the roster, and the one place a ward is
   switched on.
4. DECISIONS 2026-09-28:
   - "Tokyo's groundwork built";
   - "Tokyo's missing wards" (from the research);
   - "Before Tokyo";
   - the memory-cap entry.

## 2. Where things stand

- **Tokyo is BUILT on `worktree-japan` and held for review time** (2026-09-28;
  pushed to origin at `52c9334`, master merged in; nothing of Tokyo is on
  master). 63,989 storefronts, 490 stations (293 hollow), 52 lines labelled by
  line code; every text owner-approved; 23 of 23 checks, zero drift in 55
  cities. What it built and decided: DECISIONS 2026-09-28, the four "Tokyo"
  entries; what it left the next city: the `japan-city` skill's Tokyo sheet.
  **At review time**: the full deploy-verify (scope `city-added`, Tokyo is the
  only new city; `map_common` and `components.py` changed, so the other maps'
  legends and the notices list are worth a `map-chrome` look), `publish-city`,
  and the reboot (`app/cities.py` and `components.py` change).
- The earlier state, kept for the build role:

- **Worktree** `.claude/worktrees/japan`, branch `worktree-japan`. **This
  session takes it over** from "Fukuoka handoff", which closes first. It
  holds:
  - the Tokyo groundwork;
  - master merged to `9248386`: the review batch (Sapporo, Fukuoka, Kyoto,
    the macro-map tiers) landed at `c2864b8` and the owner has rebooted the
    app;
  - the research branch `worktree-tokyo-sources` (`36eb5d7`) merged in.

  The groundwork is only here, and master holds none of it until Tokyo's
  review time. It comprises:
  - the two skills and the roster;
  - the per-ward municipality;
  - the per-ward share check;
  - hollow no-data stations in `japan_step1` and `map_common`;
  - `japan_official.py` and its census reader.

  The last all-city drift check was zero drift in 54 cities.
- `data/` and `.venv-lean` are junctions to the main checkout's; `git status`
  may show `?? data/`, which is never staged.
- **Cached data:**
  - ward files in `data/tokyo/raw/<code>/`, and Minato's address pair in
    `data/tokyo/raw/` itself;
  - MHLW's slices in `data/mhlw/raw/`, as `<code>_food_business_all.csv`;
  - the yearbook at `data/tokyo/raw/tn24qv190800.csv`;
  - the e-Stat tables and N02 in `data/japan/raw/`.

  Tokyo's OSM station names are not fetched yet, and fetching them needs the
  owner's OK.
- **Retire when read:** the `tokyo-sources` worktree, and `main-build`
  (branches `worktree-main-build`, `review-2026-09-28b`, `macro-tiers`,
  `build-sapporo`, all inside the landed batch). Both go through Cleanup;
  run `check_worktree_data.py` first and unlink the junctions alone.

## 3. What is settled (do not re-ask)

- **8 wards ON**: Chūō, Minato, Shinjuku, Taitō, Kōtō, Meguro, Setagaya and
  Shibuya. **15 OFF**, none OPEN. None of the 15 can join the map from its
  own publications:

  | Why OFF | Wards |
  |---|---|
  | released only on request (parked) | Chiyoda, Toshima, Nerima, Edogawa |
  | PDF under site terms that bar reuse | Ōta (owner's call), Arakawa, Kita |
  | nothing published at all | Bunkyō, Suginami, Katsushika |
  | stale, partial or new permits only | Nakano, Shinagawa, Itabashi, Sumida, Adachi |

  Outreach is the last resort: every "route in" in the cards stays parked,
  and none is drafted.
- **Stations in the 15 wards are drawn HOLLOW**: ringless, not counted, with
  a tooltip and a legend row. This is built and tested (Kobe, in scratch).
  **The wording, "No business data: <ward> publishes no usable food-permit
  list", is drafted, not approved**: take it to the owner with the page
  texts. The city line is all 23 wards, so every line runs through the whole
  city. That answers the brief's stub test, which failed on 8 wards.
- **Personal services only where food is ON** (owner): seven OFF wards
  publish barber, beauty and laundry registers (Chiyoda, Bunkyō, Shinagawa,
  Ōta, Toshima, Arakawa, Katsushika). They stay hollow, and those registers
  stay unused; one line in `excluded_categories.md` says so. The layer is
  Minato, Taitō, Meguro and Shibuya.
- **Each ward's share is on the page WITHOUT MHLW's slice** (owner); MHLW's
  +0.1 to +3.1 pt is said once, in prose. Shares are measured every build
  (`OFFICIAL_SHARES`; step 2 writes `official_shares.json` to Tokyo's
  outputs), never typed.
- **MHLW's slice is added to Chūō, Kōtō, Minato and Shinjuku**, de-duplicated
  (`SUPERSEDES`) and listed in `SHARE_SKIP`.
- **Japan-wide rules of 2026-09-28** (in `japan-city`):
  - Numerals are figures before 丁目 in every English station name.
    Before 条 they are figures only where `config.JO_IS_GRID` (Sapporo).
    Tokyo's 十条 is a name ("Jūjō"), so Tokyo has no grid. Fix violations in
    `OSM_NAME_EN_OVERRIDES`, a cited table.
  - Lines served only by limited expresses COUNT (revertible).
  - Coin laundries count as Personal services; welfare-facility salons
    (厚生施設) are out.
  - `pipeline/countries/japan_fetch.py` is every city's fetch.
  - The COVID-era lists are never used.
  - Operator columns are read in memory for the name rule and never kept.

## 5. The macro-map tiers - what every new city needs

- **Every `app/cities.py` entry carries three fields**, inserted before
  `"blurb"`:
  - `coverage` (full / narrowed / one_bucket);
  - `placement`;
  - `data_age`.
- **`scripts/check_macro_facts.py` (pre-push) refuses a city** when:
  - its tier contradicts its table B row in `docs/map_inconsistencies.md`;
  - its phrases state a date or percentage that its table C / D rows do not
    hold;
  - its storefront count in `app/macro_facts.json` is stale.
- **Order of work: the city's table rows first, then the phrases, then
  `python scripts/check_macro_facts.py --write`.**
- **Owner's wording rule**: a source that states no date reads "Fetched
  <date> (no source date)".
- Tokyo is "narrowed". Colours are fixed; there is no dot sizing.
- **The macro tooltip is a panel in the map's bottom-left corner**
  (`app/components.py` CSS, in the landed batch). Keep that in mind when
  touching `components.py`.

## 7. The build role's queue after Tokyo (owner-approved, in PLAN)

In the owner's order, after Tokyo: the additions to built cities.

- **Belo Horizonte + Contagem**: Metrô BH's Eldorado and Novo Eldorado; CNEFE
  13,011; the zip is cached in `data/contagem/raw/`. No rail test needed.
- **Rio + Duque de Caxias**: SuperVia Saracuruna's three excluded stations;
  CNEFE 18,698 (`data/duque_de_caxias/raw/`). **The Gramacho-Saracuruna
  shuttle rail test comes first** (a staging probe).
- **Vancouver (Regional)** + Burnaby, New Westminster, Coquitlam, Richmond:
  28 SkyTrain stations. It waits on staging's probes (Richmond's licence
  read, New Westminster's join) and the owner's Burnaby fetch.
- **Osaka's two fixes**, a re-render each, for a review time:
  - draw the Umekita-Fukushima stretch now that limited-express lines count
    (its trains are the Haruka and Kuroshio; recommend a line to draw it as);
  - the phone-width label overlaps (22 pairs at 343 px), a shared-label-code
    fix that batches with a full re-render.
- **Port Hong Kong's Light Rail thinning and Riga's loop to
  `pipeline/stations.py` `thin()`** (owner-approved), each with its own drift
  measurement. San Francisco, Boston and Philadelphia keep their
  interchange-after-spacing variant until the owner decides.
- Later, the owner's likely next phase: Band T (trams only; EDGE first,
  perhaps) and Band B (one bucket) builds, once staging has their rules
  ready.
- **Durable scratch** (gitignored, main checkout):
  `data/_staging_scratch_2026-09-28b/`. It holds:
  - `incheon_probe/` (the lift-file join and road-interpolation
    measurement, `join_measure.py`);
  - `baltimore_probe/`;
  - `colour_search.py`;
  - `tiers2.ps1` (the tier-palette validation).

## 8. Rules for this session

- **Memory** (CLAUDE.md `[#memory]`):
  - Python is capped at 8 GB a process and 12 GB with its children.
  - **Run one heavy job on the machine at a time, announced to every live
    session before it starts and when it ends.**
  - Drift checks use `--jobs 2` at most, one per machine.
  - A MemoryError is a script to fix, never a cap to raise.
  - Never hand-write a PDF or font decoder.
- **Git:**
  - identity per command only
    (`git -c user.name=dacekroberts -c user.email=49654908+dacekroberts@users.noreply.github.com commit ...`);
  - never change git config, amend, force-push or skip hooks;
  - stage by name;
  - commit messages through a file (`git commit -F`), with the trailer
    `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- **Never push this branch to master.** Back it up with
  `git push origin worktree-japan` (the pre-push hook runs `check_all.py`).
  Landing `app/` on master IS deploying: the owner calls review time.
- **No backslash or backtick in a Bash command**: write the script to the
  scratchpad and run it.
- **Previews**: `.claude/launch.json` in this worktree takes `-tmp` entries
  that are removed when done. The browser checks (`check_map_labels.js`,
  `check_map_view.js`) run in the page: copy them to `outputs/_checks_tmp/`
  and delete that folder after.
- **Downloads need the owner's OK** (file, source, size).
- **Owner approval:** published prose and judgment calls go to the owner in
  this session (recommend, then wait). A peer's relay is not approval.
- **Pacing:** `get_usage` between steps; at 90% of the 5-hour window, finish
  the step, commit clean, and stop with a one-line next action.
- **Tell Cleanup and the staging session your session name** (`ListAgents`).
