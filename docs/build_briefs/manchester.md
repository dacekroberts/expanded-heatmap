# Manchester (Regional) — build brief

**Screened 2026-10-01 (staging, the post-review UK screen); Band B, food
only. Scope approved by the owner 2026-10-01: the 7 Metrolink districts.
Build order 1 of the UK six. Builds are HELD (owner).** Run
`python scripts/brief_check.py manchester` before writing any code. The
trail: `docs/decisions_drafts/staging.md`, "The UK six approved with their
scopes", and the master list's Band B. The handoff is
`docs/handoff_uk_six_2026-10-01.md`.

> ✅ **Prose hold lifted (2026-10-02).** The prose pass and the skills
> rework have landed, which Cleanup confirmed. **Builds stay HELD** until the
> owner releases them.
>
> - Write page text to `docs/city_page_format.md` and the reworked skills,
>   starting with `add-city` step 8.
> - `scaffold_city.py`'s template is the new format. Run it for real.
> - London's, Glasgow's and Newcastle's converted bullets are the approved
>   FSA and FHIS wording, and may be reused.
> - A sentence specific to this city is a proposal, flagged in the drafts
>   file. It does not stop the build.
> - The approved-template pre-permission (CLAUDE.md, 2026-09-30) applies.
>
> The kit's "Page text" section has the rest.

⚠️ **One-bucket city: food, with food retail, on London's method and the
shared `pipeline/fsa.py`.** Read `docs/build_briefs/newcastle.md` first, the
nearest precedent: several authorities on the FSA register, the
authority-code scope, Code-Point centroids and two notices. This brief
records only what differs. **This is the pilot of the six**: what it adds to
shared code, the other five take as config.

---

## The one-line summary

**The FSA register across the seven Greater Manchester districts Metrolink
serves: 12,451 food storefronts, keyless, under the OGL. The work is the
seven-code scope, collapsing 23 OSM relations into the network's lines, and
the light-rail test on three converted-railway branches.**

---

## Business leg — the FSA food-hygiene register (FHRS), seven authorities

Measured 2026-10-01 on the FSA API (per authority and business type; each
authority's types sum to its total). File sizes are from a HEAD request the
same day.

| Authority | Code | Total | Food service¹ | Food shops² | Storefronts | Bulk XML | Published |
|---|---|---|---|---|---|---|---|
| Manchester | 415 | 6,597 | 3,268 | 1,559 | **4,827** | 6,423,779 B | 2026-09-30 |
| Trafford | 431 | 2,221 | 967 | 503 | **1,470** | 2,204,307 B | 2026-09-29 |
| Salford | 422 | 2,107 | 946 | 515 | **1,461** | 2,077,866 B | 2026-09-30 |
| Oldham | 418 | 1,900 | 814 | 493 | **1,307** | 1,842,804 B | 2026-09-30 |
| Tameside | 430 | 1,693 | 848 | 405 | **1,253** | 1,769,230 B | 2026-09-30 |
| Rochdale | 419 | 1,900 | 747 | 485 | **1,232** | 1,863,025 B | 2026-09-30 |
| Bury | 405 | 1,221 | 659 | 242 | **901** | 1,181,439 B | 2026-09-29 |
| **Seven districts** | | **17,639** | **8,249** | **4,202** | **12,451** | **17,362,450 B** | |

¹ Restaurant/Cafe/Canteen, Takeaway/sandwich shop, Pub/bar/nightclub.
² Retailers - other, Retailers - supermarkets/hypermarkets. London's filter
(`pipeline/taxonomies/fsa_businesstype.py`).

**Download:** seven XMLs, `https://ratings.food.gov.uk/OpenDataFiles/FHRS<code>en-GB.xml`.
Named here, so a build may fetch them without asking (CLAUDE.md,
2026-09-30), with their licence row and notice.

### ⚠️ Scope is seven authority codes, not a region

Six districts sit in the FSA's North West region, which holds many more.
Select by `LocalAuthorityIdCode` (405, 415, 418, 419, 422, 430, 431) and
**assert exactly seven**. Stockport (428), Bolton and Wigan have no stop.

| District | GSS | OSM boundary (admin_level 8) |
|---|---|---|
| Manchester | E08000003 | 146656 |
| Salford | E08000006 | 146657 |
| Trafford | E08000009 | 146675 |
| Oldham | E08000004 | 146925 |
| Rochdale | E08000005 | 146926 |
| Bury | E08000002 | 146927 |
| Tameside | E08000008 | 146655 |

Code-Point Open keeps exactly these seven GSS codes, as Newcastle kept its
five.

## Placement

The screen sampled each authority's first API page, up to 100 rows per
storefront type. That is the API's default order, not random, and it leans
towards 5-rated premises. The FSA point share was 89–97% in each district
except **Tameside, at 78.9%**: about 91% overall. London's centroid tier
(Code-Point Open, already approved) places the full-postcode rows without a
point. Outward-code-only rows are private addresses and are never placed.
`pipeline/fsa.py`'s flat and childminder rules apply unchanged.

---

## Rail — Manchester Metrolink, OpenStreetMap, measured 2026-10-01

- **23 `tram` relations**: network "Manchester Metrolink", operator
  Transport for Greater Manchester.
- **11 distinct `ref` values**, which are service names such as
  "Altrincham – Bury" and "Ashton-under-Lyne – Eccles". They are not line
  letters.
- **Nine colours**: `#008800`, `#00ccff`, `#881188`, `#0066bb`, `#887766`,
  `#ff7700`, `#ff88bb`, `#ffbb00`, `#ee0011` (the Trafford Park line).
- **Odd ones out:**
  - two early-morning Airport ↔ Deansgate-Castlefield variants;
  - one relation tagged network "Metrolink", operator "TfGM", ref "ECL",
    no colour.
- **99 distinct stop names**, matching TfGM's 99.

🚨 **Collapse services into lines.** Metrolink publishes eight lines plus
the Trafford Park line, coloured as above. Collapse the relations on
`colour` (one line per colour), not on `ref`. Then decide what the ECL
relation is (likely a duplicate of the Eccles line) before drawing it.
Every line gets its public name as a label and a legend entry. Take the
names from TfGM's network map, not from the service refs.

**Gate 3 (independent of OSM):**

**NaPTAN approved as gate 3's source in all six (owner, 2026-10-01)**: the Department for Transport's national stop register (OGL), downloaded for the build's area. It needs a licence row in `docs/data_sources.md` and its notice: a second independent source beside the operator's page.
- TfGM's stop list, `https://tfgm.com/public-transport/tram/stops` (it
  answers scripts), names all 99 stops.
- The per-line counts go in config before step 1. A mismatch stops the
  step (the `tram-city` rule).

**The light-rail test.** These are Bury, Altrincham and Oldham–Rochdale:

| Part | Status |
|---|---|
| Frequency | 15 minutes across the network since 14 September 2026 (TfGM). The three branches are **converted railway**, so this is a gate. At 15 minutes it is met exactly; TfGM says it is working back to 12 minutes |
| Track share | To be measured at Step 0 from the relations' geometry: one Overpass query |
| Spacing | To be measured at Step 0 |

## Scope, CRS, region

- **Scope:** the union of the seven OSM boundaries above. **Page name
  "Manchester (Regional)"** (owner).
- **Stub check:** Manchester alone holds 42 of 99 stops. Eccles keeps 0 of
  10, Trafford Park 0 of 6, and Oldham–Rochdale 3 of 19. The regional scope
  is required.
- **CRS:** British National Grid **EPSG:27700**, as London; UTM 30N
  (EPSG:32630) is the derived fallback.
- **Region:** `"Europe"`.
- **Rings:** standard, unless the median stop gap measures about 550 m or
  less (`docs/ring_rules.md`).

## Still unknown

- ⚠️ **ECL**: what it is, before drawing.
- ⚠️ **Track share and spacing**, at Step 0.
- ⚠️ **Placement** from the full files; Tameside's sample point share is the
  lowest.
- ⚠️ **Personal exposure**: run `check_personal_exposure.py manchester`
  after step 2. Add a row in `docs/privacy_verdicts.md`.
- **Page text:** to `docs/city_page_format.md` (the banner above).

```brief-checks
[
  {
    "id": "manchester-fsa-open-data-files",
    "claim": "The FSA's open-data page lists a bulk XML for each of the seven Metrolink districts (405 Bury, 415 Manchester, 418 Oldham, 419 Rochdale, 422 Salford, 430 Tameside, 431 Trafford)",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/open-data",
    "present": ["FHRS405en-GB.xml", "FHRS415en-GB.xml", "FHRS418en-GB.xml", "FHRS419en-GB.xml", "FHRS422en-GB.xml", "FHRS430en-GB.xml", "FHRS431en-GB.xml"]
  },
  {
    "id": "manchester-fsa-terms-name-ogl",
    "claim": "THE LICENCE POSITION RESTS ON THIS PAGE, as London's does: the FHRS terms name the Open Government Licence",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/terms-and-conditions",
    "present": ["Open Government Licence"]
  },
  {
    "id": "manchester-tfgm-stop-list",
    "claim": "Gate 3's independent source: TfGM's tram stop list answers scripts and names the network's ends (Altrincham, Bury, Eccles, Rochdale, Ashton, East Didsbury, Airport)",
    "kind": "http_contains",
    "url": "https://tfgm.com/public-transport/tram/stops",
    "present": ["Altrincham", "Bury", "Eccles", "Rochdale", "Ashton", "East Didsbury", "Airport"]
  },
  {
    "id": "manchester-osm-metrolink",
    "claim": "OSM carries Metrolink as 23 tram relations with 11 distinct refs (service names, not lines) in the Metrolink bbox; lines are collapsed on colour",
    "kind": "osm_route_refs",
    "bbox": [53.33, -2.45, 53.65, -2.05],
    "routes": ["tram"],
    "expect_relations": {"tram": 23},
    "expect_refs": {"tram": 11}
  },
  {
    "id": "manchester-projected-crs-fallback",
    "claim": "Manchester's derived UTM zone is 30N (EPSG:32630), the fallback to British National Grid EPSG:27700",
    "kind": "utm_zone_from_longitude",
    "lon": -2.2426,
    "expect": "EPSG:32630"
  }
]
```
