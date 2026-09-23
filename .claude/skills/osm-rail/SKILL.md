---
name: osm-rail
description: Build a city's rail leg from OpenStreetMap instead of GTFS - when that is justified, how to derive stations without losing a line, and the traps OSM has that no transit feed has. Use when a city's agency publishes no reachable or current feed, or when a feed is stale or incomplete. Not a replacement for add-city Step 4; it is that step's OSM branch.
---

# Building a city's rail leg from OpenStreetMap

Distilled from the two cities that needed it - **Mexico City** (2026-09-22) and
**Guadalajara** (2026-09-22) - and written because the same class of mistake
happened twice in one day, one city apart, in the same country.

All fourteen cities before Mexico City read GTFS. Most of what is left on
`docs/global_country_shortlist.md`'s KEEP list does not: Taipei's TDX, São
Paulo's GeoSampa WFS, Israel's shapefiles. So this stops being an exception.

## THE META-LESSON, and it is the reason this file exists

**A rule written in the previous city's config does not reach the next city.**

`pipeline/mexico_city/config.py` says, in capitals:

> MATCH ON THE MODE, NEVER ON THE NETWORK LABEL ALONE.

It says it because OSM tags Lechería - a Ferrocarril Suburbano station - with
`network=STC Metro`, and a network-only match admitted it to Mexico City's
published excluded-stations record as a Metro station.

**One city later, Guadalajara's first Overpass query was
`node["railway"]["network"="Mi Tren"]`,** which silently omitted every one of
**Línea 4's 8 stops** - the line opened 2025-12-15 and its stop nodes carry no
`network` tag at all. The result was a station set with **zero stations in
Tlajomulco de Zúñiga**, the municipio Línea 4 exists to serve: a map missing
the same line the rejected GTFS feed was missing, reached by a different route.

The warning was correct, emphatic, and useless, because it lived in a file
nobody opens while writing the next city. This is the same structural failure
`add-country` already records about its own discard list - "prose in a
different section from the evidence, so nothing forced the two to agree."

**So: when a lesson is learned in city A's code, put it where city B must pass
through it.** In order of strength:

1. **An executable check in shared code** that raises. Unskippable.
   `pipeline/stations.py`'s three gates are this, and the spacing gate is what
   caught Guadalajara's 4 m "two stations".
2. **A skill** - this file. Read before the work, not after.
3. **A comment in the shared module** both cities call.
4. **A comment in the city's own config.** Fine for a fact about that city.
   Worthless as a warning to the next one.

A comment in (4) that is really a (1) is a latent repeat.

## When OSM is justified, and when it is not

Two cities, two different grounds, and the distinction matters because OSM is a
documented per-city exception rather than a default:

| City | Ground |
|---|---|
| **Mexico City** | **Unreachable.** Every `*.cdmx.gob.mx` host returns ConnectTimeout, on `www.` and bare, http and https. The feed's S3 `direct_download` 403s. No block page names an IP, so the browser does not help either |
| **Guadalajara** | **Stale and incomplete.** A feed exists and downloads fine - and its own `feed_info.txt` says `feed_end_date = 20230128`, its publisher is a third party (`Nubenautas` / `gtfs.studio`), and it carries three light-rail routes where the operator publishes four |

**Read `feed_info.txt` before rejecting or accepting any feed.** Guadalajara's
declared its own expiry; the rejection is a measurement, not a judgement. This
is `add-country`'s rule that a mirror is usable when the artifact self-attests
to its freshness - here it self-attested as three and a half years dead.

**Not a justification:** the agency feed being awkward, or OSM being more
convenient. Record the ground in the city's config and get the exception
approved.

### ⛔ BEFORE any of that: "the rail leg" is NOT "a GTFS feed"

**A stale or missing GTFS feed does not mean the agency route is closed.**
This project draws **station points and line geometry**. It never reads a
timetable. GTFS is one delivery format for that geometry — agencies also
publish it as **ArcGIS Feature Services, WFS, GeoJSON or shapefiles**, and
those are frequently maintained on a *different cadence* by a *different
team*.

**Madrid, 2026-09-22, is the worked example, and it was caught by a second
session rather than by this rule.** The reasoning that failed:

1. `mdb-794`, CRTM's Metro GTFS, has a calendar that ended 2026-05-27.
2. A search of CRTM's ArcGIS org **for GTFS items** found six, four refreshed
   2026-07-29 and Metro left at 2025-05-30.
3. Concluded: *"there is nothing newer to find"* → use OSM.

Step 3 does not follow from step 2, and the counter-evidence was **in the
same search output, already printed**: six `Datos abiertos: Elementos de la
Red de…` **Feature Services** dated 2026-06-04/05, scrolled past because the
filter said GTFS. CRTM's `M4_Red/FeatureServer` is `access: public` and holds
`M4_Estaciones` (293 point records → **243 distinct stations**, the real
count) and `M4_Tramos` (560 polylines) — **more complete than the GTFS feed
and more complete than OSM**, from the agency, and current.

So the order is:

1. **Agency GIS layers** — search the agency's ArcGIS org / geoportal for
   *feature services*, not only for feeds. Query `type:"Feature Service"`
   explicitly; a keyword search for GTFS will hide them.
2. **Agency GTFS**, if current.
3. **OSM**, on a recorded ground.

And when OSM is used, **keep it as the cross-check even after another source
wins**. Madrid's three sources agree on 13 lines and land at 243 / 236 / 230
stations — the spread is what shows the GTFS feed was undercounting.

## Deriving stations: use ROUTE-RELATION MEMBERSHIP

**Do not select station nodes by tag.** Select the route relations, then take
their node members:

```
relation["type"="route"]["route"~"^(light_rail|subway)$"]["network"="<Net>"](bbox)->.routes;
node(r.routes);
out body;
```

Membership in a named route relation is the strongest evidence that a node is a
station on a line, and **it cannot omit a line that has a relation** - which is
the failure a tag filter produces silently. Relation-level `network` filtering
is safe (Guadalajara's 8 relations all carry `Mi Tren`); node-level is not.

It also gives per-line membership for free, which is what gate 3 needs.

### The station object differs BETWEEN CITIES IN THE SAME COUNTRY

This is the finding that should stop anyone copying a working step 1:

| | Mexico City | Guadalajara |
|---|---|---|
| `railway=station` nodes | **184** | **1** |
| `railway=stop` (stop positions) | — | **110** |
| Collapse mechanism | by **name**, one node per line at interchanges | by **name**, exactly 2 per name (one per direction) |

Mexico City's whitelist finds **one** station in Guadalajara. Same country, one
register, one taxonomy, one licence - and a different station object. This is
why `pipeline/stations.py` shares the checks and leaves the collapse per city.

## The traps, all measured

- **Entrances are not stations.** `railway=subway_entrance`: **447** against
  184 stations in Mexico City (2.4x), 114 in Guadalajara. Israel's shapefile
  trap, in OSM. Counting them multiplies every ring.
- **Proposed infrastructure is mixed in with built, and is misspelled.** 13
  proposed Texcoco light-rail stations in Mexico City's bbox - **five tagged
  `railway=prpopsed`**. A blacklist on `proposed` lets those five through and
  draws rings around building sites. **Whitelist the values you want**
  (`railway == "station"`, or membership as above); a whitelist is immune to a
  typo and a blacklist is not.
- **A `network` tag can be absent on a new line** (Guadalajara's Línea 4, nine
  months old) **and wrong on an old one** (Mexico City's Lechería). It is a
  label, not evidence.
- **A name search with no bbox is a GLOBAL search.** Querying
  `admin_level=6 name="Guadalajara"` matched **Guadalajara, Spain** - also
  admin_level 6 - and a "keep the largest polygon" tie-breaker then selected it
  **on purpose**, producing a 26,814 km² "municipio" against the real ~151.
  Caught by a union-area gate. Two rules: bound every name search
  geographically, and never tie-break same-named boundaries by SIZE, because
  the wrong candidate is usually a bigger administrative unit.
- **Line names in the `colour` tag.** Guadalajara's Línea 4 has
  `colour=orange`, a CSS keyword rather than a hex value. Resolve it through
  the CSS named-colour table and say so; do not invent a shade.
- **`route` values are inconsistent within one system.** Guadalajara's Líneas
  1, 2 and 4 are `route=light_rail`; Línea 3 is `route=subway`. Match both.
- **Two relations per line, one per direction.** Draw ONE - the one with the
  most member way geometry - or the line is laid on itself at double the vertex
  count. `map_common.load_osm_line_shapes` does this, mirroring the GTFS
  cities' "most-used trip shape" rule.
- **An empty Overpass result is not an empty city.** A 200 with no elements
  must not be cached and must not be read as a finding: it once let a
  cross-direction check print "every ref has exactly 2 direction relations"
  over **zero** relations. Overpass hosts also 504 and 429 freely - try several
  before concluding anything, and treat a failure as a fact about that host.
- **But a 504 is usually YOUR QUERY, not the host.** See the section below
  before you conclude Overpass is down; the Toulouse build lost ten minutes to
  exactly that misreading.

- **`map_to_area` silently returns NOTHING for a relation that is not in
  Overpass's area index**, and the query then matches zero of everything with
  a cheerful 200. On 2026-09-23 that reported **San Francisco as having no
  tram or light-rail routes**, which is absurd on its face and would not have
  been on a city nobody knows. **Use a bounding box** - it needs no index -
  or verify the area resolves before trusting a count taken inside it.

- **ONE Overpass query per CITY. Never one per route, and never one per
  station.** This is the single largest recurring cost in this project's OSM
  work. A stop-spacing test written per-route ground for **12 minutes on one
  city** - 22 relations against a load-shedding host, worst case 22 x 2
  mirrors x 2 retries x a 300 s timeout - and the same pattern produced a 504
  on Bucharest's brief-check and a 10-minute Seoul probe the same day.
  Rewritten as one query per city it finished **five cities in five minutes**.
  `scripts/screen_stop_spacing.py` is the worked example.

- **Resolve a boundary BY NAME and then LOOK at what came back.** Searching
  `name=Stockholm` at `admin_level=7` matches **nothing** - the Swedish
  municipality is `Stockholms kommun` - and widening the search returns
  **two US "Stockholm Township" relations at the same admin_level**. Either
  would have produced a real, confidently wrong rail network. **A zero from a
  selector is a statement about the selector.**

- **A route relation with NO `ref` is the default expectation, not an
  anomaly.** It appeared in **five cities in one day**: Bucharest's
  `Extensie M4` (no ref, no colour), Singapore's `JRL` (5 relations, named,
  uncoloured), Stockholm's unref'd subway **and** tram, and 27 of Seoul's 65
  commuter relations. **A build keying on `ref` drops them silently; a build
  keying on relation COUNT draws a line it cannot label** - and this project's
  invariant requires every drawn line to carry its real public name and a
  legend entry. **Count both ways and reconcile the difference before
  building.**

## Keeping Overpass cheap, which is how you stop being throttled

Added 2026-09-23 from the Toulouse build. This is the difference between a
query that answers in seconds and one that 504s on every mirror, and it is
entirely caller-side.

**`out center` on WAYS is the expensive part.** Overpass has to resolve every
way's member nodes to compute a centroid, so a combined node+way query costs
far more than the node half alone. Measured that day on the Toulouse commune
bbox, same tag, same hosts, minutes apart:

| Query | Result |
|---|---|
| `node[...]; way[...];` + `out center;` | **504** on overpass-api.de, **read timeout** on kumi.systems |
| `node[...];` + `out body;` | **answered in seconds**, first host tried |

Nothing about the hosts changed. The query did.

**So, in order:**

1. **Ask for nodes first** - `node["amenity"="fast_food"](bbox); out body;`
   For POI counting that is usually 90%+ of the answer: restaurant nodes were
   **827 of the 889** node+way total in Toulouse, 93.0%.
2. **Add ways as a SECOND query** only if the node answer is not enough, and
   record which shape produced each number. **Never compare a node-only count
   with a node+way count** - that measures the query, not the city. Toulouse's
   restaurant control reads 1.28x one way and 1.38x the other, and the
   difference is entirely the query shape.
3. **Keep the in-query `[timeout:N]` low** - 90 is plenty for a city bbox. The
   HTTP timeout only caps how long *you* wait; the in-query one is what lets
   Overpass abort and tell you, via a `remark`, that it gave up.
4. **Set a total deadline and print every attempt.** `pipeline/osm.py`'s
   `fetch()` now takes `deadline` (default 900s) and prints each host it
   tries, because the old shape could spend `retries x hosts x timeout` in
   complete silence - which is indistinguishable from a hang, and was read as
   one.

⚠ **A bare client signature draws HTTP 406 from `overpass-api.de`.** That is
`add-country`'s client-signature refusal, not an IP block, and the fix is a
real `User-Agent`. `pipeline/osm.py` and `scripts/brief_check.py` both send
one; an ad-hoc probe written with plain `requests` does not, and that is how
the Toulouse probe earned its first 406 before it had run a single real query.

## Licence

OSM is **ODbL 1.0**: attribution, not a bar on modification. A rendered map is
a Produced Work, so share-alike does not reach it. But note what changes: every
map already carries `© OpenStreetMap contributors` for the **basemap**, and
once a city's line geometry is OSM that credit covers **data** too. Say so in
`docs/data_sources.md` rather than letting the existing notice imply it is only
about tiles. No file goes in `docs/licenses/` - ODbL is a published public
licence, not an agency document that can be revoked without notice.

## Checklist

- [ ] Ground for not using GTFS recorded in the city's config, and approved -
      with `feed_info.txt`'s `feed_end_date` quoted if the feed exists
- [ ] Stations derived from **route-relation membership**, not a node tag filter
- [ ] Entrances, proposed and construction excluded by **whitelist**
- [ ] Every operator-published line present; per-line counts compared where the
      operator publishes them (gate 3), and gaps named rather than filled in
- [ ] Every name search bounded by a bbox; same-name boundaries never resolved
      by size
- [ ] **ONE query per city** - never one per route or per station; the largest
      recurring Overpass cost in this project, and the one that turns a
      load-shedding host into a twelve-minute stall
- [ ] Queries written **nodes-first** (`out body`), ways added as a separate
      query only if needed, and no count compared across the two shapes
- [ ] A real `User-Agent` sent, a total deadline set, and every attempt printed
      - a 504 investigated as query cost before it is called an outage
- [ ] One alignment drawn per line; spacing gate run and its median sane
- [ ] Attribution scope updated in `docs/data_sources.md`
