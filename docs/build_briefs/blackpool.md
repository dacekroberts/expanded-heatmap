# Blackpool (Regional) — build brief

**Screened 2026-10-01 (staging, the post-review UK screen); Band B, food
only. Scope approved by the owner 2026-10-01: Blackpool with Wyre. Build
order 6 of the UK six. Builds are HELD (owner).** Run
`python scripts/brief_check.py blackpool` before writing any code. The
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

**A street and promenade tramway, Starr Gate to Fleetwood, across two
authorities: 1,744 food storefronts, the smallest page of the six. Its
operator's website refuses scripts, so gate 3 needs another independent
source.**

---

## Business leg — the FSA register (FHRS), two authorities

| Authority | Code | Total | Food service | Food shops | Storefronts | Bulk XML | Published | Point share (sample) |
|---|---|---|---|---|---|---|---|---|
| Blackpool | 898 | 1,686 | 720 | 310 | **1,030** | 1,717,662 B | 2026-09-29 | 95.8% |
| Wyre | 207 | 1,034 | 436 | 278 | **714** | 1,020,419 B | 2026-09-30 | 84.5% |
| **Two authorities** | | **2,720** | **1,156** | **588** | **1,744** | **2,738,081 B** | | |

Wyre's outward-code-only rows, which are private addresses and never
placed, ran 43 of 427 in the sample.

⚠️ **Not Wyre Forest (153)**, a different council in the West Midlands
with a near-identical name. Select by `LocalAuthorityIdCode` 898 and 207,
and **assert exactly two**.

| Authority | GSS | OSM boundary | admin_level |
|---|---|---|---|
| Blackpool (unitary) | E06000009 | 148603 | 6 |
| Wyre | E07000128 | 148604 | 8 |

Union the two boundaries, never Lancashire. Code-Point keeps exactly these
two GSS codes.

---

## Rail — Blackpool Tramway, OpenStreetMap, measured 2026-10-01

- **2 `tram` relations, both ref `T1`**: "Blackpool Tramway Southbound"
  and "Northbound". There are no network, operator or colour tags.
- **40 distinct stop names**, matching the screen's 40.
- **One line plus the Blackpool North spur**, every 10 minutes by day.
  It is street and promenade track, a street tramway, so trams-only maps
  apply (approved 2026-09-29).
- **No colour in OSM.** Choose one with `line_colour_search.py` and record
  it. The label takes the public name from the operator. That is a name,
  not prose.
- **Stops by authority:** about 25 in Blackpool and 15 in Wyre (Cleveleys
  to Fleetwood). Anchorsholme Lane is the first stop in the Blackpool
  district.

⚠️ **The North Station spur** opened in 2024. Check that both relations
carry it, so it is drawn.

🚨 **Gate 3 needs an independent source.**
- `blackpooltransport.com` returns 403 to scripts. Never work around it.
- **Proposed: NaPTAN** (Department for Transport, OGL), its tram stops for
  Lancashire and Blackpool.
- **NaPTAN approved as gate 3's source in all six (owner, 2026-10-01)**: the Department for Transport's national stop register (OGL), downloaded for the build's area. It needs a licence row in `docs/data_sources.md` and its notice.** The build downloads it without asking.

## Scope, CRS, region

- **Page name "Blackpool (Regional)"** (owner).
- **CRS:** UTM 30N **EPSG:32630**, as London's, Glasgow's and Newcastle's
  `CRS_PROJECTED` (corrected 2026-10-02 from the UK lead's report).
  EPSG:27700 is only Code-Point Open's source CRS.
- **NaPTAN files every tram stop under ATCO area 940** (the national tram
  area), not the local area codes; select the build's stops from 940 by
  location (UK lead, 2026-10-02).
- **Region:** the UK's own region, with `label_tier: "minor"` (owner,
  2026-10-02); until the integration pass creates it, `"Europe"`. See the
  kit's "The UK sub-region and the minor label tier".
- **Rings:** the promenade stops are close together. Measure the median
  stop gap: if it is about 550 m or less, use halved rings
  (`docs/ring_rules.md`).

## Still unknown

- ✅ **Gate 3's source**: NaPTAN, approved (owner, 2026-10-01).
- ⚠️ **The spur in OSM**, and **spacing** for the rings.
- ⚠️ **Wyre's placement** from its full file.
- ⚠️ **Personal exposure**, and a row in `docs/privacy_verdicts.md`.
- **Page text:** to `docs/city_page_format.md` (the banner above).

```brief-checks
[
  {
    "id": "blackpool-fsa-open-data-files",
    "claim": "The FSA's open-data page lists Blackpool's (898) and Wyre's (207) files - Wyre, not Wyre Forest (153)",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/open-data",
    "present": ["FHRS898en-GB.xml", "FHRS207en-GB.xml"]
  },
  {
    "id": "blackpool-fsa-terms-name-ogl",
    "claim": "THE LICENCE POSITION RESTS ON THIS PAGE: the FHRS terms name the Open Government Licence",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/terms-and-conditions",
    "present": ["Open Government Licence"]
  },
  {
    "id": "blackpool-osm-tramway",
    "claim": "OSM carries the Blackpool Tramway as 2 tram relations, both ref T1",
    "kind": "osm_route_refs",
    "bbox": [53.77, -3.07, 53.94, -2.98],
    "routes": ["tram"],
    "expect_relations": {"tram": 2},
    "expect_refs": {"tram": 1},
    "require_refs": {"tram": ["T1"]}
  },
  {
    "id": "blackpool-projected-crs-fallback",
    "claim": "Blackpool's projected CRS is UTM 30N (EPSG:32630), as the built UK cities'",
    "kind": "utm_zone_from_longitude",
    "lon": -3.0503,
    "expect": "EPSG:32630"
  }
]
```
