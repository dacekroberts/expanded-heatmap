# Handoff: Regional-1 to Regional-2 (2026-10-07)

Regional-1 (branch `worktree-japan-regional-1`) built all eleven cities of its
batch: Maebashi, Fukuyama, Ichinomiya, Tsu, Fukushima, Iwaki, Akita, Ōita,
Gifu, Mito and Morioka (pages 229-239, notices 176-186). Every city is
committed with a zero-drift baseline and a privacy check of 0. Nothing is
pushed: the batch lands at the phase 1 review time. The record is
`docs/decisions_drafts/worktree-japan-regional-1.md` (entries, five parked
calls, proposals, shared-code findings).

## How the batch was run (repeat it)

- **Lead plus subagents.** The lead built Maebashi itself, scaffolded the
  other ten in one commit, added every `japan.CITIES` entry in one block, and
  then ran up to three general-purpose subagents at once, one city each. The
  agents wrote only `pipeline/<slug>/`, `data/<slug>/` and `outputs/<slug>/`
  and returned their shared-file text (cities fields, page, notice, doc rows,
  verdict, drafts entry) in their final message. The lead pasted it with a
  helper script and committed per city. The agents' instructions file is in
  the Regional-1 scratchpad; it cost about 0.3M agent tokens and 1.3% of the
  weekly pool per city.
- **One Overpass query in flight per session:** the agents took a lock
  (an atomic `mkdir`) around `fetch_sources.py osm`.
- **Subagents cannot write report files** (the harness refuses); they return
  text.
- **Check `data/` is a junction** when the worktree is made (`Get-Item data |
  Select LinkType`); Regional-1's and East-1's were plain empty folders.

## Before your first city

- **Licence reads.** Six of Regional-1's briefs said "the read is pending,
  staging records it" and none was recorded. Grep each of your briefs for
  that phrase and ask Staging for every pending read in one message at the
  start. Staging read six in about an hour.
- **BODIK:** `brief_check.py`'s few metadata calls may run from any session,
  20 s apart, one city at a time (Staging, 2026-10-07). Data comes from the
  cached Step 0 files.
- **Call 198:** no region views, label tiers or label offsets; Cleanup builds
  the Japan views. `check_macro_labels.py` fails with a KeyError on the new
  cities until then: record it, leave it.

## Traps each city hit (check yours for them)

1. **A full list kept whole plus new-permit months** cannot be one
   `rebuilt_register` source under calls 161 and 172 (one `TERM_AS_OF` per
   source). Read them as two sources of one `SOURCE_KIND` (`food`,
   `food_new`), each term against its own file's date (Fukushima, Ichinomiya,
   Iwaki).
2. **`rebuilt_register` ranks on the latest expiry alone**, so a renewal
   starting after the as-of hides the permit in force (Fukuyama lost 17
   premises until its config ranked only permits started by the as-of), and
   it folds live permits of a different 種目 (Iwaki, 5 pins). Where a list is
   a snapshot of permits in term, read it whole.
3. **`wareki_date` reads no YYYYMMDD date** (Gifu's 20250620): the term rules
   then compare nothing, silently. Normalise in `source_rows`.
4. **A file named .csv may be an XLSX** (Ichinomiya's July beauty file).
5. **Line labels anchor on a line's first or longest N02 section**, which can
   lie wholly outside the city (Akita, Gifu, Mito, Morioka: 2 to 12 km out).
   Gifu's `step3_map.py` has `in_city_first`; copy it until the shared fix
   lands.
6. **Rings:** compute the true median nearest-station gap. Gifu's brief read
   641 m where the median was 545 m, inside the owner band (parked).
7. **`other_muni` is not a cut** for a prefecture-wide list (Tsu): a prefix
   cut in `source_rows` is, and old pre-merger city names (久居) appear.
8. **`check_personal_exposure.py`'s Japan pass** must read
   `japan.city_rules(slug)` (fixed on Regional-1's, East-1's and Kansai-1's
   branches identically); without it a new city over-counts.
9. **Census ratio high where snack bars are unmarked** (Akita 2.13: R3 keeps
   them in Food service); low where a list leaves rows out by design
   (Ichinomiya 1.40, Gifu 1.51, Mito 1.39). Say why in the drafts entry.

## At the batch's end (what `check_all` needs)

- `python scripts/fingerprint.py table` (the owner's key is on this machine;
  publish-city gate 4a), then re-run every city's step 3, so each map carries
  its authorship mark.
- `check_macro_facts.py --write` and `check_ring_shares.py --write` after the
  last re-render, converted to LF; their diff must touch only your cities.
- `readme_cities.py` and `rendered_surfaces.py --write`.
- Every file endpoint in full in `docs/data_sources/japan.md` (an ellipsis
  fails `check_provenance.py`), and a macron city in its slug map (Ōita).
- Each privacy-verdict row's heading column must equal its drafts entry's
  heading.
- `check_provenance.py` fails on `city_master_list.md`'s built count until
  Staging moves the batch.

## Merging (the three-way protocol, 2026-10-07)

Keep both in every shared append-style file, blocks in notice-number order:
East-1, Kansai-1, Regional-1, then yours (205-214). `japan.CITIES`: East-1 at
the dict's end, Kansai-1 after "hiroshima", Regional-1 after "kochi"; choose
another spot. Regenerate `macro_facts.json`, `ring_shares.json` and
`fingerprint_marks.json` at merge rather than hand-merging. Kansai-1 adds a
`name_city` switch to `japan_step2` (call 205): baselines may gain
`name_rule_city_rows` where it withholds a row.
