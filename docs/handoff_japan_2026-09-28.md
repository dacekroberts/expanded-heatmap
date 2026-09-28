# Handoff - Japan build: Fukuoka, then Kyoto (from "Staging and build handoff", 2026-09-28)

Written for a FRESH build session in the `japan` worktree. Read it once and
follow the pointers. When a section is done, delete it rather than adding an
addendum.

## The job

- **Build Fukuoka, then Kyoto**, the owner's order after Sapporo (DECISIONS
  2026-09-28, "Next builds"). Tokyo (8 wards) comes after them, and is not in
  this handoff. **Fukuoka built 2026-09-28** (DECISIONS "Fukuoka built";
  held for review time on this branch).
- Both are held for the owner's review time: nothing merges to master until
  the owner calls it (`docs/review_time.md`), then `publish-city`.
- **The `japan-city` skill is the manual.** Its sheets for Fukuoka and Kyoto
  mark with ▶ what each needs beyond the shared steps. Read it, then the city's
  brief, and run `python scripts/brief_check.py <city>` before any code.

## Where things stand

- **Worktree:** `.claude/worktrees/japan`, branch `worktree-japan`, made from
  `build-sapporo` at `648ec32`. `data/` and `.venv-lean` are junctions to the
  main checkout's; `git status` may show `?? data/`: never stage it. **Merge
  `origin/master` first** (this handoff lands there).
- **Why from `build-sapporo`, not master:** Sapporo (built 2026-09-28, held for
  review time) changed shared code that Fukuoka and Kyoto need:
  - `japan_step1`: **numerals as figures** (owner): a number before 丁目 is
    always a figure in the English name; before 条 only where the config sets
    `JO_IS_GRID` (Sapporo). Step 1 STOPS on a violation. **Kyoto's 条 are
    street names (Shijō, Gojō, Kujō), so no `JO_IS_GRID`**; its 丁目 still
    need figures. Fix what it catches in `config.OSM_NAME_EN_OVERRIDES`, a
    cited table ({ja: en}, the OSM spelling replaced in a comment).
  - `japan_eigyo`: coin laundries count in Personal services (source
    `coinlaundry`; owner); salons inside hospitals and care homes (厚生施設)
    are out.
  - Already on master: `pipeline/countries/japan_fetch.py`. A city's
    `fetch_sources.py` is its docstring plus `japan_fetch.main(config,
    __doc__)`; every city declares `SOURCE_FILES`.
- **Sapporo is the freshest worked example**: `pipeline/sapporo/` (config,
  thin steps, step 3), its brief, and its DECISIONS entries. Osaka's step 3 is
  the template it copied.
- **Pacing:** `get_usage` between steps; at 90% of the 5-hour window finish
  the current step, commit clean and stop with a one-line next action.

## Kyoto (second)

- **A REBUILT register**: `japan_register.kyoto_permit_stream(raw_dir,
  as_of)` from the 2021 `.xls` and 62 monthly XLSX. **Pin `as_of`.** It is an
  upper bound (closures unseen): the page says so. The stream must carry
  `name_is_operator`'s answer (it drops the operator columns today); Kyoto's
  申請者＿申請者名 / 申請者氏名 go into `OPERATOR_COLS`.
- Fetch: no API - GET the resource page, POST with the session cookie; check
  magic bytes, refuse HTML. `data.city.kyoto.lg.jp` only.
- **Re-ask the owner about Kyoto's two funiculars**: the brief says drawn
  (decided 2026-09-24), but Kobe's sightseeing funiculars were left out
  2026-09-27. Recommend, then wait.

## Owner's calls made 2026-09-28 that bind these builds

- **Lines served only by limited expresses COUNT** (revertible).
- **The e-Stat download for the Economic Census join control is approved**:
  one national per-ward 飲食店 table, run for every city (PLAN, "Join
  control"). Name its file, source and size when fetching it.
- Published prose (page, notice, `excluded_categories.md`, blurb) is drafted in
  chat and waits for the owner's approval. So do judgment calls: recommend,
  then wait.

## Also queued for Japan (small, when convenient)

- **Osaka's Umekita → 福島 stretch** is to be drawn now that limited-express
  lines count (PLAN). It has no station; only the line changes. It needs a
  line to draw it as (its trains are the Haruka and Kuroshio): recommend one
  to the owner, then a re-render for review time.
- **Osaka's phone-width label overlaps** (PLAN) are a shared-renderer fix and
  belong to a review-time batch; not this session's unless the owner says so.

## Before starting

- **Tell "Staging and build handoff" and Cleanup your session name**
  (`ListAgents`).
- **Git:** identity per command only
  (`git -c user.name=dacekroberts -c user.email=49654908+dacekroberts@users.noreply.github.com commit ...`);
  never change git config, amend or force-push; stage by name; commit messages
  with backticks through a file (`git commit -F`). Trailer:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- **Never push this branch to master.** Back it up with
  `git push origin worktree-japan` (the pre-push hook runs `check_all.py`;
  a half-built city fails its docs checks until they are written).
- **Previews:** the preview tool reads `.claude/launch.json` in the worktree
  the session started in (gitignored). Put `-tmp` entries there and remove
  them when done. The browser checks (`check_map_labels.js`,
  `check_map_view.js`) run in the page; copy them next to the maps under
  `outputs/_checks_tmp/` to load them, and delete the folder after.
- **Downloads** need the owner's OK (file, source, size), except the e-Stat
  table above.
