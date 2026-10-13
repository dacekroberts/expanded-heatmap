### 2026-10-13 - Shared-border streets (branch shared-border)

- **Built the shared-border rule in the extract route only, as a named
  option that is off by default, and turned it on for street ways.**
  `osm_extract.query(shared_borders=[union names])` admits, into the unions
  named, an element that fails every single-boundary test and passes rule 3
  against the boundaries taken together (their union, holes kept).
  `place_extract_fetch.SHARED_BORDER_UNIONS = ("streets",)` is the one
  switch; `--overpass-exact` turns it off for a run. The main cache's
  `_extract.shared_border` block lists every way admitted with the two
  municipalities it lies between, and the provenance entry's `how` repeats
  the count. Rejected: testing the union for every element (the
  prototype's form), because the default must stay the proven Overpass
  answer and a caller must be able to list what the departure added.
  Selftest cases in both files: a border between two included areas in;
  the outer edge out; a border with an area not included out; the edge of
  a hole out, and in once an included area fills the hole. With the option
  off Seattle's main cache is byte-identical to the proof's
  (`data/_osm_extracts/build_test/seattle/`).
- **Left the Overpass route as it is: a city fetched by
  `place_index_fetch.py` does not have these ways.** No query was changed.
  An Overpass-side equivalent would be one more query per
  multi-municipality city (the named highway ways around the boundaries'
  member ways at distance 0, with their nodes), filtered on this machine by
  the same union test, merged into the main cache, mirrored by a new shape
  in `place_extract_fetch.py` and proven again. Not built: the owner's call.
- **Measured on six built cities, every changed row listed in
  `data/_place_rules_2026-10-13/shared_border/report.md` and
  `report.json`; no cache, index or map of any city was written.** Each
  extract was read twice into scratch (rule off, rule on) and the index
  built from each in memory. Seattle (11 municipalities, washington-261008):
  59 ways admitted beside 47,810, all of six real streets (148th Avenue
  Northeast 38 ways between Redmond and Bellevue, South 43rd Street 6,
  International Boulevard 5, 42nd Avenue South 5, South 164th Street 3 and
  68th Avenue South 2); none private, none dropped by the index's own
  rules. Index rows 13,426 to 13,426: 1 street row added (South 43rd
  Street), 2 extended (68th Avenue South, South 164th Street), 1 alias
  gained (International Boulevard: State Route 99), and 1 row removed
  because the admitted ways join two fragments of South 164th Street into
  one row. Intersections 27,702 to 27,724: 22 added, 4 moved by 7.5 to 15
  m, none removed. Vancouver (5 municipalities, southcoast-admreg-261012):
  1 way of 6 m (Tenth Avenue, New Westminster and Burnaby), no row changed,
  one drawn line longer. Tokyo (23 municipalities, kanto-261012): 0 ways.
  Kyoto, Brussels and Tbilisi (one municipality each): 0 ways and identical
  elements, as the rule gives by construction.
- **Measured the tagged unions and left them off: the only elements on
  shared borders are river ways.** With the rule on for the main and extra
  queries as well it would admit 1 element in Seattle (Green River, Tukwila
  and Kent), 4 in Vancouver (Brunette River 3, Fraser River North Arm 1) and
  17 in Tokyo (旧中川, all 17), every one `waterway=river`, and nothing from
  the extra query. Whether any of those rivers lacks a row today was not
  measured. Adding `"main"` to `SHARED_BORDER_UNIONS` is a one-word change
  for the owner to decide.
- **Did not measure Montreal or Mexico City.** Montreal's smallest covering
  region (quebec-261012, 1,161,775,276 bytes) is over the script's 1,000 MB
  limit and was refused before its body was read; the limit is a person's
  call and was not raised. Two regions were downloaded once each through
  `osm_extract.download_extract` (southcoast-admreg-261012, 116,610,620
  bytes; kanto-261012, 518,862,268 bytes).
- **PROPOSAL for review time (a row for `docs/place_search_exclusions.md`,
  which is not on this branch):** "Streets on a border between two searched
  municipalities | In when the city's places were read from a regional
  extract; missing when they were read from Overpass, which returns a way
  only when it is inside one municipality | Seattle: 59 ways of six
  streets". Also changed: the `osm-extract` and `place-search-city` skills
  and `docs/commands.md`, one paragraph each.

### 2026-10-13 - Place search from regional extracts (branch place-extract)

- **Built the extract route as two files: a general reader and this project's
  caller.** `pipeline/osm_extract.py` holds everything another project could
  lift (region choice from the server's `index-v1.json`, the download and its
  conduct, area polygons with holes, the area tests, a parser for Overpass
  union statements, the three-pass read, Overpass's output shapes);
  `pipeline/place_extract_fetch.py` reads `place_index_fetch.py`'s three
  queries as written and writes the three place caches. Rejected: a second
  copy of the query as Python predicates (the prototype's form), because a
  union line changed in one file would not reach the other. The caller
  instead parses the union text and exits when a query's shape outside its
  union changes. `scripts/place_extract_compare.py` is the proof's report.
- **Proved it with the production code on four cities, extracts dated
  2026-10-08T20:21Z against Overpass caches of the same day.** Tbilisi:
  13,229 street ways, 79,174 street nodes and 2,218 tagged elements identical
  in id, tags, node lists and position; index 5,686 rows identical. Seattle
  (11 municipalities): 47,809 of 47,810 street ways identical, 2 tag
  differences both edited after the Overpass date (node/29546940 at 09:47Z,
  way/521303400 at 18:20Z), 2 objects only in the extract. Brussels: 5,752
  street ways and 1,389 tagged elements identical, 2 ways only in the
  extract. Kyoto (area by tag filter): 5,739 street ways and 13,570 tagged
  elements identical apart from 3 tag edits dated after the Overpass date, 2
  ways only in the extract, one of them edited at 17:52Z. No element of any
  Overpass answer was absent from the extract's.
- **Found the cause class of the unexplained objects, not the mechanism, and
  did not tune for them.** Five unedited objects in four cities are in the
  extract's answer and not Overpass's, and every one lies on the boundary:
  Seattle's way/428075842 has one node 3.6 mm inside Kent's line (under the
  1e-7 degree grid) and three on it; way/32544404 shares 16 of 19 nodes with
  Redmond's boundary and cuts up to 2.5 m inside between two of them;
  Brussels' way/14193701 clips a corner for 2 cm with every node outside and
  way/35272078 runs 0.3 m inside between boundary nodes; Kyoto's
  way/45249938 runs 32 m through a corner with all 17 nodes outside. No
  boundary way, node or relation of Seattle's eleven was edited after
  Overpass's areas date (2026-10-07T10:19Z), which rules out the
  edited-boundary reading. Of the 12 street ways the line test alone admits
  in the four cities Overpass returned 9, and neither length inside nor
  depth separates the 9 from the 3 (1.7 m inside returned, 32 m not), so no
  threshold was added. How Overpass decides these is not established.
- **Changed rule 5 on a measured difference: a center's latitude is averaged
  the way Overpass holds it.** The prototype's comparison allowed 1.5e-7
  degrees and so hid that `round((lo + hi) / 2, 7)` printed 121 of Tbilisi's
  772 center latitudes one last digit off (389 of the 772 are exact halves in
  the 8th decimal). Averaging latitudes as doubles offset by 91 degrees, and
  longitudes plainly, matched all 772; it then matched every center of
  Seattle, Brussels and Kyoto with no further change. The reason given for
  the offset (Overpass's stored form) is from memory of its source, not read
  today.
- **Chose ascending id as the one written order, and measured what it does to
  the index.** Street ways, their nodes, then nodes, ways and relations, each
  by id. Overpass's `qt` order is not reproduced. Re-ordering the Overpass
  caches themselves this way changes 0 of Tbilisi's 5,686 rows, 5 of
  Seattle's 13,426 (which of two same-name landmark ways is kept), 0 of
  Brussels' 2,059 and 158 of Kyoto's 9,331 (155 junctions whose English
  alias comes from a differently capitalised street name, 3 landmarks). A
  city refetched by the extract route will therefore show such rows as
  changed against its Overpass-built index.
- **Decided what the fetch does with caches and provenance.** A cache on disk
  is never written over without `--force`, whoever wrote it, and a kept
  cache's provenance entry is left as it was rather than re-recorded as
  kept. `--out DIR` writes all three elsewhere and records nothing (the
  proof's route). `PLACE_SPLIT` is unused and said so. `PLACE_AREA` as tag
  filters is answered from boundary and multipolygon relations only; an
  area made from a closed way is taken by its id (2400000000 + the way's
  id) and outlined as a way with geometry; a relation's own tags are never
  consulted when it is named by id.
- **Set the download's conduct in code, with no override.** A dated file once
  downloaded and since removed is refused by a ledger
  (`data/_osm_extracts/downloads.json`); the only way past is to edit the
  ledger by hand. One download at a time on the machine
  (`osm_extract.DownloadLock`), so two runs sharing a regional file are
  safe. Defaults: `place_extract_fetch.py --max-mb 1000`, the lookup's
  `--max-mb 800`. Updating a region by diffs is not built.
- **Gave the area lookup a second source, and left Overpass the default.**
  `scripts/place_search_area_lookup.py --source extract` reads
  `osm_extract.boundaries_holding` from the smallest region holding all of a
  city's stations; a city whose smallest covering region has subregions is
  left for a person. A held extract of any age is used. A relation the
  extract holds only part of (the country, sometimes the state) is not
  answered and is listed in the cache. Added `--cache-root` so a trial
  leaves a city's raw folder untouched; the proof's caches are under
  `data/_osm_extracts/build_test/lookup/`, none under any `data/<city>/raw/`.
- **Confirmed both official-code tag keys on real data.** `ref:INSEE` tied
  Strasbourg (67482) and Mulhouse (68224) in alsace-261012; `IBGE:GEOCODIGO`
  tied Porto Alegre (4314902) in sul-261012, and the six relations chosen
  carry exactly the six codes of that config's `SCOPE_CODES`. Each key was
  checked in one region only. Belgian municipalities carry `ref:INS` (Antwerp
  11002, Liège 62063, equal to those configs' NIS codes): not added to
  `CODE_TAGS`, a change for the owner.
- **Lookup results on eight cities with no search, all right by their own
  configs:** Tacoma (relation 8348295, level 8), Kobe (900329, level 7,
  `MUNICIPALITY`), Otsu (722196), Antwerp (59518), Liège (1681788),
  Strasbourg (71033), Mulhouse (38246), Porto Alegre and its five neighbors
  (242397, 242399, 242471, 242574, 242616, 242778). On built cities the
  returned set held every relation `PLACE_AREA` names (Tbilisi 1 of 1,
  Seattle 11 of 11, Brussels 1 of 1, Kyoto 1 of 1). Brussels' stations also
  sit in Ixelles and Saint-Josse-ten-Noode at level 8, which its
  `PLACE_AREA` does not name: for the owner, not changed.
- **Did not call DeepSeek.** The `deepseek-delegate` skill requires the
  owner's yes before every call to its wrapper, and a build agent cannot
  obtain one. The offline compatibility check passed (claude 2.1.296, 9 of 9
  settings). Nothing was sent.
- **PROPOSAL for review time (a reference-doc sentence no template covers):**
  the bullet "A second route to the same OpenStreetMap data: regional
  extracts from download.geofabrik.de" added to `docs/data_sources.md`'s
  place search section, written from the 2026-10-13 licence read. Also new:
  the `osm-extract` skill and the alternative named in `place-search-city`
  step 3, which does not make the extract route the default.
