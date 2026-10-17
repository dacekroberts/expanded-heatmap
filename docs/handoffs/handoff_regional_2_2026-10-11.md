# Handoff: Regional-2 to the next session in its group (2026-10-11)

Regional-2 (branch `worktree-japan-regional-2`) built all eleven cities of
its batch: Shizuoka, Kanazawa, Okazaki, Aomori, Matsue, Fuji, Matsumoto,
Tottori, Yamagata, Kure and Kurashiki (pages 258-267 and 306, notices 205-214
and 216; the whole block used). Every city is committed with a zero-drift
baseline and a privacy check of 0. Nothing is pushed: the batch lands at the
phase 2 review time. The record is
`docs/decisions_drafts/worktree-japan-regional-2.md` (the owner's Yamagata
answers, the item raised for Cleanup, the lead's parked calls, then one entry
per city with its own parked calls, proposals, registry and downstream
notes).

## State of the checks (MEASURED, `python scripts/check_all.py`, 2026-10-11)

48 of 51 pass. The three that fail:

- `check_provenance.py`: the master list's built counts (Staging moves the
  batch to Built after landing, plan change 4). Every one of the eleven
  cities reads OK.
- `check_macro_labels.py`: Fuji and Kurashiki labelled in no view (Cleanup
  builds the Japan region views, owner call 198).
- `check_line_identity.py`: one pair, Okazaki's Meitetsu Nagoya Main Line
  beside Toyota's Meitetsu Mikawa Line, both `#E80010` (parked call
  Okazaki A).

## How the batch was run (repeat it)

- **Lead plus subagents, as Regional-1.** The lead built Shizuoka, added the
  batch's eleven `japan.CITIES` and `check_personal_exposure.py` entries in
  one block, scaffolded the other ten in one commit, then ran three
  general-purpose subagents at a time, one city each. About 0.25M agent
  tokens and 12 to 18 minutes a city.
- **Subagents CAN write files outside the repo.** Each wrote its hand-back
  as sixteen small files in the session scratchpad (`docs_<slug>/`): the
  page block, the notice, the cities fields, the docs rows, the drafts
  entry. Two scratch scripts pasted them: one for the docs tables, one for
  `app/` and the drafts file. That kept the lead's context under half full
  for eleven cities. The scripts and the builders' instructions file are in
  the Regional-2 scratchpad, which does not survive the session: rewrite
  them from this description (anchors: rows above `| Hakodate (measurement)`,
  above each `## ` heading of `japan.md`, above `| **Kyoto City**`, above
  `### Berlin - `, above each `| **Germany** |` of `map_inconsistencies.md`,
  the notice above `# Berlin (notice 57)`).
- **Count the running subagents before launching one.** The lead had four
  running for a minute and stopped the newest.
- **A single small city's drift check is light work** (0.17 to 0.23 GB
  measured on eight cities): when other sessions hold the heavy-job gate's
  four slots for hours, run it ungated, one city at a time.

## Traps this batch hit (check yours for them)

1. **A builder puts the owner's email address in a hand-typed user-agent.**
   Two did, one request each (BODIK, an operator's timetable page), before
   the instruction was added. Say it in every launch prompt: the project's
   own user-agent string or none, nothing personal in a header or URL.
2. **`app/osm_notice.py` and `_OSM_STATION_NAMES` in `app/components.py`
   must both name a new Japanese city**, or `components.py` raises at import.
   Regional-1's eleven cities are in neither (found here, left for Cleanup).
3. **`record_kind` and `categories` have a fixed vocabulary**
   (`scripts/check_inconsistency_list.py`): "Permit registers", and food
   alone is "Food premises only" with `coverage: one_bucket`.
4. **Notice items must stay in number order** in `docs/data_sources.md`;
   cities finish out of order, so sort the batch's block at the end.
5. **A privacy-verdict row's heading must equal the drafts entry's heading
   word for word** (`check_privacy_verdicts.py`); four of eleven builders
   wrote a variant.
6. **A publisher replaces its file between the brief and the build.** Three
   of eleven did: Shizuoka gained September files (taken, as its brief
   says), Matsumoto's registers moved to 2026-10-01 (taken, parked for
   confirmation), Yamagata's food list moved to September (not taken; on the
   city watch by the owner's call).
7. **A brief's "shared code" item may not be in shared code.** Tottori's
   prefecture-wide address after the city name, Kurashiki's 自動販売形態 and
   Yamagata's permit match (call 182) are not. Each is parked; two stand as
   config hooks, one leaves 83 pins on the map.
8. **Every line a neighbour draws needs a registry entry before
   `check_line_identity.py` passes.** This batch registered the Aichi Loop
   Line, JR San'in, JR Kure, JR Seto-Ohashi, JR Uno Minato and the Ibara
   Line, each at the colour the built map already drew.
9. **Edit the registry by hand, not with a repeated `sed`:** a second
   substitution on the same line committed a syntax error for a few minutes.

## Not done (for review time)

- No browser check of any map's opening view (`scripts/check_map_view.js`)
  or label placement. Builders read the baked bounds from the HTML for Kure,
  Fuji, Matsue and Matsumoto (the stations' extent, not the N03 polygon);
  Shizuoka's and Kure's extents are the ones to look at first.
- `deploy-verify` (scope `city-added`) for the eleven pages.
- Notice 1's long sentence in `app/components.py` does not name this
  batch's cities (nor Kansai-1's or Regional-1's); each page's own OSM line
  does.
- The macro label widths for the seven cities not measured ahead are in
  `app/label_competition.py` (five controls reproduced).

## Merging (the three-way protocol)

Keep both in every shared append-style file, blocks in notice-number order:
East-2 (187-197), Kansai-2 (198-204), then Regional-2 (205-214), Kansai-2's
Cluj-Napoca (215), Kurashiki (216). `japan.CITIES`: Regional-2's block sits
after "morioka". `check_personal_exposure.py`: after Regional-1's block.
`pipeline/line_registry.py`: this branch adds six entries at the dict's end
and `maps` keys to four existing entries; another branch's edits to the same
`maps` lines are keep-both by hand. Regenerate `macro_facts.json`,
`ring_shares.json`, `fingerprint_marks.json`, the README list and
`rendered_surfaces.md` at merge rather than hand-merging.
