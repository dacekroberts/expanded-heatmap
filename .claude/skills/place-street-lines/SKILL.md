---
name: place-street-lines
description: A searched street drawn at its whole length on the map - the street lines side file the index step writes (app/static/places/streets/<city>.json), how a line is built from OpenStreetMap ways, the file's format, what the browser does with it, the ring that stays when no line can be drawn, what "the whole street" does and does not mean, the sizes measured on the 19 built cities, the check that holds a file to its index, and the browser test. Use in every place search rollout wave (each new searched city gets the file from its index step and one street picked in the browser test), before changing STREET_SIMPLIFY_M, chain_ways, street_lines or the search script's loadStreets, and when a reader reports a street drawn short, broken or on the wrong road. Not for adding search to a city (place-search-city), and not for transit lines (osm-rail, line_registry).
---

# A searched street's whole length

Built 2026-10-13 on the owner's ask ("can we make searching a street without
an intersection show the whole length of the street?"), on top of the place
search of `place-search-city`. Read that skill first for the index itself.
The reasoning is in `DECISIONS.md`, 2026-10-13, "A picked street is drawn at
its whole length".

## What it does

Picking a street from the search zooms to the street's extent, as before, and
then draws the street as a line in the search ring's two colours. The ring
gives way to the line; the name label stays at the street's anchor point.
The line goes when the marker goes (12 seconds, or the next search).

**The ring is the failsafe (owner, 2026-10-13: "ring where line is not
possible is a good failsafe").** The ring is drawn first, at once, and is
hidden only when a line is actually on the map. So the ring stays when:

- the index names no street file (a city built before this, or a map opened
  outside the site),
- the file's fetch fails (not retried in that page view),
- the street's row has no line in the file.

Never make the line a precondition of the marker, and never hide the ring
before the line is added.

## The pieces

| What | Where |
|---|---|
| A street's ways, joined end to end | `pipeline/place_index.py`, `chain_ways()` |
| Simplify and encode | `street_lines()`, `STREET_SIMPLIFY_M = 10` |
| The file | `streets_path(slug)` = `app/static/places/streets/<slug>.json`, written by `files()` |
| Its hashed path in the index | the index's `"streets"` key |
| Fetch, decode, draw | `PLACE_SEARCH_SCRIPT` in `pipeline/map_common.py`: `loadStreets()`, the block in `go()`, `oneRowAStreet()`'s `_rows` |
| Look | CSS `path.hm-search-streetcase`, `path.hm-search-street`, `path.hm-search-hid` |
| The check | `scripts/check_place_search.py`, rule J (`check_streets`, `street_problems`) |

**No new fetch and no new source.** The lines come from the same place cache
as the street rows (`config.PLACE_OSM_JSON`): the ways are already there
with their nodes. The file is part of the same ODbL database as the index
and carries the index's licence object.

## How a line is built

1. `build()` keeps, for each street row, the ways merged into it (the same
   merge that makes the row: one name, neighbouring 2 km cells that share a
   node).
2. `chain_ways()` joins ways that share an END node, in way-id order, so a
   rebuild gives the same bytes. A divided street stays two lines; a street
   with a gap is as many lines as it has pieces; a closed way (a roundabout)
   is left whole.
3. `street_lines()` simplifies each line by `STREET_SIMPLIFY_M` **in the
   city's own projected CRS** (`config.CRS_PROJECTED`), never in degrees,
   and encodes it.

## The file's format

```
{"license": {...the index's...}, "schema": 1, "city": "...",
 "part_of": "<slug>.json", "scale": 100000,
 "rows":  [12, 15, ...],          ascending; each a street row's position in the index
 "lines": [[[line], [line]], ...] beside it: that street's polylines
}
```

A line is a flat list of integers in units of 1/`scale` degree: the first
point's latitude and longitude, then each later point as its difference from
the one before. Decoding is a running sum. This is 62% of the bytes of plain
coordinates (measured on Seattle: 820 KB against 1,328 KB).

A key added to the index is not a schema break (`SCHEMA` stays 1). A change
to a line's encoding IS one for any reader of the street file: raise
`SCHEMA` and tell the travel app's session.

## What "the whole street" means

A line is every stretch OSM names with exactly the row's name, inside the
fetched area. Say this, not "the whole street", when a reader asks:

- **It stops where the name changes.** "Pike Street" ends where "East Pike
  Street" begins. A third of Seattle's street names (3,707 of 11,117, in
  1,274 groups) share a base with a direction-word sibling. Both rows are in
  the result list; neither is merged into the other.
- **It stops at the edge of the search area** (`config.PLACE_AREA`), where
  the fetch stopped.
- **A gap is drawn as a gap** (a park, a freeway): each piece is drawn. When
  the result list has merged several rows of one name into one answer
  (`oneRowAStreet`), every one of those rows' lines is drawn.
- **OSM's own naming shows through:** a bridge or ramp under its own name
  leaves a hole. Not counted.

## Sizes, measured 2026-10-13 on the 19 built cities

The file is fetched only at the first street picked. Raw / gzipped:

- London 2,841 / 1,094 KB; Mexico City 2,732 / 997; São Paulo 2,412 / 870.
- Seoul 1,311 / 474; Montréal 1,012 / 367; Seattle 820 / 290.
- The other 13: 75 to 733 KB raw, 29 to 272 KB gzipped.
- All 19: 15.6 MB raw, 5.8 MB gzipped (the 19 indexes: 26.3 and 6.8 MB).

The file can be larger than its index (Montréal, Barcelona: many divided and
curved streets). A coarser `STREET_SIMPLIFY_M` of 20 saved about 12% on
Seattle. **Re-measure all built cities if the constant or the encoding
changes**, and report the three largest to the owner before landing.

254,000 street rows; 11 have no line (one each in London, Mexico City,
Seoul, Barcelona, Paris, Marseille and Brussels, four in São Paulo): the
simplification left under two points. They keep the ring.

## In a rollout wave

Nothing extra is fetched. For each new searched city:

1. The index step (`step2b_place_index.py`) writes the street file with the
   index. Commit `app/static/places/streets/<city>.json` with the index.
2. In the wave's size table, add the street file's raw and gzipped size
   beside the index's. Bring any file over London's to the owner.
3. `python scripts/check_place_search.py`: rule J must pass (the index names
   the file under its current hash; every line lies inside its street row's
   own extent). `scripts/check_place_index_drift.py` compares the file too,
   since it compares everything `files()` returns.
4. In the wave's one browser test, pick ONE street on one city of the wave
   and confirm, by reading the page and not by eye alone:
   `path.hm-search-street` exists, the ring's two paths carry
   `hm-search-hid`, and the label is still shown. Then block the street
   file's URL (or test a city whose index has no `streets` key) and confirm
   the ring stays.
5. A city built before this feature has no `streets` key and shows the ring.
   Rebuilding its index adds the key, which changes the index's bytes: its
   map must be re-rendered and its `place_ids.json` is rewritten (the usual
   rule-change protocol in `place-search-city`).

## Traps

- **A fill on a polyline.** The ring's class (`hm-search-ring`) sets a fill
  in CSS, which overrides Leaflet's `fill: false`. The street uses classes
  of its own with `fill: none`. Do not reuse the ring's classes for a line.
- **A slow file landing on a later search.** `go()` keeps the marker it made
  (`mine`) and draws only if `marker === mine` when the file arrives.
- **`getIndex()`, never a bare `fetch`:** the deployed app is served under a
  path prefix; rule I of the check refuses a bare URL.
- **Rows are positions in the index.** The street file and the index must
  come from one run of the step; the hash in the index's `streets` key is
  what ties them. Never hand-edit either.
- **The measure in degrees.** Simplifying in EPSG:4326 is refused by the
  project's invariants; pass the city's CRS.

## The owner's calls (2026-10-13)

- **The line's colour is the ring's teal** ("ring teal is good, stands
  out"). Not a white-cased dark line: that is a picked TRANSIT line's look.
- **The credit carries a third link, "streets"**, beside "download" and
  "intersections", in the bottom line and in the box form alike. It shows
  once the index has named the file. The three files are one ODbL database
  (`docs/data_sources.md`, "Place search index", Access).
- **10 m everywhere.** The owner gave the word to rebuild after seeing the
  three largest files' sizes; 20 m was offered and not asked for.
- **Built in each batch, never at the end:** the file comes out of the index
  step a wave already runs. Adding it afterwards means rebuilding and
  re-rendering every index a second time.
