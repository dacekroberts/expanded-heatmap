# Handoff: Kansai-2 (2026-10-11)

Kansai-2 built its seven Japanese cities and Cluj-Napoca on branch
`worktree-japan-kansai-2` (worktree `.claude/worktrees/japan-kansai-2`),
committed, nothing pushed; it lands at the phase 2 review time. Phase 2 is
the last build wave, so this note is for whoever lands the branch (Cleanup),
or builds the next Kansai or Romanian city. Every claim is labeled.

## What is on the branch

| City | Page | Notice | Storefronts | Stations | Source |
|---|---|---|---|---|---|
| Ibaraki (Osaka) | 251 | 198 | 621 | 10 | Osaka Prefecture's barber and beauty lists, cut by address |
| Minoh | 252 | 199 | 294 | 5 | the same lists |
| Moriguchi | 253 | 200 | 375 | 6 | the same lists |
| Kadoma | 254 | 201 | 334 | 5 | the same lists |
| Neyagawa | 255 | 202 | 630 | 4 | the city's barber, beauty and laundry lists |
| Yao | 256 | 203 | 1,956 | 11 | MHLW's file alone, food only |
| Takatsuki | 257 | 204 | 1,922 | 5 | MHLW's file alone, food only |
| Cluj-Napoca | 305 | 215 | 3,801 | 20 | DSVSA Cluj's county lists, food only |

All MEASURED 2026-10-11 by each city's steps; `python pipeline/drift_check.py
<slug>` reports zero drift for all eight and each has a `baseline.json`.

**`python scripts/check_all.py`: 48 of 51.** The three left are not this
branch's to fix (MEASURED): `fingerprint.py coverage` (the owner's key marks
no new map), `check_macro_labels.py` (Minoh labelled in no view: region views
are Cleanup's, call 198), `check_provenance.py` (only the master list's
counts, Staging's: Built 206 against 214, Europe 21 against 22, Osaka
Prefecture 6 against 13).

## For the landing

- **Parked calls** are in `docs/decisions_drafts/worktree-japan-kansai-2.md`,
  with recommendations: Osaka A (Osaka's map still labels three Osaka Metro
  lines by their short names), Batch B (page sentences no template covers),
  Batch C (label widths, done), Cluj A to E.
- **Cluj-Napoca's terms question is closed** (Cluj A): DSVSA Cluj's site
  read SILENT, as Bucharest's; the owner ruled on 2026-10-11 to treat it as
  Bucharest and publish under notice 215 (ANSVSA's site read the same day),
  so the question is closed.
- **Shared code this branch changed** (MEASURED controls in the drafts):
  - `pipeline/line_registry.py`: four lines entered in the colours a built
    map already drew (Saito, Tanimachi, Imazatosuji, Nagahori
    Tsurumi-ryokuchi), and the new cities added to seven lines' `maps`.
    `pipeline/suita/config.py` and `pipeline/osaka/config.py` now read those
    four from the registry: the values are identical (checked by import), but
    **neither city's steps were re-run** (the shared `data/` rule), so their
    drift check is owed at the landing.
  - `pipeline/taxonomies/romania_dsvsa.py`: roles by file name, the county
    exclusions, the name rule's extensions. Bucharest's 36,403 rows classify
    identically (read-only control); its drift check is owed at the landing.
  - `pipeline/osm_tram.py`: `name_members`. `scripts/osm_tram_control.py`
    passes.
  - `scripts/category_continuity_table.py`: romania_dsvsa's column gained the
    pharmacy, canteen, stall and itinerant-unit rows. `check_category_continuity`
    passes with its self-test.
  - `app/label_competition.py`: four measured widths (eight controls
    reproduced).
- **Merge notes**: `app/cities.py`, `app/components.py`, `app/osm_notice.py`,
  `pipeline/countries/japan.py`, `scripts/check_personal_exposure.py`,
  `scripts/check_provenance.py`, `scripts/stress_overview.py`,
  `docs/data_sources*.md`, `docs/excluded_categories.md`,
  `docs/map_inconsistencies.md` and `docs/privacy_verdicts.md` all conflict
  keep-both with East-2 and Regional-2; keep both sides at
  `japan_register.OPERATOR_COLS_WAVE5` and the WAVE5 switches (this branch
  did not touch them). Run `python scripts/regen_generated.py` after the
  merge. `docs/session_roles.md`'s number ranges still list Kansai-2's
  (198-204, 215; pages 251-257, 305): delete them when it lands.

## Traps this batch measured

1. **A prefecture's list cut by address is a config, not code**: Ibaraki's
   `config.py` is the template for the other three (the same twelve files,
   copied from `data/osaka_pref/raw/`). The briefs' counts reproduced exactly.
2. **`line_colour_search.py <city>` reads one map.** For a line new to the
   site it returned the colour a neighbouring map's line already has (Minoh's
   line got the Hankyu Takarazuka Line's). Check the registry's colours within
   2 km before accepting it (the neighbour rule).
3. **One N02 station group can straddle the city line** (Moriguchi's
   太子橋今市: one subway line's platform inside, the other's 30 m outside).
   The collapse keeps one station carrying both lines; set gate 3 by group and
   say so in the config.
4. **Six real stations on 12.7 km² fail gate 1's 400 m floor** (Moriguchi,
   median 371 m): set `SPACING_MIN_M` with the pairs cited, never loosen the
   collapse.
5. **A brief's `OSM_BBOX` can cut the city** (Kadoma): step 1 stops; widen
   from the N03 extent and re-fetch the names with `--force`.
6. **A brief written before the foundation under-counts the join** (Kadoma:
   10 unplaced in the brief, 5 at the build).
7. **Overpass refused about one query in three** (504 on overpass-api.de,
   500 on the mirror); a second run after the 60 s wait always answered.
8. **BODIK**: one `package_search` per city answered every time; running
   `brief_check.py` twice in a row is two calls seconds apart (a slip here,
   no block followed).
9. **Romania**: read `.claude/skills/romania-city/SKILL.md`. The one that
   costs most if missed: a county's file numbers are its own.

## Naha's measurement

See the entry "Naha's one measurement" in the drafts file.
