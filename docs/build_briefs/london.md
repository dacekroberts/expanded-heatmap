# London — build brief

**Screened 2026-09-28 (staging, the large-transit gap's re-screen); Band B,
food only (owner).** Run `python scripts/brief_check.py london` before writing
any code. The trail: `DECISIONS.md` 2026-09-28 "London re-screened from the
large-transit gap", and the United Kingdom row in
`docs/global_country_shortlist.md` Tier 4.

> **Measured at the build, 2026-09-28 (build session, `worktree-london`)** -
> these supersede the screen's figures below where they differ:
> - **Downloaded** (owner's OK): the 33 London authority XMLs, 80,367,855
>   bytes, published 2026-09-17; 81,529 rows.
> - **The ~20% without coordinates is mostly out of scope**: the five
>   storefront types hold 59,610 rows, **91.0% with the FSA's own point**;
>   Other catering (35.6%) and Mobile caterer (33.4%) carry most of the gap.
>   2,764 storefront rows have neither point nor postcode. By borough, 74%
>   (Richmond) to 98% (Brent) placed.
> - **The FSA point is not a postcode centroid**: of 6,523 postcodes with 3+
>   storefronts, 14.0% put them all on one point.
> - **Canteens**: 693 of 27,262 Restaurant/Cafe/Canteen names (2.5%) read as
>   institutional or contract catering - a lower bound.
> - **Rail, OSM**: the Elizabeth line (24 relations) and all six Overground
>   lines exist with colours; most are tagged `network=National Rail`, so
>   select them by name, never by network (Dublin's DART lesson).
> - **Ring coverage by tier** (0.6 mi, Greater London, OSM relation 175342,
>   1,595.5 km²; 54,241 placed storefronts): Underground 57.8% · + DLR 59.9% ·
>   + Elizabeth line 64.6% · + Overground 73.9% · + Tramlink 74.9%.
> - **Licence** (`licence-read`): OGL v3, PERMITTED WITH CONDITIONS - the OGL
>   statement linked, the data date, no endorsement, no FSA logo or imagery.
>   Two owner calls: the FSA's privacy notice calls a business's name and
>   address personal data and the OGL excludes personal data (sole traders,
>   home caterers); and "the FHRS name" may not be used outside its imagery,
>   so credit "Food Standards Agency, UK food hygiene rating data". Private-
>   address records carry only an outward postcode: a centroid would place a
>   person's trading name at a district centre.

⚠️ **One-bucket city: food, with food retail.** Stockholm and Bucharest are
the precedent pages. The page must say plainly that shops and personal
services are missing, and why (the rating list's terms, below).

---

## The one-line summary

**The largest network in the gap, on one national register that is keyless,
current, mostly geocoded and under the OGL. The work is placement of the ~20%
without coordinates, the rail shape, and saying what is missing.**

---

## Business leg — the FSA food-hygiene register (FHRS)

| | |
|---|---|
| **Premises** | **81,633** across Greater London's **33 local authorities** (API `EstablishmentCount` sums to the same) |
| Food storefronts | **40,585**: Restaurant/Cafe/Canteen 27,279 · Takeaway/sandwich shop 9,441 · Pub/bar/nightclub 3,865 |
| Food retail | **19,088**: Retailers - other 16,763 · Retailers - supermarkets/hypermarkets 2,325 |
| Out of scope | Other catering 8,071 · Hospitals/Childcare/Caring 4,685 · School/college/university 3,508 · Mobile caterer 2,596 · Manufacturers/packers 1,141 · Hotel/B&B 971 · Distributors/Transporters 675 · Importers/Exporters 280 · Farmers/growers 33 |
| Coordinates | **80.2%** (3,300-row sample, 100 per authority, page 1); page 2 of 8 authorities: 147 of 800 without, **143 of those 147 with a postcode** |
| Addresses | 2 of 3,300 sampled rows had none |
| Currency | Files republished weekly (2026-09-10 to 2026-09-17 across the 33); half the sampled ratings date from 2024-04 or later in every authority |
| Names | `BusinessName` on every row |

**Two routes, same data:**

- **Bulk (use this for the build):** one XML per authority,
  `https://ratings.food.gov.uk/OpenDataFiles/FHRS5xxen-GB.xml`, listed on
  `https://ratings.food.gov.uk/open-data`. London's codes run 501-533
  (`LocalAuthorityIdCode`); take the 33 `FileName`s from
  `api.ratings.food.gov.uk/Authorities` filtered on `RegionName == "London"`
  rather than assuming the range. **Downloads need the owner's OK** (33
  files; state the total size, which is unmeasured).
- **API** (`api.ratings.food.gov.uk`, header `x-api-version: 2`, keyless):
  good for counts (`pageSize=1` → `meta.totalCount`), not for pulling 81,633
  rows.

**Fields** (API names; the XML carries the same content): `FHRSID`,
`BusinessName`, `BusinessType`, `BusinessTypeID`, `AddressLine1`-`4`,
`PostCode`, `geocode` (lat/lon, null on ~20%), `LocalAuthorityCode`,
`LocalAuthorityName`, `RatingValue`, `RatingDate`, `SchemeType` (FHRS),
`NewRatingPending`, `Phone`, `RightToReply`, `scores`.

### ⚠️ Traps to settle in the taxonomy

- **"Restaurant/Cafe/Canteen" includes workplace and institutional
  canteens**, which are not storefronts. Unmeasured; check the name text
  (canteen, staff, school, hospital) before trusting 27,279.
- **"Retailers - other" is food retail only by construction** (grocers,
  off-licences, bakers, butchers, newsagents with food). Label it as food
  retail, never as "shops".
- **"Other catering premises" and "Mobile caterer"** hold home caterers and
  vans; keep them out. Home-based names are the personal-exposure risk.
- **`RatingValue` is not needed and should not be shown**: displaying a
  rating triggers the FSA's accuracy and currency conditions (below).

### Why food only — the second layer is measured absent

- **VOA rating list**: carries a description (the 2026-09-21 record's "no
  category" was wrong), but its terms are "Non Domestic Rating (NDR) purposes
  only", with onward disclosure barred. Out on terms.
- **Borough NNDR lists** with the VOA description: 4 of 33 publish
  (Camden, Islington, Barnet, Hounslow), none downtown; Westminster refuses its
  list under FOI. A services layer in four outer boroughs would mislead.
- **Special-treatment licences** (nails, massage, beauty): lookup-only in
  Westminster, Camden, Hackney, Tower Hamlets and Lambeth.
- **London Datastore** (1,303 datasets): nothing premises-level for retail or
  services.

---

## Placement — the ~20% without coordinates

**Almost every row without a geocode has a postcode (143 of 147).** Two
options, both a join, not a geocoder (`address-join`):

1. **Postcode centroids** from the ONS Postcode Directory or OS Code-Point
   Open. ⚠️ Licence unread: both are OGL-family but carry OS and Royal Mail
   notices; a `licence-read` and a `docs/data_sources.md` row first. London
   postcodes average ~15 addresses, so a centroid is typically within tens of
   metres; state the tier on the page.
2. **Drop them and disclose the share**, per authority.

⚠️ **The FSA geocode's own precision is unmeasured.** It may itself be a
postcode centroid for some authorities; check stacking (distinct points per
postcode) on one authority before calling it premises-level.

---

## Licence — OGL v3 (terms page read, no `licence-read` yet)

`https://ratings.food.gov.uk/terms-and-conditions` names the **Open
Government Licence v3**, Crown copyright. Its extra conditions are about
**ratings and imagery**: use the current rating, show the date the data was
updated, do not alter the rating images, and do not use the FHRS name or FSA
logo without permission. **The page does not say whether they apply when no
rating is shown**; the build's `licence-read` settles it. Showing only
location and business type, and stating the data date, is the conservative
reading.

Notice to expect: the OGL attribution statement ("Contains public sector
information licensed under the Open Government Licence v3.0.") plus the data
date.

---

## Rail — OpenStreetMap, measured 2026-09-28 in bbox 51.28,-0.51,51.70,0.34

| Mode | Network tag | Relations | Refs |
|---|---|---|---|
| `subway` | London Underground | 97 | **11**: Bakerloo, Central, Circle, District, Hammersmith & City, Jubilee, Metropolitan, Northern, Piccadilly, Victoria, Waterloo & City |
| `light_rail` | Docklands Light Railway | 12 | 5 route refs (B-L, B-WA, S-L, SI-WA, TG-B) |
| `tram` | London Trams | 10 | 3 (2, 3, 4) |
| `train` | London Overground | 3 | 2 found (Liberty, Lioness) |

Every relation has a `colour`.

🚨 **The Overground and the Elizabeth line are the rail-shape decision.**
Both are `route=train`. The Overground query found only 2 of its 6 named lines
(Liberty, Lioness; Mildmay, Suffragette, Weaver and Windrush are tagged some
other way), and the Elizabeth line matched nothing on `network~"Elizabeth
line"` (a case or tagging difference, unmeasured). Read
`docs/sub_transit_line_filters.md` and the `osm-rail` skill before choosing.
The Underground alone is the defensible core; the Elizabeth line's central
tunnel is metro-standard and its outer branches are commuter rail (Brazil's
three-part rail test is the precedent).

⚠️ **Underground relations are branch variants** (97 relations, 11 lines):
collapse on `ref`/`name`, and keep the Northern line's two branches and the
District's as one labelled line each.

⚠️ **The Underground reaches well beyond Greater London** (Metropolitan to
Amersham and Chesham, Central to Epping). Cut at the Greater London boundary
and check what each line keeps.

---

## Scope, CRS, region

- **Scope:** Greater London, the 32 boroughs plus the City of London; FSA
  covers exactly those 33 as `RegionName == "London"`.
- **CRS:** British National Grid **EPSG:27700** (metres, national); UTM 30N
  (EPSG:32630) is the derived fallback. Never buffer in 4326.
- **Region:** `"region": "Europe"`.

## Still unknown

- 🚨 **The rail shape**: Overground and Elizabeth line tagging and inclusion.
- ⚠️ **Canteen share** inside Restaurant/Cafe/Canteen.
- ⚠️ **FSA geocode precision**, and the postcode-centroid licence.
- ⚠️ **The FSA conditions' reach** when no rating is shown (`licence-read`).
- ⚠️ **Bulk download size** (33 XML files) for the owner's OK.
- ⚠️ **Personal exposure**: `check_personal_exposure.py` after step 2.

```brief-checks
[
  {
    "id": "london-fsa-open-data-files",
    "claim": "The FSA publishes one bulk XML per authority on its open-data page; London's start at FHRS501 (Barking and Dagenham). The build downloads these, not the API",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/open-data",
    "present": ["OpenDataFiles/FHRS501en-GB.xml", "Terms and conditions"]
  },
  {
    "id": "london-fsa-terms-name-ogl",
    "claim": "THE LICENCE POSITION RESTS ON THIS PAGE: the FHRS terms name the Open Government Licence, with extra conditions on ratings and imagery. If it stops naming the OGL, the licence must be re-read before publishing",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/terms-and-conditions",
    "present": ["Open Government Licence"]
  },
  {
    "id": "london-osm-rapid-transit-refs",
    "claim": "OSM carries the Underground's 11 lines, the DLR's 5 route refs and Tramlink's 3 inside Greater London's bbox, all coloured",
    "kind": "osm_route_refs",
    "bbox": [51.28, -0.51, 51.70, 0.34],
    "routes": ["subway", "light_rail", "tram"],
    "expect_refs": {"subway": 11, "light_rail": 5, "tram": 3},
    "require_refs": {"subway": ["Bakerloo", "Central", "Circle", "District", "Hammersmith & City", "Jubilee", "Metropolitan", "Northern", "Piccadilly", "Victoria", "Waterloo & City"]}
  },
  {
    "id": "london-projected-crs-fallback",
    "claim": "London's derived UTM zone is 30N (EPSG:32630), the fallback if the build does not use British National Grid EPSG:27700",
    "kind": "utm_zone_from_longitude",
    "lon": -0.1276,
    "expect": "EPSG:32630"
  }
]
```
