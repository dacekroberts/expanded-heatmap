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

## 4. The Tokyo build, in order

1. **Config on the roster** (`pipeline/tokyo/config.py`, following Kyoto's
   and Fukuoka's):
   - `source_rows` from `wards.py`;
   - `SOURCE_MUNICIPALITY` and `MUNICIPALITY_CODES` per ward;
   - `SOURCE_ENCODING`;
   - the four `mhlw_<code>` sources, each in `ADDRESS_BY_CONSENT`,
     `OWN_POINT_FALLBACK`, `SUPERSEDES` and `SHARE_SKIP`;
   - `OFFICIAL_SHARES = True`;
   - `NO_DATA_WARDS` from the roster.

   The eight wards already ran through the shared step 2 from a scratch
   config: 99.7% block, and the shares reproduce the brief exactly. Add each
   ward's operator-column spelling to `japan_register.OPERATOR_COLS`, then
   re-run the Minato control (98.0 / 0.2 / 1.8) and
   `check_personal_exposure.py tokyo`.
2. **Rail, the biggest piece** (N02; the brief's "Rail"):
   - **Legal lines to service lines.** N02 records JR East's legal lines,
     but riders know the services. The Yamanote loop runs over 山手線,
     東海道線 and 東北線, and 東北線 also carries the Keihin-Tōhoku and
     others. `BRANCHES` (Osaka, Kyoto) only splits one line in two; Tokyo
     needs a table mapping legal sections to the public service lines that
     share the track. Write it per operator (JR East, Tokyo Metro
     through-running, Toei) before any line config. Make it an `n02-services`
     skill if it generalises. Recommend the table to the owner first.
   - **About 50 lines.** Osaka's 34 already sat at the colour search's limit
     (closest pair 18.0). Make the search spatial: only lines that come
     within about 500 m of each other must differ by ΔE 18. Keep 3:1 on both
     pages, ΔE ≥ 45 from the pins, and nearest the operator's hue. The
     search is `data/_staging_scratch_2026-09-28b/colour_search.py`.
   - **A label budget at phone width.** Every line needs a permanent label
     and a legend entry. Kyoto showed that moving one label reshuffles three
     others, so run `check_map_labels.js` at 343 px early, not last.
3. **Credits built from config**, with a check that every source has a
   credit (extending `check_provenance.py`):
   - Shibuya prescribes its own credit.
   - Taitō: four elements, including a no-warranty sentence.
   - Setagaya: its 「…改変して利用しています」 form.
   - Meguro: a labelled BODIK link.
   - The catalogue wards (Chūō, Minato, Shinjuku, Kōtō) share one combined
     notice, which carries a DATE OF USE and says the data was processed.
   - The MLIT ISJ and N02 lines are as for every Japanese city.
4. **The Economic Census join control**: restaurants on the map per ward,
   against the 2021 census's 飲食店 establishments (the owner's control).
   - The file is cached at `data/japan/raw/estat_census_r3_b1_009_1a.xlsx`
     (6.4 MB) and read by `japan_official.census()`.
   - **It has never run.** The first script dissolved each prefecture's
     whole N03 file and died with a MemoryError while a drift check ran
     beside it.
   - Write a lighter one: points to wards through the stations' ward, or
     through a single ward's polygons.
   - It is still a heavy job: announce it. Run it for all six Japanese
     cities.
5. **The page and texts, drafted in chat for the owner:**
   - a per-ward share table read from `official_shares.json`;
   - the hollow stations explained, with the missing wards named;
   - the notices;
   - `excluded_categories.md` (both scopes);
   - the blurb;
   - the macro-map fields (section 5) and label.
6. **The gates**: drift, `check_all.py`, provenance, scope disclosure, the
   inconsistency tables, brief checks, and DECISIONS entries as you go. Tokyo
   is held for review time; then `publish-city`.

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

## 6. Known small issues and traps

- **A building name holding 丁目 is read as the town** (`新宿1-3-12
  壱丁目参番館`): 4 of the 33 unplaced rows. Fix it in `permits_from_rows`
  (with the Minato control) only if the build finds more.
- **Fukuoka's yatai rule (ろ店 counts) runs in Tokyo too**: check what ろ店
  means in Tokyo's rows before trusting it; a festival stall is not a yatai.
- **Read permit dates, never labels or headers.** Nakano's portal labels its
  file 2026/6/30, but the permits end 2023-06-27. Shinjuku's server
  re-stamped its 2023 CSV as Last-Modified 2026-08-31.
- **Ward servers send a PDF or ZIP as a download.** Never open one in the
  Browser pane, where it lands at the checkout root (it happened twice); use
  HEAD and WebFetch. **WebFetch on a binary saves it** under the home
  directory, in the session's `tool-results` folder, where
  `check_stray_downloads.py` does not look.
- **Not done by the research, because nothing qualified**:
  - no `pdf-register` skill: whoever writes it must carry the `[#memory]`
    rule;
  - no new keys in `scripts/screen_japan_join.py`;
  - no outreach drafted.

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
