# Amsterdam — build brief

**Step 0 measured 2026-09-24.** Run `python scripts/brief_check.py amsterdam`
before writing any code. **Both layers come from the city's own API and both
already carry coordinates — no geocoder and no join.**

---

## The one-line summary

**Food from a live hospitality-permit register (4,092 permits, points, trade
names); shops from the BAG's use class (10,898 shop units in use, points, no
names) — with the vacancy rate disclosed on the page, and retail and personal
services in ONE category because the BAG cannot split them.** Owner's decision
2026-09-24.

---

## Layer 1 — food service: `horeca/exploitatievergunning`, MEASURED

| | |
|---|---|
| **Endpoint** | `https://api.data.amsterdam.nl/v1/horeca/exploitatievergunning/` — the city's DSO API, HAL JSON. Page with `_pageSize` (5,000 works) and follow `_links.next`; send **`Accept: */*`** or the root refuses |
| Rows | **4,092** on the evening of 2026-09-24 — **4,094** that morning: a live register. `statusVergunning` *Verleend* 4,074, *Deels verleend* 18 |
| **Currency** | every `einddatum` falls in 2026–2031 — **expired permits leave the register**, the only register in its band that drops closed premises |
| Location | `locatie`, a Point in **RD New (EPSG:28992)**, 96.7% filled; also `adres` and `postcode` |
| Name | `zaaknaam` — the trade name (*"Som Tam Thai"*) |
| Activity | `zaakCategorie` (16 values) and `zaakSpecificatie` |
| **Control** | **0.89×** OSM restaurants (1,806 vs 2,040), **0.95×** all food and drink. **Fast food is thin** (231 vs 712) — plausibly exempt from the permit |

### Taxonomy — `zaakCategorie`, first cut

| Bucket | `zaakCategorie` | Permits |
|---|---|---|
| Food service | *Restaurant* 1,701 · *Café* 870 · *Alcoholvrij* 326 · *Fastfood* 231 · *Eethuis* 93 · *Restaurant/Café met zaalverhuur* 18 · *Mengformule* 5 | **3,244** |
| **Decide at build** | *Additionele horeca* 318 (horeca inside another business — may double-count a BAG shop) · ***Onbekend* 241 (the catch-all, 5.9%)** · *Coffeeshop* 127 (cannabis sales: food, retail or out) · *Nachtzaak* 28 · *Culturele horeca* 17 · *Sociëteit* 13 | 744 |
| Out | *Hotel* 72 · *Zalenverhuur* 32 (hall hire) | 104 |

---

## Layer 2 — shops: BAG units with use class *winkelfunctie*, MEASURED

| | |
|---|---|
| **Endpoint** | `https://api.data.amsterdam.nl/v1/bag/verblijfsobjecten/?gebruiksdoel.omschrijving=winkelfunctie` — the city's copy of the national BAG. **The server-side filter is real**: a nonsense value returns 0 |
| Rows | **11,607** shop-class units, every one the current version. **10,898 are *Verblijfsobject in gebruik*** — keep; 575 *gevormd* (planned) and 134 *Verbouwing* (being rebuilt) — out |
| Mixed use | **9,837 (90%) are shop-only**; 1,061 carry a second use class as well (dwelling, office…) — in or out at build |
| Location | `geometrie`, a Point in RD New, on **100%** of the 10,898 |
| Address | `heeftHoofdadresId` → the BAG address. `standvastgoed/gebouwen` (587,741 rows, BAG-keyed) carries address, use class and point in one row if a single read is easier |
| Name / activity | **None.** `feitelijkGebruik` (actual use) is empty on all 10,898 |
| **Control** | **1.77×** OSM's 6,150 `shop=*` in the gemeente |
| Category | **one: shops and services.** Retail and personal services share the class, so the page says the split other cities show is not available here |

### 🚩 Vacancy — the owner's condition for using the BAG

**Not filterable per unit from open data.** The property snapshot has no
occupancy field, energy use is published per neighbourhood only, and the
per-unit sources (Locatus, the KvK) are paid or staff-only. **The rate is
published**: the city's statistics (`bbga`, indicator `BHLOCVKPLEEGSTAND_P`,
**source Locatus**, 1 January 2026) count **660 vacant of 14,314 sales points —
4.6%**; by district 0–7% (Centrum 4.0%, 208 of 5,001). **The page discloses
it**, along the lines of *"about 5% of shop units are empty (Locatus, 2026)"*.

### De-duplication

A takeaway or an *Additionele horeca* permit can sit in a shop-class unit, so
the same premises would appear in both layers. **De-duplicate by address**
(the permit's `adres` + `postcode` against the unit's BAG address) before
rendering, and record how many.

---

## Coordinates

**Nothing to do.** Both layers carry RD New points. Project to **UTM 31N
(EPSG:32631)** for the ring geometry, as every city projects to its own zone.

## 🚇 Rail

OSM, counted 2026-09-24, network *Stadsvervoer Amsterdam*: `route=subway`
**50** (`#29AB4D`), **51** (`#F69931`), **52** (`#00ADEF`), **53** (`#FF0000`),
**54** (`#FCFB05`). `route=tram`: **18 refs** — 1, 2, 4, 5, 6, 7, 12, 13, 14,
17, 19, 20, 24, 25, 26, 27, 29 and *EMA* (the museum tramway, out); 9 carry a
colour, and 20 has no network tag. Which are current GVB service is checked at
build. GVB / OVapi GTFS not probed — `osm-rail` applies. NS commuter rail is
out, as everywhere.

⚠️ **Trams in or out is the owner's call at build.** The standing test
(`docs/excluded_categories.md`) leaves trams out where they overlay a metro,
as in Milan — but Amsterdam's metro barely enters the canal ring (only line 52
crosses the centre), and Oslo's trams were kept on the owner's call.

## Scope

The **gemeente** (Weesp included since 2022) — both layers are gemeente-only.
⚠️ Some stations lie outside it — line 53's stops in **Diemen** at least,
ASSERTED — so rings there are partial; Oslo's *kommune only* call is the
precedent. Check which at build.

## ✅ Licences — both READ 2026-09-24

- **BAG — PERMITTED.** The Kadaster's terms govern the fields used (use class,
  status, location, address — all national BAG fields): *"geldt de Creative
  Commons Public Domain Mark v1.0"*
  (`kadaster.nl/-/welke-voorwaarden-gelden-er-voor-het-gebruik-van-bag-data-7c-algemeen`);
  PDOK's national geo-register record (updated 2026-09-23) agrees — *"Geen
  beperkingen"*, *"Er zijn geen condities voor toegang en gebruik"*. Amsterdam's
  copy is **SILENT** (`Licentie: -`, `license.name: ""`, no key in the schema)
  and incorporates nothing. **Use only national BAG fields** — the city's
  "BAG-plus" additions carry no licence. Fetching the same fields from PDOK
  would put the data directly under the Kadaster; either host works. **MUST
  DISPLAY: nothing** — a credit is a courtesy.
- **Hospitality permits — SILENT; displayed as CC BY 4.0 (owner's call
  2026-09-24).** The live schema has **no `license` key** — 55 of the city's 141
  schemas fill one in, so the omission is specific to this dataset — and the API
  says `Licentie: -`. The city's CC BY statement (*"ams:license": "cc-by"*, no
  version) lived in its **retired** catalogue record, live on 2023-09-26 and 404
  by 2026-01-18; data.overheid.nl's copy mapped it to 4.0. Dutch law puts
  government databases outside database right unless expressly reserved
  (Databankenwet art. 8(2); Auteurswet art. 15b), and no reservation was found.
  **Both readings permit the use; the owner chose the one that satisfies both.
  MUST DISPLAY**: credit **Gemeente Amsterdam**, link **CC BY 4.0**, and **state
  that the permits were filtered, bucketed and density-mapped**. No wording
  prescribed.
- **MUST NOT SAY** (both): nothing implying endorsement by the city or the
  Kadaster; **don't present the map as the official permit record** (the
  retired description said no rights derive from the data); **no city logo**.
- **MUST DO, later**: the city plans to make an API key **mandatory** (optional
  since mid-September 2026, no date set). Registering is a form —
  `keys.api.data.amsterdam.nl/clients/v1/`, name, e-mail, organisation — an
  **owner's act** when it becomes required; this project never fills it in.
  An access condition, not a licence term.

## Privacy

The permits carry **trade names**, and a sole trader's trade name can be a
person's name. Run `check_personal_exposure.py`; *Onbekend* is the first place
to look. The BAG layer carries no names.

## Region

`"region": "Europe"`.

## Still unknown

- ✅ ~~The band move~~ — **Band A, owner's call 2026-09-24**, after both licences read.
- ⚠️ The API key — optional today, mandatory from an unset date; the owner registers.
- ⚠️ Trams in or out; which stations fall outside the gemeente.
- ⚠️ *Additionele horeca*, *Onbekend*, *Coffeeshop*, *Nachtzaak* — `premises-taxonomy`.
- ⚠️ The 1,061 mixed-use BAG units; the de-duplication count.
- ⚠️ The `bbga` licence — the vacancy figure is quoted, not republished.

```brief-checks
[
  {
    "id": "amsterdam-horeca-live",
    "claim": "The hospitality-permit register answers keyless on the city's API - ~4,090 live permits, the food layer",
    "kind": "http_contains",
    "url": "https://api.data.amsterdam.nl/v1/horeca/exploitatievergunning/?_pageSize=1&_count=true",
    "present": ["totalElements", "zaakCategorie", "zaaknaam"]
  },
  {
    "id": "amsterdam-bag-shop-filter",
    "claim": "The city's BAG copy filters server-side to use class winkelfunctie - 11,607 units, 10,898 in use, the shop layer",
    "kind": "http_contains",
    "url": "https://api.data.amsterdam.nl/v1/bag/verblijfsobjecten/?gebruiksdoel.omschrijving=winkelfunctie&_pageSize=1&_count=true",
    "present": ["totalElements", "winkelfunctie"]
  },
  {
    "id": "amsterdam-vacancy-source",
    "claim": "The city's statistics publish the vacant-sales-points rate, sourced from Locatus - the figure the page discloses",
    "kind": "http_contains",
    "url": "https://api.data.amsterdam.nl/v1/bbga/indicatoren_definities/?variabele=BHLOCVKPLEEGSTAND_P",
    "present": ["Locatus", "leegstaand"]
  },
  {
    "id": "amsterdam-kvk-staff-only",
    "claim": "The full business register (hr_kvk) is gated to city-staff scopes - why the BAG is the shop layer",
    "kind": "http_contains",
    "url": "https://schemas.data.amsterdam.nl/datasets/hr_kvk/dataset",
    "present": ["FP/MDW"]
  },
  {
    "id": "amsterdam-bag-licence-pdm",
    "claim": "The Kadaster puts BAG data under the Public Domain Mark - no conditions on the shop layer",
    "kind": "http_contains",
    "url": "https://www.kadaster.nl/-/welke-voorwaarden-gelden-er-voor-het-gebruik-van-bag-data-7c-algemeen",
    "present": ["Public Domain Mark"]
  },
  {
    "id": "amsterdam-horeca-schema-no-licence",
    "claim": "The permits' published schema still declares no licence - the SILENT position the page answers with a CC BY 4.0 credit; if a licence appears, re-read it",
    "kind": "http_contains",
    "url": "https://schemas.data.amsterdam.nl/datasets/horeca/dataset",
    "present": ["exploitatievergunning"],
    "absent": ["\"license\""]
  },
  {
    "id": "amsterdam-osm-metro",
    "claim": "OSM carries Amsterdam's five metro lines 50-54 as subway relations - the geometry source",
    "kind": "osm_route_refs",
    "bbox": [52.28, 4.72, 52.45, 5.08],
    "routes": ["subway"],
    "require_refs": {"subway": ["50", "51", "52", "53", "54"]}
  },
  {
    "id": "amsterdam-projected-crs",
    "claim": "Amsterdam projects to UTM 31N",
    "kind": "utm_zone_from_longitude",
    "lon": 4.90,
    "expect": "EPSG:32631"
  }
]
```
