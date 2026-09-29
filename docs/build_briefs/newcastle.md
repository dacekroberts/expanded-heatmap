# Newcastle (Tyne and Wear) — build brief

**Screened 2026-09-28 (staging, the large-transit gap's re-screen); Band B,
food only (owner). Brief written the same day.** Run
`python scripts/brief_check.py newcastle` before writing any code. The trail:
`DECISIONS.md` 2026-09-28 "Moved Newcastle into Band B, food only", and the
United Kingdom row in `docs/global_country_shortlist.md` Tier 4.

⚠️ **One-bucket city: food, with food retail, on London's method.** Read
`docs/build_briefs/london.md` (its "Measured at the build" box) and London's
DECISIONS entries of 2026-09-28 first: the taxonomy, the licence, the
personal-information rule, the trading-as rule and postcode-centroid
placement are all settled there and carry over unchanged. This brief records
only what differs.

---

## The one-line summary

**The same FSA register as London, across the five districts the Metro
serves: 6,673 food storefronts, keyless and under the OGL. The work is
placement (a lower point share than London's), scoping to five authorities
that the FSA files under a wider region, and one rail-shape call.**

---

## Business leg — the FSA food-hygiene register (FHRS), five authorities

Measured 2026-09-28 on the FSA API (`/Establishments?...&pageSize=1` per
authority and type; every authority's 14 types sum to its total).

| Authority | Code | Total | Food service¹ | Food shops² | Storefronts | Bulk XML |
|---|---|---|---|---|---|---|
| Newcastle upon Tyne | 416 | 2,713 | 1,445 | 725 | **2,170** | 2,667,531 B |
| Sunderland | 429 | 2,324 | 948 | 593 | **1,541** | 2,276,214 B |
| Gateshead | 410 | 1,647 | 722 | 469 | **1,191** | 1,656,459 B |
| North Tyneside | 417 | 1,488 | 644 | 450 | **1,094** | 1,557,979 B |
| South Tyneside | 427 | 1,039 | 477 | 200 | **677** | 1,090,662 B |
| **Tyne and Wear** | | **9,211** | **4,236** | **2,437** | **6,673** | **9,248,845 B** |

¹ Restaurant/Cafe/Canteen 2,114 · Takeaway/sandwich shop 1,222 · Pub/bar/nightclub 900.
² Retailers - other 2,147 · Retailers - supermarkets/hypermarkets 290.

Out of scope, as in London (`pipeline/taxonomies/fsa_businesstype.py`):
Mobile caterer 540 · Other catering premises 623 · Hospitals/Childcare/Caring
524 · School/college/university 561 · Manufacturers/packers 122 ·
Hotel/B&B 74 · Distributors/Transporters 78 · Importers/Exporters 8 ·
Farmers/growers 8.

**Currency:** four files republished 2026-09-17, Sunderland 2026-09-10.

**Download:** five XMLs, **9,248,845 bytes** in total (HEAD, 2026-09-28),
`https://ratings.food.gov.uk/OpenDataFiles/FHRS<code>en-GB.xml`. **Needs the
owner's OK.**

### ⚠️ Scope is five authority codes, not a region

London's `fetch_sources.py` filters the FSA's authority list on
`RegionName == "London"`. **The five Tyne and Wear authorities sit in a wider
North East region** (with Durham, Northumberland and the Tees Valley), so
select them by `LocalAuthorityIdCode` (410, 416, 417, 427, 429) and assert
there are exactly five. The same applies to Code-Point Open: London kept
district codes starting `E09`; here keep exactly `E08000021` (Newcastle),
`E08000022` (North Tyneside), `E08000023` (South Tyneside), `E08000024`
(Sunderland) and `E08000037` (Gateshead), the GSS codes on the OSM boundaries.

💡 **This is the second FSA city and Glasgow is the third.** Lifting London's
FSA fetch, parse and centroid tier into one shared module, parameterised by
authority codes and district codes, is the build session's call on
measurable grounds (three cities, one register); London's drift check must
stay clean afterwards.

---

## Placement — a lower point share than London's

A sample of each authority's first page (up to 100 rows per storefront type,
2,290 rows; **the API's default order, not random**, and it leans towards
5-rated premises):

| | Share | London at the build |
|---|---|---|
| FSA point | **85.0%** (1,947) | 91.0% |
| No point, full postcode → a Code-Point centroid | **10.3%** (235) | 3.9% placed |
| No point, outward code only (a private address, never placed) | **4.4%** (101) | |
| No point, no postcode | 0.3% (7) | |

By authority, the point share runs from **77.8% (Newcastle upon Tyne)** to
90.6% (Gateshead). London's owner-approved centroid tier would take the
projected placed share to about 95%. **Code-Point Open** is the same product
and edition London uses (14,461,176 bytes, 2026-08, OGL, its Ordnance Survey
notice already approved and displayed on London's page); the build re-uses or re-fetches it with the owner's
OK, and the notice extends to this page.

---

## Rail — Tyne and Wear Metro, OpenStreetMap, measured 2026-09-28

| Mode | Network tag | Relations | Refs | Colours |
|---|---|---|---|---|
| `light_rail` | Tyne and Wear Metro (operator Nexus) | 4 (two directional pairs) | **2**: Green (Airport ↔ South Hylton), Yellow (St James ↔ South Shields, via the coast) | Green `#009933`, Yellow `#d39f06` |

**60 stations**: the four relations' stop members give 61 distinct names, one
of them a duplicate ("St James" and "St. James"). That matches Nexus's own 60.
Every station is inside the five districts. The map labels read "Green line"
and "Yellow line", the public names.

🚨 **The rail-shape call: the Sunderland branch.** Between Pelaw and
Sunderland the Metro runs on Network Rail track shared with Northern's trains.
Beyond Sunderland to South Hylton it is Metro-only. (Both from general
knowledge, not measured here.) **The recommendation is to keep every Metro
station.** The whole route runs as the Metro, with Metro stations and Metro
frequencies, and Newcastle sits in B as a metro, not in T. Read `docs/sub_transit_line_filters.md` before confirming. The
two Northern relations in the bbox (NR02 to Metrocentre) are national rail,
not the Metro, and stay out.

⚠️ **The coast loop is one ref drawn both ways.** Yellow's relations run St
James → South Shields round the coast. Collapse them on `ref` (London's
per-line longest-relation rule), and check that the loop through Monument is
not drawn twice.

---

## Scope, CRS, region

- **Scope:** the five metropolitan districts of Tyne and Wear, the union of
  OSM boundaries 142282 (Newcastle upon Tyne), 116279 (Sunderland), 140462
  (Gateshead), 142245 (North Tyneside) and 140390 (South Tyneside), all
  `admin_level=8`. No Tyne and Wear administrative relation exists (it is a
  ceremonial county).
- **Page name: an owner call.** "Newcastle" (the master list's name) or
  "Newcastle (Regional)", Lille's precedent for a page covering several
  authorities.
- **CRS:** British National Grid **EPSG:27700**, as London; UTM 30N
  (EPSG:32630) is the derived fallback.
- **Region:** `"region": "Europe"`.

## Still unknown

- 🚨 **The Sunderland branch**: the recommendation above, the owner's call.
- ⚠️ **Ring coverage** at 0.6 mi: unmeasured. The Metro's outer stations
  (Airport, the coast, South Hylton) are far apart.
- ⚠️ **Placement** from the full files; the sample is page 1 only.
- ⚠️ **Canteens** inside Restaurant/Cafe/Canteen: London's name test (2.5%,
  a lower bound).
- ⚠️ **Page name** (above) and the download OK (9.2 MB).
- ⚠️ **Personal exposure**: `check_personal_exposure.py newcastle` after
  step 2, and the trading-as rule.

```brief-checks
[
  {
    "id": "newcastle-fsa-open-data-files",
    "claim": "The FSA's open-data page lists a bulk XML for each Tyne and Wear authority (410 Gateshead, 416 Newcastle upon Tyne, 417 North Tyneside, 427 South Tyneside, 429 Sunderland). The build downloads these, not the API",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/open-data",
    "present": ["FHRS410en-GB.xml", "FHRS416en-GB.xml", "FHRS417en-GB.xml", "FHRS427en-GB.xml", "FHRS429en-GB.xml"]
  },
  {
    "id": "newcastle-fsa-terms-name-ogl",
    "claim": "THE LICENCE POSITION RESTS ON THIS PAGE, as London's does: the FHRS terms name the Open Government Licence. If it stops naming the OGL, re-read before publishing",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/terms-and-conditions",
    "present": ["Open Government Licence"]
  },
  {
    "id": "newcastle-osm-metro-refs",
    "claim": "OSM carries the Tyne and Wear Metro as four light_rail relations with two refs, Green and Yellow, in the Tyne and Wear bbox",
    "kind": "osm_route_refs",
    "bbox": [54.78, -1.75, 55.10, -1.30],
    "routes": ["light_rail"],
    "expect_relations": {"light_rail": 4},
    "expect_refs": {"light_rail": 2},
    "require_refs": {"light_rail": ["Green", "Yellow"]}
  },
  {
    "id": "newcastle-projected-crs-fallback",
    "claim": "Newcastle's derived UTM zone is 30N (EPSG:32630), the fallback if the build does not use British National Grid EPSG:27700",
    "kind": "utm_zone_from_longitude",
    "lon": -1.6178,
    "expect": "EPSG:32630"
  }
]
```
