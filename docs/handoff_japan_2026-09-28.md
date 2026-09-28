# Handoff - Japan build: Tokyo (from "Fukuoka handoff", 2026-09-28)

Written for the FRESH Tokyo-only build session in the `japan` worktree. It is
Tokyo's plan. The build role's other work (the review batch, the macro-map
tiers, the non-Tokyo queue) is in `docs/handoff_tokyo_build_2026-09-28.md`;
read that too. Fukuoka and Kyoto, this file's earlier job, were built
2026-09-28 and are in the review batch. **When a section is done, delete it
rather than adding an addendum.**

## Read first, in this order

1. **The `japan-city` skill**, then **the `tokyo-ward` skill**, which covers
   only what a ward adds. Between them they are the manual.
2. **`docs/build_briefs/tokyo.md`**, especially "Ward cards" (every ward
   settled 2026-09-28) and "Rail". Run `python scripts/brief_check.py tokyo`
   before any code.
3. **`pipeline/tokyo/wards.py`**: the roster, and the one place a ward is
   switched on.
4. DECISIONS 2026-09-28: the Tokyo groundwork, hollow no-data stations, and
   "Tokyo's missing wards" (from the research session).

## What is settled (do not re-ask)

- **8 wards ON**: Chūō, Minato, Shinjuku, Taitō, Kōtō, Meguro, Setagaya and
  Shibuya. **15 wards OFF**, none OPEN; each ward's reason is in the roster
  and its card. No missing ward can join from its own publications, and
  outreach is parked (the last resort).
- **Stations in the 15 wards are drawn HOLLOW**: ringless, not counted, with
  the tooltip "No business data: <ward> publishes no usable food-permit
  list" and a legend row. This is built and tested (Kobe, in scratch). The
  city line is all 23 wards (active plus no-data), so every line runs
  through the whole city. That answers the brief's stub test, which failed
  on the 8 wards alone.
- **Personal services only where food is ON** (owner, 2026-09-28): seven OFF
  wards publish barber, beauty and laundry registers (Chiyoda, Bunkyō,
  Shinagawa, Ōta, Toshima, Arakawa, Katsushika). They stay hollow, and those
  registers stay unused. One line in `excluded_categories.md` says so. The
  personal-services layer is therefore Minato, Taitō, Meguro and Shibuya.
- **Each ward's share is on the page, WITHOUT MHLW's slice**; MHLW's +0.1 to
  +3.1 pt is said once, in prose. The shares are measured every build
  (`OFFICIAL_SHARES`; step 2 writes `official_shares.json` to Tokyo's
  outputs), never typed.
- **MHLW's slice is added to Chūō, Kōtō, Minato and Shinjuku**, de-duplicated
  (`SUPERSEDES`), and listed in `SHARE_SKIP`.
- Standing Japan calls: lines served only by limited expresses COUNT;
  numerals as figures before 丁目 (十条 is a name, "Jūjō", so there is no
  `JO_IS_GRID`); the COVID-era lists are never used; operator columns are
  read in memory for the name rule and never kept.

## The build, in order

1. **Config on the roster** (`pipeline/tokyo/config.py`, following Kyoto's
   and Fukuoka's): `source_rows` from `wards.py`; `SOURCE_MUNICIPALITY` and
   `MUNICIPALITY_CODES` per ward; `SOURCE_ENCODING`; the four `mhlw_<code>`
   sources, each in `ADDRESS_BY_CONSENT`, `OWN_POINT_FALLBACK`, `SUPERSEDES`
   and `SHARE_SKIP`; `OFFICIAL_SHARES = True`; and `NO_DATA_WARDS` from the
   roster. The eight wards were already run through the shared step 2 from
   a scratch config: 99.7% block, and the shares reproduce the brief
   exactly. Add each ward's operator-column spelling to
   `japan_register.OPERATOR_COLS`, then re-run the Minato control
   (98.0 / 0.2 / 1.8). Then run `check_personal_exposure.py tokyo`.
2. **Rail, the biggest piece** (N02; see the brief's "Rail"):
   - **Legal lines to service lines.** N02 records JR East's legal lines,
     but riders know the services. The Yamanote loop runs over 山手線,
     東海道線 and 東北線, and 東北線 also carries the Keihin-Tōhoku and
     others. `BRANCHES` (Osaka, Kyoto) only splits one line in two; Tokyo
     needs a table mapping legal sections to the public service lines that
     share the track. Write it per operator (JR East, Tokyo Metro
     through-running, Toei) before any line config, as a small `n02-services`
     skill if it generalises. Recommend the table to the owner first.
   - **About 50 lines.** Osaka's 34 already sat at the colour search's limit
     (closest pair 18.0). Make the search spatial: only lines that come
     within about 500 m of each other must differ by ΔE 18. Keep 3:1 on both
     pages and ΔE ≥ 45 from the pins. The search is `colour_search.py`, in
     `data/_staging_scratch_2026-09-28b/`.
   - **A label budget at phone width.** Every line needs a permanent label
     and a legend entry. Kyoto showed that moving one label reshuffles three
     others, so run `check_map_labels.js` at 343 px early, not last.
3. **Credits built from config** (a check that every source has a credit,
   extending `check_provenance.py`). Shibuya, Taitō (four elements,
   including a no-warranty sentence), Setagaya (its 「…改変して利用しています」
   form) and Meguro (a labelled BODIK link) each prescribe their own credit.
   The catalogue wards (Chūō, Minato, Shinjuku, Kōtō) share one combined
   notice that carries a DATE OF USE and says the data was processed. The
   MLIT ISJ and N02 lines are as for every Japanese city.
4. **The Economic Census join control** (restaurants on the map per ward
   against 2021 census 飲食店 establishments; the owner's control). The
   census file is cached at
   `data/japan/raw/estat_census_r3_b1_009_1a.xlsx` (6.4 MB) and read by
   `japan_official.census()`. **It has never run.** The first script
   dissolved each prefecture's whole N03 file and died with a MemoryError
   while a drift check ran beside it. Write a lighter one: points to wards
   through the stations' ward, or through a single ward's polygons. It is
   still a heavy job, so announce it. Run it for all six Japanese cities.
5. **The page and texts, drafted in chat for the owner:**
   - a per-ward share table read from `official_shares.json`;
   - the hollow stations explained, with the missing wards named;
   - notices and `excluded_categories.md` (both scopes);
   - the blurb and the macro-map `coverage`, `placement` and `data_age`
     (Tokyo is "narrowed"; `check_macro_facts.py`, in the other handoff's
     section 2);
   - the macro label.
6. The usual gates: drift, `check_all.py`, provenance, scope disclosure, the
   inconsistency tables, brief checks, and DECISIONS entries as you go. Tokyo
   is held for review time like the rest.

## Known small issues

- **A building name holding 丁目 is read as the town** (`新宿1-3-12
  壱丁目参番館`): 4 of the 33 unplaced rows. Fix it in `permits_from_rows`
  (with the Minato control) only if the build finds more.
- **Read permit dates, never labels or headers.** Nakano's portal says
  2026/6/30 but its file ends 2023-06-27; Shinjuku's server re-stamped its
  2023 CSV as Last-Modified 2026-08-31.
- **Fukuoka's yatai rule (ろ店 counts) runs in Tokyo too**: check what ろ店
  means in Tokyo's rows before trusting it.

## Where things stand

- **Worktree** `.claude/worktrees/japan`, branch `worktree-japan`: Sapporo,
  Fukuoka and Kyoto (in the review batch from `02637d6`), then the Tokyo
  groundwork. That is the two skills, the roster, the per-ward municipality,
  the share check, hollow no-data stations in `japan_step1` and
  `map_common`, `japan_official.py` and the census reader. The last
  all-city drift check was zero drift in 54 cities. `data/` and `.venv-lean`
  are junctions to the main checkout's; never stage `data/`.
- **The research is merged in** (branch `worktree-tokyo-sources`, 36eb5d7):
  the Ward cards, the Tokyo rows of `docs/data_sources/japan.md`, and its
  DECISIONS entries. Its closing note, `docs/handoff_tokyo_sources_2026-09-28.md`,
  is to be deleted once read. Retire that worktree through Cleanup
  (`check_worktree_data.py` first).
- **Cached data**: ward files are in `data/tokyo/raw/<code>/` (Minato's
  address pair is in `data/tokyo/raw/` itself), the four MHLW slices the
  build uses are in `data/mhlw/raw/` (`<code>_food_business_all.csv`), the yearbook is at
  `data/tokyo/raw/tn24qv190800.csv`, and the e-Stat tables are in
  `data/japan/raw/`. Downloads still need the owner's OK (file, source,
  size): N02 is shared and cached; OSM names for Tokyo are not yet fetched.

## Rules for this session

- **Memory** (CLAUDE.md `[#memory]`): Python is capped at 8 GB a process and
  12 GB with its children. **Run one heavy job on the machine at a time,
  announced to every live session before it starts and when it ends.** Drift
  checks use `--jobs 2` at most, one per machine. A MemoryError is a script
  to fix. Never open a ward PDF or ZIP in the Browser pane (it lands at the
  checkout root).
- **Git:** identity per command only
  (`git -c user.name=dacekroberts -c user.email=49654908+dacekroberts@users.noreply.github.com commit ...`);
  never change git config, amend, force-push or skip hooks; stage by name;
  commit messages through a file (`git commit -F`). Trailer:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- **Never push this branch to master.** Back it up with
  `git push origin worktree-japan`.
- **No backslash or backtick in a Bash command**: write the script to the
  scratchpad and run it.
- Published prose and judgment calls go to the owner first: recommend, then
  wait. Pacing: `get_usage` between steps; at 90% of the 5-hour window,
  finish the step, commit clean, and stop with a one-line next action.
- **Tell Cleanup and the staging session your session name** (`ListAgents`).
