# Handoff - Kobe build (from "Tram rescopes", 2026-09-27, late)

Written for a FRESH build session in the `kobe` worktree. Read it once and
follow the pointers. When a section is done, delete it rather than adding an
addendum.

## The job, and why Kobe

- **Build Kobe, the first Japanese city, then write the `japan-city` skill
  from the build before any other Japanese city starts** (owner's standing
  rule: Taiwan and Japan each get a per-country skill after their first city).
  `taiwan-city` and `brazil-city` are the models: shared modules, traps
  measured, owner's standing calls, and a sheet for each city still to build
  (Osaka, Sapporo, Fukuoka, Kyoto, Tokyo's 8 wards).
- **Kobe was picked (owner, 2026-09-27) as the clean medium-size case**: one
  city-wide permit list, block join 97.1%, no rebuilt register (Kyoto), no
  second source (Fukuoka) and no large chōme fallback (Sapporo). It exercises
  the path the larger cities need: permit list, MLIT block join, N02 rail with
  JR and the private railways, and a 生活衛生 personal-services layer.

## Where things stand

- **Worktree:** `.claude/worktrees/kobe`, branch `worktree-kobe`, made from
  `origin/master` at `6af4529`. `data/` and `.venv-lean` are junctions to the
  main checkout's. `git status` shows `?? data/`: never stage it.
- **The brief is `docs/build_briefs/kobe.md`.** Run
  `python scripts/brief_check.py kobe` before writing any code. A failing
  check means the brief needs correcting; never relax the check.
- **Cache already on disk from screening (not re-downloaded):**
  - `data/kobe/raw/`: `20260407150739.csv` (the food list),
    `r7_biyousho.csv`, `r7_riyousho.csv`, `r7_cleaning.csv` (tab-separated
    despite the name) and `isj/`;
  - `data/japan/raw/`: `N02-24_GML.zip` and `N03-20250101_28_GML.zip`
    (Hyōgo).

  `pipeline/kobe/fetch_sources.py` must still declare every one of them, so
  a fresh checkout can rebuild; with the cache present they skip. **Any NEW
  download needs the owner's OK** (file, source, size).
- **Shared code exists, and no city uses it yet:**
  - `pipeline/countries/japan.py`: N02 rail with the Shinkansen excluded,
    N03 city line, `stub_test()`, per-city ward codes;
  - `pipeline/countries/japan_register.py`: the MLIT join, with every
    normalisation rule and the city that taught it.

  Build on them, and don't fork them into `pipeline/kobe/`. A rule Kobe
  needs goes into the shared module. Afterwards, re-run the Minato control
  (`scripts/screen_japan_join.py`) as that module's docstring says.

## Skills, in order

`add-city` (Step 0 is mostly done in the brief) → `scaffold-city` →
`premises-taxonomy` (業種情報公開名称, 43 types; the brief has the bucket
table) → `address-join` → `cjk-text` (encodings on Windows, the U+2010 hyphen
in addresses, and the privacy check's blindness to CJK names). Rail is **MLIT
N02, not OSM and not GTFS**, so `osm-rail` does not apply.

## Owner's calls already made (see the brief's top block)

- The Shinkansen is out, and only stations inside the city line count.
- 菓子製造業 and そうざい製造業 count, in Retail. Measure the factory and
  central-kitchen share from trade names before publishing.
- Rail includes JR, Hankyu, Hanshin, Sanyō and Kobe Electric, all cut at
  the city line.

## Calls still open (recommend in chat, wait for a yes)

- **The Maya and Rokkō funiculars** (in N02). Barcelona drew its funiculars;
  Toulouse's cable car was an owner call.
- **Any urban line `stub_test()` cuts to a stub** goes back to the owner.
- **Notification-only (届出) food businesses** are missing from the list. The
  page discloses it; MHLW's national data is a later layer, not this build.

## Traps named in the brief

- **営業者名 carries individuals' names**, and so does 営業所TEL. Read only
  屋号, 業種情報公開名称 and 営業所所在地, and select by name. Run
  `check_personal_exposure.py` knowing it cannot read CJK names (`cjk-text`).
- **N02 stations are LineStrings**: centroid them.
- **MLIT N03 is for picking stations and anchoring labels. Never draw it**
  (the Survey Act; `docs/data_sources.md`, Japan section).
- **The licence display is load-bearing**:
  - the exact 出典 line for Kobe's list, 「…を加工して作成」, and the CC BY
    2.1 JP link;
  - MLIT's PDL 1.0 credit;
  - no claim that the pins are businesses open now;
  - nothing that makes it look as if the city made the map.

  Put them in `docs/data_sources.md` and draft the page wording in chat.
- **UTM 53N (EPSG:32653)**, region "East Asia".

## Before starting

- **Tell Staging, Cleanup and "Tram rescopes" your session name**
  (`ListAgents`).
- **Pacing:** start cheap, and check `get_usage` between steps. At 90% of the
  5-hour window, finish the current step, commit clean, and stop with a
  one-line note naming the next action.
- **Nothing merges to master until the owner calls review time**
  (`docs/review_time.md`). Publishing goes through `publish-city` then.
- **Previews:** the preview tool reads `.claude/launch.json` in the worktree
  the session STARTED in. Put a `-tmp` entry there, and remove it when done.
- **Never check out `master` in a worktree.** Merge `origin/master` into the
  branch, and publish with `git push origin <branch>:master` after a
  `git fetch` in the same breath.

## Rules beyond CLAUDE.md and memory (as the build handoff)

- **Git:**
  - Identity per command only:
    `git -c user.name=dacekroberts -c user.email=49654908+dacekroberts@users.noreply.github.com commit ...`
  - Never change git config, amend, or force-push.
  - Stage by name after reading `git status`.
  - Trailer: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
  - A commit message with backticks goes in a file (`git commit -F`).
- **Published prose** (the page, notices, `excluded_categories.md`) is
  drafted in chat and waits for the owner's review.
- **Leave alone:** `opd.pdf` at the main checkout's root, the Taipei PDF in
  `data/taipei/raw`, and the two personal files in the home directory.
