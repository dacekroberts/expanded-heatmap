# Data sources — Georgia

<!-- internal -->The Georgia part of the project's provenance record,
[`data_sources.md`](../data_sources.md), written when Tbilisi was built
(2026-10-02) from its `pipeline/tbilisi/config.py`. The country's Step 0
profile, [`georgia_step0_endpoints.md`](../georgia_step0_endpoints.md), is the
evidence trail; where the two disagree, this file wins. The numbered notices
this project must display, the removal-request commitment and the deploy gate
apply to every country and are kept in that record.<!-- /internal -->

Tbilisi's businesses come from one national source, the National Statistics
Office of Georgia's Statistical Business Register, and its metro from
OpenStreetMap.

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| Tbilisi | **Statistical Business Register** (National Statistics Office of Georgia, Geostat; a keyless JSON API over the live register) - one row per economic entity (a company or an individual entrepreneur), not per premises, with a factual address distinct from the legal one, a coordinate, and its activity in NACE Rev. 2 with a national fifth digit | All three categories: 11,114 Retail, 1,074 Food service and 1,064 Personal services storefronts placed, of 16,356 kept by the classification. A company shows its registered name, in Georgian; an individual entrepreneur shows the category only | `https://br-api.geostat.ge/api/documents` | `factualAddressRegion=11` (where the entity operates in the city of Tbilisi, not where it is registered) and `isActive=true`: 63,511 entities. The API has no column selection, so personal numbers, the names of individual entrepreneurs, heads and partners, phone, e-mail, web and both address strings are dropped in memory before anything is saved | 2026-10-02 |

**What the register cannot show, and how it is read:**

- **A business, not a shop.** A chain appears once, at one address, so the map
  undercounts chains and businesses with several premises.
- **"Active" is Geostat's status**: "an enterprise which is engaged in
  economic activity", read from the entity's declarations, so a business
  opened in the last year or two may not appear yet.
- **Placement**: the register's own coordinate (`X` is the latitude, `Y` the
  longitude). 1,620 kept storefronts have no coordinate and are not shown.
  1,522 more sit on one of thirteen points that are district or settlement centers
  shared by dozens of businesses with no street address (four of them within
  115 m of a metro station), and are not shown either. 3 have a coordinate
  outside the city.
- **Classification**: divisions 47 (retail), 56 (food service) and 96
  (personal services), plus vehicle and parts sales in division 45, at the
  national leaf; the leaves left out are listed on What Is Excluded.

## Transit feeds

### Rail geometry that is not a GTFS feed

| City | System / operator | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| Tbilisi | **Tbilisi Metro** (Tbilisi Transport Company): the Akhmeteli-Varketili Line (16 stations) and the Saburtalo Line (7), from **OpenStreetMap** - four `route=subway` relations, two per line (73679 and 7786076; 2050846 and 7786075), their stop members collapsed by name and matched to the 23 `station=subway` nodes | The Overpass mirrors in `pipeline/osm.py`, bbox `41.60,44.65,41.86,45.05`, one query | 2026-10-02 | No public GTFS feed was found. The station count matches the operator's own, "27.3 km with 23 stations on two lines" (Stakeholder Engagement Plan, October 2024, `https://ttc.com.ge/sites/default/files/2024-10/Tbilisi%20Metro_New%20RS_SEP_09Oct2024_0.pdf`). OpenStreetMap's "Nadzaledevi" is labeled Nadzaladevi, the operator's spelling. Line colors from OpenStreetMap (line 2's `green` as `#008000`). OpenStreetMap, ODbL 1.0 - notice 1 and the rail-geometry notice |

## Boundary layers

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| Tbilisi | **OpenStreetMap's city boundary**, relation 1996871 (admin_level 4), 504 km2 | The Overpass mirrors, in the city's one query | The city of Tbilisi: every station is inside it, and a business whose coordinate falls outside it is not shown. OpenStreetMap, ODbL 1.0 - notice 1 |

## Licenses

| Source | Verdict | Must display | Must not |
|---|---|---|---|
| Geostat, Statistical Business Register | **Permitted with conditions.** Geostat's [Terms of Use](https://www.geostat.ge/en/page/monacemta-gamoyenebis-pirobebi) allow use "for any purpose, including commercial and non-commercial use, without restriction ... without prior permission"; third-party copyright and Geostat's logos and trademarks are outside the grant | Geostat as the source: "Users should indicate Geostat as a source of information when using data of GEOSTAT". Notice 114 | Use Geostat's logo; imply Geostat's endorsement |
| OpenStreetMap | ODbL 1.0, the project's standing credit (notice 1) | © OpenStreetMap contributors | |
| Tbilisi Transport Company | Only its published station count is used, as a check; none of its data is shown | | |
