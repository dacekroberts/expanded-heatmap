# Handoff: East-1 to East-2 (2026-10-07)

East-1 built its twelve cities on branch `worktree-japan-east-1`, committed,
nothing pushed: Higashiyamato, Nishitōkyō, Tama, Higashimurayama (Tama
ledgers); Ageo (Regional), Sōka, Tokorozawa, Kasukabe (Saitama Prefecture's
lists); Fuchū (Tokyo), Chōfu, Tachikawa, Hino (Tama ledgers). Pages 210-221 and
notices 157-168 are all used. Every figure, judgment and parked call is in
`docs/decisions_drafts/worktree-japan-east-1.md`; this note is what the next
Japan session needs that the drafts file does not say.

## What East-1 left in shared code (lands with East-1)

- `pipeline/countries/tokyo_tama.py`: the Tama ledgers' leg (five ledgers plus
  MHLW's 13000 file), the cut by address prefix (raises on the city's name
  elsewhere, skips multi-city areas, reads a doubled 東京都), the call-109
  column drop, the catalogue credit.
- `pipeline/countries/saitama_pref.py`: Saitama Prefecture's leg (the live GIS
  layers read with their points, the R8.3.31 old-law list under call 171, the
  生活衛生 lists per health centre plus months, the cut by address, its own
  paged fetch). A one-city page passes `(MUNICIPALITY,)`; never add
  "municipalities" to `japan.CITIES` for one city. Koshigaya and Kawaguchi
  are health-centre cities with their own lists: read their briefs before
  assuming this module applies.
- `pipeline/countries/japan_official.py`: the yearbook's Tama rows and table
  19-7 (`registers()`).
- `pipeline/countries/japan_step2.py`: opt-in `SHARE_DATES` (the share at the
  official count's date, calls 187-189) and `REGISTER_SHARES`. Built cities
  unchanged (all 34 re-run read-only, byte for byte).

## How the batch was run (about 12 cities in one sitting)

- **Lead first, subagents second.** The lead added each `japan.CITIES` entry,
  scaffolded the page with its reserved number, copied the cached files into
  `data/<slug>/raw/`, set `OSM_BBOX` and ran every Overpass query itself, one
  at a time (a 504 or 429 waits 60 s; it worked on the retry each time). Then
  up to three subagents each finished one city's `pipeline/<slug>/` (rail,
  colours, steps 1-3, census control) and reported figures; they never
  touched shared files, git or Overpass. The lead wrote every doc, page and
  notice and committed city by city.
- **Committing one city while others are scaffolded:** `app/cities.py` holds
  every scaffolded entry, and a page whose pipeline is uncommitted breaks the
  clean-clone import check. Stage a copy of `cities.py` without the unbuilt
  entries (`git hash-object -w <copy>`, then `git update-index --cacheinfo
  100644,<hash>,app/cities.py`), leaving the working file whole.
- **Worktree setup:** the new worktree had no `data/` junction; create it
  (`New-Item -ItemType Junction -Path data -Target <main checkout>\data`) and
  build `.venv-lean` before the import check.
- **`check_deploy_imports.py` crashes on a macron in a commit subject**
  (cp1252): run it as `PYTHONUTF8=1 python scripts/check_deploy_imports.py`.
- **At the batch's end**, in this order: `fingerprint.py table` (adds the new
  maps' and pages' marks; the owner's key is on this machine and is never
  printed), re-render each new map (step 3), `check_ring_shares.py --write`,
  `check_macro_facts.py --write`, `readme_cities.py`, `rendered_surfaces.py
  --write`, rows in all four tables of `docs/map_inconsistencies.md`. Check
  each `--write` diff touches only your cities.
- **Expected failures, not yours to fix:** `check_provenance.py` on the master
  list's built counts (Staging moves cities to Built after landing, plan
  change 4) and `check_macro_labels.py` on the new cities' label widths
  (Cleanup builds Japan's region views and labels, owner call 198). Everything
  else in `check_all.py` is green on East-1's branch.

## Traps the twelve cities found

- **The shares the page states are read from `outputs/<slug>/official_shares.json`**
  (the page code reads it), never typed. Leave notifications out of the
  restaurant share (`SHARE_SKIP`): a notification typed 飲食 is a stall.
- **MHLW's rows match far more ledger premises than the briefs estimated**
  (`SUPERSEDES` keys on town, block, trade name and bucket after the join):
  expect MHLW to add tens of pins, not hundreds.
- **An interchange N02 collapses across the city line** (a platform 16-32 m
  outside) makes a line's in-city count exceed the operator's: leave that line
  out of `GATE3` with a comment.
- **Two different stations 38 m apart** (Tama's Keio and Odakyu pairs) make gate
  1 read "still platforms": `SPACING_MIN_M` (Tbilisi's precedent) and the
  spacing rule read by place.
- **A city tip just outside the fetched OSM box** stops step 1: widen
  `CITY_BBOX` only (Fuchū), never re-query.
- **Lines leaving the prefecture** need `N03_NEIGHBOR_PREFS` ("13", "14", "11",
  "12").
- **Call 171 with call 172:** a late-starting new-law permit is often the
  renewal of an old-law permit still in term; `saitama_pref` drops an old-law
  row as renewed only where its twin is in term on the as-of, so the premises
  shows once. Never key old-law permits on the number alone (one number names
  two premises 26 times in Ageo and Ina, 8 in Kasukabe).

## Open for the owner (parked calls 1-5 in the drafts file)

1. Line colours where one operator colour covers several lines (Seibu, the New
   Shuttle, Tobu's Urban Park Line): set B recommended.
2. The excluded-station reason on a two-municipality page (shared step 1).
3. The Leo Liner's on-map label.
4. A publisher point refused as a default when one premises' address is
   written several ways (shared `own_point_fallback`; Kasukabe's AEON Mall).
5. "JR Chuo Line" against Tokyo's "JR Chuo Line (Rapid)".

Also for review time: the label checks the subagents could not render (the
Haijima stub, the Dobutsuen branch, the Chuo and Ome stubs at Tachikawa,
Higashi-Tokorozawa's stub), a blank trade name showing a blank pin label (10
pins across five Tama cities), and the merge with Kansai-1 and Regional-1:
keep both at every shared anchor, East-1's block first, then Kansai-1's, then
Regional-1's (notice-number order); regenerate the JSONs rather than merging
them by hand.
