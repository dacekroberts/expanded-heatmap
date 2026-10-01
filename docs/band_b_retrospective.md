# Band B, start to finish: twelve narrower pages from one build session

A record of the Band B build session (worktree `band-b`, 2026-09-29 to
2026-09-30), written so the next batch of builds is cheaper. The cities' own
facts live on their branches (each `docs/decisions_drafts/<city>.md`, or
`DECISIONS.md` for the first five) and in their briefs; this file is the
narrative that connects them, and the record of what went wrong.

**Twelve cities, twelve branches, nothing on master.** Every branch was cut from
`origin/master`, merged `origin/macro-legend` before scaffolding, merged master
again before its push, passed `check_all.py` and `check_deploy_imports.py --ref
HEAD`, and was pushed only at 0 behind. Landing is the cleanup session's.

## What was built

| Page | City | Business source | Storefronts | In a ring | Stations | Tier | Branch |
|---|---|---|---|---|---|---|---|
| 76 | Ottawa | Ottawa Public Health inspections (food only) | 4,896 | 32.4% | 25 | one_bucket, light_rail | `ottawa` |
| 77 | Minneapolis | City food inspections (food only) | 1,793 | 35.7% | 15 | one_bucket, light_rail | `minneapolis` |
| 78 | Pittsburgh | Allegheny County food facilities (food only) | 1,730 | 18.3% (halved rings) | 20 | one_bucket, light_rail | `pittsburgh` |
| 79 | Kitchener–Waterloo (Regional) | Region of Waterloo inspections (food, personal) | 2,086 | 41.5% | 19 | narrowed, light_rail | `kitchener-waterloo` |
| 80 | Palma | Consell de Mallorca restaurant register (food only) | 3,432 | 34.6% | 10 | one_bucket, metro | `palma` |
| 81 | Yokohama | City barber, beauty, laundry registers (personal only) | 7,843 | 83.4% | 140 | one_bucket, metro | `yokohama` |
| 82 | Hiroshima | City counter list + MHLW filings (food only) | 13,567 | 67.3% (halved rings) | 124 | one_bucket, metro | `hiroshima` |
| 83 | Namyangju | SEMAS (all three) | 18,344 | 54.9% | 17 | full, metro | `namyangju` |
| 84 | Ansan | SEMAS (all three) | 19,711 | 63.8% | 13 | full, metro | `ansan` |
| 85 | Uijeongbu | SEMAS (all three) | 13,103 | 85.3% | 20 | full, metro | `uijeongbu` |
| 86 | Dallas | Texas Comptroller sales-tax permits (Houston's) | 15,885 | 26.4% | 44 | narrowed, light_rail | `dallas` |
| 87 | Anyang | SEMAS (all three) | 15,177 | 64.2% | 7 | full, metro | `anyang` |

Eight of the twelve are the band's own shape - a page narrower than three
buckets, saying what is missing. The four Korean satellites and Dallas were
added to the queue mid-run (the satellites from the Gyeonggi brief, Dallas from
the discards, Anyang last).

## The order it ran in, and why it held

The queue was the owner's (Ottawa, Minneapolis, Pittsburgh, Kitchener–Waterloo,
Palma, Yokohama, Hiroshima, then the satellites, then Dallas, then Anyang), and
it held because each city was built whole before the next started: brief check,
scaffold, steps, the gate sequence, drift check, merge, push, READY. Read-only
preparation (Step 0 re-verification, licence reads) ran ahead in agents while
builds stayed sequential, which is what let the queue move without two builds
sharing a working tree.

The gate sequence was fixed after the first three and never reordered:
personal exposure, provenance, scope disclosure, the inconsistency rows and
`cities.py` fields, the master list, the README, macro facts, category
continuity, the macro label, the decisions entry, commit; then drift check and
baseline, ring shares, commit; then merge master, `check_all`, deploy imports,
re-fetch, push at 0 behind, READY. **Doing them in that order meant each check
found only its own problem**: provenance never failed on a missing table row,
because the rows were written by then.

## How it differed from earlier builds

- **Narrower pages as a category, not an exception.** Before this band a
  one-bucket page was a special case argued per city (Hong Kong, the FSA
  cities). Band B built eight of them under one bar - the owner's
  reduced-bucket rule - and the site gained the vocabulary to say so: the
  two-key macro legend (mode by colour, completeness by fill), and two new
  `categories` values the owner approved at build ("Personal services only"
  for Yokohama; "Health inspection register" as a record kind for
  Kitchener–Waterloo).
- **Templates over first principles.** The Canadian and US builds each wrote
  a pipeline; here only two cities needed new shared code (Palma's Catastro
  join, `pipeline/countries/spain_catastro.py`; Kitchener–Waterloo's
  layer-to-zip join stayed city-local). Every other city was an existing
  template with a config: Kobe's and Fukuoka's for the Japanese two, Bucheon's
  for the four satellites, Houston's for Dallas. The satellites took their
  config, page, docs rows and master-list move from small generators once the
  first was built, so each later one was mostly waiting on Overpass.
- **City-local hooks before shared changes.** Yokohama's zipped CSVs and its
  `詳細業種` type column, and Hiroshima's `許可条件` and vehicle columns, were
  read through the `config.source_rows` hook Kyoto had added, so the shared
  Japanese join (and its Minato control) never changed. Only two shared
  changes were made, both backward compatible and both proved so (below).
- **Many sessions on one machine.** Earlier builds ran alone. This one ran
  beside a cleanup session, a staging session and three tram-kit sessions, so
  heavy jobs were announced, then gated (`scripts/heavy_job.py`, which arrived
  mid-run); page numbers were negotiated (France moved to 100-119 when it
  overlapped Band B's 76-87); and owner calls often arrived relayed.
- **Owner calls made at build, not before.** The open questions were asked
  inside the builds - the K-W zips, Palma's frequency and size, Yokohama's
  category, Dallas's Streetcar and M-Line, Dallas's mode and coverage - each as
  a recommendation with its tradeoff. Others arrived by relay: K-W's record
  kind, Palma's and Hiroshima's metro mode, and Anyang's assignment.

## How smoothly it ran, against the early US and Canadian builds

The fair comparison is with Los Angeles, New York, Vancouver and Montreal - the
builds that wrote the rules this band ran on (`us_build_retrospective.md`,
`canada_retrospective.md`). The short answer: **building was much smoother;
integration was not, and part of the smoothness is integration cost deferred
to landing.**

**What made the builds smoother - almost all of it inherited.**
- **The errors that defined the early builds were caught by gates, not by
  re-reading.** Canada's dominant class was the denominator (Montreal's 440
  storefronts per station, summed over rings, was 151; Calgary's and Toronto's
  "stations" were platforms), each found after a ranking had been published.
  Here the same classes appeared and stopped at a gate before any commit:
  Hiroshima's tram stops tripped the platform-spacing gate (and were genuinely
  close, so the floor moved by precedent, not by eye); every gate-3 mismatch
  (Dallas, Line 4, the Gyeongchun Line) was traced to a fact before it passed.
- **Briefs were checked, not discovered.** Vancouver and Montreal were
  re-briefed in the middle of their build day; Toronto's brief checks were
  "stale and passing". Every Band B city arrived with a brief whose
  `brief-checks` ran first, and a brief that was wrong (Yokohama's 17,408,
  Dallas's "full", Hiroshima's open licence point) was corrected in the brief,
  not worked around in code.
- **Licences were already read.** The US build's three worst corrections were
  licence positions taken from a cited page instead of the instrument (New
  York's footer, Philadelphia's terms by reference). Here every source had a
  `licence-read` verdict before the build, and the open points were owner calls
  already made (Pittsburgh's and Dallas's indemnities, Hiroshima's full list).
- **Privacy was a check with a verdict.** Los Angeles taught that a missing
  trade name falls back to a person; here `check_personal_exposure.py` ran on
  every city with a printed verdict, and the Japanese and Korean name rules,
  Houston's organisation-type rule and the home-address rules were already
  shared code.
- **Templates instead of new pipelines.** Vancouver needed two registries, two
  taxonomies, a parcel join and a boundary that was a line; New York needed
  four registries and a dispatching taxonomy. Ten of the twelve Band B cities
  were an existing template with a config.

**What was not smoother.**
- **Coordination.** Twelve branches, each merging master and macro-legend,
  meant a DECISIONS conflict on almost every branch, two committed-marker
  incidents averted only by checking, notice numbers that cannot be reserved,
  ordinals and counts that are wrong on every branch but one, and labels that
  only a combined-tree scorer could place. Canada built and landed in one
  evening; none of Band B has landed.
- **Rules changing mid-run.** The two-key legend re-tiered three finished
  cities; the drafts rule, the heavy-job gate and the Overpass rule arrived
  between builds. Each was cheap to adopt, but each is another reason a
  branch's state depends on when it was cut.
- **A fixed per-city overhead.** Fourteen gates and a drift check per city is
  far more ceremony than Los Angeles had. It is what made the builds
  predictable, and it is why a small satellite still took a full gate run.

**The mistakes changed kind.** The early builds' mistakes were measurement
mistakes - wrong denominators, platforms counted as stations, stale mirrors,
licence positions taken on trust. Band B's (below) were framing and process
mistakes: a question put to the owner on the wrong rule, a precedent not
weighed, a chained commit, a guessed width, CRLF, a probe that printed too
much. That is the signature of a pipeline whose measurements are now guarded
and whose remaining risk sits in the human steps around it.

## What changed during the run

Rules arrived while builds were in flight, and each branch took them at its
next merge:

1. **The two-key macro legend** (owner, 2026-09-30, on `origin/macro-legend`):
   every branch merges it before scaffolding; `mode` is the highest mode drawn,
   `coverage` is decided by table B; food shops count as food. Ottawa,
   Minneapolis and Pittsburgh were re-tiered after their builds.
2. **DECISIONS drafts** (owner, 2026-09-30): from Yokohama on, entries go to
   `docs/decisions_drafts/<branch>.md`, one file per city branch so the
   branches never conflict with each other.
3. **The heavy-job gate** and a correction to it: a fixed "12 GB for two jobs"
   budget was replaced by admission against memory actually available. Every
   satellite step measured 0.3-0.6 GB; Dallas's placement 0.43 GB.
4. **Overpass discipline**: one query in flight per session; a 504 means wait.
   One brief check failed transiently on a partial answer and passed on rerun.
5. **Downloads and prose pre-approved**, with a template departure flagged in
   the drafts file rather than stopping the build (Dallas's two sentences).

## The shared code that changed

- **A per-city N02 edition** (`japan.N02_EDITIONS`, `japan.n02(slug)`).
  N02-24 predates Hiroden's 2025 route into Hiroshima Station and still drew the
  closed 猿猴橋町 stop; MLIT's N02-25 (published 2026-04-07) has the new layout.
  Hiroshima reads N02-25; the six built Japanese cities still read N02-24,
  checked identical in memory (10,123 stations, same group codes) rather than by
  re-running their steps from a branch. Moving them is each city's own change.
- **A per-city floor for gate 1** in the Japanese step 1
  (`config.SPACING_MIN_M`), because a tram-heavy station set is genuinely
  closer than 400 m; Hiroshima takes the 200 m the tram cities take.

## The errors, by kind

Recorded because each one is cheaper to prevent than to find.

**Judgment calls framed wrong.**
- *Palma's frequency.* I asked the owner whether to discard Palma on the
  15-minute rule. The owner pointed out that frequency gates converted railway
  only (Buffalo's 20 minutes stayed); purpose-built track discloses its
  timetable. Read the test's own wording before citing it against a city.
- *Dallas's coverage.* I passed on the brief's "full" without weighing
  Houston, which uses the same register and is narrowed because Texas taxes few
  personal services. I corrected the question before building on it, and the
  owner chose narrowed. A proposal inherited from a brief still needs its
  precedent checked.

**Process slips.**
- *Committed conflict markers* (Kitchener–Waterloo): `merge_append_only.py`
  hit a Windows file lock, and a chained command committed and pushed
  DECISIONS.md with markers in it. Fixed by hand; from then on every
  resolution ran `dec_verify.py` (markers 0, every heading of both sides
  present) before staging. `check_conflict_markers.py` is now on master.
- *Pushing while behind*, twice on Kitchener–Waterloo; after that, push only
  at 0 behind, re-fetched in the same command.
- *A guessed label width*: Anyang's was typed before it was measured. Caught
  before scoring and replaced by the measured 51.6 px; the check would have
  accepted the guess, since it refuses only a missing width.
- *CRLF from Python writes*: on this machine text-mode writes, and several
  `--write` generators, leave CRLF in LF files (app/cities.py came out with
  2,358). Git normalises it, so diffs looked clean. Every edit script now
  writes bytes, and every `--write` is followed by a conversion check.

**A privacy slip.** A schema probe for Hiroshima printed the first five rows of
each sheet whole to my console, operator names and an applicant address among
them. Nothing reached a file or a commit; every later probe printed column
names and counts only. A probe of a register with personal columns should
select its columns before printing anything.

**Source surprises that the gates caught.**
- Stale national data (N02-24 and Hiroden), caught because OSM had no tram
  stop where N02 had one.
- A translated station name (修大協創中高前 as "Hiroshima Shudo University
  Hiroshima Kyoso Junior and High School") and run-together compounds
  ("Byeollaebyeolgaram", "Singiloncheon"), caught by reading every name.
- Gate 3 mismatches each traced to a fact, never adjusted to pass: Dallas's
  closed Convention Center (role `inactive`) and its not-yet-mapped Hidden
  Ridge; Line 4's relations stopping short of the Jinjeop extension; the
  Gyeongchun Line's branches in OSM against its infobox.
- An undocumented type code (Dallas's `ADDRESSTYPE`), left unused rather than
  guessed, at the cost of Houston's Residential-point home rule.

## What the next builds should inherit

- **Promote the scratch tools that carried the batch.** The combined-tree
  label scorer (every branch's new cities and changed offsets, scored in
  memory) is the only way to place labels for branches that land in an unknown
  order; Dallas's placement moved San Diego's label, which no single branch
  could have seen. The master-list movers (Band B, Band A, and the satellite
  row that stays open) and the satellite config generator belong in
  `scripts/`.
- **A CRLF check** in `check_all`, beside the conflict-marker one.
- **A width check that refuses a value not measured in the same run as its
  controls**, or at least a comment naming the run.
- **One Japanese migration to N02-25**, city by city, each decided by its drift
  check.
- **Dallas's address types**: one question to the City's GIS office would let
  Houston's home rule run there.

## What landing has to resolve

- **Notice numbers**: Ottawa, Kitchener–Waterloo, Palma, Yokohama and
  Hiroshima each add one required notice numbered next after master's last
  (the check requires the list contiguous from master), so they renumber in
  landing order.
- **Ordinals and counts**: two branches say "Japan's seventh", four "South
  Korea's tenth"; the master-list counts are branch-relative.
- **The SEMAS notice's heading** gains a satellite on each of four branches.
- **The Gyeonggi satellites row** closes when the last of the four lands.
- **For review time**: Dallas's two page sentences beyond Houston's template,
  San Diego's moved label, and the Dallas home rule that cannot run.
