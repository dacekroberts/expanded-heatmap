# Birmingham (Regional) — build brief

**Screened 2026-10-01 (staging, the post-review UK screen); Band B, food
only. Scope approved by the owner 2026-10-01: Birmingham, Sandwell and
Wolverhampton, built now; the Dudley branch is a dated watch item. Build
order 2 of the UK six. Builds are HELD (owner).** Run
`python scripts/brief_check.py birmingham` before writing any code. The
trail: `docs/decisions_drafts/staging.md`, "The UK six approved with their
scopes". The handoff is `docs/handoff_uk_six_2026-10-01.md`.

> 🛑 **PROSE HOLD (owner, 2026-10-01).** The owner is reworking the site's
> prose. **Draft no page text**: no description, no scope sentence, no What
> Is Excluded wording, no notice wording beyond a licensor's required
> attribution, and no README or Overview copy. **Do not copy London's,
> Glasgow's or Newcastle's page text**: that is the prose being replaced.
> Build the data steps and the map. Leave every prose slot as a
> `TODO(prose-hold)` marker, and list each one in the drafts file. The
> approved-template pre-permission (CLAUDE.md, 2026-09-30) does not apply
> to this round.

⚠️ **One-bucket city on the shared `pipeline/fsa.py`.** Read
`docs/build_briefs/newcastle.md` and Manchester's brief, the pilot, first.
This brief records only what differs.

---

## The one-line summary

**The FSA register across the three authorities West Midlands Metro serves
today: 9,827 food storefronts. The work is the three-code scope, one tram
line run as several service patterns, and a check at Step 0 on whether the
Dudley line has opened.**

---

## Business leg — the FSA register (FHRS), three authorities

Measured 2026-10-01 (FSA API; HEAD for sizes).

| Authority | Code | Total | Food service | Food shops | Storefronts | Bulk XML | Published |
|---|---|---|---|---|---|---|---|
| Birmingham | 402 | 10,239 | 4,003 | 2,490 | **6,493** | 10,329,919 B | 2026-09-30 |
| Sandwell | 423 | 2,746 | 1,029 | 794 | **1,823** | 2,679,813 B | 2026-09-30 |
| Wolverhampton | 436 | 2,178 | 884 | 627 | **1,511** | 2,255,456 B | 2026-09-29 |
| **Three authorities** | | **15,163** | **5,916** | **3,911** | **9,827** | **15,265,188 B** | |

Placement sample (first API page per type): FSA point 90.8% (Birmingham),
85.7% (Sandwell), 93.3% (Wolverhampton). Code-Point centroids for the
rest, as London.

**Scope:** select `LocalAuthorityIdCode` 402, 423 and 436, and **assert
exactly three**. The OSM boundaries are all admin_level 8:

| Authority | GSS | OSM boundary |
|---|---|---|
| Birmingham | E08000025 | 162378 |
| Sandwell | E08000028 | 162485 |
| Wolverhampton | E08000031 | 173722 |

**Download:** three XMLs. They are named here, so the build may fetch them.

---

## Rail — West Midlands Metro, OpenStreetMap, measured 2026-10-01

- **7 `tram` relations, refs `1` and `2`**: network "West Midland Metro",
  operator Midland Metro Limited (WMCA), colour `#ec008c`.
- **Line 1 has six relations.** It runs as service patterns: Wolverhampton
  Station or Wolverhampton St Georges to Edgbaston Village, plus a
  Millennium Point branch. Collapse them on `ref` into one drawn line.
- **The operator lists 35 stops** on its maps page,
  `https://westmidlandsmetro.com/maps/`, which answers scripts. Millennium
  Point and Albert Street opened in April 2026.

🚨 **Line 2 is in OSM already**: "Midland Metro Line 2", Wednesbury to
Dudley and Brierley Hill. Several of its stops are named with "[Aug 2026]"
(Dudley Port, Dudley Interchange, Dudley Castle & Zoo, Flood Street). **At
Step 0, read the operator's page for whether Line 2 is in passenger
service.**
- **If it is not:** draw Line 1 only, and leave Line 2 out of the OSM
  query.
- **If it is: add Dudley as a fourth authority (owner, pre-approved
  2026-10-01).** That is FSA 409 (about 1,799 storefronts) and its OSM
  boundary, so the open line is not drawn as a stub. Record the date the
  line was confirmed open.

**Not this network:** two `light_rail` relations in the box are the
Stourbridge Town branch shuttle (West Midlands Trains, national rail). Leave
them out. OSM's stop names include a near-duplicate ("Dudley Street Guns
Village" and "Dudley Street, Guns Village"). Alias it.

**Gate 3:** the operator's 35 stops, per line in config, before step 1.

**NaPTAN approved as gate 3's source in all six (owner, 2026-10-01)**: the Department for Transport's national stop register (OGL), downloaded for the build's area. It needs a licence row in `docs/data_sources.md` and its notice: a second independent source beside the operator's page.

**The light-rail test:**
- **Frequency:** 8–12 minutes by day (the operator's FAQ; its 2025
  timetable says every 8). Snow Hill to Priestfield is former Great
  Western Railway trackbed, so the gate applies, and it passes.
- **Track share and spacing:** measured at Step 0.

## Scope, CRS, region

- **Page name "Birmingham (Regional)"** (owner).
- **Stub check:** Birmingham alone holds 16 of 35 stops (46%), a stub.
  Sandwell has 10 and Wolverhampton 9 (the screen's assignment by stop
  coordinates).
- **CRS:** EPSG:27700; UTM 30N (EPSG:32630) is the fallback.
- **Region:** `"Europe"`.

## Still unknown

- ⚠️ **Line 2's status** (above): if open, Dudley joins (pre-approved).
- ⚠️ **Track share and spacing**, at Step 0.
- ⚠️ **Personal exposure**, and a row in `docs/privacy_verdicts.md`.
- **Watch item:** the Dudley branch, about late 2026. It belongs in PLAN with
  a date.
- 🛑 **All prose** (the hold).

```brief-checks
[
  {
    "id": "birmingham-fsa-open-data-files",
    "claim": "The FSA's open-data page lists a bulk XML for Birmingham (402), Sandwell (423) and Wolverhampton (436)",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/open-data",
    "present": ["FHRS402en-GB.xml", "FHRS423en-GB.xml", "FHRS436en-GB.xml"]
  },
  {
    "id": "birmingham-fsa-terms-name-ogl",
    "claim": "THE LICENCE POSITION RESTS ON THIS PAGE: the FHRS terms name the Open Government Licence",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/terms-and-conditions",
    "present": ["Open Government Licence"]
  },
  {
    "id": "birmingham-operator-stop-list",
    "claim": "Gate 3's independent source: the operator's maps page answers scripts and names the line's stops (Edgbaston Village, Wolverhampton, Wednesbury, Grand Central, Library)",
    "kind": "http_contains",
    "url": "https://westmidlandsmetro.com/maps/",
    "present": ["Edgbaston Village", "Wolverhampton", "Wednesbury", "Grand Central", "Library"]
  },
  {
    "id": "birmingham-osm-metro",
    "claim": "OSM carries West Midlands Metro as 7 tram relations with refs 1 and 2 (Line 2, the Dudley line, to be checked as open or not at Step 0)",
    "kind": "osm_route_refs",
    "bbox": [52.45, -2.15, 52.60, -1.85],
    "routes": ["tram"],
    "expect_relations": {"tram": 7},
    "expect_refs": {"tram": 2},
    "require_refs": {"tram": ["1", "2"]}
  },
  {
    "id": "birmingham-projected-crs-fallback",
    "claim": "Birmingham's derived UTM zone is 30N (EPSG:32630), the fallback to EPSG:27700",
    "kind": "utm_zone_from_longitude",
    "lon": -1.8904,
    "expect": "EPSG:32630"
  }
]
```
