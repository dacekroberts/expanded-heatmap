---
name: multi-source-city
description: Assemble a city's business coverage from several registries when no single one covers all three buckets - diagnose it, find a source per bucket, wire the dispatching taxonomy, and run the licence and privacy checks that every added source multiplies. Use when a city's best business dataset turns out to be activity-specific permits rather than a general register (New York and Philadelphia both are), or when a bucket comes back empty.
---

# Building a city from several registries

Distilled from New York, the first city built this way, and Philadelphia's
Step 0. Read `add-city` first - this is a branch of its Step 0 and Step 5, not
a replacement.

**The pattern this exists for:** most large US cities do not license general
retail. A city either has a general business register (San Diego, San
Francisco, Los Angeles on NAICS; Chicago on its own licence taxonomy) or it
has activity-specific permits, in which case one registry cannot fill the
three buckets and a single-source build produces a false map.

## Step 1 - Diagnose before you scaffold

**Pull the category distribution before writing any pipeline code.** Not the
row count, not the schema - the distribution. This is the cheapest query in
the whole build and it is what tells you which kind of city you have.

```
# Socrata
$select=<category_field>, count(1) as n&$group=<category_field>&$order=n DESC
# Carto / PostGIS
SELECT <category_field>, count(*) AS n FROM <table>
  WHERE <active_filter> GROUP BY 1 ORDER BY n DESC
```

Then read it against the three buckets and ask: **could a reader find a
restaurant, a grocer, a clothes shop and a hairdresser in here?**

What the two diagnosed cities looked like:

| City | Distribution said | Verdict |
|---|---|---|
| New York (DCWP `w7w3-xahh`) | 13,385 of 35,245 active premises licences are home improvement contractors. **Zero** restaurants, grocery, clothing, pharmacies or salons | Regulated-activity list. Needed 4 sources |
| Philadelphia (L&I `business_licenses`) | **79%** of 118,535 active licences are `Rental` - residential landlord registrations. Food well covered (~9,059); no retail or salon licence type exists | Activity-specific. Needs a decision before building |

**Two traps at this step:**

- **A dataset title is not evidence.** Both of the above were recorded in
  the city shortlist of the time (`docs/city_shortlist.md`, retired
  2026-09-27 for `docs/city_master_list.md`) as viable single sources on the strength of their
  titles and a schema check. The schema was fine; the *contents* answered a
  different question.
- **A big row count hides the problem.** Philadelphia's 118,535 active
  licences look like plenty until 93,471 of them are landlords. Always look at
  the distribution, never the total.

If one bucket is missing, go to Step 2. If a bucket is missing and no source
exists for it, go to Step 6 - say so rather than shipping a skewed map
silently.

## Step 2 - Find a source per bucket

These archetypes have held across every city checked so far. Verify each live;
do not assume a city has the equivalent.

| Bucket | Look for | Why it works | Verified example |
|---|---|---|---|
| **Food service** | The health department's restaurant inspections or food-service permits | Every restaurant is inspected, so coverage is near-complete - usually the strongest source in the whole build | NYC DOHMH `43nn-pn8j` (31,319 establishments); Boston "Active Food Establishment Licenses" |
| **Retail - grocery** | The **state** agriculture/markets retail food store licence | Bodegas, delis, supermarkets. Statewide, so it needs geographic scoping | NYS `9a8c-vfzj` (11,472 NYC rows) |
| **Personal services** | The **state** cosmetology / barber / appearance-enhancement **business** licence | Salons, nail, skin care, barbers - squarely NAICS 8121 | NYS `y3u4-jbgh` |
| **Retail - regulated slice** | The city's own consumer-protection licences | Tobacco, e-cigarette, secondhand, electronics, pawn. Narrow, and mostly *adjunct* - see Step 4 | NYC DCWP `w7w3-xahh` |
| **Retail - general** | **Usually does not exist.** Clothing, books, hardware, florists are unlicensed in most US cities | — | — |

**Two structural notes:**

- **State sources are statewide.** They carry no city marker, so scope them by
  point-in-boundary, not by a city-name field - postal city names inside one
  city are unreliable (Ridgewood, Corona and Astoria are all Queens). New
  York's step 2 dropped 15,387 upstate salons this way.
- **Prefer a business-level licence over an individual one.** Where a registry
  licenses both, the individual types are people, not storefronts: NYS
  appearance enhancement has `DOSAEBUSINESS`/`DOSBARSHOPOWNER` (keep) and
  `DOSAERENTER`/`DOSBARRENTER` (drop - a chair renter inside someone else's
  shop, which would double-count the shop *and* put a person on the map).

## Step 3 - Licence and terms checks, once per source

**This is the step that gets skipped, and every added source multiplies it.**
Four sources means four licence positions, four sets of terms, and up to four
notices the site must display. Record each in `docs/data_sources/<country>.md` as you
verify it, per `add-city` Step 0 item 4 - a city is not done until its terms
are recorded, because afterwards an unrecorded gap looks exactly like a
checked one.

For each source, before it is used:

1. **The declared licence.** Socrata exposes it at
   `<domain>/api/views/<id>.json` - read `license`, `licenseId`,
   `attribution`, `attributionLink`.
2. **If none is declared, find the governing terms** - and look for the
   *portal's* terms document, not the parent site's footer.
3. **Anything the project must DISPLAY.** Add it to the "Notices this project
   MUST display when published" section, which gates the public deploy.
4. **Anything needing a human decision** - a purpose limitation, a bar on
   modification. Raise it; do not read the clause generously. Record the
   verdict and its reasoning in the session's drafts file
   (`docs/decisions_drafts/`, folded into `DECISIONS.md` later) and attribute
   the call.

The rows and notices are reader text on About the Data: one row per source
under the city's name, the city's coverage gaps in its own rows, no process
notes outside `<!-- internal -->` markers (`docs/city_page_format.md`,
sections 2 and 3).

**Findings worth carrying in, all of them counter-intuitive:**

- **A missing licence field does not mean permissive** - and it does not mean
  prohibited either. New York City declares no licence on any dataset because
  **Local Law 11 of 2012 forbids it from imposing one**: data sets "must be
  available without registration requirement, license requirement, or usage
  restrictions". The absence was compliance.
- **A parent site's footer is not the data's terms.** nyc.gov's "All Rights
  Reserved" covers that website's content, not datasets published under the
  Open Data Law. Reading it as governing gave exactly the wrong answer.
- **State and city portals differ within one metro.** Open NY's terms are
  among the most permissive anywhere ("you may use it as you wish, subject to
  no other requirements"); the city's are governed by statute. A four-source
  New York build spans both.
- **Terms can be tighter than the open-data framing suggests.** Chicago
  requires a **verbatim disclaimer** wherever a derivative application is
  accessed. LA Metro forbids modifying its data. Neither is a reason to skip a
  source - it is a reason to record and comply.
- **A page that blocks automated fetching is not a dead end.** Chicago's data
  terms return 403 to a scripted request; the browser loads them fine.

**The standing removal commitment covers new sources automatically** (see
`docs/data_sources.md`). Do not weaken it for a source with tighter terms -
record the terms and comply.

## Step 4 - Architecture: one dispatching taxonomy

New York's shape, which needed **no change to `map_common.py`**:

- `pipeline/taxonomies/<city>.py` exposes the normal interface plus
  `EXTRA_COLUMNS = ("source",)`, and `classify()` dispatches on that column.
  The multi-column mechanism already existed for Chicago's `business_activity`.
- `VALUE_COLUMN` holds **each source's own category string**, so a tooltip
  shows the registry's own words ("Pizza", "Retail food store").
- `FIELD_LABEL` must be generic ("Category") - it is shared across sources.
  It renders in every tooltip, so it and any English label the module
  writes are American English (`premises-taxonomy` Step 8).
- The city's `config.py` gets a `SOURCES` table: per source, the raw file, the
  endpoint, the **server-side filter applied at download**, and which columns
  carry the name, category and address.
- Step 2 gets one loader per source, each normalising to the same shared
  columns plus `source`, then concatenates and runs
  `filter_to_storefront(df, <city>)` once.

**Membership is often the classification.** A restaurant-inspection registry
contains only food service, so every row maps to that bucket regardless of its
cuisine field - do not build a mapping table where a constant will do, and say
so in a comment.

## Step 5 - Cross-source deduplication

A bodega with a food counter can hold a health permit, a state food store
licence *and* a city tobacco licence. Three sources, one storefront.

- **Merge on address AND a normalised business name - never address alone.**
  One address routinely holds many separate shops; in New York 14,830 rows
  shared an address with another row. Address-only merging deletes real
  businesses.
- **Under-merging is the safer error.** A spelling difference between two
  registries leaves a business counted twice, which inflates density slightly
  rather than erasing storefronts. **Print both numbers** so the trade-off is
  visible, and state it on the city page (New York's bullet is in Step 6).
- **Rank the sources** (`SOURCE_PRIORITY`): the registry that identifies a
  business most specifically wins. Food permit, then grocery licence, then
  salon licence, then the city's regulated licences.
- **Adjunct licences come last.** A tobacco, e-cigarette or sidewalk-stand
  licence is a *permission a business holds*, not the business. Rank them
  lowest so they add a pin only where no other registry names that site -
  which is how a bodega is counted once, as a grocer, rather than three times.
  Chicago's single-source pipeline already does this for its own TOBACCO
  licence; the same idea across sources.

## Step 6 - Privacy, per source, and honesty about coverage

**Every source has its own name-fallback risk; check them separately.** Add the
city to `scripts/check_personal_exposure.py` and run it after step 2, per
`CLAUDE.md`.

- **Never load a registrant-name column.** New York's salon registry has
  `license_holder_name`; it is not in the download's `$select`, and step 2
  **asserts** it never arrives. That is why New York can report that no pin
  *can* be a registrant's name - a structural claim, not a measurement.
- **Look for a structured residence signal** before falling back to regex on
  address text. NYC's DCWP has `unit_type` (APT/STE/FL/RM as separate values);
  Philadelphia has `legalentitytype` (Individual vs corporate), which is
  better than any name heuristic. San Diego's 0.04% reading was a measurement
  *gap*, not a clean result, because its unit values are bare ("A", "101").
- **A category that is mostly individuals is a scope error first.** Excluding
  it is easier to justify as a correction to what the map is about than as a
  privacy carve-out, and it fixes both: NAICS 454 nonstore retailers,
  Philadelphia's `Rental`, DCWP's `Individual` licence type.

**Then say what the map does not cover, on the city page.** If a bucket is
thin, a reader will otherwise infer something about the city's high streets
from a fact about its licensing. The page format is `docs/city_page_format.md`
section 1: these are bullets under **The businesses**, between the map's
captions and "Using the map". New York's bullets, as the page carries them
now, are the model:

> - **Four registries, because New York has no general business license.**
>   Food service comes from the Health Department's restaurant permits, grocery
>   and bodega retail from the State's retail food store licenses, salons and
>   barbers from the State's appearance-enhancement licenses, and a narrow
>   slice of regulated retail from the city's own Consumer and Worker
>   Protection licenses.
> - So **the Retail category here covers less of the trade than in most
>   cities on this site.** A clothing shop or a bookshop needs no license from
>   any of these four registries, so it is simply absent, while restaurants
>   appear because the city inspects them.
> - Read the balance between categories as a fact about New York's
>   licensing, not about its high streets.
> - Where one business appears in two registries it is counted once, matched
>   on address and name; a spelling difference between two registries can
>   leave it counted twice.

These fill in the scaffold's **The businesses** bullet ("the data source, and
any category it is missing"), so a new city's version needs no read-back; a
sentence beyond what the scaffold's bullets cover is a proposal, flagged in
the drafts file (`docs/city_page_format.md`, section 6), and the build goes
on.

Record the same in `docs/excluded_categories.md`, **in the city's own
section** (`### <City> - ...` under "Excluded in one city"), as what is
*missing* rather than *excluded*: New York's section carries it as a
paragraph led "**Missing rather than excluded**". The shared "What is missing
rather than excluded" and "Honest limits" sections hold only what is true of
every city. The distinction matters, because everything else on that page was
a choice and this was not.

## Checklist

- [ ] Category distribution pulled and read against the three buckets
- [ ] A source identified per bucket, or the gap stated explicitly
- [ ] Individual/renter licence types dropped in favour of business ones
- [ ] State sources scoped by boundary polygon, not city name
- [ ] **Licence, terms and any required notice recorded per source** in
      `docs/data_sources/<country>.md` (notices in `docs/data_sources.md`'s
      gate); clauses needing a decision raised, not resolved
      generously
- [ ] Dispatching taxonomy with `EXTRA_COLUMNS = ("source",)`; `map_common.py`
      untouched
- [ ] Dedup on address + name, both numbers printed, priority ranked, adjunct
      licences last
- [ ] No registrant-name column loaded anywhere; an assertion proves it
- [ ] `scripts/check_personal_exposure.py` run, the verdict in the drafts
      file and its row in `docs/privacy_verdicts.md`
- [ ] Thin buckets stated as bullets under **The businesses** on the city
      page and in the city's own section of `docs/excluded_categories.md`
      (`docs/city_page_format.md`)
