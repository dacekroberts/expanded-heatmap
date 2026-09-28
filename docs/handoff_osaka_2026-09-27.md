# Handoff - Osaka build (from "Kobe build handoff", 2026-09-27, late)

Written for a FRESH build session in the `osaka` worktree. Read it once and
follow the pointers. When a section is done, delete it rather than adding an
addendum.

## The job, and why Osaka

- **Build Osaka, Japan's second city, with the `japan-city` skill.** Kobe
  (built 2026-09-27, the first) put everything national in
  `pipeline/countries/`: `japan_step1.py` (N02 rail cut at the N03 city line),
  `japan_step2.py` (the permit lists, taxonomy, MLIT join and the name rule)
  and `japan_register.py`. Kobe's own step files are three lines each. **Osaka
  should mostly be a config** (`pipeline/kobe/config.py` is the worked
  example).
- **Why Osaka next** (recommended in the skill, and first in the owner's
  2026-09-24 order):
  - one city file, and a 99.1% block join checked against the city's own
    coordinates (median 38 m);
  - no new mechanism needed in `japan_step2`;
  - its one hard question, the list at about 67% of MHLW's restaurant count,
    already has owner-approved page wording (the brief, L80-87).
- **What Osaka tests that Kobe did not**: scale. It has 24 wards, about
  61,752 food premises plus 15,775 personal services, and a network far
  denser than Kobe's (Osaka Metro, the New Tram, JR, Hankyu, Hanshin, Keihan,
  Kintetsu, Nankai and the Hankai tram).

## Where things stand

- **Worktree:** `.claude/worktrees/osaka`, branch `worktree-osaka`.
  - It was made from **`worktree-kobe` at `843929c`, NOT from
    `origin/master`**. The shared Japanese modules exist only on the Kobe
    branch until review time lands it.
  - When Kobe lands on master, merge `origin/master` into this branch. Osaka
    publishes after Kobe, or in the same batch, never before it.
  - `data/` and `.venv-lean` are junctions to the main checkout's.
- **The brief is `docs/build_briefs/osaka.md`.** Run
  `python scripts/brief_check.py osaka` before writing any code. A failing
  check means the brief needs correcting; never relax the check.
- **Cache already on disk from screening (not re-downloaded):**
  - `data/osaka/raw/`: `260630zenku.csv` (the food list, 2026-06-30),
    `ri20260331.csv`, `bi20260331.csv`, `cleaning20260331.csv` and `isj/`
    (48 files, 24 wards x 2). The older `*zenku.csv`, xlsx and PDFs beside
    them are screening evidence; do not build on them.
  - `data/japan/raw/`: `N02-24_GML.zip` and `N03-20250101_27_GML.zip` (Osaka).
  - `pipeline/osaka/fetch_sources.py` must still declare every file the build
    reads, so a fresh checkout can rebuild; with the cache present they skip
    (copy Kobe's).
- **One download is still needed: the OSM station-name query** (Kobe's shape,
  one Overpass `railway=station|halt` query over the city's box, probably
  150-400 KB). **Ask the owner first** (file, source, size), as Kobe did. Kobe's
  approval covered Kobe's query only. Any other new download needs the
  owner's OK too.

## Skills, in order

1. `japan-city`: read the whole skill first, and its Osaka sheet.
2. `add-city`: Step 0 is done in the brief; re-read Steps 4-9.
3. `scaffold-city` (`--taxonomy japan_eigyo --region "East Asia" --country Japan`).
4. `cjk-text`.

Rail is **MLIT N02**, not OSM and not GTFS, so `osm-rail` does not apply.

## Owner's calls already made (do not re-ask)

- The Shinkansen is out, and only stations inside the city line count.
- 菓子 and そうざい count, in Retail. The factory share is measured and the
  rows kept.
- The name rule: a trade name that IS the operator's own name shows the
  permit type. Osaka's list carries **営業者名**, already in
  `japan_register.OPERATOR_COLS`.
  - **The brief's privacy section (L186-188) says never to read the operator
    column. The owner's name rule supersedes that** (skill, "Before any
    city").
  - Check the barber and beauty registers' operator column names against
    `OPERATOR_COLS`.
- **Trams count** (owner, 2026-09-27), so the Hankai tram is drawn. It keeps
  17 of 32 stations inside the city: half a line, not a stub.
- English station names come from OSM `name:en`, with Japanese beside them.
- The 67% gap page wording is approved (brief L80-87). Use it verbatim.

## Calls still open (recommend in chat, wait for a yes)

- **Lines served only by limited-express trains**: never ruled on (PLAN,
  "Rail", "Owner, once for all five"). If an N02 line inside Osaka has no
  local service, bring it to the owner. Do not decide it in config.
- **Any urban line `stub_test()` cuts to a stub** goes back to the owner.
  Osaka Metro keeps 80-100% of each line (brief L151). Print the full table,
  including the JR and private lines.
- **Label density.** Osaka will draw far more lines than Kobe's 15. If the
  map is unreadable, bring the owner options (for example, one label per
  operator family). Do not drop lines silently.
- **The brief's stale lines**, to correct rather than obey:
  - L148 has the Shinkansen open, L116 has 菓子 / そうざい "decide at build",
    and L153-158 has the scope as the owner's call. All three were decided at
    L7.
  - L86 says 2,149 rows and L102 says 2,150: re-measure.

## Traps to expect (from the brief and Kobe)

- **The 経度 / 緯度 columns are swapped** (brief L101).
  `permits_from_rows` swaps them back already. Use them as an independent
  check on the join, as the screen did (median 38 m), and never as the map's
  source.
- **Kanji variants**: 曽根崎新地 / 曾根崎新地 alone is 1,807 permits. The rule
  is already in `japan_register.VARIANTS`. Underground malls stay unplaced.
- **N02's legal sections**: expect several N02 lines per public line, and
  JR's 東海道線 carrying both the JR Kobe and JR Kyoto lines. Build
  `config.LINES` from `stub_test()`'s table; step 1 stops on any in-city N02
  line the config does not name. Branches with their own public names go in
  `config.BRANCHES` (Kobe's Wadamisaki).
- **Line colours**: readable on both basemaps first (3:1 against `#0B1220` and
  `#ffffff`), then Delta-E 45 against the pins, then about 18 between lines.
  With 30-odd lines the pairwise floor will bind. Measure it (Kobe's search is
  described in the skill, trap 10) rather than eyeballing.
- **The macro map**: Osaka sits about 30 km from Kobe, so at the East Asia
  zoom the two labels will collide. Measure Osaka's width in the app's own
  document with two known widths reproduced, then re-score every East Asia
  label (`scripts/check_macro_labels.py`). Kobe's offset may have to move.
- **Any change to `japan_register.py`** re-runs the Minato control and every
  screen, old against new (skill, "What already exists").
- **N03 is for picking stations and anchoring labels only. Never draw it.**

## Licences

Read 2026-09-24 (brief, "Licences"; `docs/data_sources/japan.md`, Osaka City
row).
- Osaka City's lists are CC BY 4.0 / Government Standard Terms 2.0. **MUST
  DISPLAY**:
  - `「食品営業許可施設一覧」（大阪市）（https://www.city.osaka.lg.jp/kenko/page/0000575579.html）を加工して作成`;
  - the same form for pages 0000431136 and 0000552712.
- **MUST NOT**: present the map as the city's own, or use city logos.
- The MLIT and N03 lines are Kobe's notice 50, copied. Draft Osaka's notice,
  page prose and `excluded_categories.md` section in chat for the owner.

## Before starting

- **Tell Staging, Cleanup, "Tram rescopes" and "Kobe build handoff" your
  session name** (`ListAgents`).
- **Pacing:** start cheap, and check `get_usage` between steps. At 90% of the
  5-hour window, finish the current step, commit clean, and stop with a
  one-line note naming the next action.
- **Nothing merges to master until the owner calls review time**
  (`docs/review_time.md`). Publishing goes through `publish-city` then.
- **Previews:** the preview tool reads `.claude/launch.json` in the worktree
  the session STARTED in. Put a `-tmp` entry there and remove it when done.
  Kobe served `outputs/<city>` with `python -m http.server`, and the app with
  `.venv-lean/Scripts/python.exe -m streamlit run app/Overview.py`.
- **Never check out `master` in a worktree.**

## Rules beyond CLAUDE.md and memory (as the Kobe handoff)

- **Git:**
  - Identity per command only:
    `git -c user.name=dacekroberts -c user.email=49654908+dacekroberts@users.noreply.github.com commit ...`
  - Never change git config, amend, or force-push.
  - Stage by name after reading `git status`.
  - Trailer: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
  - A commit message with backticks goes in a file (`git commit -F`).
- **Scratch scripts print Japanese**: call `sys.stdout.reconfigure(encoding="utf-8")`
  first, as Kobe's session learned twice. **Regexes and backslashes go in a
  file, never a Bash heredoc** (the hook blocks it).
- **Published prose** (the page, notices, `excluded_categories.md`) is
  drafted in chat and waits for the owner's review.
- **Leave alone:** `opd.pdf` at the main checkout's root, the Taipei PDF in
  `data/taipei/raw`, and the two personal files in the home directory.
