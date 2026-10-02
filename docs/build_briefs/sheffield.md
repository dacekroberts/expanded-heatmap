# Sheffield — build brief

**Screened 2026-10-01 (staging, the post-review UK screen); Band B, food
only. Scope approved by the owner 2026-10-01: the city, without the
Rotherham Tram-Train; food only first, with the city's rates list screened
later. Build order 4 of the UK six. Builds are HELD (owner).** Run
`python scripts/brief_check.py sheffield` before writing any code. The
handoff is `docs/handoff_uk_six_2026-10-01.md`.

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

⚠️ **One-bucket city on the shared `pipeline/fsa.py`.** Read Manchester's
brief, the pilot, first.

---

## The one-line summary

**One council: 3,447 food storefronts on the FSA register. Supertram's three
routes inside the city are drawn; the Tram-Train to Rotherham is not. The
operator's website refuses scripts, so gate 3 needs another independent
source.**

---

## Business leg — the FSA register (FHRS), Sheffield

| Authority | Code | Total | Food service | Food shops | Storefronts | Bulk XML | Published |
|---|---|---|---|---|---|---|---|
| Sheffield | 425 | 4,859 | 2,396 | 1,051 | **3,447** | 4,771,509 B | 2026-09-29 |

**The FSA point share is 96.4%** (the screen's sample).

**Scope:** `LocalAuthorityIdCode` 425 only. The OSM boundary is **106956**,
admin_level 8, GSS `E08000039`. Rotherham (420) is out with the Tram-Train.

**A second bucket, screened later (owner).** Sheffield's business-rates
list is on Data Mill North, `datamillnorth.org/dataset/business-rates-exlkl`:
- OGL v3, latest file 2026-05-06;
- no liable-party names;
- descriptions such as "Shop And Premises", "Hairdressing Salon And
  Premises", "Cafe" and "Restaurant";
- no coordinates.

It needs three things:
- **a licence read**: London barred the VOA's own list on "NDR purposes
  only";
- **an address join** to Code-Point centroids;
- **a call on "Shop And Premises"**, which mixes retail with services.

**Not this build.**

---

## Rail — Sheffield Supertram, OpenStreetMap, measured 2026-10-01

- **8 `tram` relations, refs `BLUE`, `YELL`, `PURP` and `TT`.** Network
  "Travel South Yorkshire", operator "South Yorkshire Future Trams".
- **Colours:** Blue `#0000FF`, Yellow `#FFFF00`, Purple `#800080`, and
  Tram-Train `#000000`.

| Route | Ends | Daytime service |
|---|---|---|
| Blue | Halfway ↔ Malin Bridge | every 12 minutes (from 13 April 2026, the Mayoral Combined Authority) |
| Yellow | Middlewood ↔ Meadowhall Interchange | every 12 minutes (same source) |
| Purple | Herdings Park ↔ Cathedral | hourly |
| Tram-Train | Cathedral ↔ Rotherham Parkgate | every 30 minutes |

- **52 distinct OSM stop names** across all four. The network has 51 stops,
  48 of them in Sheffield.

🚨 **Leave out ref `TT` (owner).** The Tram-Train runs every 30 minutes on
Network Rail track beyond Tinsley, which fails the converted-railway
frequency gate (Aarhus L1's precedent). Its own stops, Magna, Rotherham
Central and Parkgate, go with it. Purple's hourly service runs on
purpose-built track, so it is disclosed, not disqualifying (Buffalo's
rule).

⚠️ **Yellow's colour `#FFFF00`** will fail the project's contrast checks
(`linecolour`, `check_map_markup.py`) on a light basemap. Darken it as Tours
and Dijon were, and record the change.

🚨 **Gate 3 needs an independent source.**
- `supertram.com` serves a Radware CAPTCHA to scripts, and Stagecoach's
  page returns 403. Never pass the challenge.
- **Proposed: the national stop register NaPTAN** (Department for
  Transport, OGL), whose tram stops carry stop type TMU or PLT for the
  South Yorkshire area.
- **NaPTAN approved as gate 3's source in all six (owner, 2026-10-01)**: the Department for Transport's national stop register (OGL), downloaded for the build's area. It needs a licence row in `docs/data_sources.md` and its notice.** The build downloads it without asking.

## Scope, CRS, region

- **Page name "Sheffield"** (owner).
- **Stub check:** 48 of 51 stops are in the city, so no stub.
- **CRS:** EPSG:27700; UTM 30N (EPSG:32630) is the fallback.
- **Region:** `"Europe"`.

## Still unknown

- ✅ **Gate 3's source**: NaPTAN, approved (owner, 2026-10-01).
- ⚠️ **Track share and spacing** (the light-rail test), at Step 0.
- ⚠️ **Personal exposure**, and a row in `docs/privacy_verdicts.md`.
- **Page text:** to `docs/city_page_format.md` (the banner above).

```brief-checks
[
  {
    "id": "sheffield-fsa-open-data-file",
    "claim": "The FSA's open-data page lists Sheffield's file (425)",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/open-data",
    "present": ["FHRS425en-GB.xml"]
  },
  {
    "id": "sheffield-fsa-terms-name-ogl",
    "claim": "THE LICENCE POSITION RESTS ON THIS PAGE: the FHRS terms name the Open Government Licence",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/terms-and-conditions",
    "present": ["Open Government Licence"]
  },
  {
    "id": "sheffield-osm-supertram",
    "claim": "OSM carries Supertram as 8 tram relations with 4 refs - BLUE, YELL, PURP and TT (TT, the Tram-Train, is left out, owner)",
    "kind": "osm_route_refs",
    "bbox": [53.33, -1.55, 53.47, -1.30],
    "routes": ["tram"],
    "expect_relations": {"tram": 8},
    "expect_refs": {"tram": 4},
    "require_refs": {"tram": ["BLUE", "YELL", "PURP", "TT"]}
  },
  {
    "id": "sheffield-projected-crs-fallback",
    "claim": "Sheffield's derived UTM zone is 30N (EPSG:32630), the fallback to EPSG:27700",
    "kind": "utm_zone_from_longitude",
    "lon": -1.4701,
    "expect": "EPSG:32630"
  }
]
```
