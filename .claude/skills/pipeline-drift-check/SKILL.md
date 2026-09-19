---
name: pipeline-drift-check
description: Use after changing any pipeline/**/*.py script (a city's step files, pipeline/map_common.py, pipeline/taxonomies/), or when asked to verify the committed outputs/ still match what the pipeline actually produces. Re-runs every city's pipeline and diffs the result against git HEAD, including the one non-obvious step Folium's HTML needs (normalizing its random per-render element IDs) before a diff is trustworthy. Needs at least one commit to diff against.
---

# Verifying the pipeline against committed outputs/

The core invariant: the Streamlit app only ever reads `outputs/<city>/`;
it never runs the pipeline. So `outputs/` can silently drift from what the
pipeline would produce if a script changes and nobody re-runs it. This is
the check that catches that. The mechanics live in `pipeline/drift_check.py`
- run it, don't re-derive it.

## 1. Run it

From the project root, with the full pipeline environment (not
`.venv-lean` - that one has no geopandas/folium):

```bash
python pipeline/drift_check.py            # every city with pipeline/<city>/step*.py
python pipeline/drift_check.py san_diego  # one city
```

For each city it prints the raw inputs (size, modified time), runs every
`pipeline/<city>/step*.py` in sorted order (so a city that needs an extra
step - geocoding, say - is picked up automatically), then compares each
file under `outputs/<city>/` to `git show HEAD:<path>`:
- byte-identical, or
- `heatmap.html` identical after Folium-id normalization, or
- `DRIFT` / `NEW` / `MISSING`, with exit code 1.

Why the normalization exists: Folium/Leaflet assigns a random 32-hex-char
id to every element on every save, so a raw diff of `heatmap.html` shows a
change even when nothing real changed. Files are compared as raw bytes,
never decoded text - a Windows text decode uses the console codepage and
corrupts multi-byte characters, producing a false diff. Line endings are
also normalized (CRLF -> LF, at byte level): on Windows with
`core.autocrlf`, pandas writes CRLF while git stores LF, so a regenerated
CSV would otherwise always look like drift.

## 2. Code drift vs source drift - the distinction this project needs

Unlike a one-shot download, this project's raw data comes from live open-
data portals that update (San Francisco's business dataset carries a daily
`data_as_of`). The script re-runs against the raw files already on disk and
never re-downloads, so a `DRIFT` result means one of two things - tell them
apart before acting:

- **Raw inputs unchanged since the last baseline** (the printed modified
  times predate it) -> the outputs changed because *code* changed. Either
  it's the intended effect of your change, or unexpected drift to
  investigate (a unified diff of the normalized bytes, or search for the
  specific string/count that should have changed).
- **Raw inputs were refreshed** (re-downloaded after the baseline) -> the
  outputs changed because the *source* changed. That's expected, not a bug:
  regenerate, commit, and record a new baseline entry.

## 3. Compare the printed counts to the last baseline

Each step prints its own row counts (e.g. raw -> city -> storefront ->
coordinate-valid). Compare them to the most recent "ran the full pipeline"
entry in `DECISIONS.md`. Matching counts with zero drift is the expected
result for a change that shouldn't have touched upstream steps; a real
difference means the change had a wider effect than intended, or the
baseline itself is stale.

## 4. Revert cosmetic-only diffs, commit real ones together

- Normalized-identical: no real change. If git shows a diff anyway,
  `git checkout -- outputs/<city>/heatmap.html` rather than committing a
  no-op.
- Real change: commit the pipeline script and the regenerated `outputs/`
  files in the same commit - never the script alone, never regenerated
  outputs without the script change that produced them. Then add a
  baseline entry (see the `decisions-entry` skill).

## 5. Also worth doing after any pipeline change

Catch pages that silently depend on pipeline intermediates instead of
`outputs/` (a real class of bug for an app that deploys without its
pipeline data, surfacing as a production `FileNotFoundError`): temporarily rename `data/`
aside, run the `deploy-verify` agent (or reload every page against
`.venv-lean`), confirm nothing errors, then rename `data/` back. Never
delete it - rename and restore.
