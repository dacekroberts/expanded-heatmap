# Build brief — Calgary

**Not the next city.** Ranked fifth of six Canadian candidates on the
comparable measure. This brief exists because the re-ranking of 2026-09-21
corrected several facts about Calgary, and those corrections are worth banking
before they are forgotten.

Claims are **MEASURED** or **ASSERTED**, per
[`session_roles.md`](../session_roles.md).

---

## Where it ranks, and on what

**MEASURED 2026-09-21**, reproducible with
`python scripts/rank_canada_storefront_density.py`:

**75 storefronts within the 0.6 mi ring per in-city station** — 6,243 across
83 stations. For scale: Vancouver 206, Montréal 151, Surrey 135, Edmonton 76,
Calgary 75, Toronto 41, against D.C. ~173 and Boston ~39.

**The published figure was 103**, measured on every licence rather than
storefronts (1.4x inflation — the smallest of the five mis-measured cities,
because Calgary's register is unusually premises-oriented already).

**Calgary and Edmonton are now a tie**, at 75 and 76, where the published
figures had them at 103 and 153. Neither is clearly ahead of the other, so
choose between them on cost rather than density.

**It is the biggest map of the four remaining**: 83 in-city stations, more than
Boston's 71 and second only to Toronto's 234. At ~2x Boston's density it is
viable, not marginal — but it is the thinnest of the Canadian candidates that
clears Boston.

## Sources

### Business — `vdjc-pybd`, Socrata

| | |
|---|---|
| Endpoint | `https://data.calgary.ca/resource/vdjc-pybd.csv` (add `$limit`) |
| Licence | **OGL – City of Calgary**, which covers the business data **and** Calgary Transit |
| `SOURCE_ENCODING` | `utf-8` |

**MEASURED:** 23,203 rows, 12 columns — `getbusid, tradename, homeoccind,
address, comdistcd, comdistnm, licencetypes, first_iss_dt, exp_dt,
jobstatusdesc, point, globalid`.

- `point` **100%** populated, so **no geocoding step**.
- `tradename` **0% blank** — so **no name-fallback problem at all**, and no
  registrant-name column exists to omit. A strong privacy position, like
  Miami's and Montréal's.
- `jobstatusdesc` has 7 values: Renewal Licensed 15,962, Pending Renewal 2,889,
  Licensed 2,542, Renewal Invoiced 1,614, Move in Progress 168, Close in
  Progress 26. **ASSERTED:** which of these count as active. Decide explicitly
  — "Close in Progress" plainly should not, and the two "Renewal" states
  plainly should.

**CORRECTION — `licencetypes` has 96 real categories, not 173.** The recorded
173 came from splitting on a bare `"\n"` when the delimiter is **`",\n"`**,
which shreds each value and counts the fragments as categories. **MEASURED:**
1,169 naive distinct → **96** true distinct on `",\n"`, with **9,136 rows
carrying more than one category**. A taxonomy module built on 173 — or worse,
on 1,169 — would have been nonsense.

**CORRECTION — `homeoccind` is `N` on all 23,203 rows.** The profile already
flagged it as unusable; this confirms it is not merely unreliable but
constant. So Calgary, like Vancouver, has **no licence-level home-business
flag** and would need a zoning or parcel substitute if one is wanted. Note
Vancouver's turned out to remove nothing.

**Its vocabulary is unusually clean and explicitly premises-based**, which is
why its inflation was the lowest of the five. The top categories:

```
7,516  RETAIL DEALER - PREMISES          937  OUTDOOR PATIO
3,539  FOOD SERVICE - PREMISES (SEATING) 917  MASSAGE CENTRE (COMMERCIAL)
2,591  FOOD SERVICE - PREMISES           913  TOBACCO RETAILER
2,103  PERSONAL SERVICE                  890  APARTMENT BUILDING OPERATOR
2,025  WHOLESALER                        653  VAPE RETAILER
1,640  MANUFACTURER                      540  MOTOR VEHICLE DEALER - PREMISES
1,617  CONTRACTOR (NO PROV. LICENCE)     458  ENTERTAINMENT ESTABLISHMENT
1,527  ALCOHOL BEVERAGE SALES (RESTAURANT) 429 LIQUOR STORE
1,189  MOTOR VEHICLE REPAIR AND SERVICE  349  SECONDHAND DEALER
1,058  FOOD SERVICE - PREMISES (NO SEATING)
```

A screening-level bucket map for these is already written, with reasons, in
`scripts/rank_canada_storefront_density.py` (`CALGARY_BUCKETS`). **It is a
ranking aid, not a build-grade taxonomy** — it maps 19 categories and leaves
the other 77 unmapped rather than carrying an explicit verdict for each, which
is what `classify()` raising on an unknown value requires. Start from it, do
not ship it.

Three judgment calls it already encodes, each met before in this project:

- **`ALCOHOL BEVERAGE SALES (*)` and `OUTDOOR PATIO` are endorsements**, held
  by a premises that already has a food-service licence. Counting them
  double-counts one restaurant — D.C.'s endorsement problem.
- **`PERSONAL SERVICE (INDEPENDENT CHAIR OPERATOR)`** is a chair renter inside
  someone else's shop. New York drops these: they double-count the shop and put
  a person on the map.
- **`MASSAGE CENTRE (COMMERCIAL)` counts as a personal service here, although
  Vancouver's `Massage Therapy (RMT)` does not.** The difference is real:
  massage therapy is a regulated health profession in British Columbia and is
  **not** regulated in Alberta.

### Transit — Calgary Transit CTrain

**MEASURED:** 2 routes at `route_type 0`, the Red and Blue Lines, 83 served
stops → 83 distinct station names. All in-city.

**Its catalogue feed (Mobility Database id 712) carries NO `feed_info.txt`**,
so it declares neither a licence nor an expiry. That means the staleness check
cannot run on it — which is a reason to find the agency's own feed for a build,
not a reason to relax. `route_type 0` is LRT here, correctly coded.

**ASSERTED:** the agency's own feed URL. Not located during the re-ranking;
the catalogue mirror was used.

### Boundary

**ASSERTED — and there is a known trap.** Calgary publishes **two "City
Boundary" layers and one of them is 184 bytes of valid, useless GeoJSON**
(recorded in `add-country`'s failure modes). Verify the one you take has real
geometry and a plausible area before using it. All 83 stations are in-city, so
the boundary is a check rather than a filter — but do not skip it.

### Projected CRS

**EPSG:32611** (UTM 11N), from longitude ≈ −114.1. Per city, never copied.

## What a build would cost

- **A taxonomy module for 96 categories**, split on `",\n"`, with a dispatch
  rule for the 9,136 multi-category rows (Boston's `FT+RF` question).
- **A verdict on each of the 96**, since `classify()` raises on unknowns.
- **One notice**: OGL – City of Calgary, covering both the business data and
  Calgary Transit — the only Canadian city where one licence does both.
  Exact wording in `licenses/canada-required-notices.md`.
- **No geocoding step**, no name-fallback work, and no residence inference
  unless one is wanted.

## Open questions

1. **Which `jobstatusdesc` values are active.**
2. **A build-grade verdict for all 96 categories**, replacing the 19-category
   screening map.
3. **The dispatch rule** for rows holding several categories.
4. **Which of the two city-boundary layers is the real one.**
5. **Calgary Transit's own GTFS URL**, since the mirror has no `feed_info.txt`.
6. **Whether a residence signal is wanted at all**, given `homeoccind` is
   constant and Vancouver's parcel substitute removed nothing.
