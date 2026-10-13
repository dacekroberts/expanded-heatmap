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
