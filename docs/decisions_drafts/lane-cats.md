# DECISIONS drafts - lane-cats (`lane-cats`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-03 - Washington D.C. drops "Beauty Booth" under the person-licence rule (owner: "drop and note")

- **The owner ruled on the one pending departure the person-licence rule
  found** (2026-10-02, "A category rule for a person's own license"): D.C.'s
  "Beauty Booth" (6 licence rows, a chair rented inside a salon) leaves
  Personal services.
  - `pipeline/taxonomies/dc_businessactivity.py`: moved from
    `PERSONAL_SERVICES` to `EXCLUDED`, with the rule as its reason.
  - `scripts/category_continuity_table.py`: the pending cell is now
    `fixed(...)`, so the check enforces "out"; `AWAITING_OWNER` is empty.
- **"Note":** one sentence in D.C.'s section of
  `docs/excluded_categories.md`. The city page names only General Business
  and the residential rentals among its exclusions, so it gains no sentence.
- **Measured on the re-run (steps 2 to 4):** 5,269 to 5,265 premises after
  dedup; 5,207 to 5,203 pins (Personal services 501 to 497); 3,845 within a
  ring. The 6 rows sit at 5 sites, and **only 1 of the 5 keeps another salon
  or barber pin**; the other 4 leave the map with the licence.
- **The geocoder cache was re-keyed, not re-fetched.** Step 2 renumbers
  `record_id` after dedup, so dropping one un-geocoded booth row changed the
  Census batch's payload and so its cache key. Each response line answers one
  input address, so the cached response for the old payload (448 rows,
  `batch_000_9bd4f1b831.csv`) was re-keyed to the new ids by identical input
  address: 447 of 447 matched, and the one old row with no new row is the
  dropped booth (450 L'Enfant Plz SW). Written as `batch_000_422667ddd6.csv`;
  step 3 then ran offline (`HEATMAP_NO_NETWORK=1`). Census matched 385 of
  447; 62 unplaced.
- **The page's geocoder sentence corrected to 385 and 62**: it still said
  387 and 64, the 2026-09-21 build's figures (of 451), already stale before
  this change.
- **Privacy check re-run (`check_personal_exposure.py washington_dc`):
  unchanged.** 0 emails, phones or care-of markers; 14 sole-proprietor
  person-like pins of 3,845 (0.36%); 0 at a residential unit. The verdict row
  in `docs/privacy_verdicts.md` needs no change.
