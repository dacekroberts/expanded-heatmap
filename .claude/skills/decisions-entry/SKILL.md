---
name: decisions-entry
description: Use when adding an entry to DECISIONS.md - after any judgment call, scope change, bug fix with a wrong-number consequence, city added or ruled out, superseded earlier decision, or pipeline verification run. Encodes the log's format and voice so entries stay consistent instead of being re-derived each time.
---

# Writing a DECISIONS.md entry

`DECISIONS.md` is this project's append-only record of judgment calls and
of the numbers that were true when they were made. It is **never edited
after the fact**: a superseded decision gets a *new* entry saying what
changed and why, with the old entry left standing. That is the difference
between this file and `docs/project_context.md`, which describes the
*current* state and is rewritten as things change.

## Where it goes

**A build or docs session writes to its OWN drafts file, not to
`DECISIONS.md`** (owner, 2026-09-30): `docs/decisions_drafts/<session-or-branch>.md`,
e.g. `docs/decisions_drafts/tram-kit.md`. Same format and voice as below,
newest first, each `### YYYY-MM-DD - <label>` section exactly as it should
land. Commit it on your own branch (a docs session may push its own file to
master; one file per session never conflicts). Do not run
`decisions_index.py` for a drafts file. The cleanup session folds every
drafts file into `DECISIONS.md` in one pass when the owner hands them off,
then empties them. Until the fold, cite the draft's heading wherever a
DECISIONS heading is required: `check_category_continuity.py` reads drafts
headings as well.

**The cleanup session** writes `DECISIONS.md` directly, as follows.

Newest first under `## Changes`, inside the most recent
`### YYYY-MM-DD - <label>` dated section; start a new dated section if it's
the first entry of a new day/session.

Only the current week (Sunday to Saturday) lives in `DECISIONS.md`. Older
entries are in `docs/decisions/<Sunday>.md`, moved there verbatim by
`scripts/archive_decisions.py`. To supersede an archived entry, write the new
entry in `DECISIONS.md` as usual and name the old one's heading and week file.
Never append to an archive by hand.

## Format

One entry = one bullet:

```
- **[Bold, one-sentence statement of what was decided or found.]** [Prose:
  why, in enough detail that the reasoning is checkable rather than
  asserted. Real numbers ("260,103 -> 20,562"), not vague ones. State the
  alternative that was rejected and what the decision rules out. Name the
  files touched.]
```

## Voice

Neutral past tense ("Decided...", "Found...", "Dropped..."), not first
person. The log was written by Claude from session context, so it stays
neutral unless the owner rewrites it in their own voice. Don't invent a
voice mid-file.

## What belongs

- A judgment call with a real rejected alternative (why THIS, not that).
- A city added, ruled out, or re-scoped, with the live-verified evidence.
- A bug fix with a wrong-number consequence - state both figures.
- A superseded decision (link it: "supersedes the 2026-09-18 entry on X").
- Verification runs, including "zero drift" - evidence is worth recording.
  These double as the row-count baseline `pipeline-drift-check` compares to,
  so include the per-step counts for every city.
- Renames and scope changes that change what a reader of the site sees.
- In a build's drafts file: each sentence written to a page or a reference doc
  that no approved template covers, flagged as a proposal for review time
  (`docs/city_page_format.md` section 6). A sentence from a template needs no
  entry.

**Never quote a registrant's own name**, not even as the example of a privacy
rule: use a placeholder ("SURNAME GIVEN-NAME INITIAL"), or the key from
`python pipeline/name_keys.py "NAME"` (`docs/city_page_format.md` section 5).

## What doesn't

- Pure copy edits with no factual consequence.
- Pipeline mechanics with no judgment attached ("ran step 2" isn't a
  decision; what you found is).
- Current-state description - that goes in `docs/project_context.md`.
- Open work - that goes in `PLAN.md`.

## Then

If the decision changed current state, update `docs/project_context.md` to
match (rewriting it is fine there) and tick or add the item in `PLAN.md`.
Read two or three recent entries before writing one - the rhythm matters
more than this template.
