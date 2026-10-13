### 2026-10-13 - Several regional extracts read as one (branch multi-region)

- **Built the owner's "proper fix" for a search area that crosses a region
  border: the reader takes the few small regions that together cover the
  area and reads them as one.** `osm_extract.choose_regions` keeps ONE region
  whenever one covers the area and either nothing else meets it or its file
  is under the cap; otherwise it takes the smallest set by total bytes, at
  most four regions (`SET_MAX_REGIONS`), each under the cap. Sizes come from
  HEAD requests, so nothing is downloaded to learn a size. Rejected: raising
  the cap to the parent region (us-northeast is 1,803,892,540 bytes for a
  city that needs 512,803,904), and merging files on disk with a second tool
  (a new dependency and a second copy of the data). Four was chosen as the
  limit because Philadelphia needs two and no measured city more than two;
  an area needing five is nearer a country than a city and is left for a
  person. Files: `pipeline/osm_extract.py`, `pipeline/place_extract_fetch.py`,
  `scripts/place_search_area_lookup.py`.
- **Decided a set must be ONE snapshot, bound 0 seconds
  (`SET_MAX_SPREAD_S`).** Measured on the 23 extracts held that day: every
  file of one daily run states the same timestamp to the second (19 at
  2026-10-12T20:21:35Z, 4 at 2026-10-08T20:21:06Z), and two runs are a day
  apart, so no bound between zero and a day separates anything. A day was
  rejected because an object moved across the cut between two snapshots can
  be in neither file, which no comparison of copies detects. `download_set`
  therefore completes a set at the date most of it is already held at (the
  server keeps several days of dated files), which is also the fewest
  downloads; every file still goes through `download_extract`, one at a
  time, never one in the ledger.
- **Decided what to do with two copies of one object, and refused to guess.**
  An extract keeps whole every way and relation that crosses its cut, so the
  files of a set overlap. Equal copies: the first is kept. A copy holding
  fewer of its nodes' positions: the fuller one, since a cut-short copy is
  incomplete, not different. Two full copies that differ: the read stops and
  names the object and both files (`osm_extract._Once`). Rejected: taking the
  higher version, because files of one snapshot cannot differ and a
  difference means the set is not what its timestamps claim. On the real
  files every shared object was an equal copy: 122 for Philadelphia (63
  boundary member ways, 35 ways, 20 relations, 2 nodes, the boundary relation
  and one member node).
- **Proved the set on Philadelphia with real files, and found the second
  file added nothing.** us/new-jersey (164,191,466 bytes) + us/pennsylvania
  (348,612,438), both dated 261012. The outline assembled from the two files
  equals the Overpass outline cache on disk (relation 188022, 168 members,
  geometry, tags and bounds identical; Overpass data 2026-10-13T06:19:51Z).
  The answer was 27,683 street ways, 153,170 street nodes, 3,420 tagged
  elements and 458 extra. Read from pennsylvania ALONE with the scope checks
  off, the answer is the same, byte for byte: the 0.0002% of the area inside
  New Jersey's polygon is river. **The acceptance bar set for this work,
  nothing in the Overpass answer missing from the set's, was NOT tested for
  the two place caches: Philadelphia has no Overpass place cache on disk
  (only its outline), us-northeast was not on disk, and no Overpass request
  was allowed.** 346.8 s with both downloads, peak 1,625 MB (pennsylvania
  alone: 118 s, 1.05 GB); the Korean sets peaked at 2,136 MB after a first
  try in the same process (south-korea alone: 0.97 GB). A set's memory is
  more than its largest file's alone; the cause was not looked into.
- **Found Washington D.C. is not a multi-region city under its current
  config.** `PLACE_AREA` on branch search-wave1 is the District's relation
  alone (162069), which us/district-of-columbia (21,028,680 bytes, held
  since another session's download) covers by itself; Maryland's and
  Virginia's polygons overlap it by 0.5% and 4.0% but the one region is under
  the cap, so it is taken. The changed reader's answer from that file is
  byte-equal to the caches the unchanged code wrote that day (16,074 street
  ways, 113,347 street nodes, 1,892 tagged, 630 extra): the single-region
  path did not move. A regional D.C. area with Maryland and Virginia
  municipalities would be a three-file set (not downloaded, not tested).
- **Decided an area reaching past its region's polygon is one of two cases,
  told apart by the index (asked for by the rollout session after Gimpo and
  Incheon stopped).** The part outside lies in ANOTHER region: that region
  joins the set, however small the part. The part lies in NO other region
  (open sea): the region is accepted as water-side overflow when the part is
  at most 1% of the area (`OVERFLOW_MAX_SHARE`) and every boundary closed
  from the files read; the size is printed and recorded in the cache's
  source line and `_extract.stats.overflow`. A region larger than the one
  read (its country, its continent) does not count as "another region".
  Measured: Gimpo 0.04 km2 outside south-korea (0.014% of 294.8 km2) and
  Incheon 8.82 km2 (0.089% of 9,906.4 km2), and BOTH lie inside north-korea's
  polygon (the Han estuary), so both are sets, not overflow: north-korea
  (92,675,862 bytes, downloaded once) + south-korea (held). Gimpo: 4,904
  street ways, 75,007 street nodes, 422 tagged, 136 extra, 21 objects in both
  files, all equal. Incheon: 15,971 street ways, 126,760 street nodes, 2,508
  tagged, 529 extra, 98 in both files, all equal. Neither city has an
  Overpass place cache, so counts only; each set's answer equals
  south-korea's alone byte for byte (scope checks off). One percent is
  ten times the largest measured mismatch; **no overflow over open sea has
  been measured, so the bound is untested on a real city** and is to be
  re-measured on the first one accepted.
- **Decided the command chooses again, once, when the region was chosen from
  stations and the area then read reaches into another region.** Without an
  outline cache the area is unknown until the boundary is read; the run
  stops with `AreaPastRegion` and `place_extract_fetch.cli` repeats the
  choice from the area as read. Rejected: probing every city's boundary
  before choosing (a cost on every city for a rare case). Gimpo's first try
  cost 10.7 s.
- **Added the refusal the rollout session asked for: a cache KEPT on disk is
  held to the current `config.PLACE_AREA`.** The area comes from the cache's
  provenance entry when that entry names the file, else from the query the
  cache carries; ids in another order are the same area. A different area
  exits non-zero naming both, before anything is written; a cache recording
  no area is kept with a printed warning.
- **Changed the area lookup: a city whose stations span two regions is read
  from the set, where it was left for a person.** It uses the same
  `choose_regions`; a relation cut at one file's edge is whole across the
  set. This also means a city spanning regions is now answered from its one
  covering region when that file is under the cap, which the earlier rule
  ("never from a file with subregions") did not allow. The lookup's cap is
  1000 MB, as the fetch's (raised on search-rollout the same night).
