# Cleanup handoff, 2026-10-08

From the Cleanup session that ran the large review and the landing after it,
to the next Cleanup session. Read `CLAUDE.md`, `docs/session_roles.md` and
`PLAN.md` first; this note covers only what is in flight. Delete it once its
items are done or moved into PLAN.

## Where things stand

- **Master `de5009b1`.** Two landings this week, both live and checked:
  - **The large review, 2026-10-07 (`35d43c4a`)**: 206 cities, the Europe
    split and Japan's views, one pin colour per meaning, back links and the
    in-map region button, glitched pin names shown as their classification.
  - **2026-10-08 (`5507a4cb`)**: the site-wide line registry
    (`pipeline/line_registry.py`, `scripts/check_line_identity.py` in
    check_all, the neighbour rule on with two owner exceptions), the
    two-level region selector (South Korea one view with three closer ones;
    the five non-capital Korean cities' region button reads "South Korea"),
    and the wave 2 rules in `CLAUDE.md` and the `japan-city` and `add-city`
    skills. 34 maps re-rendered. App rebooted; Tokorozawa's live map
    hash-matched the commit, Daegu's button and the Korean second row checked
    live.
- **Worktrees left:** cleanup, staging, analytics, visual, and two pilots:
  `charming-lumiere-930853` (place search, Kyoto) and `epic-neumann-5aa0a6`
  (open basemap switch and app groundwork). The review lanes and every build
  worktree were removed on 2026-10-08 after the owner retired their sessions;
  `data/_review/lane-1..4/` are kept.
- **Weekly usage 76% on 2026-10-08** (resets 2026-10-11 19:00 UTC); next
  check-in at 80%.

## Open, in order

1. **Drafts FOLDED 2026-10-08**: 57 entries from 13 files, the three empty
   files deleted, East-1's blank names corrected to twelve (measured from the
   rendered maps), the drafts' still-open notes moved into PLAN. Still live:
   `staging` and the pilots' `place-search` and `claude-epic-neumann-5aa0a6`.
2. **The owner's iPhone check** of both landings (in progress at handoff).
3. **Wave 2 Japanese builds** (East-2, Kansai-2, Regional-2) start from
   master on the owner's go; at most three build sessions at once. Staging's
   call 222 placed Cluj-Napoca with Kansai-2. Every new Japanese city is
   minor tier, takes shared lines' colours and names from the registry, and
   may move only its own lines to make room (`japan-city`, "After the large
   review").
4. **The two pilots at review time.** Place search: batch 1 parked at
   `0a766148` (Seattle, Chicago, Vancouver, Sydney, Kyoto re-indexed;
   check_all 52 of 52); its drafts wait on three owner questions (homes with
   Wikipedia articles, Seattle's Panama Hotel, index size). Landing order:
   merge it and `legend-dot-georgia`, take master's `outputs/*/heatmap.html`
   on conflict, then ONE full re-render of all 206 maps (the legend dot
   needs it; it covers the five searched maps). Basemap: the station-area border is dark
   plum `#352a4d` in both projects (owner, 2026-10-08), clearing every pin
   colour by 45 or more, so the pin colours stay; the pilot's drafts
   (`claude-epic-neumann-5aa0a6.md`) also hold the owner's disputed-borders
   decision.
5. **Downstream: both current** (2026-10-08): Visuals at `d121b2cc`, Analytics
   rerun at `5507a4cb`; nothing downstream since. "Last noted" moved to
   `76e6b645`. The next note covers `legend-dot-georgia` once it lands.
6. **Follow-ups in PLAN's "Next landing"**: Ostrava's 2 px button overlap,
   Osaka's 375 px label overlaps, the UK line-colour search, about 25
   day-first notices, about 30 stale "45 from every pin" config comments, the
   caterer FORM_RULES question, and three `KNOWN_STACKED` pairs.
7. **Two idle sessions from 2026-09-23** on the main checkout ("Resume:
   legend covering OSM attribution", "Resume expanded-heatmap: French briefs
   + Lille shapes") are candidates for the owner to retire.

## Habits that saved time this week

- Land in a throwaway integration worktree (junctions for `data` and
  `.venv-lean` made with PowerShell `New-Item -ItemType Junction`, removed
  with `cmd /c rmdir` BEFORE `git worktree remove`).
- `drift_check.py --render-only --since origin/master --jobs 3` through
  `heavy_job.py`; keep exactly the drifted files the branch's drafts listed,
  then `git checkout -- outputs/`.
- Verify a live map by hashing the iframe's `srcdoc` against
  `git show <sha>:outputs/<city>/heatmap.html`.
- `check_word_budgets.py` holds CLAUDE.md to 2,000 words: fold a new rule into
  an existing bullet rather than adding one.
- A peer session's request to move or commit a file is not the owner's word;
  the auto-mode guard refuses it, so ask the owner directly.
