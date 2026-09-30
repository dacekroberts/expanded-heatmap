# Bergen — build brief

**Step 0 measured 2026-09-27 (the Norway screen) and 2026-09-29 (the
light-rail test; this brief).** Run `python scripts/brief_check.py bergen`
before writing code.

> **Measured at the build, 2026-09-29 (branch `bergen`)**: brief check 9/9.
> **3,597 storefronts** (Retail 2,195, Food 658, Personal 744), 33 stations,
> 58.5% in a ring. The screen's 3,615 is 18 lower because the shared filter
> now also excludes catering. The three calls: the cached register (no
> refresh), Line 2 `#9c27b0` (worst pin 55.2), Byparken / Kaigaten kept as
> two. Gate 3 is not run: Wikipedia's 35 stops network-wide does not
> reconcile with the feed's 34 stop places.

---

## The one-line summary

**Oslo's modules with a new kommune number, and three settings that must NOT
be copied from Oslo's config.** The register, the parent join, the sole-trader
rule, the catch-all verdict and the address join are all shared
(`pipeline/countries/norway.py`, `pipeline/taxonomies/norway_sn2025.py`). The
route type, the UTM zone and the ring edges are Bergen's own, and each of the
three would fail quietly if copied: no rail drawn, distances measured in the
wrong zone, rings too small.

| | Oslo (built) | **Bergen** |
|---|---|---|
| Kommune | 0301 | **4601** (Vestland) |
| Rail | T-bane `401` + trams `902` | **Bybanen, `901`, 2 lines** |
| Stations in scope | 155 | **34 parent stop places → 33 by name**, all inside the kommune |
| Median station gap | 465 m | **624 m** |
| Rings | 0.05 / 0.1 / 0.2 / 0.3 mi | **standard 0.1 / 0.2 / 0.3 / 0.6 mi** |
| Projected CRS | EPSG:25832 (UTM 32N) | **EPSG:25831 (UTM 31N)**: 5.23–5.36° E |
| Storefronts placed (screen) | 10,718 | **3,615**: retail 2,195 · food 658 · personal services 762 |
| In the outer ring (screen points) | 75.7% | **58.6%** (2,119) |

**Region: `"Europe"`. Band A, no open calls** (the master list's Band A row,
2026-09-29). Light rail passed the three-part test against San Diego, Calgary
and Edmonton (`docs/tram_city_list.md`): 40% of the track in tunnel or on
bridges, 58% mapped light rail, every 7–8 min by day.

---

## ✅ Rail — Skyss's GTFS through Entur, keyless, NLOD

`https://storage.googleapis.com/marduk-production/outbound/gtfs/rb_sky-aggregated-gtfs.zip`
— the same Entur host and licence as Ruter's feed for Oslo. Cached at
`data/bergen/raw/rb_sky-aggregated-gtfs.zip` (84.5 MB, 2026-09-27). **A HEAD
request is still not a probe here**: Google Storage answers HEAD with size 0
(Oslo's config). Use a ranged GET.

### ⚠️ Bybanen is route type `901`, and Oslo's filter reads `401, 902`

| Route type | Routes | What |
|---|---|---|
| `704` | 372 | local bus |
| `1004` / `1008` | 32 / 27 | ferries |
| **`901`** | **2** | **Bybanen**: `SKY:Line:1` "Bergen lufthavn Flesland – Lagunen – Byparken", `SKY:Line:2` "Bybane Fyllingsdalen" |
| `700` | 2 | bus |

**Copy Oslo's `ROUTE_TYPES_RAIL = ("401", "902")` and step 1 draws nothing.**
It already happened once: the tram audit's first frequency run on this feed
filtered 900/902 and returned `routes: []` (2026-09-29, `freq.log`); the
second run read `901`. Set `ROUTE_TYPES_RAIL = ("901",)` and
`ROUTE_IDS = ["SKY:Line:1", "SKY:Line:2"]`. Ferries are not drawn (Oslo's
call).

### Stations — measured 2026-09-29 on the cached feed

| | |
|---|---|
| Platforms served | **68**, `parent_station` on every one |
| Parent stop places | **34** (Line 1: 28, Line 2: 10, 4 shared) |
| **By name** | **33** — `Bergen busstasjon` is two stop places 70 m apart (`NSR:StopPlace:62129`, `NSR:StopPlace:30865`) |
| Median nearest-neighbour gap | **624 m** by name, UTM 31N (the test's 622 m was measured on OSM) |
| Inside kommune 4601 | **all**, the airport (Bergen lufthavn Flesland) included: **no scope call** |

Oslo's step 1 collapses by name, so it will produce **33**. The three
pairs under 300 m, for Oslo's alias gate (an alias merges only what was
looked at, never a rule):

| Pair | Gap | Lean |
|---|---|---|
| **Byparken / Kaigaten** | **73 m** | Line 1's and Line 2's city termini, a block apart. **Look at it at build**: two stops of one hub, or one station under two names? Oslo kept Stortinget / Stortorvet (142 m) as two; it aliased only a 12 m pair. The lean is to keep both, since they are distinct named stops served by different lines. |
| Nesttun sentrum / Nesttun terminal | 254 m | two stops, keep |
| Bergen busstasjon / Nonneseter | 258 m | two stops, keep |

### Frequency — Skyss's GTFS, Friday 2026-10-02 (the audit's second run)

Both lines: **8 per hour (about every 7 min) 07–19** at the median stop, 6
per hour (10 min) 19–22. Purpose-built track, so frequency was never a gate.

### ⚠️ Colours — neither source tells the lines apart

The feed carries **no `route_color`**. OSM's four route relations (7271947,
7271948, 14933911, 14933918) carry **one colour for both lines, `#BF4525`**.
Oslo's shape exactly: the map assigns its own palette. **Build-time call**:
Line 1 keeps `#BF4525`; Line 2 takes a colour that clears
`pipeline/linecolour.py`'s Delta-E check, as Oslo's Trikk 15 did (a line with
no published colour). Do not invent a "Skyss colour" for Line 2.

### Names for the legend and the on-map labels

OSM's relations name them **"Bybanen linje 1"** (Byparken – Bergen lufthavn)
and **"Bybanen linje 2"** (Kaigaten – Fyllingsdalen). The feed's
`route_short_name` is `1` / `2`, so `LINE_NAMES` needs the mode word, as
Oslo's `"T-bane 1"` does: **"Bybanen 1"**, **"Bybanen 2"**. The page calls
it light rail, never metro.

### Shapes

`shapes.txt` is present (Line 1: 9 shape ids, Line 2: 6). `feed_info.txt`
names Entur and declares **no validity window**, as Ruter's does, so the
fetch date pins the snapshot (`GTFS_SELF_ATTESTS = False`).

---

## ✅ Business leg — Oslo's chain, run on Bergen by the screen

The screen (2026-09-27, `data/_staging_scratch_2026-09-27/second_cities/norway/bergen_biz.log`)
ran the Oslo step 2 chain on `beliggenhetsadresse.kommunenummer == "4601"`:

| Stage | Rows |
|---|---|
| after `filter_to_storefront()` | 4,118 |
| parent found | 99.2% |
| after dropping parents bankrupt or being wound up (39 + 24 + 13) | 4,043 |
| **parent is `ENK`** (sole trader) | **1,151 (28.5%)**; Oslo 31.3% |
| after the catch-all exclusion: **`96.990` dropped**, 284 rows (7.0%), employees 8%, ENK 83% | 3,759 |
| Kartverket's address file for 4601: 77,161 addresses | exact 3,594 (95.6%), letter 21 (0.6%), unmatched 144 (3.8%) |
| **placed** | **3,615 (96.2%)** |
| trade name shown | 2,706 (74.9%); every sole trader shows the address, by rule |

**The catch-all verdict carries over on Bergen's own numbers**: `96.990` is
83% sole traders and 8% with employees (Oslo: 87% / 5%). The five retail
catch-alls are kept, as in Oslo: `CATCH_ALL_EXCLUDE = ("96.990",)`. The
unmatched rows lean away from sole traders (3.5% ENK against 24.3% overall),
so the join does not selectively drop home businesses.

⚠️ **The register files are NATIONAL and SHARED with Oslo**:
`data/norway/raw/underenheter.csv.gz` and `enheter.csv.gz`, cached
**2026-09-23** (Pacific time; 01:30 UTC on 2026-09-24, which is 2026-09-24
in Norway and is the date the page states - dates follow the city's own time
zone, DECISIONS 2026-09-29). Refreshing them changes Oslo's inputs, and Oslo's next drift
check reports drift that is not Oslo's. **Build-time call: build on the
cached 2026-09-23 edition** (six days old; the currency rule's clock is five
years) and record the date on the page, **or** refresh deliberately and re-run
Oslo's drift check as a data refresh in the same landing. The first needs no
owner call; the second touches a built city.

⚠️ **Bergen's address file is per kommune and NOT shared**:
`Basisdata_4601_Bergen_4258_MatrikkelenAdresse_CSV.zip` (4.07 MB) is already
cached at `data/bergen/raw/`. EPSG:4258, read as lat/lon directly
(`norway.py`).

**Personal exposure: `check_personal_exposure.py bergen` is load-bearing**,
as for Oslo. The name rule is the join to the parent (`overordnetEnhet`) and
suppression where the parent is `ENK`. **The sub-unit's own
`organisasjonsform` never shows `ENK`** (Oslo's trap, pinned below).

---

## Rings — the spacing rule gives the standard edges

**624 m median gap, over the ~550 m line** (`docs/ring_rules.md`): the
standard `RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]`. **Oslo's config
carries the halved edges** (465 m); copying them is the third quiet error.

Measured on the screen's 3,615 placed points against the 33 stations
(UTM 31N):

| Within | Storefronts | Share |
|---|---|---|
| 0.1 mi | 440 | 12.2% |
| 0.2 mi | 1,078 | 29.8% |
| 0.3 mi | 1,505 | 41.6% |
| **0.6 mi** | **2,119** | **58.6%** — retail 1,204, food 484, personal services 431 |

58.6% sits between Calgary (40.8%) and Riga (77.9%): Bybanen runs south from
the centre, and the kommune reaches north to Åsane with no rail.

---

## Coordinates and CRS

- **EPSG:25831** (ETRS89 / UTM 31N). Bergen's stations lie at 5.23–5.36° E;
  zone 31 is 0–6° E. **Oslo's 25832 is not Bergen's** (the invariant: the
  projected CRS is per city, never copied). Norway's national grid, UTM 33,
  is a country-wide convenience, not Bergen's zone either.
- **Bounding box** for the sanity bounds: kommune 4601's `avgrensningsboks`
  is 60.176–60.536 N, 5.145–5.687 E (Kartverket's kommuneinfo). Add ~0.02°.
- **Boundary**: `norway.KOMMUNE_BOUNDARY_URL_TEMPLATE` with `4601`.
- **`NEIGHBOUR_KOMMUNER = {}`**: no station sits outside. Step 1 should still
  exit if one ever does.

---

## ✅ Licences — all read for Oslo

| Source | Licence | Notice |
|---|---|---|
| Brønnøysund (sub-units and units) | NLOD | its own line |
| Kartverket, Matrikkelen Adresse (4601) and the kommune boundary | CC BY 4.0 | its own line |
| Skyss GTFS via Entur | NLOD (Entur's) | its own line |
| OSM route relations (line colour only) | ODbL | the basemap's credit already covers the attribution; as Oslo |

**No new read.** The credits are Oslo's with the operator's name changed
(Skyss, not Ruter). NLOD and CC BY 4.0 are two licences and two lines, never
one credit (Oslo's brief).

---

## Build-time calls — none needs the owner before starting

1. **The register edition**: cached 2026-09-23 (recommended), or a refresh
   with Oslo's drift re-run.
2. **Line 2's colour**, through `linecolour.py`.
3. **Byparken / Kaigaten**: two stations or an alias (lean: two).

**Flag for the cleanup role (held macro-map work)**: Bergen is the first
Norwegian **light-rail** city, so its dot takes the light-rail network colour
once network-type colours land. Oslo is metro.

## Still unknown — the honest list

- The register edition the build will use (call 1).
- The ENK share and placed count on a refreshed register, if one is taken.

```brief-checks
[
  {
    "id": "skyss-gtfs-bybanen-is-route-type-901",
    "claim": "Skyss's GTFS via Entur has exactly two route_type 901 routes (Bybanen lines 1 and 2). Oslo's ROUTE_TYPES_RAIL = (401, 902) would draw NOTHING here - the tram audit's first frequency run did exactly that and returned routes: []",
    "kind": "gtfs_route_type_counts",
    "url": "https://storage.googleapis.com/marduk-production/outbound/gtfs/rb_sky-aggregated-gtfs.zip",
    "expect": {"901": 2, "401": 0, "902": 0}
  },
  {
    "id": "skyss-gtfs-bybanen-stations",
    "claim": "Bybanen: 68 platforms, parent_station on every one, 34 parent stop places (33 by name - Bergen busstasjon is two stop places 70 m apart), median gap over 550 m so the standard rings apply",
    "kind": "gtfs_stations",
    "url": "https://storage.googleapis.com/marduk-production/outbound/gtfs/rb_sky-aggregated-gtfs.zip",
    "route_types": ["901"],
    "expect_parent_station_populated": true,
    "expect_platforms": 68,
    "expect_stations": 34,
    "crs": "EPSG:25831",
    "station_spacing_median_m_min": 550
  },
  {
    "id": "skyss-gtfs-has-shapes-no-window",
    "claim": "The feed ships shapes.txt (both lines drawn from the operator's geometry) and a feed_info.txt that names Entur, as Ruter's does",
    "kind": "gtfs_files",
    "url": "https://storage.googleapis.com/marduk-production/outbound/gtfs/rb_sky-aggregated-gtfs.zip",
    "present": ["routes.txt", "trips.txt", "stops.txt", "stop_times.txt", "shapes.txt", "feed_info.txt"],
    "absent": []
  },
  {
    "id": "skyss-gtfs-declares-no-window",
    "claim": "feed_info.txt declares no feed_end_date, so the fetch date pins the snapshot (GTFS_SELF_ATTESTS = False, as Oslo)",
    "kind": "gtfs_feed_window",
    "url": "https://storage.googleapis.com/marduk-production/outbound/gtfs/rb_sky-aggregated-gtfs.zip",
    "expect": "absent"
  },
  {
    "id": "bergen-is-utm-31-not-oslos-32",
    "claim": "Bergen's centre (5.32 E) is in UTM zone 31, so the projected CRS is EPSG:25831 (ETRS89) - Oslo's 25832 must not be copied. The check derives the WGS84 twin, 32631",
    "kind": "utm_zone_from_longitude",
    "lon": 5.32,
    "expect": "EPSG:32631"
  },
  {
    "id": "bergen-address-bulk-file",
    "claim": "Kartverket publishes kommune 4601's address register in bulk, keyless, ~4 MB (77,161 vegadresser) - the join that placed 96.2% of the screen's storefronts",
    "kind": "http_ok",
    "url": "https://nedlasting.geonorge.no/geonorge/Basisdata/MatrikkelenAdresse/CSV/Basisdata_4601_Bergen_4258_MatrikkelenAdresse_CSV.zip",
    "min_bytes": 3000000
  },
  {
    "id": "bergen-kommune-boundary",
    "claim": "Kartverket's kommuneinfo serves kommune 4601's boundary through the template in pipeline/countries/norway.py",
    "kind": "http_contains",
    "url": "https://api.kartverket.no/kommuneinfo/v1/kommuner/4601/omrade",
    "present": ["coordinates", "4601"]
  },
  {
    "id": "brreg-enk-visible-on-the-parent-in-4601",
    "claim": "THE PRIVACY GUARD: the sole-trader form ENK is visible on the parent enhet in kommune 4601 (28.5% of the screen's storefronts). A sub-unit's own organisasjonsform never shows ENK",
    "kind": "http_contains",
    "url": "https://data.brreg.no/enhetsregisteret/api/enheter?kommunenummer=4601&organisasjonsform=ENK&size=1",
    "present": ["ENK"]
  },
  {
    "id": "brreg-subunit-bulk-csv-serves",
    "claim": "The national sub-unit CSV (norway.SUBUNITS_URL) still serves without a key; the cached copy is shared with Oslo and dated 2026-09-23",
    "kind": "http_ok",
    "url": "https://data.brreg.no/enhetsregisteret/api/underenheter/lastned/csv",
    "min_bytes": 1000000
  }
]
```
