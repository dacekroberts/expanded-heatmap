# Does publishing a business name at an address breach a Canadian licence?

Written 2026-09-21, during the Canadian screen. **A developer's reading of
primary sources, not legal advice** — the same framing `docs/data_sources.md`
uses. Every quote below is from the statute or the regulator, not a summary.

## Why this note exists

Every Canadian Open Government Licence in `docs/licenses/` carves **Personal
Information** out of the grant, and each defines it by pointing at its own
province's statute. So the carve-out cannot be read without the statutes, and
the four provinces do **not** say the same thing. An early assumption during
the screen — that publishing a sole trader's name would breach the licence —
was wrong for Ontario and is differently wrong everywhere else.

The question that matters: **is a business name at an address, where the
business may be a person operating from home, Personal Information?**

## Ontario — verified, and the most permissive

MFIPPA s.2(2.1) / FIPPA s.2(3), via the IPC's own interpretation bulletin
(stored here as `ipc-ontario-interpretation-bulletin-personal-information.pdf`):

> "Personal information does not include the name, title, contact information
> or designation of an individual that identifies the individual in a
> business, professional or official capacity."

And s.2(2.2) / s.2(4) closes the home-business gap explicitly:

> "For greater certainty, subsection (3) applies even if an individual carries
> out business, professional or official responsibilities from their dwelling
> and the contact information for the individual relates to that dwelling."

The bulletin adds that "individual" means natural persons only — "Had the
legislature intended to include a sole proprietorship, partnership,
association or corporation, it could and would have used the appropriate
language."

**So in Ontario a home-based sole trader's business name at their home address
is inside the grant.** Toronto's `Client Name` column is very likely licensed,
not excluded.

What survives is the IPC's second limb: business-capacity information can
still be personal if disclosure "would reveal something of a personal nature
about the individual".

## British Columbia — verified, and nearly as permissive

FIPPA Schedule 1, from bclaws:

> "contact information" means information to enable an individual **at a place
> of business** to be contacted and includes the name, position name or title,
> business telephone number, business address, business email or business fax
> number of the individual

and personal information is recorded information about an identifiable
individual **other than contact information**.

**The gap Ontario closes, BC leaves open.** BC says "at a place of business";
it does not say, as Ontario does, that this holds when the business is carried
on from a dwelling. A home-based sole trader is therefore less clearly covered.

**This does not bite in practice, because Surrey resolves it in its own data.**
Surrey's Business Directory carries `LicenseType`, splitting 14,015 Home
Occupation from 13,066 Commercial/Industrial. Filtering to
Commercial/Industrial — which this project would do anyway, being a storefront
map — removes exactly the ambiguous set. Vancouver has no equivalent flag, so
the question stays live there.

## Alberta — the licence points at a repealed statute

OGL – City of Calgary v2.1 defines Personal Information as having "the meaning
set out in section 1(n) of the Freedom of Information and Protection of
Privacy Act (Alberta)". Per the Alberta government's own fact sheet:

> "In December 2024, Alberta's government passed legislation to **repeal the
> Freedom of Information and Protection of Privacy (FOIP) Act** and split it
> into two pieces of legislation – one dealing with protection of privacy and
> the other dealing with access to information. The acts and associated
> regulations came into force in June 2025."

So Calgary's carve-out cites a repealed Act. The Protection of Privacy Act
(POPA) is its privacy successor. Whether the reference reads across to POPA,
freezes at FOIP's repealed text, or is simply stale was **not** established
here, and POPA's own definition of personal information was not obtained.

Not a blocker — Calgary's business data is otherwise clean, and it ships
`homeoccind`, the same home-occupation flag that resolves the question in
Surrey. But it makes Calgary's carve-out the least certain of the four, and
it is worth a second look before building.

## Québec — structurally different, and the weakest of the four

P-39.1 art. 1, as amended by Law 25 (2021 c.25 a.100), from Légis Québec:

> "Les sections II et III de la présente loi ne s'appliquent pas à un
> renseignement personnel qui a un caractère public en vertu de la Loi. Elles
> ne s'appliquent pas non plus aux renseignements personnels qui concernent
> **l'exercice par la personne concernée d'une fonction au sein d'une
> entreprise**, tels que son nom, et sa fonction, de même que l'adresse,
> l'adresse de courrier électronique et le numéro de téléphone de **son lieu
> de travail**."

Two differences from Ontario and BC, both of which cut the same way:

1. **It is not a definitional exclusion.** Ontario and BC say such information
   *is not* personal information. Québec says two divisions of the Act *do not
   apply* to it. The information remains personal information; the Act's reach
   is narrowed. That is structurally weaker.
2. **"Une fonction au sein d'une entreprise"** — a function *within* a
   business — is framed for employees and officers, not for the sole trader who
   **is** the business. And "son lieu de travail" is, for a home-based sole
   trader, their home.

Note also that Montréal's own licence does not defer to a statute at all. It
adds its own prohibition: "Nous proscrivons tout usage malveillant ou abusif de
nos données, notamment toute tentative d'identifier une personne, une
entreprise ou une organisation" — unusual in naming businesses and
organisations alongside persons. It reads as a re-identification prohibition
rather than a bar on republishing data already identified at source, but that
is a judgment call.

**This does not bite Montréal either, and for the best possible reason.**
`locaux-commerciaux` is a field survey of *premises*, not a register of
*registrants*. Its name column is `NOM_ETAB` — the establishment's name. There
is no registrant, licensee or owner name column anywhere in it. The strongest
Canadian candidate sits under the weakest privacy regime and is untouched by
it, because its data is premises-based rather than person-based.

## What this means for the project

**The project's existing discipline is above the legal floor in every one of
the four provinces, deliberately.** That is how `DECISIONS.md` already frames
it for the US cities: Los Angeles' registry would have published ~4,000
individuals' names at their premises, and the project declined even though the
data was public and publishing was permitted.

So the residence filtering and the never-download-owner-names habit stay what
they were — a stated ethical position, not a compliance obligation. That is a
**stronger** footing than compliance, because it does not move when a statute
is repealed, as Alberta's just was.

Per-city, the practical position:

| City | Name column in the data | Exposure |
|---|---|---|
| **Montréal** | `NOM_ETAB` — establishment | **None.** Premises survey, no person names at all |
| **Surrey** | `BusinessName`, never blank | **MEASURED — small but real, ~1%.** An earlier claim that dropping Home Occupation "resolves" it was **wrong**; see below |
| **Calgary** | `tradename`, **never blank** | **MEASURED — clean.** The 25.54% person-pattern rate is almost all false positives; see below |
| **Edmonton** | `business_name` (no trade-name column at all) | **MEASURED — a real problem.** See below |
| **Vancouver** | `businessname` + `businesstradename` | **MEASURED — a real problem.** See below |
| **Toronto** | `Operating Name` + **`Client Name`** | Licensed under Ontario's business-capacity rule, but `Client Name` is a person or company and should not be downloaded regardless |

## Vancouver and Edmonton, measured 2026-09-21

Using `scripts/check_personal_exposure.py`'s own patterns against the raw
registries — Vancouver's 58,346 current-year Issued licences, Edmonton's
43,672 rows. **These are raw-registry rates, not mapped-pin rates**, so they
are not directly comparable to the US figures in `DECISIONS.md`, which are
measured after step 2 filtering. They are indicative, and both are bad.

**Vancouver — the storefront filter makes it worse, not better.**

- Trade name is blank on **63.0%** of rows, so the pipeline would fall back to
  the legal name on nearly two-thirds of them. That is the Los Angeles trap
  (68%) at almost the same severity.
- **8.21%** of displayed names match the person pattern (4,792), of which 1,182
  sit at a unit address.
- **1,467 rows take the "Person (Trade Name)" form** — the New York pattern
  that is invisible to every other test.
- Critically, person-like names **concentrate in exactly the categories this
  project maps**: Limited Service Food 22.3%, Restaurant 20.0%, Retail Dealer
  18.6%, Retail Dealer - Food 13.2%, Beauty Services 7.8%. Restricted to those
  storefront types the rate is **16.94%**, against 8.21% across all types.
  Filtering to storefronts **doubles** the exposure.

**Edmonton — has a hidden home flag, which does not save it, and needs a
geocoder as well.**

- `business_address` is literally the string **`<Home Based Business>`** on
  **14,114 rows (32.3%)**. Not a column, a placeholder in the address. **Zero
  of those rows carry coordinates**, so they drop out of any map automatically.
- But the *mappable* set — 23,265 rows with coordinates and a real address —
  still carries **17.45% person-like names (4,059)**, slightly *higher* than
  the home-based subset's 15.91%. The flag does not solve the problem.
- **Only 53.3% of rows have coordinates at all.** Edmonton therefore needs
  geocoding for roughly 47% of its rows, which makes Toronto not the only
  Canadian city with a geocoder dependency.
- Edmonton has **no trade-name column**, so there is no fallback question:
  the only name available is the business/legal name.

## Calgary, measured — and it corrected the method

23,203 rows. Two structural facts change the reading:

- **`homeoccind` is `N` on all 23,203 rows.** The flag exists but has one
  value here, so this export is already non-home by construction. An earlier
  claim in this project that Calgary "ships a home-occupation flag" as a usable
  discriminator was **wrong** — there is nothing to discriminate.
- **`tradename` is blank on 0.0% of rows.** There is no registrant-name
  fallback, because a trade name is always present.

The person pattern flags **25.54%** (5,925) — the highest rate of the three
measured. **It is almost entirely false positives.** A random sample of 18
hits contained **zero people**: SANDSTONE CHEVRON, CHICKADEE REFILLERY, ROYAL
FADEZ, CRUMBL COOKIES, AFFINITY TIRES, APARTMENT BUILDING. The `PERSON` regex
matches any two capitalised words, and two-word trade names are extremely
common.

### The discriminator is trade-name availability, not the name pattern

This is the lesson to carry to every future city, and it is already the first
thing `check_personal_exposure.py`'s own docstring names — "pins whose
displayed name can ONLY be the owner/registrant fallback … the authoritative
measure". The regex is the *secondary* heuristic and its precision collapses
when the column is a chosen trade name.

| City | Trade name available? | Real exposure |
|---|---|---|
| **Calgary** | 100% | **~none** — no fallback is possible |
| **Montréal** | `NOM_ETAB` 100% | **~none** — establishment names |
| **Toronto** | `Operating Name` **99.2%** | **~none on the fallback axis** — see below |
| **Surrey** | `BusinessName` 100% | **~1%** — small but real, see below |
| **Vancouver** | **blank on 63%** | **Real.** Falls back to the legal name on two-thirds of rows |
| **Edmonton** | **no such column** | **Real.** The business/legal name is the only name |

## Surrey and Toronto, measured 2026-09-21 — both earlier claims were wrong

**Surrey: dropping Home Occupation does NOT resolve the exposure.** The claim
that it did was asserted without measurement and is false. The person-pattern
rate is essentially identical on both sides of the split:

| Subset | Rows | Person-pattern |
|---|---|---|
| Home Occupation (dropped) | 14,016 | 9.11% |
| Commercial/Industrial (kept) | 13,066 | **9.38%** |

The split is a *premises* filter, not a *name* filter, and there is no reason
it would have been the latter. A random sample of 18 hits from the kept set
contained **2 apparent real people** among 16 businesses (Burger King,
Scholastic Canada, Urban Barn, Healthmart Pharmacy…), so the true-positive rate
is roughly 11% and the real exposure is about **1% of kept rows — on the order
of 135 pins**. That is San Francisco's territory (1.19%), which this project
treated as "the real one" and built a filter for. Surrey needs the same.

**Toronto: `Operating Name` is blank on only 0.8%**, so Toronto lands in
Calgary's group, not Vancouver's — there is effectively no registrant-name
fallback. Its 25.42% person-pattern rate on `Operating Name` is the same
two-word-trade-name noise measured in Calgary.

Two real things remain for Toronto:

- **`Client Name` is unambiguously a person column** — 395 surname-first
  ("Smith, John") forms in the sample, against 1 in `Operating Name`. It must
  never be downloaded, exactly as Philadelphia's registrant columns are not.
- **202 rows (2.7%) have `Operating Name` identical to `Client Name`**, so
  they publish the legal name even though the trade-name field is populated.
  Small, and worth filtering.

**Sampling caveat for Toronto:** the datastore returns rows in `_id` order, so
this is the first 32,000 of 159,872, not a random sample — 7,443 of them
uncancelled. The blank rate is unlikely to vary much, but the *active* share
may, and the figures should be re-measured on the full export before a build.

**What this re-ranks.** Montréal, Calgary and Toronto are clean on the
fallback axis. Surrey and Edmonton looked like they needed filters; the next
section shows they do not, and that Vancouver is the only real gap.

## Canada's home signal is at the LICENCE level, not the parcel level

Every US city in this project infers "is this someone's home?" from a parcel
or assessment join — San Diego's `ownerocc`, San Francisco's homeowner
exemption, Los Angeles' `Roll_HomeOwnersExemp`, Philadelphia's homestead
exemption. Checked 2026-09-21, **no Canadian province publishes an
owner-occupancy flag**: BC Assessment is not open data, and the open municipal
property datasets carry zoning and assessed values but nothing about occupancy.

Canada compensates with something **more direct**: the municipality states
whether the licence is for a home-based business.

| City | Licence-level home signal | Rows |
|---|---|---|
| **Surrey** | `LicenseType = 'Home Occupation'` | 14,015 of 27,082 |
| **Edmonton** | `business_address = '<Home Based Business>'` | 14,114 of 43,672 — **and none carry coordinates** |
| **Calgary** | `homeoccind` | `N` on all 23,203 — already excluded from this export |
| **Vancouver** | **none** | — |

That is a *better* signal than the US inference chain, because it is the city
asserting the fact rather than the project deducing it from land use plus an
exemption flag.

### This corrects an over-correction made earlier in this file

An earlier note said Surrey's Home Occupation split "does NOT resolve the
exposure", because the person-pattern rate is 9.11% on the dropped side and
9.38% on the kept side. That is true and it is the wrong test. It conflates
two different things:

- the **name-pattern rate**, which a premises filter has no reason to change;
- the **privacy exposure**, which is *a person's name published at their home*.

Dropping Home Occupation removes precisely the rows where those coincide. The
residual person-named businesses sit at Commercial/Industrial premises — "Jane
Smith Hair Salon at 123 Main St" — which is business identity information,
squarely inside BC's contact-information carve-out for "an individual **at a
place of business**", and the same thing every built US city already publishes.

**So Surrey and Edmonton are mitigated by their own data.** Surrey by dropping
Home Occupation; Edmonton by construction, since its home-based rows have no
coordinates and cannot be mapped at all.

### Vancouver is the only genuine gap, and its join is structurally hard

Vancouver has no licence-level home flag, so it needs the US-style approach.
The land-use half exists: **`property-tax-report`** (1,553,448 records,
OGL–Vancouver) carries `zoning_classification` with clean values — One-Family
Dwelling 202,740, Two-Family Dwelling 48,300, Multiple Dwelling 87,557,
Commercial 132,576 — plus `legal_type` (LAND 627,846 / STRATA 924,073).

**But joining it by address does not work.** Tested 2026-09-21 against the
29,660 mappable licences: **6.5% matched**. The formats are systematically
different:

- direction is **prefixed** in licences (`W 8TH AV`) and **suffixed** in the
  tax roll (`8TH AVE W`);
- street types differ — `AV` against `AVE`;
- only **35%** of licence street names appear verbatim in the tax roll;
- civic numbers are stored as **ranges** (`from_civic_number` /
  `to_civic_number`) with nulls, so exact matching fails structurally.

This is San Francisco's problem exactly, and San Francisco's answer applies:
**join spatially, not by address.**

### Tested 2026-09-21 — the spatial route works, and better than San Francisco's

Business point → `property-parcel-polygons` (99,701 parcels, spatial) →
`property-tax-report` on `tax_coord` = `land_coordinate` → zoning. In
EPSG:32610:

| Step | Result |
|---|---|
| Point **inside** a parcel | **29,642 of 29,660 — 99.9%** |
| + nearest parcel within 40 m | 18 more, median 0.0 m → **100.0%** |
| Parcel → zoning class | **29,549 — 99.6%** |

Better than San Francisco, which reached 93.4% at a median 1.4 m, and far
better than San Diego, whose coordinates sit 5–15 m off their own lot and
needed a buffered nearest-centroid query per point. **Vancouver's coordinates
sit on their parcels.**

### The filter this produces is small

| | Rows | Share |
|---|---|---|
| Purely residential zoning | 2,947 | 9.9% |
| Person-like name | 3,134 | 10.6% |
| **Both — the filter candidate** | **232** | **0.78%** |

And **174 of those 232 are `Long-term Rental`**, which this project excludes as
non-storefront anyway — as it did for D.C.'s 49% rental rows and
Philadelphia's. The residual after a storefront filter is on the order of
**~58 pins**: Restaurant 13, Retail Dealer - Food 7, Limited Service Food 6,
Health Care 6. That is Philadelphia's territory (8 pins), not San Francisco's
(217).

**So Vancouver is not the expensive problem it looked like.** It needs the
two-hop spatial join rather than an address join, and that join is cheap and
accurate.

### The one real blind spot

**`Comprehensive Development` is the zoning on 11,935 mappable licences — 40%
of them** — and it is a mixed-use designation, so those rows are never flagged
residential. A home-based business on CD-zoned land is invisible to this
filter, and CD covers exactly the dense central areas where a "home" is a
condo. Philadelphia's mixed-use lesson, inverted: there, land use *over*-fired
on mixed use; here it *under*-fires.

### The obvious refinement was tested and REJECTED — do not retry it

`legal_type` (LAND vs STRATA) rides along on the same join, and STRATA plus a
person-like name on CD land looks like it should isolate the condo home
business. Tested 2026-09-21. **It carries no signal.**

Of 11,935 CD-zoned mappable licences: LAND 9,648, STRATA 2,271, OTHER 16. Of
the 1,183 with a person-like name: LAND 928, STRATA 253.

| | STRATA share |
|---|---|
| All CD licences | 19.0% |
| CD licences with a person-like name | 21.4% |
| **Enrichment** | **1.12x** — i.e. none |

If STRATA marked home businesses, person-like names would concentrate there.
They do not.

**The business types settle it.** The 253 candidates are Restaurant 37, Health
Care Professionals 37, Limited Service Food 29, Retail Dealer 23, Legal
Services 20, Beauty Services 14. A random sample of 16 names: *Tim Hortons,
Taco Time, Kiku Sushi, Daikichi Sushi, Caffe Artigiano, La Tasca, Praxis Legal,
Metric Architecture, Hummingbird Notaries, CoastKids Pediatrics, Aquarius
Chiropractic…* — **not one looks like a home business**, and most are not even
people (the two-word false positive again).

**STRATA on CD land means "a commercial unit in a mixed-use building", not "a
flat someone lives in".** Which is exactly what Comprehensive Development
zoning is designed to produce. A unit number does not separate them either —
42% of the candidates have one, and so do commercial units.

**So the CD blind spot is real but much smaller than it looked.** What it
misses is mostly not a home. A genuine home business in a CD-zoned condo would
most likely be licensed as Long-term Rental or Short-term Rental Operator,
which this project excludes as non-storefront regardless.

Recorded as a rejected approach so the next person does not spend the same
afternoon on it.
