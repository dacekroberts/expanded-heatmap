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

- **Tokyo LANDED on master at `80a7a76`** (review time, 2026-09-28): 63,989
  storefronts, 490 stations (293 hollow), 52 lines labelled by line code.
  deploy-verify (`city-added`) found the legend covering 5 labels at the 1000 px
  frame; fixed and re-checked before the push. **Open: the owner's reboot, then
  the live check** (the Tokyo page, the macro map, one untouched city). What it
  built and decided: DECISIONS 2026-09-28, the "Tokyo" entries; what it left
  the next city: the `japan-city` skill's Tokyo sheet. PLAN: Tokyo's page
  scrolls sideways on a phone (its table), for the next `app/` batch.
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

## 7. The build queue (owner, 2026-09-28, after Tokyo landed)

**The earlier queue is wiped.** Two new frontrunners lead it, in this order:

1. **Berlin** (Band B, from the discards 2026-09-28; master list row). IHK
   Berlin's Gewerbedaten: 367,575 per-premises points at their addresses (WFS
   `gdi.berlin.de/services/wfs/gewerbedaten`, CSV 126 MB), WZ/NACE codes, no
   names, monthly, CC0 / dl-de/zero-2.0. Food and shops only: hairdressers
   and laundries belong to the crafts chamber, so Personal services is
   missing (disclosed). Germany's first city: **`add-country` first**, then
   `add-city`. Before the build, per the row: a `licence-read`; a WZ taxonomy
   module keyed on subclasses (restaurants 5611); the personal-exposure check
   (46-59% of storefront entries report 0 employees); registered offices
   stacked at arcade addresses; the rail shape (U-Bahn, the S-Bahn ring,
   trams). **Downloads need the owner's OK** (the CSV is 126 MB).
2. **London** (Band B, from the transit-gap re-screen 2026-09-28). The FSA
   food-hygiene register, keyless API: 81,633 premises, food only (no second
   layer covers central London), 80.2% with coordinates in a sample. The
   UK's first city: **`add-country` first**. Before the build: a
   `licence-read` of the FSA register; placement for the ~20% without
   coordinates (postcode centroids, their own `data_sources` row); the
   personal-exposure check (mobile and home caterers); the rail shape
   (Underground, Overground, DLR, Elizabeth line, Tramlink).

Neither has a brief yet: the first step for each is the brief
(`docs/build_briefs/<city>.md` with a `brief-checks` block), from staging's
screen in the master list's Band B rows.

**Off the queue** (still recorded in PLAN, measured, unqueued until the owner
puts any back): Belo Horizonte + Contagem, Rio + Duque de Caxias, Vancouver
(Regional), Osaka's two fixes (the Umekita stretch; the 343 px label
overlaps), the Hong Kong / Riga `thin()` port.

**Durable scratch** (gitignored, main checkout):
`data/_staging_scratch_2026-09-28b/` (the Incheon and Baltimore probes, the
old `colour_search.py` - superseded by `scripts/line_colour_search.py` -
and `tiers2.ps1`).

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
