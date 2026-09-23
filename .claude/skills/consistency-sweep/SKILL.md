---
name: consistency-sweep
description: Audit what the build and research sessions leave behind - stale prose written in the future tense, hand-kept counts that drifted, cross-references broken by renumbering, sources in use with no licence read, tables that stopped rendering, orphaned branches and worktrees. Use when asked to check whether the project's own documents are still true, to clean up after a city or country landed, or when a session is claiming the cleanup role. Not for building a city (add-city) or screening one (add-country).
---

# Sweeping for what the other sessions do not look at

The build and research sessions are pointed forward: add a city, screen a
country, land a feature. Both leave a wake, and neither has a reason to look at
it. This role reads what the project says about itself and checks whether it is
still true.

**It does not build and it does not research.** A city's pipeline, a country's
screen and a licence that has never been read are other sessions' work. This
one corrects the record, and makes the record hard to falsify next time.

## Never ship a check you have not watched FAIL

A check that passes proves nothing until you have made it fail on purpose. On
2026-09-22 a newly written limb reported success while examining **nothing**:
it read longitudes from `app/cities.py` with `getattr(node, "value", None)`,
and a negative number is an `ast.UnaryOp` wrapping a Constant, so every western
longitude parsed as `None` - **zero of sixteen cities**. The section printed
its confident green line anyway. It was caught by breaking a city's CRS on
purpose and noticing the check stayed silent, not by reading the code.

So for every limb: break the thing it guards, watch it report, restore, watch
it pass. And where a limb can be starved of input rather than given bad input,
**assert that it had input** - that one now fails if it reads fewer longitudes
than there are cities.

This is the same shape as everything else in this taxonomy: something that
looks right and is invisible to the tool examining it.

## The one principle that matters: prefer a check to a correction

**A correction fixes an instance. A check fixes the class, and keeps fixing it
after this session is gone.**

The worked example is 2026-09-22. A reader noticed that four Canadian cities
were missing from the provenance tables. Promoting them by hand was an hour's
work and would have been the whole job. Writing
`scripts/check_provenance.py` instead took somewhat longer and immediately
found **five more gaps nobody had noticed** - Mexico City and Guadalajara
entirely absent, and unrecorded residence-filter layers in San Diego, San
Francisco and Los Angeles. Then, the same day, it caught a *sixth*: a merge
silently dropped an endpoint URL while leaving the row looking perfectly
correct.

So when a sweep finds a defect, ask in this order:

1. **Can a script decide this?** Numbering, cross-references, table structure,
   "is every X recorded in Y" - all of these are deterministic. Write the check,
   let it fail, then fix what it found.
2. **Can a script flag it for a human?** Staleness and drifted counts are
   heuristic. A report that lists candidates is still worth far more than a
   memory of having looked once.
3. **Only then, fix it by hand** - and say in `DECISIONS.md` why it was not
   checkable, because that sentence is what stops the next person re-deriving
   the same conclusion.

A check that fails on a real defect is working correctly. Do not add an entry
to its ignore list to make it green; an ignore list is for defects someone has
decided to carry, with a date, and it may only shrink.

## Verify against `origin/master`, never against the tree you are in

**On 2026-09-22 three findings were relayed from other sessions and two were
wrong** - not mistaken, *stale*. Both sessions had branched before a merge
landed and were describing a file that had since changed by 339 lines. One
reported a NOTE that had been deleted hours earlier; one reported a branch as
unmerged when its commit was already an ancestor of `origin/master`.

Acting on either would have meant re-doing finished work or merging something
already in. So:

```bash
git fetch origin
git show origin/master:<path> | ...          # read the real current file
git merge-base --is-ancestor <sha> origin/master   # is this REALLY unmerged?
git log --oneline origin/master..<branch>          # what does it actually add?
```

This cuts both ways. Verify before acting on a claim **and** before dismissing
one. Of the three that day, the one that survived checking was real, and it was
in a file this same session had edited an hour earlier without noticing it.

## The defect taxonomy

Every entry below is a real instance from this project, which is why the list is
this specific. Sweep for the shape, not the example.

### 1. Prose written in the future tense about a present that arrived

The largest category, and the most invisible, because the document reads
perfectly - it is just describing a world that no longer exists.

- `canada_step0_endpoints.md` opened "**No Canadian city is built.** When one
  is, these rows merge into `data_sources.md`" while six were built.
- `docs/licenses/canada-required-notices.md`: "Notices Canada would require, if
  any Canadian city is built."
- `docs/licenses/README.md`: "Canada - screened, none built", and four rows
  above it, "WMATA - *not yet a row; D.C. is unbuilt*".

**Grep for the tense, not the topic:** `none built`, `not built`, `unbuilt`,
`if any`, `when one is`, `would require`, `not yet`, `eventually`, `for now`,
`candidate, not built`, `still open`, `to be decided`.

**The fix is not deletion.** These files are the evidence trail for how
something was found. Relabel them - state plainly that they are superseded, name
what now holds the live answer, and add an explicit precedence line ("where this
file and X disagree, X wins"). Then say which of their claims did *not* survive.

### 2. Hand-kept counts, which always drift

Four were found in one file in one day, and one contradicted itself two clauses
later:

- "for the **fourteen** cities now built there are **thirteen** sources" - there
  were sixteen and sixteen, and the same sentence went on to say "six of the
  twelve".
- "New York contributes four of **the eight registries**" - the table held 37.
- "**All six** of these agreements are stored locally" - seven.
- "**Two files** are not raw fetches" - four, and two of the unlisted ones had
  said so in their own headers for a day.
- "the **only** item left unread" - a second unread source had been added to the
  same table.

**Prefer deleting the count to correcting it.** Keep the durable observation and
let a check own the number. A count maintained by hand beside the list it counts
will drift again, and it is most dangerous in a section that gates something -
a deploy, a licence position, a privacy claim.

**The test for whether a count is safe is its DENOMINATOR, not its accuracy.**
Sweeping this project's counts to the floor left twenty standing, and every one
of them is scoped to something that cannot grow without the sentence being
rewritten anyway:

- a **constant of the world** - "all five boroughs = the city", "the six
  pre-1998 municipalities that amalgamated into Toronto";
- **fixed project vocabulary** - "all three buckets" is this project's
  definition of what it maps, not a tally;
- a **closed set** - "the two Alberta cities" and "all six Canadian sources",
  where the country's build is complete; "the two diagnosed cities", which
  changes only when the skill naming them is being edited;
- a **dated statement** - "all fourteen cities before Mexico City read GTFS".

Every count that had rotted, by contrast, counted something **open**: cities
built, sources recorded, agreements stored, registries in a table. So the
question is not "is this number right today" - a rotted count was right once
too. It is **"can the thing this counts grow without anyone touching this
sentence?"** If yes, delete the number and name the thing instead.

**Then ask whether the document is CURRENT-STATE or DATED**, because the
answer inverts the action. `DECISIONS.md`, a handover pinned to a commit, a
retrospective - their counts are evidence of what was true when written, and
**updating one destroys the record**. Only a document that claims to describe
the present has a count worth deleting. `check_stale_claims.py` excludes the
dated ones by name and pattern for exactly this reason, and a sweep that
"corrects" a retrospective has done damage, not work.

### 3. Cross-references broken by renumbering

A numbered list that other files cite by number is a coupling nobody declares.
Renumbering the notices list on 2026-09-22 broke `docs/build_briefs/edmonton.md`,
which said "item 14 carries it".

**`check_provenance.py` check F now decides this**, and a range check would
not have: renumbering moved Edmonton from item 14 to 15, and the brief went on
saying "item 14 carries it" - a citation that still RESOLVED, to Calgary. So
the check compares the cited notice's SUBJECT against the subjects named
around the citation, and fails when the neighbourhood is talking about a
different notice than the one it cites. Verified by reintroducing the real
break: it reports `cites item 14 (Calgary), but the text around it names
['Edmonton']`.

**The hard part was namespaces, not numbers.** "Item N" means at least three
different lists here - the notices list, the deploy-gate list under "What
closing this fully requires", and `global_country_shortlist.md`'s own "#### Item
N" sweep. The first version checked all of them against the notices list and
produced thirteen bogus notes; every one was a citation of a different list.
Only "notice N", and "item N" whose sentence also names `data_sources.md`, are
treated as notices citations now - and "Gate item N", "Step 0 item N" and
`#### Item N` headings are excluded explicitly. **A check that reports other
people's correct work as broken is worse than no check**, because the next
reader learns to skip the section.

Still worth doing by hand before renumbering:
`grep -rn "item [0-9]\|notice [0-9]\|step [0-9]"`. Better still - check
whether the list needs numbers at all, or whether an anchor would do.

Watch for **appended blocks that never renumber**. Two countries' notices were
appended after an existing block and produced two item 8s and two item 15s in
the list that gates the public deploy.

### 4. Structure that stopped rendering

Markdown fails silently. A table row separated from its header by a prose
paragraph renders as literal pipe-delimited text, and the file still looks fine
in a diff.

- Orphaned rows: a `| … |` line with no `|---|` delimiter above it in the same
  block.
- Column-count mismatches: a row with fewer cells than its header renders
  misaligned. One row in the master provenance table had five against six.
- Rows missing their closing `|`. GFM permits this and they render - but the
  obvious way to write a table checker is
  `startswith('|') and endswith('|')`, which **silently skips them**. That is
  the whole problem in miniature: content that looks right and is invisible to
  the checker.

**`check_provenance.py` check I decides the first two and fails.** It was
written inline six times during one sweep before being committed, which is the
usual sign that something belongs in a script. Two traps in writing it, both
worth knowing if it ever needs changing: a HEADER row sits above its own
delimiter and so legitimately has no width yet - checking without a one-line
look-ahead flags every header in the file - and fenced code blocks contain
pipe-delimited text that is not a table.

### 5. Sources in use with no terms established

The licence review is organised per city, so a source belonging to no city
slips through. Four did:

- A **naming layer** - the polygons that say which municipality an excluded
  station is in. Vancouver's is the **Province of British Columbia's**, a
  different publisher from either city in that build, and it required its own
  notice. It had been publishing into the site unread.
- A **residence join** - the parcel or assessor layer that decides whether a
  licence is somebody's home. Three US cities use one; none was recorded.

Ask what a build **reads**, not what it **draws**. If a file under
`data/<city>/raw/` came from the internet, it needs a provenance row and a
licence position, even when nothing it produces is visible on the map.

And expect the answer to be strange occasionally: one source in this project
**prohibits** being credited at the scale its map is drawn at, so the absence of
a notice there is a deliberate compliance position and "fixing" it would breach
the terms.

### 6. Labels that stopped describing their contents

`## Transit feeds (GTFS)` held three rail sources that were not GTFS. A heading
is a claim like any other.

### 7. Comments describing code that changed

`pipeline/san_diego/config.py` says a per-point lookup was "REPLACED" by a bulk
download. It was not - the bulk approach was tried, abandoned, and the constants
it needed are still in the file, read by no script. The docstring two files away
tells the true story.

**Record what the code does, not what the comment claims**, and note the
divergence rather than silently trusting either.

**`check_stale_claims.py` category D finds the candidates**: config constants
that no script reads, counting real reads rather than mentions. A dead constant
is harmless in itself - it is a prompt to go and read the comment above it,
which is where the stale claim lives.

Two things that pass this check are worth knowing, because both look like bugs
and are not. **San Francisco's `COUNTY_BOUNDARY_URL` is read by nothing**, and
its `fetch_sources.py` says why in terms: the three older inputs "were
downloaded before this script existed... and they are not re-fetched here,
because re-downloading a business export changes every count in
`DECISIONS.md`". A documented deliberate gap. **Vancouver's
`MUNICIPALITIES_KEEP` is read by nothing** because that layer NAMES rather than
filters, which is exactly what its provenance row says. Reading the comment is
the step, not deleting the constant.

### 5a. Promises to a reader that nobody can keep

A page that says "the excluded stations are listed in
`outputs/montreal/excluded_stations.csv`" has made a claim on behalf of someone
who will go and look. `outputs/` is committed and `data/` is not, so a city
added in a hurry can cite a file that never leaves the machine it was built
on - and nothing about the page looks wrong from the inside.

`check_provenance.py` check J resolves every `outputs/...` path named in a page
or a doc and fails if it is missing OR merely uncommitted. It was clean when
written, across 17 paths; it exists for the seventeenth city rather than for
the sixteen that are already right.

### 8a. Compliance artefacts that quietly stop being evidence

A hash, a stored document, a recorded date - these exist so a claim can be
checked later, and they fail silently by construction: nothing breaks when a
digest stops matching, so nothing announces it.

`docs/licenses/README.md` records a SHA-256 per stored licence so the clauses
quoted in `data_sources.md` are "checkable against the text that was actually
agreed to". On 2026-09-22 **two of nineteen hashes described bytes that existed
nowhere**, and two more licence files had no hash at all. The cause was not
carelessness: `.gitattributes` sets `* text=auto eol=lf`, so git rewrote CRLF
to LF *after* each hash was taken - once for a file fetched from a server that
sent CRLF, once for a file a Python script wrote on Windows.

**So compute a digest from the COMMITTED file, never the one you just
fetched**, and prefer a check to a convention: `check_provenance.py` check G
now verifies all of them on every run.

### 8. Repository artifacts that outlive their work

Empty worktree directories, branches merged long ago, worktree registrations
pointing nowhere. Harmless individually; together they make the project look
busier than it is and obscure the one branch that genuinely matters.

```bash
git worktree list                     # vs. what is actually on disk
git worktree prune --dry-run -v
git branch --merged origin/master
git rev-list --count origin/master..<branch>   # 0 = safe to delete
```

## What this role does NOT touch

**Never merge a branch you do not own.** On 2026-09-22 a branch looked abandoned
- two commits, no worktree, nineteen commits behind. Its commit message said it
was held off master deliberately, because landing it would publish a city before
its sibling and deploy a broken imported module until a reboot. **A branch that
documents its own hold is a decision, not a loose end.** Read the commit message
before concluding anything from the branch graph.

What you *can* do for such a branch, without touching it:

```bash
git merge-tree --write-tree origin/master <branch>   # conflicts? no side effects
```

and then clear its blockers **on master** - which is how Madrid's provenance
rows came to be written before its wiring landed, so the check would not fail
the moment someone merged it.

**Do not edit a file another session has modified and uncommitted.** `git
status` in the main checkout shows this. Leave the line for them.

**Do not rewrite a city's pipeline, a taxonomy, or step logic.** If a sweep finds
a real bug there, record it and hand it over - that is a build session's work and
it needs that session's context.

## Working rules

- **After running `drift_check.py`, check `git status` before committing.** On
  Windows it leaves `outputs/` files modified even when it reports zero drift:
  regenerated files come back CRLF against committed LF, and Folium assigns
  fresh random element ids each render. `git checkout -- outputs/` restores
  them. A sweep that commits that churn rewrites files the deployed app reads,
  for no change.
- **Sweep narrow, commit immediately.** This role has no exclusive paths, so its
  protection is a short window between reading a file and committing the
  correction. A sweep that touches nine files over two hours will meet somebody.
- **One defect class per commit** where it can be helped, because the commit
  message is the only place the *class* gets named.
- **Log the class, not just the instance**, in `DECISIONS.md`. "Fixed a stale
  heading" is worth little; "three files said Canada was unbuilt, because a
  country profile writes in the future tense and nothing makes it come back" is
  the finding.
- **Say what you did not fix, and why.** A defect you decided to carry, with a
  date, is a work item. One you silently skipped is invisible in exactly the way
  this whole role exists to prevent.

## Checks that exist today

| Check | What it decides |
|---|---|
| `python scripts/check_provenance.py [--strict]` | every built city has rows in all three provenance tables; every URL its `config.py` **resolves to** is recorded; notices and `_NOTICES` are in bijection; notice numbers unique and contiguous; **`city_master_list.md`'s built counts match `app/cities.py`**, total and per country; **every `item N` citation still points at the notice it names**; **every stored licence's SHA-256 matches**; **every relative markdown link resolves**; **every table row renders and matches its header's width**; **every `outputs/` file named in prose exists and is committed**; **OSM attribution on every map, every CRS matches its longitude, no map step forks the renderer** |
| `python scripts/decisions_index.py --check` | `DECISIONS.md`'s generated index is current |
| `python pipeline/drift_check.py` | committed `outputs/` still match what the pipeline produces |
| `python scripts/check_no_fetch_in_steps.py` | no `pipeline/*/step*.py` reaches the network **inside a drift check** - directly, or through a shared `pipeline/*.py` module; a module that calls `refuse_if_offline()` is reported **guarded** rather than passed; **fails if `drift_check.py` stops arming the guard**, and if a `KNOWN_GAPS` entry has quietly been fixed and left listed |
| `python scripts/check_no_fetch_in_steps_selftest.py` | **that check still fails when it should**, six ways, against throwaway copies - the first executable answer in this project to "never ship a check you have not watched fail" |
| `python scripts/check_deploy_imports.py` | a clean clone imports under the lean venv |
| `python scripts/brief_check.py <city>` | a build brief's claims still hold against live sources |
| `python scripts/check_personal_exposure.py <city>` | no personal information in a city's published output |
| `python scripts/check_stale_claims.py` | **reports, never fails.** Prose in the future tense about something that IS built; totalising hand-kept counts; headings whose rows no longer match the label; **config constants no script reads**; **universal claims on the published surface** ("the only city", "no other city", "every city here") - run `--only E` whenever a city lands, because each hit is a bet on the next city |

**Import configs, do not grep them.** `check_provenance.py` imports each city's
`config.py` and walks its resolved values, because Vancouver builds four
endpoints from a prefix via f-strings and no literal exists to grep. A grep
would have reported them missing and been believed.

Categories 1, 2 and 6 are covered by `check_stale_claims.py`, which **reports
and always exits 0** - every rule in it is a guess about English, and a noisy
gate gets ignored, which is worse than no gate.

**Three tuning decisions in it are worth knowing before trusting a clean run**,
because each one trades recall for a report anyone will actually read:

- `DECISIONS.md` and `PLAN.md` are excluded. The first is append-only history
  where "no Canadian city is built" is a correct record of that day; the second
  is open work where "not yet" is the point.
- A future-tense marker only counts when the same line names a **built** city or
  region. This misses agency names: `SFMTA` and `LA Metro` are not `San
  Francisco` and `Los Angeles`, so two of the three stale notice labels it was
  built to catch were found by a follow-up grep rather than by the tool.
- Counts must be spelled out **and** totalising ("all six", "the eight"). Digits
  matched 1,012 measurements; undetermined counts matched 265 mostly-correct
  scoped facts. Requiring a determiner cut it to 74.

So a clean A section means "nothing obvious", not "nothing". It found a real
defect on its first run - three notices in the deploy gate marked NOT YET
DISPLAYED that had been displayed for some time - and it would have missed two
of those three on its own.
