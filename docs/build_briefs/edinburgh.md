# Edinburgh — build brief

**Screened 2026-10-01 (staging, the post-review UK screen); Band B, food
only. Scope approved by the owner 2026-10-01: the city. Build order 3 of the
UK six. Builds are HELD (owner).** Run `python scripts/brief_check.py edinburgh`
before writing any code. The handoff is `docs/handoff_uk_six_2026-10-01.md`.

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

⚠️ **Scotland: Glasgow's route.** Read `docs/build_briefs/glasgow.md` first.
Edinburgh is on Food Standards Scotland's FHIS (`SchemeType` 2), in the same
FSA files and the same 14 business types. Glasgow's FHIS licence reading
(OGL v3) and its credit wording carry over. `pipeline/fsa.py` reads both
schemes.

---

## The one-line summary

**One council, one tram line, every stop inside it: 3,933 food storefronts
on FHIS. The simplest of the six. One check: the register total looks low
against Glasgow's.**

---

## Business leg — FHIS, City of Edinburgh

| Authority | Code | Scheme | Total | Food service | Food shops | Storefronts | Bulk XML | Published |
|---|---|---|---|---|---|---|---|---|
| Edinburgh (City of) | 773 | FHIS (2) | 5,144 | 3,160 | 773 | **3,933** | 4,797,431 B | 2026-09-29 |

**The FSA point share is 96.6%** in the screen's sample (the first API
page per type).

⚠️ **The total looks low.** 5,144 premises against Glasgow's 6,632 for a
city of similar size. Check at build whether the file is complete:
- compare it with FSS's own count for the council, if published;
- check that no premises category is missing.

**Do not pad it.** A short register is disclosed, not supplemented.

**Scope:** `LocalAuthorityIdCode` 773 only. The OSM boundary is
**1920901**, "City of Edinburgh", admin_level 6, GSS `S12000036`.

**No second bucket.** The council's Shop Survey layers (2015: 7,137 units
with use class) fail the five-year currency ceiling. Scotland's valuation
roll is lookup-only.

---

## Rail — Edinburgh Trams, OpenStreetMap, measured 2026-10-01

- **3 `tram` relations, with no `ref`, network or operator tags:**
  - "Edinburgh Trams: Newhaven => Airport";
  - its reverse;
  - "Tram Extension to Newhaven".
- **23 distinct stop names.** The operator's timetables page,
  `https://edinburghtrams.com/timetables`, answers scripts and names the
  ends.
- **One line, Airport to Newhaven, every 7 minutes by day**, on
  purpose-built track. Every stop is inside the city.

🚨 **Check the third relation.** "Tram Extension to Newhaven" is likely a
leftover of the 2023 extension's construction mapping, now part of the main
line. Confirm that it duplicates the through relations before excluding
it, so the line is drawn once.

**The line has no `ref` in OSM.** The label and legend need the public name
from the operator, which is a name and not prose. Record it in config.

**Gate 3:** 23 stops, per the operator's timetable page.

**NaPTAN approved as gate 3's source in all six (owner, 2026-10-01)**: the Department for Transport's national stop register (OGL), downloaded for the build's area. It needs a licence row in `docs/data_sources.md` and its notice: a second independent source beside the operator's page.

## Scope, CRS, region

- **Page name "Edinburgh"**, the city only (owner).
- **CRS:** EPSG:27700; UTM 30N (EPSG:32630) is the fallback.
- **Region:** `"Europe"`.
- **Rings:** check the median stop gap, since the city-centre stops are
  close.

## Still unknown

- ⚠️ **The register total** (above).
- ⚠️ **The third relation** (above).
- ⚠️ **Personal exposure**: Glasgow found 185 flat-address home bakers.
  `pipeline/fsa.py`'s flat rule applies. Add a row in
  `docs/privacy_verdicts.md`.
- **Page text:** to `docs/city_page_format.md` (the banner above).

```brief-checks
[
  {
    "id": "edinburgh-fsa-open-data-file",
    "claim": "The FSA's open-data page lists the City of Edinburgh's FHIS file (773)",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/open-data",
    "present": ["FHRS773en-GB.xml"]
  },
  {
    "id": "edinburgh-fsa-terms-name-ogl",
    "claim": "THE LICENCE POSITION RESTS ON THIS PAGE, as Glasgow's does: the terms name the Open Government Licence",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/terms-and-conditions",
    "present": ["Open Government Licence"]
  },
  {
    "id": "edinburgh-operator-timetables",
    "claim": "Gate 3's independent source: Edinburgh Trams' timetables page answers scripts and names the line's ends and stops (Newhaven, Airport, Ingliston, Picardy Place)",
    "kind": "http_contains",
    "url": "https://edinburghtrams.com/timetables",
    "present": ["Newhaven", "Airport", "Ingliston", "Picardy Place"]
  },
  {
    "id": "edinburgh-osm-trams",
    "claim": "OSM carries Edinburgh Trams as 3 tram relations with no ref (two directions and a Newhaven-extension relation to check for duplication)",
    "kind": "osm_route_refs",
    "bbox": [55.90, -3.40, 55.99, -3.15],
    "routes": ["tram"],
    "expect_relations": {"tram": 3},
    "expect_refs": {"tram": 1}
  },
  {
    "id": "edinburgh-projected-crs-fallback",
    "claim": "Edinburgh's derived UTM zone is 30N (EPSG:32630), the fallback to EPSG:27700",
    "kind": "utm_zone_from_longitude",
    "lon": -3.1883,
    "expect": "EPSG:32630"
  }
]
```
