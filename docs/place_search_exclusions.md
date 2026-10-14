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
| A street whose every way is private (access=private or no) on residential or unclassified | `PRIVATE_STREET_HIGHWAYS`, `street_public`; `PRIVATE_STREET_LEAD` and a way's own article keep one; where a city sets `PLACE_KEEP_NAMED_PRIVATE_STREETS` only a code-named one goes | street pass | 2026-10-13 |
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
| A second row for one transfer complex | `COMPLEX_MERGE_M`: station rows sharing one Wikidata entry are one row, the others' names its aliases; never two names the map draws (`complex_parts`, the fifth pass) | merges | 2026-10-13 (second batch) |
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

## The third pass (2026-10-13, branch search-rules-3)

| Left out | Rule | Where | Kind |
|---|---|---|---|
| Public art with no Wikipedia article of its own | tourism=artwork; a wikidata tag alone admits none; an article the tags cannot place keeps the row | `landmark()` | landmark |
| An exhibit under its class's or kind's article | an entry another object carries (`own_item`); a locomotive or railway car with neither a tourism tag nor an article under its own name (`RAIL_EXHIBITS`); a vehicle with no historic tag likewise | `landmark_drop`, `_exhibit` | landmark |
| A park an apartment estate or its management office runs | `ESTATE_OPERATOR` on leisure=park; a park tied to an estate only by name stays | `landmark_drop` | landmark |
| A park or garden whose name leads with a house word | `HOME_LEAD_ON_PARKS`, German only | `_home` | landmark |
| A Stolperschwelle | `STOLPERSTEIN_MEMORIALS`, artwork_type=stolperstein | `landmark_drop` | landmark |
| A dead railway alignment with no wikipedia tag | `dead_railway`, ways only; a standing structure is not this class | `landmark()` | landmark |
| A name ending "(geschlossen)", "(abgebrannt)", "(stillgelegt)", "(außer Betrieb)" | `HISTORICAL_NAME`; never "ehem." | tagged pass | any |
| A site or boundary relation that repeats another row's entry more than 300 m off | `SITE_RELATION_TYPES`, `ROW_MERGE_M` | merges | landmark, place |
| A bare type word behind an article, or in two languages | `BARE_ARTICLES`, `_bare_word`: every part bare | `bare_type` | landmark, place |
| Korean, Chinese, Spanish and German bare type words; Korean "N호" park lots; "Cluster N" | `BARE_TYPE_NAMES`, `CODED_TYPE` | `bare_type` | landmark, place |
| A private street on living_street ways | `PRIVATE_STREET_HIGHWAYS`; a way open on foot is not private (`FOOT_OPEN`) | street pass | street |
| A customers-only service road named by a Korean description | `CUSTOMER_ROAD_ENDS` | street pass | street |
| A code beside a path type on minor ways, German | `PATH_CODE`; never "Straße N" | `street_description` | street |
| A public_transport=station object with no railway tag | dropped beside a station's row; alone, kept only on a rail mode, a station tag, a network tag or a map station's name | merges | station |
| A station's outline under the station's name | merged into the station node within `OUTLINE_BESIDE_M` (`_station_core`, or a shared Wikidata entry) | merges | station |

**Kept against a rule:** a station of the map or of a rail network is never
dropped for a bare type name (`RAIL_STATION_VALUES`, `map_stations`); a quiet
station is accounted for in `config.PLACE_QUIET_STATIONS`; `config.PLACE_KEPT`
is also read by the estate-area rule; a river row is dropped or kept by the
id of any of its ways. The index holds no transit line: lines reach the
search box from the map itself.

## The fourth pass (2026-10-13, branch search-rules-3)

| Left out | Rule | Where | Kind |
|---|---|---|---|
| A library with no article of its own | `has_article`: the wikipedia tag, or an entry of the object's own with an article in the city's Wikidata cache; the same test as public art. `article_lookup_kind` is the one list of kinds the lookup is asked about, read by the rule and by the fetch script alike; an article under the object's own name is its own here whatever subject tag repeats it | `landmark()` | landmark |
| An object admitted only by its subject's Wikidata entry | `SUBJECT_ENTRY_KEYS` | `landmark()` | landmark |
| A second row for a monument drawn in segments | one folded name and one Wikidata entry, ways and relations, at any distance | merges | landmark |
| A station tagged passenger=no or public_transport=no | unless the map draws it | tagged pass | station |
| A home named with the house word last | `HOME_NAME_END`: Latvian "villa", Norwegian "gård" | `_home` | landmark |

**Kept or added:** `int_name` is read as an alternate name; "store" is no leak word in a
Danish, Norwegian or Swedish city (`LEAK_SET_ASIDE`); a glued street name passes beside a leak
word in a suffix language; a second language below the 90% floor is declared in
`config.PLACE_LANGUAGES_ALSO`; `config.PLACE_STATION_STRIP` takes an ending off station names.
Swedish "-gård" stays a street ending on every way (candidate 37, pulled by the owner).

## The fifth pass (2026-10-13, branch search-rules-5)

| Left out | Rule | Where | Kind |
|---|---|---|---|
| A place of worship named only by its denomination or hall type ("Kingdom Hall of Jehovah's Witnesses", "Methodist Church", "Gurdwara") | `worship_only`: every word a listed denomination word or phrase, a hall-type word or a joiner (`WORSHIP_DENOMINATIONS`, `WORSHIP_HALLS`, `WORSHIP_JOINERS`, per language; `WORSHIP_RESPELL` for a denomination as its mappers spell it), with one hall-type word at most; amenity=place_of_worship only, the leading name only | `landmark_drop` | landmark |
| A station closed to the public | `STATION_PRIVATE_ACCESS`: access=private on a station object (Washington's Capitol subway, a railway's training stations in Tokyo); access=no is not read, since a public halt in Marseille carries it | tagged pass | station |

**Kept against those rules:** a place of worship whose name holds any other word (a saint, a
place, a street, an ordinal: "First Baptist Church"; a second hall-type word: "Temple Baptist
Church"), one with a Wikipedia article of its own, and one named by id in `config.PLACE_KEPT`;
a station the map draws, whatever its access tag (the station guard).

**Two stations of the map are never one row (a fault mended, not a class left out):** the
transfer-complex merge (`COMPLEX_MERGE_M`) folded Boston's Boylston into Park Street, since
OpenStreetMap gives both nodes one Wikidata entry. A complex whose rows bear two or more
names the map draws is split at those names (`complex_parts`); a row under any other name
joins the nearest. Distance is not the test.

**Not mended:** Boston's Green Street station is indexed as "Green" because that is its
`name` in OpenStreetMap (relation 20304842); no rule strips a street word from a station
name, and a name is not corrected here.

## The sixth pass (2026-10-13, branch search-rules-5)

From the sixteen rulings on the pilot reads and the held rows (`DECISIONS.md`, "the pilot reads
and the held rows; sixteen rulings"), items 1, 2, 7 and 9 and the faults fixed without a ruling.

| Left out | Rule | Where | Kind |
|---|---|---|---|
| The readers' bare type words in fifteen languages; spaced CJK forms ("어린이 공원"); "제1호근린공원", "開発2号公園", "Estação 3", "第一中庭" as codes beside a type | `BARE_TYPE_NAMES_6`, `_bare_word`, `CODED_TYPE` | `bare_type` | landmark, place, station (the guard decides) |
| A church named only by its chain or body (ruling 2) | the fifth pass's rule with `WORSHIP_BODIES` and wider lists (Portuguese, Spanish, Dutch, Japanese, Chinese, Latvian); only joiners and one hall-type word may follow a body's name; a nationality is listed only inside a denomination's name | `worship_only` | landmark |
| A religious office, education hall or residence tagged a place of worship (ruling 1) | `worship_office`: `WORSHIP_OFFICE_HEADS` (the name's head), `WORSHIP_OFFICE_WORDS` (a whole word; a CJK word anywhere); an English word is not read in a name that holds CJK | `landmark_drop` | landmark |
| A facility of an apartment estate or a mall tagged a park, a playground or a square (ruling 7) | `estate_facility`: the operator names a condominium, a residents' body, an estate's management or a mall (`ESTATE_FACILITY_OPERATOR`); the operator heads the name and a facility word closes it; an estate's brand and a facility word (`ESTATE_BRANDS`, `ESTATE_FACILITY_ENDS`); a name that says "inside" | `landmark_drop` | landmark |
| A park named as a square, beside a street row of its name (ruling 9) | `square_led`, `SQUARE_HEADS`, within `SQUARE_DUP_M`; against streets only | duplicate pass | landmark |
| A station with operational_status=closed; a freight station by its name | `station_out_of_service`, `STATION_FREIGHT_WORDS` | tagged pass | station |
| A station entrance or a ticket gate tagged a station | `STATION_ENTRANCES`: no row beside a station row of its name within `OUTLINE_SAME_M`, and none at all unless the map draws its name | merges | station |
| A bus rapid transit station kept on its network tag | `BUS_NETWORK`: a bus network's tag is no rail sign for a station object with no railway tag | merges | station |
| A suburb's or a borough's boundary beside its own node | `BOUNDARY_NODE_M`: the node of the same place value and name, a closing bracket set aside, within 5 km | place branch | place |
| Ways with no entry beside the one relation of their name that carries it | `SEGMENTS_MIN` ways or more fold into the relation's row, at any distance | merges | landmark |
| A name ending "(FECHADO)" | `HISTORICAL_NAME` | tagged pass | any |
| "Hôtel particulier", "Ancien hôtel" as whole names | `BARE_TYPE_NAMES_6` | `bare_type` | landmark, place |

**Kept against those rules:** an article of the object's own keeps a row against every one of
them; for a place of worship an entry of its own with an article in the city's Wikidata cache
keeps it too (the cache is read, never asked: `article_lookup_kind` is unchanged);
`config.PLACE_KEPT`; a station the map draws (the station guard), which is why Amsterdam's
diversion-only stop "Oranje Nassaulaan" stays. "Church of Christ Presbyterian" and
"Russian-Ukrainian Seventh Day Adventist Church" keep their rows. A convent under a name of its
own is a place, not an office (owner, 2026-10-13: "Convento de Santa Teresa"; "convento" is no
office head), and Mexico City's "El Polvorín" is a proper name ("polvorín" is no bare type word).
A park named for an estate
with no facility word stays; a park under a street word or a garden word ("Avenida de Brasil",
"Jardins de ...", a Paris "Square ...") stays beside the way of its name.

**Where the leak-word test no longer fires (a fault mended):** a junction row; a French
landmark named "Hôtel de", "Hôtel du", "Hôtel des", "Hôtel d'" or "Hôtel-" and a word
(`FRENCH_MANSION`; a hotel business so named is held out by its lodging tag); a French street
under "brasserie" (`LEAK_STREET_ALLOW`). `scripts/check_place_search.py` E reads a review of
such a row as no longer needed, never as stale. "Hôtel" and a family name alone is still a
review.

**Listed and not built:** a square inside a mall, a theme park or a zoo known only by its
coordinates (Osaka's ATC and Hankyu plazas, Universal Studios' zones, Tennoji Zoo); cemetery
tombs tagged historic=monument (Madrid, 6); Japanese house words (住宅, 邸) on a listed house;
Madrid's place=locality field names (ruling 8: counted per city in the batch 6 report, no rule);
English "convent" and "seminary", Spanish orders' names, Korean halls' own names (참신관, 대건관);
a relation folded into one of its own segments by `NEAR_DUP_M` before the segment merge.

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
