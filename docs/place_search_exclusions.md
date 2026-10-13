# What place search leaves out

The internal record of every settled class the place-search index leaves
out, and of the classes it keeps against one of those rules. Started
2026-10-13 on the owner's word ("add to list of dropped categories ... start
one now and retrofit"). `docs/excluded_categories.md` is the businesses' list;
this one is search's. The reader-facing version is the section "What the
map's search leaves out" in `docs/excluded_categories.md`, in the owner's
approved wording (landed 2026-10-13).

Every rule lives in `pipeline/place_index.py` unless a row says otherwise. A
date is the `DECISIONS.md` entry (or its week file under `docs/decisions/`)
that holds the owner's words. Counts are not repeated here: they are in the
comment beside each rule, dated, and in the decisions log.

**When a class is added or changed:** add or edit its row here in the same
commit, give the rule a case in `python pipeline/place_index.py --selftest`
and a break in `scripts/place_index_breaks.json`, and follow the rule-change
protocol in the `place-search-city` skill.

## The scope

| Left out | Rule | Where | Decided |
|---|---|---|---|
| Businesses, as a kind | The index holds places only and is never joined to a business register | module docstring | 2026-10-07 |
| Anything outside the searched area | `config.PLACE_AREA`: the municipalities the map covers, nothing wider without `PLACE_AREA_KEPT` | `scripts/check_place_scope.py` | 2026-10-12 |
| An object by id | A home, a business, a removed object or a glitched name no rule catches | `config.PLACE_DROPPED` | 2026-10-08, 2026-10-11 |

## Streets

| Left out | Rule | Where | Decided |
|---|---|---|---|
| Platforms, corridors, driveways, parking aisles, roads proposed or under construction | `SKIP_HIGHWAY`, `SKIP_SERVICE`; a street closed for rebuilding is kept by name in `config.PLACE_REBUILT` | `build()`, street pass | 2026-10-07, 2026-10-11 |
| A minor way whose name does not read as a way | `MINOR_HIGHWAYS`, `WAY_WORDS`, `_reads_as_way`; kept with wikidata or wikipedia | street pass | 2026-10-07 |
| A street named for a business, a home or private access | `LEAK_WORDS`, `_named_street` | street pass | 2026-10-08 |
| A street whose every way is a private minor way | `street_open`; except a name led by `PRIVATE_STREET_LEAD` (French) | street pass | 2026-10-11 |
| A street whose every way is private (access=private or no) on residential or unclassified | `PRIVATE_STREET_HIGHWAYS`, `street_public`; `PRIVATE_STREET_LEAD` and a way's own article keep one | street pass | 2026-10-13 |
| A busway or a race track | `NOT_STREET_HIGHWAYS`, `street_real`; a way's own article keeps one | street pass | 2026-10-13 |
| A minor-way street named by a description, a bare type or way word, or a type and a code | `street_description`, `STREET_DESCRIPTIONS`; never a street with a way of residential class or above | street pass | 2026-10-13 |
| A pedestrian area as a street | `area=yes` is skipped; with an article of its own it is a landmark | street pass, `square_areas` | 2026-10-08, 2026-10-13 |
| A way whose highway tag lists a skipped value beside another (`platform;bus_stop`) | each value of the tag is read against `SKIP_HIGHWAY`, under whatever name | street pass | 2026-10-13 (second batch) |
| A street private on every way, where some ways are alleys | `PRIVATE_STREET_SERVICES`: a private `service=alley` way is read as a private residential one | street pass | 2026-10-13 (second batch) |
| An interchange, a ramp, a name ending "Drwy" | `street_never`, whatever the ways (interchange names are kept in a city whose config sets `PLACE_KEEP_INTERCHANGES`: Hong Kong); a name ending "Ramp", "Ramp On" or "Ramp Of" on ramp-class ways only (`RAMP_NAME`, `RAMP_HIGHWAYS`); a circular junction whose every way is a motorway's | street pass | 2026-10-13 (second batch) |
| An HOV or managed-lane label | `MANAGED_LANE`, on a street whose every way is a motorway's | street pass | 2026-10-13 (second batch) |
| "Alley" and digits; an alley named by its two cross streets | `NUMBERED_ALLEY`, `CROSS_STREET_ALLEY`, on a way of any class (`ANY_WAY_DESCRIPTIONS`); format characters set aside first (`_plain`) | `street_description_2` | 2026-10-13 (second batch) |
| "Path between X and Y"; a cycle facility named for the street it runs on; a name ending "Driveway" | `PATH_BETWEEN`, `CYCLE_FACILITY`, `DRIVEWAY_NAME`, on a street whose every way is a minor way | `street_description_2` | 2026-10-13 (second batch) |

**Kept against those rules (owner, 2026-10-13, second batch):** a named roundabout
(`ROUNDABOUTS_STAY`, keyed on `junction=roundabout` or `circular`, never on the name); named
bridges, viaducts and tunnels; two real names in one; frontage and service roads named for a
freeway; a trail under a name of its own ("Los Angeles River Bike Path", "Footscray Road
Trail"); "Back Lane" (taken out of `STREET_DESCRIPTIONS`); a name ending "Driveway" on a
residential-class way (Ottawa's Queen Elizabeth Driveway; San Diego's business driveways on
such ways stay by id). **One city's own way words:** `config.PLACE_WAY_WORDS` adds words to
that city's minor-way test only.

**Kept against the Overpass answer (2026-10-13):** a street way on a border two searched
municipalities share, which lies in neither one's interior, is in when the city's places were
read from a regional extract (`place_extract_fetch.SHARED_BORDER_UNIONS`) and missing when
read from Overpass. Seattle: 59 ways of six streets.

## Stations

| Left out | Rule | Where | Decided |
|---|---|---|---|
| A bus or ferry terminal, a cable car terminal | `RAIL_MODES`, `OTHER_MODES`, `NOT_RAIL` | tagged pass | 2026-10-08 |
| A station not yet open | railway=construction or proposed, the lifecycle tags, construction=yes on any stop, opening_date after the cache; listed in `docs/place_search_unopened_stations.json` | tagged pass | 2026-10-08, 2026-10-11, 2026-10-13 |
| A closed station | `station_closed`: end_date behind the cache, a disused or abandoned prefix, disused=yes, abandoned=yes | tagged pass | 2026-10-13 |
| An emergency platform | emergency=designated | tagged pass | 2026-10-08 |
| A ride | `station_ride`: usage=tourism, attraction=*, a miniature railway; never tourism=attraction alone | tagged pass | 2026-10-13 |
| A business tagged a station | no rail tag at all and a commercial tag | tagged pass | 2026-10-13 |
| A station named by a bare type word | `bare_type` with neither wikidata nor wikipedia | tagged pass | 2026-10-13 |
| A second row for one tram stop | `PLATFORM_MERGE_M`: tram platforms of one name are one row; an interchange stays two | merges | 2026-10-13 |
| A stop-area relation beside its station's own row | `public_transport=stop_area` on a relation groups a station's parts; it stays where no other station row is within `OUTLINE_BESIDE_M`, bears its name within `OUTLINE_SAME_M` or shares its Wikidata entry (Washington's two streetcar stops) | merges | 2026-10-13 (second batch) |
| A bus station that lists a rail mode | `amenity=bus_station` with no railway tag, whatever `light_rail=` or `train=` says | tagged pass | 2026-10-13 (second batch) |
| A station's outline beside the station's own row | a way or relation tagged `public_transport=station` with no railway tag, within `OUTLINE_BESIDE_M` of a rail-tagged station row or `OUTLINE_SAME_M` of one of its name; one further off stays | merges | 2026-10-13 (second batch) |
| A second row for one transfer complex | `COMPLEX_MERGE_M`: station rows sharing one Wikidata entry are one row, the others' names its aliases | merges | 2026-10-13 (second batch) |
| A station with an end date written with stray characters ("=1959") | `_past` sets the characters aside; `station_closed` | tagged pass | 2026-10-13 (second batch) |

## Neighborhoods (places)

| Left out | Rule | Where | Decided |
|---|---|---|---|
| A single dwelling or farm, and every place kind not listed | `PLACE_VALUES` | tagged pass | 2026-10-07 |
| A housing estate: an area on residential land, an area with a house number, a numbered block, a name ending "Estate" with no wikidata or article | `NUMBERED_BLOCK`, `ESTATE_NAME`; an area with an article of its own is kept | place branch | 2026-10-08, 2026-10-11, 2026-10-13 |
| A hamlet with a population tag under 50 | `HAMLET_MIN_POPULATION`, unless notable | place branch | 2026-10-11 |
| A place named for a business or a home | `LEAK_WORDS` | place branch | 2026-10-08 |
| A place named by a bare type word | `BARE_TYPE_NAMES`; kept on an article of its own | place branch | 2026-10-11, 2026-10-13 |
| A place that is not there | `lifecycle(place=True)`: a demolished or abandoned flag, or such a prefix on the place key | place branch | 2026-10-13 |
| A second row for one place | `NEAR_DUP_M` (an area beside its node), `ROW_MERGE_M` (one name within 300 m) | `add()`, merges | 2026-10-08, 2026-10-13 |
| A place named "X Estates"; a mobile-home or trailer park tagged a place | `ESTATES_NAME`, `MOBILE_HOME_PARK`, with no wikidata and no article | place branch | 2026-10-13 (second batch) |
| A settlement's boundary beside the node that bears its name | `BOUNDARY_DUP_PLACES`: a boundary tagged city, town, village, hamlet, suburb or borough, where a settlement node of that name is in the cache, at any distance; a lesser boundary (a townland) stays | place branch | 2026-10-13 (second batch) |

## Landmarks

| Left out | Rule | Where | Decided |
|---|---|---|---|
| A business: a commercial tag, a commercial building, a private operator | `COMMERCIAL_KEYS`, `COMMERCIAL_VALUES`, `COMMERCIAL_BUILDINGS`; a private operator or an office tag is outweighed by an article of the object's own (`KEPT_COMMERCIAL_REASONS`), a brand, shop or lodging tag never | `landmark_drop` | 2026-10-07, 2026-10-13 |
| A tourism, amenity or aeroway landmark with neither wikidata nor wikipedia | `NOTABLE_ONLY`; places of worship need none | `landmark_drop` | 2026-10-07 |
| A home | `_home`, `_public_home`; kept when open as a museum or attraction, or in `config.PLACE_VISITABLE`; an article is no exemption, except where access=private is the only home sign on something that is no garden, park or palace (`_private_access_only`) | `landmark_drop` | 2026-10-08, 2026-10-13 |
| A landmark named as a bare Japanese personal name | `bare_personal_name` | `landmark_drop` | 2026-10-07 |
| A garden that is not notable, or residential | leisure=garden | `landmark_drop` | 2026-10-07 |
| A landmark named for a business or a home | `LEAK_WORDS`, `HOME_WORDS`; a business word passes on an article and a review in `config.PLACE_REVIEWED` | `landmark_drop`, check E | 2026-10-08 |
| A name that is only a type, or a code beside a type | `BARE_TYPE_NAMES`, `CODED_TYPE`; a registered code is a name; a bare word is kept on an article of the object's own, never the type's | `bare_type`, `landmark_drop` | 2026-10-11, 2026-10-12, 2026-10-13 |
| A museum exhibit | `EXHIBIT_HISTORIC`, an indoor painting | `_exhibit` | 2026-10-11 |
| A Stolperstein; a tomb named for a family | memorial=stolperstein, `FAMILY_TOMB` | `landmark_drop` | 2026-10-08, 2026-10-11 |
| A grave or a plaque without a Wikipedia article of its own | `grave_or_plaque`, `own_article`; a Wikidata entry alone admits none; statues, busts and public memorials are untouched; where the tags cannot say whose the article is, the row stays as it was | `landmark()` | 2026-10-13 |
| Wayside shrines and crosses, boundary stones, milestones, plain memorials and tombs | `SKIP_HISTORIC`, unless a tourism, amenity or leisure tag, wikidata, or an article of its own | `landmark_drop` | 2026-10-07, 2026-10-13 |
| A landmark that is not there | `lifecycle`: demolished, razed, removed, abandoned or not yet open by its own tags, read narrowly (the comment sets out each limit); a place that stands and is closed for works is kept by id in `config.PLACE_CLOSED_FOR_WORKS` (the not-yet-open class only) | `landmark()` | 2026-10-13 |
| A register or inventory entry: `historic=maritime`, `naval`, `military` or `engine` | `REGISTER_HISTORIC`: kept only on a Wikipedia article of its own, or a Wikidata entry no other object of the cache carries (`own_item`; never for an engine), or by id in `config.PLACE_KEPT` | `landmark()` | 2026-10-13 (second batch) |
| A numbered building under its district's register number | `SHARED_REGISTER_MIN`: a `ref:nrhp` three or more objects share keeps no coded name (`own_register`); wikidata or wikipedia on the object still does | `landmark_drop` | 2026-10-13 (second batch) |
| A street's way as a landmark | a way with a highway tag that is no area and no square, whatever historic or tourism tag it carries (`NOT_A_STREET_WAY`), ONLY where a street row bears the name the landmark row would have, bridge:name leading (`_bridge_led`); with no such street row it stays a landmark | tagged pass | 2026-10-13 (second batch) |
| A name ending "(historical)" | `HISTORICAL_NAME`, on any tagged row | tagged pass | 2026-10-13 (second batch) |
| A derelict canal; a place of worship tagged disused=yes with neither an article nor a Wikidata entry of its own; a demolished waterway | `lifecycle`: `waterway=derelict_canal`, `disused=yes` with `amenity=place_of_worship`, `waterway` among `LIFE_FEATURES` | `landmark()` | 2026-10-13 (second batch) |
| A row admitted only by a Wikidata entry three or more rows share | `SHARED_WIKIDATA_MIN`, `held_by_wikidata` | merges | 2026-10-13 |
| A square a street already names; a second row for one landmark | `SQUARE_DUP_M`, `NEAR_DUP_M`, `ROW_MERGE_M` | duplicate passes | 2026-10-08, 2026-10-13 |
| A place value that is no neighborhood (plots, city blocks, islands) | skipped; an island or islet with an article of its own is a landmark (`ISLAND_VALUES`), a district with one a neighborhood (a county that borders the city is dropped by id: Prague's two) | tagged pass, `config.PLACE_DROPPED` | 2026-10-08, 2026-10-13 |

## Names

| Left out | Rule | Where | Decided |
|---|---|---|---|
| A name that is no name: a placeholder, an error value, a number alone, contact details | `JUNK_NAMES`, `JUNK_MARKS`, `_CONTACT` | `junk_name`, check F | 2026-10-08 |
| A name in a third script, where a local name exists | `_local_first`; never repaired | `_names` | 2026-10-11 |
| A junction named by a number | `junction_numbered` | tagged pass | 2026-10-08 |

## Considered and not built as rules

Castles (a web check is owed), coded names the rule misses and zoo contents
(both by id), an operator's or network's name as the sign of a ride,
archipelagos, `disused` and `was:` on a place or landmark, a monument or a
gallery held to the notable rule (measured 2026-10-11 and not applied).
Misspelled names are not corrected: a corrected name would not be
OpenStreetMap's (the page says so, 2026-10-13).

From the second batch (2026-10-13), ruled as drops and NOT built, because no
test on the cached tags and names is safe; each stays a by-id drop in
`config.PLACE_DROPPED`: cemetery and church-ground avenues (the caches hold no
cemetery outline to place a way inside); campus lawns and courts named for a
building (leisure=park with no tag in common); a name ending "Driveway" on a
residential-class way (Ottawa's parkways bear it too); a cycle facility with
no street type word in its name; "The Island" in Manchester (three residential
ways, no junction tag); homes with an article and no home tag; an end date
behind the cache on a landmark (read on stations only). A standing abandoned
or ruined landmark stays whatever its article (`ABANDONED_NEED_ARTICLE`).

**Kept by the owner's word, by id (`config.PLACE_KEPT`, 2026-10-13):** an object the bare-type or the register-entry rule
would drop. Seattle's Ballard Locks (four ways) and London's Greenway (two objects). The word stays on the list for
every other object.
