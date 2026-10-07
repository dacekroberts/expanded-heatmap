# DECISIONS drafts - macro-facts-guard

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-07 - The macro_facts.json write guard

- **`scripts/check_macro_facts.py --write` now refuses, exits 1 and writes
  nothing when `data/` is missing or when a city still in `app/cities.py`
  would lose the storefront count HEAD's `app/macro_facts.json` holds for it.**
  On 2026-10-07 `scripts/regen_generated.py` ran in the `europe-split`
  worktree, which had no `data/` junction: all 170 cities were skipped as
  "no processed data here", `{"storefronts": {}}` was written (170 counts ->
  0), regen reported "rewritten app/macro_facts.json" with exit 0, and the
  empty file was committed. `app/label_competition.py` ranks the macro map's
  labels by those counts, so it ran on empty counts until the file was
  restored. A skipped city is correct for the check (a fresh checkout names
  it and passes the rest); for `--write` it can only mean missing inputs.
  The refusal names the missing junction, the shared folder's absolute path
  (from `git rev-parse --git-common-dir`) and the `mklink /J` command, and
  `regen_generated.py` reports it as `FAILED` and exits 1, which it already
  did for any generator that exits non-zero. The yardstick is HEAD's file,
  not the one on disk, so a shrunken file left by an earlier run cannot pass
  the next one; the disk file is the fallback only when git cannot answer.
  Rejected: (1) a plain "fewer entries than committed" count test, which
  would also block a city removed from `app/cities.py` (a removal request,
  a rename); the guard compares only cities still listed, so a removed
  city's count drops without tripping it; (2) carrying the committed count
  over for a skipped city, which would publish a number no one re-measured;
  (3) a guard in `regen_generated.py` alone, which leaves a direct `--write`
  unguarded. The check mode (the pre-push hook) is unchanged. The write
  also passes `newline="\n"`, so a direct `--write` no longer leaves CRLF.
  Verified: with no `data/`, both `check_macro_facts.py --write` and
  `regen_generated.py` exit 1 and leave `app/macro_facts.json` unmodified;
  with an empty `data/` folder, the write refuses (0 of 170, all listed as
  missing); with the junction in place, `regen_generated.py` reports all
  seven generated files "current", exit 0. `app/ring_shares.json`'s
  generator reads the committed maps in `outputs/`, not `data/`, so it has
  no such hazard.
