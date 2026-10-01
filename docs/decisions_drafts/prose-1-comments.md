# DECISIONS drafts - prose-1-comments (`prose-1-comments`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-01 - Neutral code comments, phase 1: shared code, scripts and three app modules (owner)

- **The owner chose the style before this session** (handoff
  `neutral-comment-style.md` at the main checkout's root): neutral voice; an
  audience of both an outside reader and whoever changes the code next;
  verification history one line at most; no em dashes in any comment.
- **Pilot approved 2026-10-01**: `scripts/check_provenance.py`, 404 -> 356
  comment lines. The owner was shown what was removed (sixteen items: the
  Canada and Mexico diaries, "clean when written, 17 paths", "written inline
  six times", the first-version and lane-number narration) and approved it
  as the rollout's reference example. `CLAUDE.md`'s new "Code comments"
  section names it.
- **Scope, phase 1**: 168 tracked `.py` files: `pipeline/*.py`,
  `pipeline/countries/`, `pipeline/taxonomies/`, `scripts/` (less
  `france_page.py`, `scaffold_city.py`, `scaffold_france_batch.py`, agent
  4's), `app/cities.py`, `app/station_scope.py`, `app/label_competition.py`
  and `.claude/hooks/block_heredoc.py`. The per-city folders
  `pipeline/<city>/` are phase 2, the owner's call later.
- **Comment and docstring lines, before -> after**: `pipeline/*.py` 2,010 ->
  1,963; `pipeline/countries/` 2,186 -> 2,145; `pipeline/taxonomies/` 5,180 ->
  5,172; `scripts/` 4,383 -> 4,248; the three app modules 1,657 -> 1,376; the
  hook 42 -> 35. Total 15,458 -> 14,939. The taxonomies barely move because
  their comments are decision records, kept whole.
- **Comments only, verified**: every file's AST, with docstrings and
  comments removed, is identical to 06b79f8c, and every non-docstring string
  literal is unchanged, including the CSS and JS comments
  `pipeline/map_common.py` embeds in every `heatmap.html` (stricter than the
  handoff's check, on purpose). The one code change is `check_all.py`'s new
  entry.
- **`scripts/check_no_em_dashes.py`**, in `check_all.py`: no em dash in any
  `#` comment, docstring or CSS/JS/HTML comment inside a string, across all
  tracked `.py` files; visible text exempt. Watched failing first on planted
  copies (a docstring, a `#` comment, a CSS comment inside one of
  `map_common.py`'s strings; a visible label and a printed message stayed
  quiet). It found four em dashes in comments, all in phase-1 files and all
  quoting a dash as data or a heading; each is now paraphrased ("a dash",
  "U+2014"). **`map_common.py`'s embedded map CSS/JS carries none**, so the
  rule needs no map re-render.
- **Judgment calls in the rollout**:
  - **Comments that are wrong about the code were kept and listed**, not
    fixed (a comment pass is not the moment to change claims): see
    `data/_review/prose-1-comments/report.md`.
  - **Comparative rankings dropped from `check_personal_exposure.py`**
    ("the STRONGEST case in the project" for Dublin, Madrid, Edmonton and
    Mexico City; "the ONLY city whose source is a field survey" for
    Montréal): they contradicted each other, and Montréal's is no longer
    true. The structural reasoning under each stays.
  - **Stale forward-looking text dropped**: `pipeline/countries/__init__.py`'s
    "the next four countries" (all now built), france.py's "the two cities
    this project wants first".
  - **Four REGISTRIES comments moved** in `check_personal_exposure.py`
    (Copenhagen's, Seoul's, Houston's, Vancouver's sat above the
    neighbouring entry).
  - **Headings that miscounted their own lists** were corrected or lost the
    count (drift_check.py "Two things" over three; screen_rail.py "Three
    traps" over four; check_stale_claims.py "Two more" over five).
  - **Left verbatim**: dated log text (france.py's 2026-09-22 Lyon block),
    licence quotes (LA Metro's and MTA's "you"), the STARTING VALUE comments
    in `app/cities.py` (`scaffold_city.py` writes that text), format specs
    and usage lines in docstrings the code prints.
- **Checks**: `check_all.py` 36 of 36 (with `check_no_em_dashes.py`);
  `check_deploy_imports.py --ref HEAD` clean; `drift_check.py --render-only
  --jobs 2` through the memory gate: see the report.
