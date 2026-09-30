# DECISIONS drafts - tram kit (`worktree-tram-kit`, then `tram-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-09-30 - All builds activated, with six working rules for concurrent sessions (owner)

- **The owner gave the go for every build session**: Band B, the France
  builds, the Czech builds and the tram kit. The go was relayed by the tram
  kit to each live session. The Czech kit asked the owner to confirm it in
  its own session, which is the right behaviour for a relayed permission.
- **The six rules, in the owner's words where given:**
  1. **Heavy jobs**: "If two heavy jobs go under the memory thresholds we
     established, run those concurrently." The relay first set the budget at
     12 GB summed over two jobs (the 12 GB with-children cap). A measurement
     minutes later disproved it: only 2.3 GB of 15.9 was available, with
     eight Claude sessions taking 6.3 GB, Opera 1.8, and an orphaned
     staging grep 4.7 (PID 17392, started 13:54, a
     `.{0,30000}` pattern over a licence page, its parent gone). The tram
     kit was not permitted to stop another session's process, so that was
     left for the owner. **Corrected rule**: at most two heavy jobs, each
     started only when available memory is at least its peak plus 2 GB; an
     unknown peak counts as 8 GB.
  2. **Priority**: the tram kit goes before the Czech builds. So the tram
     kit writes `pipeline/osm_tram.py` first, starting with Odense.
  3. **DECISIONS.md drafts per session**: "keep drafts for decisions.md for
     each build session and pass off all at once for cleanup to implement".
     Each session writes `docs/decisions_drafts/<session>.md`, and cleanup
     folds them all in at once. That ends the append-only merge conflicts,
     four of which fell on this session's pushes on 2026-09-30 alone.
  4. **Overpass**: "stagger osm requests": one query in flight per session,
     and at least 60 s after a 504 or 429. Both mirrors were 504ing under
     several sessions' load that day.
  5. **Plan**: the owner is no longer on Pro.
  6. **Downloads and prose are pre-permitted**: the sources a brief names,
     and page text written from an approved template. A departure from a
     template is flagged, and does not stop the build.
- **Memory monitoring: a start gate, not a monitor.** The owner asked
  cleanup to "monitor all sessions for memory. Or whatever reactive protocol
  is efficient and safe". The tram kit recommended a gate,
  `scripts/heavy_job.py`, with a ledger in the shared `data/` junction that
  admits a job only if it fits in available memory, drops dead pids, and
  lists any process over 1.5 GB. Polling spends tokens all day and still
  reacts after the damage; a gate costs one call per heavy job. It was handed
  to the multi-city cleanup session to build. A second session named
  "Cleanup Session" belongs to another project (link-station-commercial),
  received the broadcast by mistake, and declined it.
- **Rejected**: a fixed summed budget (disproved by measurement above), and
  a polling monitor session.
