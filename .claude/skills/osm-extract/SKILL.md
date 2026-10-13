---
name: osm-extract
description: Answer an Overpass area query from a regional OpenStreetMap extract (.osm.pbf) filtered on this machine instead of asking an Overpass mirror - when that is the better route, the five rules that make the answer equal Overpass's and how each was learned, the download server's conduct rules, the proof to run before trusting a new query to it, and the traps. Use when a city's place fetch keeps failing or queueing on the mirrors, when a wave of cities shares one region, when a lookup or fetch must run with no Overpass request, and before pointing any new Overpass query at pipeline/osm_extract.py. The general sections are written for any project that uses Overpass. Not for rail geometry (osm-rail) and not for the place index's rules (place-search-city).
---

# Answering an Overpass query from a regional extract

Built 2026-10-13, after the place search rollout spent a night waiting on two
Overpass mirrors: 504s, 429s, one query in flight per mirror, and five caches
served from data months old. A regional extract is one file download and no
queue. The question was whether a local filter gives the SAME answer. It does,
to the element, once five rules are followed, and what is left over is
measured below.

Two files, and the split is the point:

- `pipeline/osm_extract.py` is GENERAL. It knows nothing about place search:
  the region index, the download and its conduct, area polygons, the area
  tests, a parser for Overpass union statements, the three-pass read, and
  Overpass's output shapes. Another project can lift it as it stands (it
  needs pyosmium 4, shapely 2 and numpy; its one project hook is
  `_refuse_if_offline`).
- `pipeline/place_extract_fetch.py` is this project's caller: it reads the
  queries from `pipeline/place_index_fetch.py`, writes the three place caches
  and records provenance. `scripts/place_search_area_lookup.py --source
  extract` is the second caller.

## When to use an extract instead of Overpass

| Use an extract | Stay on Overpass |
|---|---|
| The query is cut by an area and returns thousands of elements (every named street of a city) | A light query: a handful of objects by id, `out tags` on a few relations |
| Several cities share one region (one download, many reads) | One small city in a region whose file is several hundred MB, asked once |
| The mirrors are refusing, queueing or serving old data | The data must be minutes fresh: an extract is a daily file |
| The run must make no Overpass request (an unattended queue beside another one) | The area's smallest covering region is country-sized (over `--max-mb`) AND no set of at most four smaller regions covers it (see "An area that crosses a region border") |

An extract costs a download of 100 to 700 MB for the regions measured, 10 to
80 s of reading and 0.9 to 2.5 GB of memory. An Overpass place fetch costs no
download and, when the mirror answers, about as long; when it does not, hours.
Which route is the DEFAULT is the owner's call; this skill describes the
second route, not a ruling.

## The five rules, and how each was learned

Each came from a measured difference between an extract's answer and an
Overpass answer of the same day. They live in `osm_extract.Area`,
`osm_extract.query` and `osm_extract.bbox_center`, and each has a selftest
case that also shows what the broken rule would have answered.

1. **Each boundary is its own area. Never test against the union.** A query
   over `area(id:A,B,C)` holds an element when it is inside A, or B, or C. A
   way lying exactly on the border that A and B share is inside neither.
   Learned on Seattle (11 municipalities): the union admitted 60 street ways
   Overpass did not return, all on shared borders.
2. **Inner rings are holes.** An enclave is not in the area. This project's
   `place_index.municipalities` ignores inner rings on purpose (it draws an
   outline), so the cut polygon is built separately
   (`osm_extract.boundary_polygon`).
3. **A way is in when one of its nodes is strictly inside, or its line passes
   through the interior.** Touching the boundary, at a point or along it, is
   not enough. "Intersects" admits every street that ends at the city line;
   "a node inside" alone drops a road that crosses a corner of the city
   between two nodes outside it.
4. **A relation is in when a member node or a member way is in by rule 3.**
   Member relations are not followed.
5. **`out center` is the middle of the bounding box**, not a centroid, at 7
   decimals, and the latitude is averaged the way Overpass holds it (an
   integer of 1e-7 degrees offset by 91 degrees). Half of all centers are an
   exact half in the 8th decimal; plain rounding printed 121 of Tbilisi's 772
   center latitudes one last digit off, and the offset form matched all 772,
   then all of Seattle's, Brussels' and Kyoto's without further change.

**Order is not reproduced, and is not meant to be.** Overpass's `qt` order
follows its own disk layout. `osm_extract.query` returns nodes, ways and
relations each by ascending id, so the same extract and query always give the
same bytes. Any consumer with order-dependent tie-breaks will break ties
differently: say so wherever that consumer is documented, and measure it (see
the proof, step A).

## The proof (2026-10-13), and what is left over

`scripts/place_extract_compare.py <city> <dir>` compares element by element,
then builds both indexes. Extracts dated 2026-10-08T20:21Z against Overpass
caches fetched the same day, production code, nothing tuned after Tbilisi:

| City (region file) | Street ways | Street nodes | Tagged elements | Only in the extract | Dated edits | Index rows differing by tie-break |
|---|---|---|---|---|---|---|
| Tbilisi (georgia, 102 MB) | 13,229 identical | 79,174 identical | 2,218 identical | 0 | 0 | 0 of 5,686 |
| Seattle, 11 municipalities (washington, 364 MB) | 47,809 identical | 292,836 identical | 3,886 identical but 2 by edits | 2 | 2 tag edits | 5 of 13,426 |
| Brussels (belgium, 696 MB) | 5,752 identical | 28,292 identical | 1,389 identical | 2 | 0 | 0 of 2,059 |
| Kyoto, area by tag filter (kansai, 353 MB) | 5,739 identical but 2 by edits | 62,725 identical | 13,570 identical but 1 by an edit | 2 | 3 tag edits, and 1 of the 2 added ways was edited after the Overpass date | 158 of 9,331 |

No element was in Overpass's answer and absent from the extract's. Every
position matched to the last decimal.

**What is left over: objects that graze the boundary.** Five objects in four
cities are in the extract's answer, were not edited, and were not in
Overpass's:

- Seattle, a street with one node 3.6 mm inside Kent's line (less than the
  1e-7 degree grid) and its other three nodes on the line.
- Seattle, a park whose outline shares 16 of 19 nodes with Redmond's
  boundary and cuts up to 2.5 m inside between two of them.
- Brussels, a street with every node outside whose line clips a corner for
  2 cm; and one with 7 of 10 nodes on the line, 0.3 m inside between them.
- Kyoto, a street with all 17 nodes outside that runs 32 m through a corner,
  1.5 m deep.

By geometry all five ARE in the area, so rule 3 is not wrong about them. Of
the 12 street ways rule 3 admits by its line test alone in the four cities,
Overpass returned 9 and not these 3, and neither length nor depth separates
the two groups (it returned one that is 1.7 m inside and not one that is 32 m
inside). **The mechanism inside Overpass is not established.** Expect one or
two boundary-grazing objects per city more than Overpass gives, and do not
tune rule 3 to remove them: any threshold that drops these also drops ways
Overpass returns.

## The proof procedure for a NEW query

Do this before any query is trusted to the extract route. Without it there is
no evidence, only a parser that did not complain.

1. Pick two built cities of different shape whose Overpass answer is on disk
   and whose data date still has a dated extract on the server (the server
   keeps several days of dated files). One with several boundaries, one with
   an enclave or a tag-filter area if the query will meet those.
2. Download each region's extract of THAT date:
   `python pipeline/osm_extract.py download <region-id> --dated <YYMMDD>`.
3. Build beside the real caches, never over them:
   `python scripts/heavy_job.py run --label <city>-place-extract --session <you> --wait 30 -- python pipeline/place_extract_fetch.py <city> --pbf <file> --out <dir>`.
4. `python scripts/place_extract_compare.py <city> <dir>`. Section A is the
   tie-break count (same elements, two orders); section B is every row that
   differs because an element differs.
5. **Give every difference a cause.** An element edited between the two data
   dates is an edit: check its timestamp in the extract (public extracts keep
   timestamps and versions; they drop user names). An unedited object on the
   boundary is the leftover class above. Anything else is "unknown", written
   down as unknown, and the query stays on Overpass until it is explained.
6. A difference that turns out to be a rule goes into `osm_extract.py` with a
   selftest case built from the measured values, and into the list above
   with how it was learned. Then run the proof again on a city the rule was
   NOT learned from.

`osm_extract.parse_statement` reads `nwr["k"]`, `["k"="v"]`, `["k"!="v"]`,
`["k"~"re"]`, `["k"!~"re"]` and `[!"k"]` cut by `(area.x)`. It raises on a
bbox, `around`, a recursion, a case flag or a POSIX character class: a
statement it cannot represent stops the caller. Teach it the statement and
prove it; never skip the line.

## An area that crosses a region border

Built 2026-10-13 (owner's ruling of that day: read the few small regions as
one, do not download the country). Region polygons follow coasts and state
lines loosely, so a city on a border river or an estuary often has a sliver
of its boundary outside its own region. Three cases, told apart by the
server's index (`osm_extract.beyond`):

| The part of the area outside the region | What happens |
|---|---|
| lies in ANOTHER region of the index | that region joins the set, however small the part (`choose_regions`) |
| lies in NO other region (open sea) and is at most 1% of the area (`OVERFLOW_MAX_SHARE`) | accepted as water-side overflow: printed, and recorded in the cache's source line and `_extract.stats.overflow` |
| lies in no other region and is larger, or a boundary does not close from the files read | the run stops |

**A set is chosen only when one region will not do.** One region is taken
when it covers the area and either nothing else meets the area or its file
is under `--max-mb`. Otherwise `choose_regions` takes the smallest set by
total bytes, at most four regions (`SET_MAX_REGIONS`), each under the cap.
Sizes come from HEAD requests, two a region, and no file is downloaded to
learn its size. The run says which set and why.

**A set is one snapshot.** `download_set` takes every file at ONE date: the
date most of the set is already held at, so a set is completed with the
fewest downloads (`--dated`, which the server keeps for several days). A set
whose files state different data timestamps is refused (`set_timestamp`,
bound 0 s): every file of one daily run carries the same timestamp to the
second (23 files measured, two runs), and across two runs an object moved
over the cut can be in NEITHER file, which no comparison can see.

**Every id is taken once** (`osm_extract._Once`). An extract keeps whole
every way and relation crossing its cut, so the files overlap. Equal copies:
the first is kept. A copy holding fewer of its nodes' positions: the fuller
one is kept. Two full copies that differ: the read STOPS and names the
object and both files. Files of one snapshot cannot differ, so no copy is
taken on a guess. A boundary whose member ways lie in different files is
assembled from all of them.

**Memory is more than the largest file's alone**, though the files are read
in turn: 1.6 GB for pennsylvania with new-jersey against 1.05 GB for
pennsylvania alone, and 2.1 GB for south-korea with north-korea after a
first try in the same process against 0.97 GB alone. Declare the sum to the
gate. Why the first file's memory is not given back was not looked into.

**When the region was chosen from the stations** (no outline cache yet) the
area is not known until the boundary is read. A run that then finds the
area reaching into another region stops with `AreaPastRegion`; the command
line chooses again from the area it has just read, once, and takes the set.
The cost is the two light passes of the first try.

Measured 2026-10-13, extracts of 2026-10-12T20:21:35Z:

| City | Chosen from | Regions read | Outside the first region | Result |
|---|---|---|---|---|
| Philadelphia | its outline cache | us/new-jersey (164 MB) + us/pennsylvania (349 MB); us-northeast is 1,804 MB | 0.0002% of the area, in new-jersey | 27,683 street ways, 3,420 tagged, 458 extra; 122 objects in both files, all equal; outline identical to Overpass's (168 members with geometry); 347 s with both downloads, 1.6 GB |
| Washington D.C. | its outline cache | us/district-of-columbia alone (21 MB) | nothing | one region, as before; byte-equal to the caches the unchanged code wrote |
| Gimpo | its 9 stations, then the area as read | north-korea (93 MB) + south-korea (289 MB); asia is 15,613 MB | 0.04 km2, 0.014% of the area, in north-korea | 4,904 street ways, 422 tagged, 136 extra; 21 objects in both files, all equal; first try 10.7 s, 115 s in all with one download, 2.1 GB |
| Incheon | its 79 stations, then the area as read | the same two files, both held | 8.82 km2, 0.089% of the area, in north-korea | 15,971 street ways, 2,508 tagged, 529 extra; 98 objects in both files, all equal; first try 26.9 s, 125 s in all, 2.1 GB |

**The second file can add nothing, and is still required.** In all three
cities the answer from the first region ALONE (scope checks off) is the
set's answer byte for byte: Philadelphia's 180,929 + 458 elements, Gimpo's
79,912 + 136, Incheon's 142,748 + 529. The part in the neighbour's polygon
is river or estuary. That is known only after reading both, so it is not a
reason to skip the set; it IS a reason to expect the same of the next
border-river city.

**Not proven against Overpass.** None of the three cities had an Overpass
place cache on disk, and no Overpass request was made. What was compared:
Philadelphia's outline with Overpass's outline cache (identical), each set
with its first region alone (identical), and D.C. with the unchanged code's
caches (identical). The five rules are unchanged, so the four-city proof
above still stands for them; a set against an Overpass answer of the same
day is still owed.

## The download server's conduct rules

Licence read 2026-10-13 (`docs/data_sources.md`, "Place search index"): ODbL
1.0, OpenStreetMap's credit, no credit to the server's operator required, no
written usage policy. Its "Download responsibly!" request is the policy, and
`osm_extract.download_extract` holds it in code:

- **The smallest region that contains what is needed**
  (`smallest_region`, from `index-v1.json`, itself downloaded once).
- **Never the same file twice.** A dated file on disk is used; one that was
  downloaded and since deleted is refused by `data/_osm_extracts/downloads.json`.
- **Resolve `-latest` to its dated file** with a HEAD (the server answers 307
  with the dated name) and download that name.
- **One download at a time** on this machine (`DownloadLock`); a second run
  wanting the same file waits and then finds it.
- **Only `download.geofabrik.de`.** `osm-internal.download.geofabrik.de`
  carries user metadata behind an OSM login and is refused, also as a
  redirect target.
- **A large region wanted often is updated by diffs**, not downloaded whole
  each day. Not built here: until it is, a region is re-downloaded only when
  its held file is over the freshness limit and a city actually needs it.
- A plain user-agent that names the client and no person.

## Traps

- **A boundary can close while the data behind it is missing.** An area
  reaching past the region's edge is refused (`check_region`, against the
  index polygon), and a boundary whose ring is cut is refused by
  `boundary_polygon`. The answer is the set of regions that together cover
  the area ("An area that crosses a region border"), chosen by the module:
  never two files of different dates, and never a hand-made merge.
- **A kept cache is held to the current area.** With no `--force`, a cache
  on disk whose provenance (or own query) names another area than
  `config.PLACE_AREA` stops the run, naming both. A cache that records no
  area is kept with a warning.
- **A relation that runs past the region's edge has members the extract
  lacks.** Its center is then the middle of what is there. `query` counts
  these (`relations_with_absent_members`) and says so; a river or a long
  route is the usual case.
- **The area never depends on the boundary's tags.** Buffalo's relation lost
  `boundary` and `admin_level` in an edit of 2026-10-11; a fetch takes it by
  id regardless. The area LOOKUP filters on `boundary=administrative`, so it
  does not offer such a relation and leaves the city for a person: correct,
  and it must never resolve to the tagged neighbor instead.
- **An area can be made from a closed way** (Overpass area id 2400000000 +
  the way's id; Miami names two). Handled: the outline cache then holds a way
  with its geometry.
- **A tag-filter area is matched against relations only** (type boundary or
  multipolygon). An area Overpass makes from a tagged closed way has to be
  named by id.
- **The lookup cannot answer for a relation cut at the region's edge**: the
  country, usually the state. It lists them (`not_whole`) rather than
  guessing. A city whose stations span two regions is read from the set of
  regions holding them (the same choice as the fetch), and a relation cut at
  one file's edge is then whole.
- **Freshness is the extract's own timestamp**, read from its header, never
  the file's date on disk. The place caches refuse one older than 7 days.
- **Overpass's areas are older than its data.** Its answers carry
  `timestamp_areas_base` beside `timestamp_osm_base` (21 hours apart on the
  proof's caches). A boundary edited in that gap gives a real difference:
  check both dates before calling one unexplained.
- **Memory is the node positions of the whole region**, held for one pass:
  0.9 GB for a 102 MB file, 2.5 GB for 696 MB. Run it through
  `scripts/heavy_job.py`.

## In this project

- A city's caches: `python pipeline/place_extract_fetch.py <city>` (the
  region, or the set of regions, is chosen, held or downloaded for it;
  `--pbf` names a file, and given more than once names a set). The same
  command serves a multi-region city: nothing extra is passed. It writes
  only the caches that are missing; `--force` replaces. It takes no Overpass
  mirror lock and makes no Overpass request.
- A plan's empty search areas: `python scripts/place_search_area_lookup.py
  <plan.json> --source extract`.
- Both are registered in `scripts/check_all.py` by their selftests, and
  `scripts/check_no_fetch_in_steps.py` sees the downloader as fenced inside
  `fetch()` and guarded by `pipeline/offline.py`.
