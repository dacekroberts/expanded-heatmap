# Nottingham (Regional) — build brief

**Screened 2026-10-01 (staging, the post-review UK screen); Band B, food
only. Scope approved by the owner 2026-10-01: regional, meaning the city,
Broxtowe, Rushcliffe and Ashfield. Build order 5 of the UK six. Builds are
HELD (owner).** Run `python scripts/brief_check.py nottingham` before
writing any code. The handoff is `docs/handoff_uk_six_2026-10-01.md`.

> 🛑 **PROSE HOLD (owner, 2026-10-01).** The owner is reworking the site's
> prose. **Draft no page text**: no description, no scope sentence, no What
> Is Excluded wording, no notice wording beyond a licensor's required
> attribution, and no README or Overview copy. **Do not copy London's,
> Glasgow's or Newcastle's page text**: that is the prose being replaced.
> Build the data steps and the map. Leave every prose slot as a
> `TODO(prose-hold)` marker, and list each one in the drafts file. The
> approved-template pre-permission (CLAUDE.md, 2026-09-30) does not apply
> to this round.

⚠️ **One-bucket city on the shared `pipeline/fsa.py`.** Read Manchester's
brief, the pilot, first.

---

## The one-line summary

**Four authorities and two NET lines: 3,702 food storefronts. The
city-and-county boundary mix is the one new thing: a unitary city beside
three Nottinghamshire districts.**

⚠️ **Correction (2026-10-01, at the brief):** the master list and the
approval entry first said 4,723 storefronts for this scope. That was an
addition error at the screen. **The four authorities hold 3,702.**

---

## Business leg — the FSA register (FHRS), four authorities

| Authority | Code | Total | Food service | Food shops | Storefronts | Bulk XML | Published | Point share (sample) |
|---|---|---|---|---|---|---|---|---|
| Nottingham City | 899 | 3,051 | 1,256 | 765 | **2,021** | 3,054,281 B | 2026-09-29 | 96.2% |
| Ashfield | 259 | 977 | 347 | 236 | **583** | 884,232 B | 2026-09-29 | 90.6% |
| Rushcliffe | 266 | 916 | 382 | 178 | **560** | 924,078 B | 2026-09-29 | 80.2% |
| Broxtowe | 261 | 812 | 353 | 185 | **538** | 807,473 B | 2026-09-30 | 91.4% (full file) |
| **Four authorities** | | **5,756** | **2,338** | **1,364** | **3,702** | **5,670,064 B** | | |

Rushcliffe's point share is the lowest of the six cities' authorities. Its
outward-code-only rows, which are private addresses and never placed, ran
42 of 383 in the sample. The Broxtowe figure is from its whole file
(currency: latest RatingDate 2026-09-10, 537 of 722 dated rows from
2025–26).

**Scope:** select `LocalAuthorityIdCode` 899, 259, 266 and 261, and
**assert exactly four**. Gedling (262) has no stop.

| Authority | GSS | OSM boundary | admin_level |
|---|---|---|---|
| City of Nottingham (unitary) | E06000018 | 123292 | 6 |
| Broxtowe | E07000172 | 154058 | 8 |
| Rushcliffe | E07000176 | 77311 | 8 |
| Ashfield | E07000170 | 154043 | 8 |

⚠️ **Mixed admin levels.** The city is a unitary authority at admin_level
6. The three districts are admin_level 8 inside Nottinghamshire, which is
relation 181040, admin_level 6. Union these four boundaries. **Never the
county.** Code-Point keeps exactly these four GSS codes.

---

## Rail — NET, OpenStreetMap, measured 2026-10-01

- **4 `tram` relations, refs `1` and `2`**: network "NET", operator
  Tramlink Nottingham, all coloured `#003828`.
  - Line 1 North (Hucknall) and Line 1 South (Toton Lane);
  - Line 2 North (Phoenix Park) and Line 2 South (Clifton South).
- **Each ref is two half-line relations**, meeting in the city centre.
  Collapse each line from its two halves. The longest-relation rule would
  keep only half a line.
- **Both lines share one colour**, so the map needs two distinguishable
  colours. Use the project's `line_colour_search.py`, and record the change.
- **50 distinct OSM stop names**, against about 51 from the operator. Gate 3
  settles the count: per line, from the operator's timetables page
  `https://www.thetram.net/timetables`, which answers scripts.
- **Every 7–10 minutes**, Monday to Saturday, both lines (operator).
- **Short former-railway sections:** the Hucknall line beside the Robin
  Hood line, and the old Great Central formation at Clifton. Both pass the
  frequency gate.

## Scope, CRS, region

- **Page name "Nottingham (Regional)"** (owner).
- **Stops by authority** (the screen):
  - **Broxtowe 9:** Toton Lane to Middle Street, including Beeston;
  - **Ashfield 2:** Butler's Hill and Hucknall;
  - **Rushcliffe:** Clifton South, plus up to two stops on the boundary.
- **CRS:** EPSG:27700; UTM 30N (EPSG:32630) is the fallback.
- **Region:** `"Europe"`.

## Still unknown

- ⚠️ **Gate 3's per-line counts.**
- ⚠️ **Track share and spacing**, at Step 0.
- ⚠️ **Rushcliffe's placement** from its full file.
- ⚠️ **Personal exposure**, and a row in `docs/privacy_verdicts.md`.
- 🛑 **All prose** (the hold).

```brief-checks
[
  {
    "id": "nottingham-fsa-open-data-files",
    "claim": "The FSA's open-data page lists the files of Nottingham City (899), Broxtowe (261), Rushcliffe (266) and Ashfield (259)",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/open-data",
    "present": ["FHRS899en-GB.xml", "FHRS261en-GB.xml", "FHRS266en-GB.xml", "FHRS259en-GB.xml"]
  },
  {
    "id": "nottingham-fsa-terms-name-ogl",
    "claim": "THE LICENCE POSITION RESTS ON THIS PAGE: the FHRS terms name the Open Government Licence",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/terms-and-conditions",
    "present": ["Open Government Licence"]
  },
  {
    "id": "nottingham-operator-timetables",
    "claim": "Gate 3's independent source: NET's timetables page answers scripts and names the lines' ends and centre (Hucknall, Clifton South, Toton Lane, Phoenix Park, Old Market Square)",
    "kind": "http_contains",
    "url": "https://www.thetram.net/timetables",
    "present": ["Hucknall", "Clifton South", "Toton Lane", "Phoenix Park", "Old Market Square"]
  },
  {
    "id": "nottingham-osm-net",
    "claim": "OSM carries NET as 4 tram relations (two half-lines per line) with refs 1 and 2",
    "kind": "osm_route_refs",
    "bbox": [52.86, -1.30, 53.06, -1.10],
    "routes": ["tram"],
    "expect_relations": {"tram": 4},
    "expect_refs": {"tram": 2},
    "require_refs": {"tram": ["1", "2"]}
  },
  {
    "id": "nottingham-projected-crs-fallback",
    "claim": "Nottingham's derived UTM zone is 30N (EPSG:32630), the fallback to EPSG:27700",
    "kind": "utm_zone_from_longitude",
    "lon": -1.1505,
    "expect": "EPSG:32630"
  }
]
```
