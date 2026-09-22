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
- [ ] One alignment drawn per line; spacing gate run and its median sane
- [ ] Attribution scope updated in `docs/data_sources.md`
