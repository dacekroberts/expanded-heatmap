# Cleanup handoff, 2026-10-03

For the next cleanup session. Read CLAUDE.md and `docs/project_context.md`
first; this note is only what they do not say. Claims are labeled
**[verified]** (checked by this session, with the evidence named) or
**[unverified]** (reported to it, not checked). Delete this file once its
items are done or moved into PLAN.

## Where things stand

- **[verified]** master is live with **158 cities** (live check after the
  owner's reboot, master 37eec480: the 14 Japan wave 2 pages, the four
  regional extensions, Required_Notices listing 115-132 and 137-140).
  `check_all.py` 46/46.
- **[verified]** One commit on `prose-pass` waits for its push and a reboot
  when this note was written: 716888c6, the Overview's region caption (a
  region view says only "Showing N cities in <region>.", owner) and the
  "All required source notices" link moved into the reference-links row
  above the notices (owner). A short local render check was running; if the
  push did not happen, re-run that check, push, ask the owner to reboot,
  live-check those two things.
- The cleanup worktree is `.claude/worktrees/cleanup` on `prose-pass`; it
  lands work by merging onto `prose-pass` and pushing `HEAD:master` with
  the fetch-merge-push loop (CLAUDE.md, "Re-check origin/master").

## Sessions running (expanded-heatmap only)

Never close, archive or recommend retiring another project's sessions (the
owner's hard line; memory "External project sessions").

| Session | Worktree / branch | State |
|---|---|---|
| Expanded Heatmap Visuals | `visual` / `visual-handoff` | ongoing; drafts entry **040ea615** to fold at the next landing |
| Expanded Heatmap Analytics | `analytics` / `analytics-handoff` | ongoing; private; its `data/_analysis/` edits needed the owner's own settings.local.json allow rules (data/ is a junction) |
| Expanded-heatmap staging session | `staging` / `worktree-staging` | fresh since 2026-10-03, from `docs/handoff_staging_2026-09-30.md` |
| Make map dots and lines easy to tap on phones | `charming-vaughan-f62c30` / `mobile-tap-targets` | building. Owner's three asks (2026-10-03): wider tap targets on phones; a fixed details box (bottom-left or equivalent) instead of a tooltip that clips off the map's edge, with a highlight on the selected dot; and clustered dots around commercial hubs, where the first tap expands a cluster and the second often collapses it instead of selecting the dot. Brings the owner a before/after; all maps re-render after approval; lands at review time. Check all three at its landing |
| Jpn Wave 2, Extension regional builds | worktrees removed | LANDED; the owner archives them (the empty folders go then) |

The two 2026-09-23 "Resume ..." sessions in the main checkout are finished
and archivable (the owner's call).

## Standing rules added 2026-10-03 (all on master)

- **Downstream note after every push**: `scripts/downstream_changes.py <old>
  <new>`, sent to Visuals and Analytics; for new cities add card face or
  caption and open terms questions from the build's drafts
  (`docs/session_roles.md`, "Downstream sessions"). Three were sent today.
- **Measured memory figures**: omit `--peak-gb` and the gate declares the
  label's last measured peak; `--estimate "scaled from ..."` otherwise
  (CLAUDE.md memory rule). The history file now records every run.
- **check_macro_facts reads each city's config `DATA_PROCESSED`**, so a
  regional build checks against `data/<slug>/processed/regional/`. The four
  extended cities (Belo Horizonte, Rio, Los Angeles, Vancouver) read there
  with `REGIONAL = True`; folding back to plain `processed/` is optional.
- **Notice numbers**: next claim 141; 133-136 released unused. Next page 190.

## Waiting on the owner (ask; each has a safe default already built)

1. **SFMTA clause 4** (notice 3): kept on the cautious reading; drop only if
   the owner reads it as applying to use agreements alone (PLAN).
2. **Japan, from wave 2's drafts** (DECISIONS 2026-10-03, "Japan wave 2: the
   shared-code pass" and "The name rule treats a cooperative..."):
   (a) switch the seven opt-in address rules on for the 20 earlier Japanese
   cities (unplaced rows fall: Fukuoka 92 to 29, Hiroshima 152 to 7, Kumamoto
   62 to 14, Matsuyama 84 to 63; nine maps re-render); (b) the cooperative
   rule for them (about 30 co-op trade names un-withheld across eight maps);
   (c) 複合型そうざい製造業 and deli-by-form permits as Food shops (about 55
   pins across eight cities, plus wave 2's); (d) Sasebo's 4 カフェー permits:
   Food service or adult venue; (e) "a JR stretch left out for frequency" as
   a standing station-scope row, or Shimonoseki alone; (f) Kawasaki's macro
   dot at Shin-Yurigaoka. Cleanup recommended yes to (a) and (b), lean yes
   to (c); the owner had not answered.
3. **Linha 6-Laranja** (São Paulo) stays out until full service (owner OK'd
   the sentence saying so); re-check when it leaves trial operation.

## Open work, in suggested order (all in PLAN.md)

1. **Overview caption against its labels** (owner): East Asia's caption says
   6 but the map labels more (REGION_LABELS_ALSO anchors). Fix, and ADD A
   CHECK for every region at 375, 768 and 1200.
2. **Overview at phone width**: split Japan West (owner approved; its pinned
   zoom 6.0 drops 16 of 22 dots at 375); correct `check_macro_labels.py`'s
   375 canvas (assumes 343, measured 333) and re-score; LA's and Rio's
   "(Regional)" labels clipped at 375.
3. **Each page's "Data:" line still prints ISO dates** ("as of 2026-08-31")
   while the prose now uses "August 31, 2026" [verified by the live check].
   Owner's US style suggests changing the line's formatter; ask first, it
   touches every page.
4. **Rome's tram 3 and Oslo's tram 13 stops**: each needs a fresh pull.
5. **Heavy-job follow-ups**: what drives 4.5-4.7 GB in multi-city Japanese
   drift runs; orphans left by a stopped background shell.
6. The licence gaps still open (Milan's ATM, STM, MLIT's credit for the
   Japanese cities; missing rows), the UK watch items, and the rest of PLAN.

## Housekeeping left

- `docs/handoff_japan_wave2_2026-10-02.md` and
  `docs/handoff_extensions_2026-10-02.md` describe landed work; the
  extensions' note asks to be deleted once all four landed. Configs'
  comments (belo_horizonte, los_angeles, rio_de_janeiro) and
  `docs/handoff_staging_2026-09-30.md` name them, so update those references
  in the same commit.
- `docs/session_roles.md`'s role rows for Japan wave 2 and the extensions
  can be marked LANDED 2026-10-03.

## How this session worked (worth keeping)

- Big batches as **parallel lanes**: each lane its own branch and worktree
  (data/ and .venv-lean as junctions), a shared brief in the scratchpad,
  no generated files edited in lanes; cleanup merges, regenerates
  (`check_macro_facts --write`, `check_ring_shares --write`,
  `rendered_surfaces --write`), runs the gate, shows the owner every new
  sentence, pushes, and runs deploy-verify lanes on dv1-dv3.
- **Shared data/**: any step re-run from a branch rewrites what master's
  checks read. Today it bit twice (Belo Horizonte, D.C./Tbilisi); land fast
  or write variants under a new folder.
- A stalled agent (no tool call for an hour, no process) is stopped and its
  uncommitted work taken over and re-run from its code; console encoding
  (`PYTHONIOENCODING=utf-8`) was the cause once.
