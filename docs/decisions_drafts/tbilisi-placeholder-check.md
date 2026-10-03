# DECISIONS drafts - Tbilisi's full placeholder check (`tbilisi-placeholder-check`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-02 - Tbilisi: the full placeholder check run; the rule gains a five-company minimum (owner); thirteen points, 13,211 storefronts

- **The full register pull ran** (owner, 2026-10-02, after the landing at
  `e4af1c4d`): 63,511 active rows in 32 pages of 2,000, about 70 minutes,
  peak 0.18 GB, each company's numbered factual address kept only as a
  12-hex hash. The build had skipped it and run a bounded check (the
  previous drafts, folded at the landing).
- **The rule as approved found 25 points**, the eleven listed plus 14 new.
  Read and measured, twelve of the 14 were not placeholders: a tie among
  one-off addresses (the "commonest" bare name held by 1 to 3 companies),
  a street written without a house number (Kazbegi Avenue, Chavchavadze,
  Javakhishvili, Khosharauli, Tsinamdzghvrishvili), the Eliava market (4
  companies) or the airport (4). The test reads "no digit" as "bare", which
  a street name without a number passes.
- **The owner's call (2026-10-02, recommended)**: the commonest bare
  district or settlement name, or blank, must be shared by **at least five
  of the point's companies**, and a person reads the name (a district or
  settlement goes in `PLACEHOLDER_POINTS`, a street, market or other real
  place in `NOT_PLACEHOLDERS`; step 2 exits on a candidate in neither and on
  a listed point no longer a candidate). Tbilisi is the only city with this
  problem, so no precedent applies.
- **With the minimum, 12 candidates**: ten of the listed eleven plus
  **Samgori** (41.6813, 44.859586: "სამგორი", 5 of 22 companies, 17
  storefronts, 631 m from Samgori station) and **a blank point**
  (41.695453, 44.796282: 13 of 41 companies, 24 storefronts, 373 m from
  Liberty Square), both added.
- **Krtsanisi (41.613415, 44.908357), listed at Step 0 and approved with the
  ten, does not reach the minimum** and is kept by reading
  (`PLACEHOLDERS_BY_READING`): 50 of its 66 companies give 50 DIFFERENT
  street addresses on the one point, and the rest write the village name
  Ponichala seven ways, so no single name reaches five; a centroid all the
  same. 9.2 km from the nearest station, so no ring is affected. The lead's
  claim to the owner that the minimum "leaves exactly 13" had checked only
  the new points; it holds with this one point kept by reading.
- **Counts**: thirteen points, 1,522 storefronts left off (was 1,481 on
  eleven); **13,211 placed (80.8%)** (was 13,252): Retail 11,085, Food
  service 1,064, Personal services 1,062. 8,043 (61%) within 0.6 mi of a
  station: 6,699 / 692 / 652. Category only (individual entrepreneurs)
  8,301; company names 4,910.
- **Privacy re-checked** (`check_personal_exposure.py tbilisi`): 0
  individual entrepreneurs shown by name of 8,301; 148 company names read as
  a person's full name, 147 with their legal form. The verdict stands:
  publish.
- **Updated**: the config's rule and lists, step 2 (the full check only; a
  cache without the address key exits naming the fetch), the map, ring
  share, macro facts, the inconsistency rows, About the Data (the "checked
  in part" disclosure removed, the check now complete), What Is Excluded
  (the rule's wording), the master list, PLAN and `app/cities.py`'s
  placement figure. Drift check run and the baseline re-recorded.
- **The shared cache, and a mistake corrected the same day.** The `--force`
  re-pull replaced the raw file master reads (`.build.csv`), and the run on
  this branch wrote `data/tbilisi/processed`, which every checkout shares:
  master's `check_macro_facts` then read 13,211 against its 13,252 and
  blocked every session's push (Cleanup, 2026-10-02). Restored: the keyed
  pull is kept as `.keyed.csv`, which this branch now reads; master's
  `.build.csv` was rewritten from it with master's `factual_address_bare`
  column (the same derivation the build's pull used; the same register, same
  day, 63,511 rows); master's own step 2, run from a checkout of
  `origin/master`, reproduced 13,252, and `check_macro_facts` and
  `check_ring_shares` passed there. **This branch's drift baseline is not
  recorded**: recording it writes the shared processed folder, so it waits
  for the branch to land (then: `drift_check.py tbilisi --update-baseline`).
  Lesson: a branch whose step writes `data/<city>/processed` must not run it
  before it lands, even for its own city; and a re-pull goes under a new
  file name, never over the one master reads.
