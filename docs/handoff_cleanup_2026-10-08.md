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
- **Worktrees left:** cleanup, staging, analytics, visual, two pilots, and
  Cleanup's `review-prep` (branch `legend-dot-georgia`, held for review
  time; its `data` and `.venv-lean` are junctions: unlink each alone first).
  - **`charming-lumiere-930853` (place search): NEVER remove, prune or
    retire it until place search has landed on master** (owner, 2026-10-08:
    "block attempts to delete the worktree until the changes have landed";
    this covers cleanup-sweep's retire-worktrees scope). After the landing,
    unlink its `data/` junction alone, then remove it.
  - `epic-neumann-5aa0a6` (open basemap switch and app groundwork). Its
    `data/` is a REAL folder, not a junction: `data/_basemap_build` (4,969
    files, 4.34 GB) and `data/_heavy_jobs_history.json` existed only there
    (`check_worktree_data.py`, 2026-10-08); its session was asked to copy
    them to the main checkout (no-clobber) until the check passes.
  - **Permanent names (owner, 2026-10-08):** with no session inside and
    everything committed, `git worktree move` the pilots to
    `.claude/worktrees/place-search` (between batch 2b and batch 3) and
    `.claude/worktrees/basemap` (after the copy passes), and `git branch -m`
    to `place-search` and `basemap`. Then update every handoff, memory note,
    batch prompt and `docs/session_roles.md`'s table naming the old ones. A
    move keeps the branch, files and junctions; it is not a removal, so the
    place-search hold still applies to the new path.
  - The review lanes and every build worktree were removed on 2026-10-08
    after the owner retired their sessions; `data/_review/lane-1..4/` are
    kept.
- **Weekly usage 82% on 2026-10-08** (resets 2026-10-11 19:00 UTC); the 10%
  check-ins ended that day (owner).

## Open, in order

1. **Drafts FOLDED 2026-10-08**: 57 entries from 13 files, the three empty
   files deleted, East-1's blank names corrected to twelve (measured from the
   rendered maps), the drafts' still-open notes moved into PLAN. `staging`
   FOLDED too (owner, 2026-10-08): 87 entries, calls 222-230; the 15 dated
   2026-10-03 moved to `docs/decisions/2026-09-27.md` by
   `archive_decisions.py`. The folder `docs/decisions_drafts/` is empty on
   master (git keeps no empty folder); the next drafts file recreates it.
   Still live, on their branches: the pilots' `place-search` and
   `claude-epic-neumann-5aa0a6`.
2. **The owner's iPhone check PASSED** (2026-10-08), all ten items; the oval
   legend dot and the typable dropdowns it found are on `legend-dot-georgia`.
3. **Wave 2 Japanese builds** (East-2, Kansai-2, Regional-2) start from
   master on the owner's go; at most three build sessions at once. Staging's
   call 222 placed Cluj-Napoca with Kansai-2. Every new Japanese city is
   minor tier, takes shared lines' colours and names from the registry, and
   may move only its own lines to make room (`japan-city`, "After the large
   review").
4. **The two pilots at review time.** Place search: tip `079c8dcb` (base
   `8cf5ed4c`; Kyoto, Seattle, Chicago, Vancouver, Sydney; check_all 52 of
   52); the owner answered its three questions (homes with Wikipedia: out;
   Panama Hotel: kept as a historic site, a precedent; size: optimized,
   iPhone passed). Its session may be archived; its WORKTREE stays (batch 2a
   and 2b sessions use it, `data/` is a junction). Its drafts
   (`place-search.md`) fold now or after 2a, the owner's choice. Owner's
   review-time calls: go live as is (suggestions WIP), the corner-credit
   test, the Cities menu out of the map, and whether "Download this index"
   also links the intersections file (ODbL 4.6). Landing order:
   merge it and `legend-dot-georgia`, take master's `outputs/*/heatmap.html`
   on conflict, then ONE full re-render of all 206 maps (the legend dot
   needs it; it covers the ten searched maps). `check_render_current.py`
   fails on the branch until that render (the comment rewording changes the
   shipped blocks), so nothing from it is pushed before. The pilot's four conditions:
   (a) its committed indexes (`app/static/places/<city>.json`,
   `outputs/<city>/place_search.json`) land unchanged, and any re-run
   `step2b_place_index.py` runs BEFORE that city's step 3; (b)
   `scripts/check_place_search.py` after the re-render (stale index hashes);
   (c) `.streamlit/config.toml`'s `enableStaticServing = true` lands with
   it, or the indexes 404 live; (d) deploy-verify (`map-chrome`) opens the
   search box on one searched map live; (e) at the merge, `place_index.junk_name`
   runs AFTER `map_common.repaired_name`, so "Patel?s" is repaired, not dropped
   (branch tip 9db1e20a). TRIAL MERGE (2026-10-08, `git merge-tree`, re-run on
   batch 2a's `4fda9817`; origin/master + legend-dot-georgia + place search): master
   and the branch merge clean; place search then conflicts in `PLAN.md`
   (take master's, add its pointer), the ten searched maps' `heatmap.html`
   (take master's; the full re-render replaces them) and ONE hunk of
   `pipeline/map_common.py`: both branches add text just above `LEGEND_ROW`;
   keep both, place search's `_PLACE_SEARCH_TEMPLATE` block first, then the
   legend-dot comment. `app/components.py`, Kyoto's page and the rest merge
   on their own. BATCH 2a (Montreal, Barcelona, Marseille, Prague,
   Brussels; held for the owner, three questions in its drafts) was
   committed on a detached HEAD at `4fda9817`; REATTACHED the same day (the
   branch fast-forwarded, now `55f024b8`, worktree on the branch, clean).
   Before merging, still confirm the branch ref is the tip you expect.
   Basemap: the station-area border is dark
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
