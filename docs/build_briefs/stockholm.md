# Stockholm — build brief

**Screening closed 2026-09-22; rail counted 2026-09-23.** Run
`python scripts/brief_check.py stockholm` before writing any code.

> **Measured at the build, 2026-09-29 (build session, branch `stockholm`)** -
> these supersede the figures below:
> - **Downloaded** (owner's OK): all 289,742 inspection rows, every field,
>   75.5 MB as CSV (145 pages of 2,000); the count and the field list are
>   gated. Still frozen: no row after 2025-10-21.
> - **Types**: 21 distinct `VerksamhetsTyp` values; only restaurant and retail
>   are storefronts. `Övrigt` (185 premises) read by name - head offices,
>   delivery firms, distributors - and excluded (owner).
> - **The name test the brief asked for**: 718 of 4,967 restaurant-typed
>   premises are institutional kitchens (preschools 386, schools 206, care 78,
>   staff canteens 11, others 37) and are left out (owner); 12 retail-typed
>   pharmacies too. Staging's rule had five substring errors ("lss" in Olsson,
>   "sfi" in Kungsfisk, "lager", "kontor", "kyrka" in Slaktkyrkan), bounded at
>   the build; six words added (hemtjänst, dagverksamhet, daglig verksamhet,
>   äldreomsorg, montessori, föräldrakoop). Re-validated: **96.5%** right when
>   it says storefront; the untyped recovery is still **225** (owner: added,
>   flagged).
> - **5,262 placed storefronts** (Food service 4,193, Food shops 1,069; 217
>   from the name); 209 (3.8%) without a position. The served point equals the
>   SWEREF 99 18 00 position to 0.0 m. **89.4% within a ring** (the brief said
>   88.7% before the name test).
> - **Rail**: OSM's relations lack stations in two ways. A mirror older than
>   the relations dropped eleven stop nodes (step 1 now gates every member),
>   and Tekniska högskolan is a platform member only, while Hallonbergen is in
>   no relation (added from its station node). **Gate 3 exact**: 100 stations,
>   and routes 10: 14, 11: 12, 13: 25, 14: 19, 19: 35. 82 inside the kommun,
>   18 outside, each with its kommun. Drawn as SL's three lines, Swedish
>   labels, routes in the legend (owner).
> - **The kommun is 215.8 km²** in UTM 34N. No placed storefront's address
>   carries a flat, floor or c/o marker.

> **Re-measured 2026-09-28 (staging), before the build.** These supersede the
> figures below where they differ.
> - **Band B since 2026-09-27**: the one-bucket question below is answered.
>   Stockholm passed the Band C memo as a food page (owner). Zurich and
>   Göteborg went to Band T, trams only.
> - **The dedupe key is `ObjektId`**: 8,146 distinct values, exactly the
>   premises count. 5,188 premises change name, address, type or position
>   across their inspections, so take each one's **latest** record (by
>   `TillsynsDatum`).
> - 🚨 **Not daily any more.** Inspections run 2018-01-02 to **2025-10-21**,
>   and the layer was last edited 2025-10-22 (the Hub feed's `modified` says
>   the same). There are no rows since. Every storefront-typed premises was
>   last inspected in 2024 or 2025, so the snapshot is recent but frozen.
>   The page states the data date. ~~Building on a register frozen for 11
>   months is an owner call.~~ **Decided (owner, 2026-09-28): build on it as
>   it stands.**
> - **The untyped premises are the ones not inspected since 2023.** The type
>   field arrived with the 2024 inspections: every typed premises was last
>   inspected in 2024-25, every untyped one in 2023 or earlier.
>   - By name, the 1,391 are institutions 522, unidentifiable 501,
>     pharmacies 117, and **storefronts 251** (134 food service, 117 food
>     shops).
>   - The name rules, tested on typed premises, are right **96.9%** of the
>     time when they say "storefront".
>   - **Proposed (awaiting the owner):** add the 225 of those 251 last
>     inspected in 2022-23, flagged as classified from the name, which gives
>     about 5,996 storefronts.
>   - The measurement script is `sthlm_untyped.py`, kept (gitignored) in `data/_staging_scratch_2026-09-29/`. The
>     build writes the rules into its taxonomy, with the same validation as
>     a check.
> - **`VerksamhetsTyp` types each premises** (the screen said nothing of it):
>   | Type | Premises |
>   |---|---|
>   | Restaurang-, catering- och barverksamhet | **4,946** |
>   | Detaljhandel | **996** |
>   | Retail with another type | 25 |
>   | Wholesale, transport, production, water works and their mixes | 603 |
>   | Övrigt | 185 |
>   | None | **1,391 (17.1%)** |
>
>   The storefronts are the first two types, including premises that carry
>   them together with another: **5,771 placed**. Catering and institutional
>   kitchens sit inside the restaurant type, so a name test is needed
>   (Göteborg's register was 26.5% non-storefront). **The 1,391 untyped
>   premises are an owner call**: leave them out and disclose it
>   (recommended), or classify them by name.
> - **Placement**: 236 premises (2.9%) have no position. Positions are
>   SWEREF 99 18 00 (EPSG:3011) as well as the point geometry.
> - **The unref'd subway relation** is "Gul linje till Älvsjö" (21104772,
>   `#f5c700`), the Yellow line, which is not in service (general knowledge;
>   check its tags). Leave it out. The T-bana has **7 refs** (10, 11, 13,
>   14, 17, 18, 19), with colours tagged as words (blue, red, green).
> - **Ring coverage** (0.6 mi, the 5,771 placed storefront premises, UTM
>   34N): T-bana **88.7%**; adding pendeltåg and the local railways
>   (Roslagsbanan, Saltsjöbanan) gives 92.3%. **The recommendation is T-bana
>   only**, Berlin's and London's trade (+3.6 points left out), with trams
>   out.
> - **CRS**: the UTM zone derived from Stockholm's longitude (18.07° E) is
>   **34N (EPSG:32634)**, not 33. SWEREF 99 TM (EPSG:3006) is the national
>   alternative.

⚠️ **One-bucket city.** It shares a single owner decision with **Zurich** and
**Göteborg** — *does a food-density page belong in a project whose other
cities carry three buckets?* **Answer it once and three cities move.**

---

## The one-line summary

**The largest of the three one-bucket cities, with a real metro — and the only
one whose licence had to be argued rather than read off a field.**

---

## Business leg — a public ArcGIS FeatureServer

| | |
|---|---|
| **Distinct premises** | **8,146** |
| Derived from | **289,742 inspection rows** — ⚠️ **the register is INSPECTIONS, not premises** |
| Trade names | **100%** |
| Addresses | **96.9%** |
| Coordinates | **WGS84 points** |
| Refresh | **daily**, from Ecos 2 |
| Publisher | **Stockholms stad, miljöförvaltningen** |

🚨 **8,146 is a DISTILLED figure, not a row count.** The source serves
**289,742 inspection records**; the premises are what remains after
de-duplication. **Göteborg's equivalent register needs no dedupe at all**
(*"Alla aktiva livsmedelsverksamheter"* — active businesses, not inspections),
which is the single biggest structural difference between the two Swedish
cities.

⚠️ **The dedupe key has not been decided.** Trade name is 100% and address is
96.9%, so a name+address key would drop ~3% — but whether the same premises
appears under varying name spellings across years is unmeasured.

### ⚠️ Its own catalogue confirms there is no second bucket

Stockholms stad publishes **291 datasets** and **exactly one** commercial
register. Inside its own catalogue, `restaurang` and `företag` both return
**0**, and **Sweden has no general business licence**. **The absence is
measured, not unexplored.**

---

## ✅ Licence — SILENT, and it took step 5 to get there

**Resolved 2026-09-22**, and the reasoning matters more than the verdict:

| Source | Says |
|---|---|
| `dataportal.se` | `Åtkomsträttigheter: **Begränsad**` (restricted) |
| The ArcGIS item | `access: public`, serves without credentials, `licenseInfo` **empty** |
| **The publisher's OWN Hub DCAT feed** | ✅ **`accessLevel: public` on all 109 datasets**, `license` **CC0 on 8** |

🚨 **`dataportal.se` is a HARVESTER, not the publisher** — `read-licence`
step 5. **A contradiction between a catalogue and a publisher is decided in
favour of the publisher**, and the publisher says public.

💡 **And the blank licence field is meaningful precisely BECAUSE 8 of 109
carry CC0.** A missing licence can mean *"no mechanism"* or *"declined to
license"* — here **the mechanism is demonstrably in use**, which is what makes
the blank a silence rather than a refusal.

**Verdict: SILENT, with the pages named.** Weaker than Göteborg's and
Zurich's **CC0**, and established rather than assumed.

---

## ✅ Rail — a real metro, and this project's own figure was wrong

Counted 2026-09-23 inside **Stockholms kommun**, OSM relation **398021**:

| Mode | Relations | Named | Coloured | Refs |
|---|---|---|---|---|
| **`subway`** | **15** | **15** | **15** | **8** — 10·11·13·14·17·18·19 + one unref'd |
| `tram` | 6 | 6 | ⚠️ **4** | 4 — 12 · 7 · 7N · ? |
| `light_rail` | 6 | 6 | 6 | 3 — 21 · 30 · 31 |
| **Rail station nodes** | **92** | | | |

🚨 **This project carried *"metro 7, tram 21"*. The tram figure was wrong by
more than 3×.** It came from the same screen that gave Copenhagen a tram it
does not have.

⚠️ **One subway relation and one tram relation carry NO `ref`.** A `ref`-keyed
build drops them silently; a count-keyed build draws a line it cannot label.
**Fourth city in one day with this** — see Bucharest, Singapore, Seoul.

⚠️ **Two of six tram relations have no `colour`**, so a partial palette must
be invented if trams are drawn.

### 🚨 Resolving the boundary is a trap

`["name"="Stockholm"]["admin_level"="7"]` matches **NOTHING** — the Swedish
municipality is **`Stockholms kommun`**. Widening the search returns **nine**
candidates including **two US "Stockholm Township" relations at the same
admin_level 7**. **A looser selector picks one of those and reports a real,
wrong, confidently-zero rail network.**

**Use relation 398021.**

---

## Region

`"region": "Europe"`.

## Still unknown

- 🚨 **The dedupe key** — 8,146 from 289,742 is distilled, and how is undecided.
- ⚠️ **The one-bucket owner decision** — shared with Zurich and Göteborg.
- ⚠️ **Stop spacing**, if trams are drawn — the test's control failed on
  2026-09-23 and it is unmeasured for all three cities.
- ⚠️ **What the unref'd subway relation is.**
- ⚠️ **Non-storefront share** — Göteborg's equivalent register was **26.5%**
  schools, wholesalers and head offices. Stockholm's is unmeasured, and an
  inspection register has every reason to carry the same.

```brief-checks
[
  {
    "id": "stockholm-publisher-feed-says-public",
    "claim": "THE LICENCE POSITION RESTS ON THIS FEED. dataportal.se says Begransad (restricted) but is a HARVESTER; the miljoforvaltning's own Hub DCAT feed declares accessLevel public across its datasets, with CC0 on 8 of 109. read-licence step 5 decides a contradiction in favour of the publisher. If this feed changes, the SILENT verdict must be re-argued",
    "kind": "http_contains",
    "url": "https://open-data-sthlm-miljo.hub.arcgis.com/api/feed/dcat-us/1.1.json",
    "present": ["accessLevel"]
  },
  {
    "id": "stockholm-osm-boundary-is-stockholms-kommun",
    "claim": "OSM relation 398021 is Stockholms kommun, the area the rail was counted in. Pinned because name=Stockholm at admin_level 7 matches NOTHING - the kommun is 'Stockholms kommun' - and widening the search returns two US 'Stockholm Township' relations at the same admin_level, either of which would report a confidently wrong rail network",
    "kind": "http_ok",
    "url": "https://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%5Btimeout%3A60%5D%3Brel(398021)%3Bout%20ids%3B",
    "min_bytes": 100
  },
  {
    "id": "stockholm-livsmedelstillsyn-layer",
    "claim": "The register is ArcGIS layer Livsmedelstillsyn/41: points, keyed per premises by ObjektId, typed by VerksamhetsTyp, one row per inspection",
    "kind": "arcgis_layer",
    "url": "https://services-eu1.arcgis.com/81H0sgjoIWj6WxIM/arcgis/rest/services/Livsmedelstillsyn/FeatureServer/41",
    "expect_geometry": "esriGeometryPoint",
    "present": ["ObjektId", "AnlaggningsNamn", "Adress", "VerksamhetsTyp", "TillsynsDatum"]
  },
  {
    "id": "stockholm-register-frozen-since-2025-10",
    "claim": "TRIPWIRE: the layer has held 289,742 inspection rows, the last dated 2025-10-21, since 2025-10-22. If this FAILS, the register has resumed updating: re-measure the premises count and the data date",
    "kind": "http_contains",
    "url": "https://services-eu1.arcgis.com/81H0sgjoIWj6WxIM/arcgis/rest/services/Livsmedelstillsyn/FeatureServer/41/query?where=1%3D1&returnCountOnly=true&f=json",
    "present": ["\"count\":289742"]
  },
  {
    "id": "stockholm-osm-tbana-refs",
    "claim": "OSM carries the T-bana's seven refs in Stockholm's bbox",
    "kind": "osm_route_refs",
    "bbox": [59.22, 17.75, 59.45, 18.20],
    "routes": ["subway"],
    "require_refs": {"subway": ["10", "11", "13", "14", "17", "18", "19"]}
  },
  {
    "id": "stockholm-projected-crs",
    "claim": "Stockholm's derived UTM zone is 34N (EPSG:32634) - it lies just east of 18 E - not 33N",
    "kind": "utm_zone_from_longitude",
    "lon": 18.0686,
    "expect": "EPSG:32634"
  }
]
```
