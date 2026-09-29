# Glasgow — build brief

**Screened 2026-09-28 (staging, the large-transit gap's re-screen); Band B,
food only (owner, B over N). Brief written the same day.** Run
`python scripts/brief_check.py glasgow` before writing any code. The trail:
`DECISIONS.md` 2026-09-28 "Glasgow to Band B, food only".

> **Measured at the build, 2026-09-28 (build session, `worktree-glasgow`)** -
> these supersede the screen's figures below where they differ:
> - **Govan is not missing.** Each Subway relation carries all 15 stations:
>   the loop starts and ends at Govan, a `stop_entry_only` and a
>   `stop_exit_only` member, which a count of `stop` roles alone misses. No
>   station is added by hand.
> - **Home businesses at flats**: 185 of 4,958 storefronts have an address line
>   starting "Flat", mostly home bakers and cooks listed as
>   Restaurant/Cafe/Canteen WITH the FSA's point, a few under a person's own
>   name; 5 more are childminders listed as cafés. Never placed (owner; the
>   flat rule reaches London too, `pipeline/fsa.py`).
> - **Coordinates**: 55 of the rest (1.2%) have no point; no centroid tier
>   (owner). 4,708 storefronts placed; **42.3% within a ring**.
> - **Licence** (`licence-read`): OGL v3 by the FSA's terms, and FSS states v3
>   for its own copy of the same data; credit "Food Standards Scotland, Food
>   Hygiene Information Scheme data, via the Food Standards Agency" (owner),
>   notice 61.

⚠️ **One-bucket city: food, with food retail, on London's method.** Read
`docs/build_briefs/london.md` (its "Measured at the build" box) and London's
DECISIONS entries of 2026-09-28 first: the taxonomy, the personal-information
rule, the trading-as rule and postcode-centroid placement carry over. **What
does not carry over automatically is the licence and the credit wording**:
Glasgow is on Scotland's scheme (below).

---

## The one-line summary

**The smallest network in the gap (15 stations on one loop) over one
authority's FSA file: 4,958 food storefronts, 99% with a point. The work is
Scotland's licence and wording, one station OSM's relations omit, and a page
honest about how little of the city a 15-station loop reaches.**

---

## Business leg — the FSA register, Scotland's FHIS scheme

Measured 2026-09-28 on the FSA API (per-type counts sum to the total).

| | |
|---|---|
| **Authority** | Glasgow City, code **776**, `SchemeType` 2 (FHIS), republished 2026-09-15 |
| **Premises** | **6,632** |
| Food service | **3,655**: Restaurant/Cafe/Canteen 2,187 · Takeaway/sandwich shop 1,109 · Pub/bar/nightclub 359 |
| Food shops | **1,303**: Retailers - other 1,150 · Retailers - supermarkets/hypermarkets 153 |
| **Storefronts** | **4,958** |
| Out of scope | Mobile caterer 425 · Other catering 348 · Hospitals/Childcare/Caring 342 · School/college/university 202 · Manufacturers/packers 139 · Hotel/B&B 110 · Distributors/Transporters 84 · Importers/Exporters 23 · Farmers/growers 1 |
| Coordinates | **99.0%** (495 of 500, first page per storefront type, the API's default order): 1 full postcode, 1 outward code, 3 with none |
| Bulk file | `https://ratings.food.gov.uk/OpenDataFiles/FHRS776en-GB.xml`, **6,028,925 bytes** (HEAD). **Needs the owner's OK** |

**The same 14 business types as England's**, so `fsa_businesstype` maps
Glasgow unchanged. The difference is the rating: FHIS gives **"Pass" or
"Improvement Required"**, not 0-5 (the sample: Pass 498, "Pass and Eat Safe"
2). The project shows no rating, so this matters only for wording (below).

**Placement barely arises**: 99% carry the FSA's point. Code-Point Open covers
Great Britain, so London's centroid tier would work (district code
`S12000049`; check it against the edition's own code, since Glasgow's changed
in 2019), but for about 1% it may not be worth a second licence notice. **An
owner call at the build**: centroids (London's Ordnance Survey notice extends to the page) or leave
the ~1% unplaced and disclosed.

---

## Licence — the gap London's read did not cover

- `ratings.food.gov.uk/terms-and-conditions` names the **OGL** for "food
  hygiene ratings information and services". It says the business information
  is held for local authorities in England, Northern Ireland, Wales **and
  Scotland**. It does **not** mention FHIS or Food Standards Scotland.
- **The build's `licence-read` must add Food Standards Scotland's own FHIS
  pages** (`foodstandards.gov.scot`) and settle two points:
  1. **The credit.** London's reads "Food Standards Agency, UK food hygiene
     rating data". For Glasgow, is it the same dataset title, or a Scottish
     credit? The rule against using "the FHRS name" outside its imagery
     suggests the page should never call Scotland's data FHRS.
  2. **Whether any FHIS condition** (its own imagery, "Eat Safe") reaches a
     page that shows no rating.

---

## Rail — Glasgow Subway, OpenStreetMap, measured 2026-09-28

| Mode | Network tag | Relations | Ref | Colours |
|---|---|---|---|---|
| `subway` | Strathclyde Partnership for Transport (operator Glasgow Subway) | **2**: Outer Circle, Inner Circle | **1**: "Subway" | Outer `#FF6600`, Inner `#3D3D3C` |

- **One line, drawn once.** The two relations are the two directions of one
  loop. Draw a single line labelled "Subway" (the public name; "Glasgow
  Subway" in the legend) in SPT orange, never the Inner Circle's grey as a
  second line.
- 🚨 **Govan is missing.** The relations' stop members give **14 distinct
  names of the Subway's 15 stations**; Govan is not among them. London's
  precedent: add a station OSM's relations omit from its station node, and stop
  adding it once OSM carries it.
- ⚠️ **A spelling to correct**: OSM's "St Georges Cross" is signed "St
  George's Cross".

**Coverage is the page's honest limit.** Fifteen stations on a 10.5 km loop
(general knowledge) through the centre, the West End and the south bank. The
ring coverage of Glasgow City's 4,958 storefronts is unmeasured and will be
low: the city's other rail is national rail (the Argyle and North Clyde
lines), which the Subway page leaves out. **At the build**: measure the
coverage and state it on the page.

---

## Scope, CRS, region

- **Scope:** Glasgow City council area, OSM relation **1906767**
  (`admin_level=6`, GSS `S12000049`), the same area as FSA authority 776.
  The Subway lies entirely inside it.
- **CRS:** British National Grid **EPSG:27700** (covers Scotland); UTM 30N
  (EPSG:32630) is the derived fallback.
- **Region:** `"region": "Europe"`.

## Still unknown

- 🚨 **The Scottish licence read and the credit wording** (above).
- ⚠️ **Ring coverage**, likely low; to be stated on the page.
- ⚠️ **Govan's station node** and the St George's Cross spelling.
- ⚠️ **Centroids or not** for the ~1% without a point.
- ⚠️ **Canteens** inside Restaurant/Cafe/Canteen: London's name test.
- ⚠️ **Personal exposure**: `check_personal_exposure.py glasgow` after
  step 2, and the trading-as rule.
- ⚠️ **The download OK** (6.0 MB).

```brief-checks
[
  {
    "id": "glasgow-fsa-open-data-file",
    "claim": "The FSA's open-data page lists Glasgow City's bulk XML (authority 776, FHIS). The build downloads it, not the API",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/open-data",
    "present": ["FHRS776en-GB.xml"]
  },
  {
    "id": "glasgow-fsa-terms-ogl-and-scotland",
    "claim": "The FHRS terms name the Open Government Licence and say the business information is held for local authorities including Scotland's. They do not name FHIS, which is why the build's licence-read must add Food Standards Scotland's pages",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/terms-and-conditions",
    "present": ["Open Government Licence", "Scotland"]
  },
  {
    "id": "glasgow-osm-subway-refs",
    "claim": "OSM carries the Glasgow Subway as two subway relations (Inner and Outer Circle) sharing the one ref 'Subway' in Glasgow's bbox",
    "kind": "osm_route_refs",
    "bbox": [55.80, -4.40, 55.92, -4.15],
    "routes": ["subway"],
    "expect_relations": {"subway": 2},
    "expect_refs": {"subway": 1},
    "require_refs": {"subway": ["Subway"]}
  },
  {
    "id": "glasgow-projected-crs-fallback",
    "claim": "Glasgow's derived UTM zone is 30N (EPSG:32630), the fallback if the build does not use British National Grid EPSG:27700",
    "kind": "utm_zone_from_longitude",
    "lon": -4.2518,
    "expect": "EPSG:32630"
  }
]
```
