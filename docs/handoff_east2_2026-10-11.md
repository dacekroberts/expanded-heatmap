# Handoff: East-2 to the next Japan session (2026-10-11)

East-2 built its eleven cities on branch `worktree-japan-east-2`, committed,
nothing pushed: Koshigaya, Sagamihara, Fujisawa (A); Kawaguchi, Funabashi,
Matsudo, Ichikawa, Urayasu, Sakura, Yachiyo, Ichihara (B). Pages 240-250 and
notices 187-197 are all used. Every figure, judgment and parked call is in
`docs/decisions_drafts/worktree-japan-east-2.md`; this note is what the next
Japan session needs that the drafts file does not say. Claims are MEASURED
unless marked ASSERTED.

## What East-2 left in shared code (lands with East-2)

- `pipeline/countries/chiba_pref.py`: Chiba Prefecture's 環境衛生関係施設一覧
  (dataset 6, PDL 1.0) for every Chiba page whose health center is the
  prefecture's (not Chiba City, Funabashi or Kashiwa, which have their own).
  A page's config sets `MUNICIPALITY`, `HEALTH_CENTER` (its sheet) and
  `EXPECTED_ROWS`, and reads the rest from the module; `pipeline/matsudo/` is
  the worked example. The shared cache is `data/chiba_pref/raw/`. A seventh
  Chiba page needs its sheet added to `SHEET_AREAS` and its header checked
  (the module raises on a header it does not know).
- `pipeline/line_registry.py`: eleven new entries (Odakyu Enoshima, JR
  Yokohama, Sotetsu Izumino, JR Chuo-Sobu, JR Keiyo, Tobu Urban Park, Tozai,
  Keisei Main, Keisei Matsudo, Hokuso, Toyo Rapid Railway) and the new maps
  joined to the existing ones. Tokyo's, Yokohama's and Kasukabe's configs
  still hold literals of the same values (built cities, left for Cleanup).
- `japan.CITIES`: eleven entries, Kawaguchi's with its `"gaiji"` table.
- No change to `japan_register.py`, `japan_step1.py`, `japan_step2.py`,
  `japan_fetch.py` or the taxonomy, so the Minato control was not owed.

## How the batch was run (eleven cities in one sitting)

- **Lead first, subagents second**, as East-1: the lead added every
  `japan.CITIES` entry, scaffolded all pages in one commit, and ran every
  Overpass query itself from a scratch script, one at a time, in each city's
  N03 extent rounded out to 0.01 (Overpass answered 504 or 429 on about half
  the first tries; 60 s back-off worked every time). Then up to three
  subagents each finished one `pipeline/<slug>/` and reported figures. The
  lead wrote every page, notice and docs row and committed city by city.
- **Give each subagent a written common brief and the exact OSM box.** A
  city's `fetch_sources.py osm` run afterwards by the lead records the file
  already on disk in provenance without a network call (`osm.fetch` keeps a
  cached file).
- **A registry-first rail pass saves rework:** build the city with the most
  lines first (Funabashi), register every line a built map already draws,
  and the neighbours take their colours from the registry with nothing to
  reconcile. `check_line_identity.py` names every join still missing.
- **The docs rows are mechanical once one city is written**: the same six
  files take the same insertions per city (two rows, a transit row and a
  boundary row in `data_sources/japan.md`, the count word and notice list
  there, the notice block and the Japan row in `data_sources.md`, a section
  in `excluded_categories.md`, a privacy row, four rows in
  `map_inconsistencies.md`). `check_provenance.py` refuses an endpoint not
  written in full.
- **Worktree setup:** create the `data` and `.venv-lean` junctions first
  (`New-Item -ItemType Junction`), as East-1's note says.
- **The heavy-job gate is shared with other projects' sessions:** a drift
  check refused for a full gate is re-run with `--wait`.

## Traps the eleven cities found

- **The briefs' pin counts do not subtract unplaced rows**, and their joins
  were measured on the wave-2 rules alone: expect a few more block-tier rows
  and a pin count lower by the unplaced rows.
- **`late_start` (call 172) drops renewals already granted** where a list
  carries a first-permit date before the as-of and a term starting after it
  (Kawaguchi: 142 rows, about 90 operating restaurants). Parked.
- **A private-use glyph in a trade name renders as an empty box**:
  `map_common.glitched_name` does not flag U+E000-U+F8FF (Kawaguchi, 3
  pins). Parked; Kawaguchi does not land until it is settled.
- **A closure removes one row, not every row of its key** (Sagamihara: a
  salon that changed hands).
- **A zipped register of CSVs** needs a city `file_rows` (Sagamihara).
- **Operator-like company-name columns** (開設者名称, 営業者名称) stop step 2's
  new-city check: record them in `config.NOT_OPERATOR` behind a guard that
  every value carries a company marker, and report the spelling for the
  shared tuple.
- **OSM's English names are not always the operator's** (Bay Side Station,
  Chikucenter): an override needs a cited spelling, so they are parked rather
  than guessed.
- **Three different lines now share #20A800** (JR Joban, Toyo Rapid, JR
  Narita). Nothing collides today; the next map that draws two of them
  together moves one.

## Open for the owner and Cleanup

The parked calls in the drafts file, in order of weight: Kawaguchi B (glyphs,
holds its landing), Kawaguchi A (late-start renewals), Funabashi A (Keiyo
against Musashino, a built city's line), the station-name spellings,
Kawaguchi C (the Saitama Stadium Line's name). Also for review time: the
proposed page sentences listed there, the credit titles of notices 187 and
188, and the label checks at 343 px for the ten-line Funabashi map.
