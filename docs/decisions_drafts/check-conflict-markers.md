# DECISIONS drafts - conflict-marker check (`check-conflict-markers`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-09-30 - Conflict markers fail the pre-push hook; merge_append_only stops loudly on a failed write

- **What happened.** On kitchener-waterloo, `merge_append_only.py
  DECISIONS.md` hit a Windows file lock (OSError, Errno 22) and the merge was
  committed with `<<<<<<< HEAD`, `=======` and `>>>>>>> origin/master` still
  in DECISIONS.md. `check_all.py` passed it 26 of 26: nothing read for
  markers, and `decisions_index.py --check` compares headings, which a
  conflict leaves intact. Removed in 3d93d29.
- **`scripts/check_conflict_markers.py`, in the hook.** It reads every
  tracked file outside data/ (binary skipped by a NUL sniff), working tree
  as check_all does, and fails naming file and line on a line starting
  `<<<<<<< ` or `>>>>>>> `, and on a bare `=======` or diff3 `||||||| `
  between them. A bare `=======` outside a conflict is a Markdown heading
  underline and passes. About 3 s on 1,210 files, most of it the rendered
  maps under outputs/. On `3d93d29^`'s DECISIONS.md it names lines 289, 299
  and 315, the three markers that were committed.
- **Its selftest** (`check_conflict_markers_selftest.py`, also in the hook):
  nine shapes with known answers, including half a conflict, CRLF, diff3, an
  indented or mid-line marker and eight brackets; a conflict spliced into the
  live DECISIONS.md; and the real tree as the positive control.
- **`merge_append_only.py` now writes through `write_or_die()`**: write, read
  back, retry once after 2 s, then exit non-zero with a message that says the
  file still holds markers or is half written, not to `git add` it, and to
  restore it with `git checkout --merge -- <path>`. A lock held by an editor
  or a sync client is often gone a moment later; the hook is the backstop
  when it is not.
