# Review lane kit

The standing setup for a review run in lanes - several sessions, each taking
one angle on one pinned commit, while cleanup fixes and lands. Built
2026-10-01 from the lessons of the 2026-09-30 mega-review
(`docs/review_lanes_2026-09-30.md`, "How it went"), for the site-wide prose and
UI pass and every large review after it. A run's own lane plan (who takes
what) is a dated doc beside that one; this file is what every run shares.

## 1. When to start

**After the last build of the batch lands**, never during one: the tram kit's
arrival mid-review cost every lane a delta round (lesson 2). If a build is
running and the review cannot wait, pin the commit anyway and give the late
cities a short delta pass of their own afterwards - never re-pin the running
lanes.

## 2. Set up the lanes

```bash
python scripts/review_lanes.py create --sha <commit> --lanes 4
```

Each lane gets `.claude/worktrees/review-lane-N`, detached at that commit,
with `data/` and `.venv-lean` as junctions to the main checkout's (never a
copy; never pip-install into it), and its own ports in its `.claude/launch.json`
under deploy-verify's configuration names, so a lane tells deploy-verify to
leave them as they are:

| Lane | Streamlit | Static maps | Capture `--cdp` | Review folder |
|---|---|---|---|---|
| 1 | 8811 | 8812 | 9311 | `data/_review/lane-1/` |
| 2 | 8821 | 8822 | 9321 | `data/_review/lane-2/` |
| 3 | 8831 | 8832 | 9331 | `data/_review/lane-3/` |
| 4 | 8841 | 8842 | 9341 | `data/_review/lane-4/` |

Lane N's ports are 88N1, 88N2 and 93N1. Cleanup's own app uses 8822, which
lane 2's static server would take, so **cleanup runs no local app while lane 2
is up** (it checks the live site or lane 2's). The review folder is shared and
gitignored: a lane's report, captures and prose proposals go there, so cleanup
reads them without a hand-off. `python scripts/review_lanes.py list` shows
every lane's commit, whether it is dirty, and its junctions.

## 3. Divide the surfaces, not the pages you remember

`docs/rendered_surfaces.md` (generated; `check_all` fails it when stale) lists
every page the app renders, what each one renders besides its own text - the
docs the About and What Is Excluded pages show verbatim, every city's
`excluded_stations.csv`, the JSON files - and every city page's URL and slug.
A lane plan assigns every row of it to a lane, and says so (lesson 3: no lane
owned `docs/data_sources/*.md`, and a barred brand reached the About page).

## 4. Let the checks read first

`python scripts/check_all.py` on the pinned commit, before any lane starts. It
now covers what cost lane 4 about 1M tokens of reading (lesson 1):

| Check | Replaces reading for |
|---|---|
| `check_privacy_verdicts.py` | a city published with no recorded verdict |
| `check_provenance.py` (F) | a stale notice number, bold, quoted or "notice N (City)" |
| `check_barred_marks.py` | a barred brand on any rendered surface |
| `check_macro_labels.py` | label collisions, clipping, dots on top of dots, off-canvas members |
| `check_scope_disclosure.py` | a city whose rail or business scope does not reach the reader |
| `check_inconsistency_list.py`, `check_macro_facts.py`, `check_ring_shares.py` | the Why the Maps Differ figures |
| `check_inline_arrays.py`, `check_render_current.py`, `check_map_markup.py` | a map an iPhone cannot run, a stale shared block, unreadable labels |

A lane spends its reading on what no check can judge: whether the prose is
true, clear and consistent in tone, and whether the layout works.

## 5. Capture pages with one browser

```bash
python scripts/heavy_job.py run --label lane-N-capture --peak-gb 2.5 --session <lane> -- node scripts/capture_pages.mjs --base http://localhost:88N1 --pages cities --widths 375,768,1200 --themes light,dark --cdp 93N1 --out data/_review/lane-N/captures
```

For each page x width x theme it saves a screenshot, the page's text with
the map's own text (legend, labels, notices) appended, and `errors.json` (an
empty list per capture is the pass). Page names have no leading slash
(`Overview`, `About_the_Data`, `Edmonton_Heatmap`; `all` or `cities` read
`docs/rendered_surfaces.md`): Git Bash rewrites a leading "/" into a Windows
path. `--tall` makes one image of the whole page. Against the live site use
`--base https://expanded-heatmap-daceroberts.streamlit.app/~/+`.

**Memory (lesson 4): declare real peaks.** Measured: one capture 1.1 GB
(2026-10-01); a lane's app about 0.2 GB; deploy-verify driving three browsers
at once 7.43 GB (2026-10-01). Count each browser, or run one at a time. At
most two heavy jobs run on the machine.

## 6. Prose comes back as proposals, never as edits

A lane never edits a page. Each sentence it would change becomes a proposal
in `data/_review/lane-N/proposals.md` - the format is in
`scripts/prose_proposals.py`'s docstring: file, `fix` or `proposal`, why,
precedent, and the old text **copied from the file, not the rendered page**.
Then:

```bash
python scripts/prose_proposals.py collate
```

validates every proposal (the old text in its file exactly once, no two
overlapping) and writes `data/_review/proposals_all.md`, one numbered list for
the owner. The owner approves by ID; cleanup runs `apply --ids ...` (or
`--kind fix` where the owner approves every factual fix at once), which
refuses any proposal whose old text has changed since. That is CLAUDE.md's
"drafted in chat before it is written" at the scale of a site-wide pass.

## 7. Reports

Each lane writes `data/_review/lane-N/report.md` and messages the cleanup
session, by the name `ListAgents` shows for it (its bracketed id changes when a
session restarts: "[3d7ab8]" became "[f2d0ed]" on 2026-10-01; "Cleanup Session"
with a capital S is a different project). Every finding:
the page or file, the width and theme, what it shows, and whether it blocks
the landing. Cleanup fixes on its own branch; the lane that found a defect
re-checks only that defect, at the narrow scope. Owner only: the iPhone check,
the reboot, and the calls the lanes surface.

## 8. Tear down

```bash
python scripts/review_lanes.py remove
```

unlinks each lane's junctions, then removes the worktree, and stops if
`data/` lost an entry. A lane with changed tracked files is left for a look -
a lane never edits. The review folders stay until the landing is done.
