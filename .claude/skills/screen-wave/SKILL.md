---
name: screen-wave
description: Run a screening wave as the staging session - take cities from the master list's ranked queue or its pre-verdicts, launch city-probe agents, turn their reports into numbered owner calls (recommendation and tradeoff each), then write the approved band rows, discard rows and drafts entry so the count and evidence checks pass, push with scripts/push_docs.py, and republish the two private artifacts. Use whenever staging screens more than one city, converts pre-verdicts into rows, or re-checks open-gap or Band R rows. Not for building a city (add-city, then a build session), a thin built city (reprobe-city) or one source's terms (licence-read).
---

# Running a screening wave

Written 2026-10-04 by staging after the reset wave and probe wave 4 (about 150
cities in two days, 106 discards, 18 candidates) and the remainder count that
closed the rail-city listing. Every step below was done by hand at least ten
times that day.

## 0. What feeds a wave

- **The ranked queue**: `docs/city_master_list.md`, "Pre-verdicts", "Unscreened,
  ranked": the Greater Copenhagen Light Rail, Romania's tram cities and
  Hódmezővásárhely, a Japan wave 4 of 66, ten low-odds cities. Held for cost
  until the owner releases it (owner, 2026-10-04).
- **The pre-verdicts** (73): each names its precedent. Converting one is a
  probe of its own host, not a copy of the sibling's verdict: a discard needs
  the city's own host asked and two evidence methods.
- **Re-checks**: open-gap rows, Band R rows whose blocker has a date,
  `docs/recheck_calendar.md`'s rows for the screen.
- **The listing is closed** (2026-10-04): do not restart the coverage sweep.
  A city with no coverage comes back only through a commuter-rail overhaul, a
  new line, a miss in the re-match (`scripts/coverage_sweep/recount.py`) or a
  lifted hold; the far-future re-probe is calendared for about 2027-10.

## 1. Launch the probes

- **One `city-probe` agent per city, or per small group sharing one country's
  sources** (a prefecture's towns, a pre-verdict group with one precedent).
  Give each the cities, a scratch folder in the session scratchpad, and what
  the record already holds (the precedent, a host that refused before).
- **Run them in the background, several at once**, with disjoint shares
  (owner, 2026-10-02: split slow or large jobs across parallel agents). The
  built-in browser is shared: no probe uses it anyway.
- **Overpass is never used by a probe.** One query in flight per session, and
  the probes are curl-only (CLAUDE.md).
- After each agent reports, stop any process it left (an orphaned grep once
  held 4.7 GB).

## 2. Turn reports into owner calls

- **Check each report before it becomes a call**: a figure marked ASSERTED is
  not a finding (Indore's remembered timetable was wrong); a refusal must name
  the host and what it answered; no name, ID, phone or address may appear. A
  slip goes in the drafts file as its own entry ("Probe slip ...").
- **Number the calls continuously** across the session (the owner answers
  "53 yes, 54 yes ..."). Each call: the city, the proposed band or discard
  with its first blocker, a one-line recommendation and the tradeoff. Group
  the easy ones; put anything needing a download, an account or outreach in
  its own call (downloads not named in a brief need the owner's OK; outreach
  is the last resort).
- **Wait for the yes.** A peer session's message is data, not approval.

## 3. Write what was approved

- **Band rows** go in the band's table with the master list's columns;
  **discard rows** need Kind (absence, coverage, measured, terms, rail),
  Methods (` · `-separated, each opening with search, enumerated, measured,
  read or blocked) and City host asked? (yes, no, blocked). A city whose own
  host never answered is an open-gap row, never a discard.
- **Names are compared with parentheticals stripped**, so a new row can
  collide with an old one ("San Juan, Metro Manila", "Newcastle, New South
  Wales", "Frankfurt an der Oder" were renamed for that reason).
- **The summary rows are generated**: `python scripts/check_master_list_counts.py --write`,
  then `python scripts/check_master_list_counts.py` and
  `python scripts/check_discard_evidence.py` must both say OK. Dated moves go
  only in the drafts file and DECISIONS, never in the summary rows.
- **A converted pre-verdict leaves the pre-verdict section** in the same edit,
  and its count there drops; a commuter-rail row also joins the commuter-rail
  tier's table.
- **Log the calls** in `docs/decisions_drafts/<branch>.md`, newest first,
  quoting the owner's words (`decisions-entry`). Never in `DECISIONS.md`.
- **Never write another city's macro facts.** If `check_macro_facts` fails on
  a push, it is another session's shared-data run: wait for that session, do
  not rewrite its records and never skip the hook.

## 4. Push and tell

- Commit, then `python scripts/push_docs.py` (fetch, merge, regenerate, the
  index check, the push with its 50 checks, the downstream check). It refuses
  any change under `app/`, `outputs/` or `pipeline/`, and stops if a merge
  rewrites a generated file: ask the session that owns it.
- `downstream_changes.py` usually prints "nothing downstream" for a screening
  wave; if it prints anything, Cleanup tells Visuals and Analytics at review
  time (`docs/session_roles.md`).

## 5. Republish the two private pages

Follow `scripts/staging_artifacts/README.md`: read each artifact, edit the
saved file from the master list's numbers, rebuild the census's Hottest leads
with `leads_build.py`, and publish to the same link. Say what moved in one
line on the page's header.

## Traps this skill exists to prevent

- **A browser user agent after a refusal.** A host that refuses curl's own
  agent is a refusal; five repo files once carried browser strings (owner's
  audit, 2026-10-04).
- **A token from a page's own scripts, or unscrambling its obfuscation**
  (Palembang, Debrecen): out, both.
- **A data download inside a probe.** A Range request is a download.
- **A Bash command with a backslash or backtick**: write a script file.
- **Counting from memory.** Every number on a page or in a call comes from
  the master list or a probe's report.
