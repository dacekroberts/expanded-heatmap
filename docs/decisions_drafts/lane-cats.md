# DECISIONS drafts - lane-cats (`lane-cats`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-03 - Japan leftovers: the fetch's row counts, Okayama's stand-in point, the default-point threshold (owner)

- **The owner approved the shared fix for the recorded row counts.**
  `japan_fetch.fetch_city` counted every file with `city_rows(dest)`'s
  default reading. The Japan lead's suggestion was to count through
  `config.source_rows` wherever a city defines one. **Measured on every
  Japanese city first, that would have changed five other cities' counts**,
  because their `source_rows` rebuilds or filters a register rather than
  reading one file:
  - Kitakyushu food 3,383 to 2,417 and Matsuyama's MHLW file 11,575 to 4,205
    (filtered);
  - Sakai's standing list 10,123 to 10,087 (the rebuilt register) and its ten
    monthly files to 0;
  - Kochi's and Tokyo's per-file keys are not `source_rows` keys at all
    (KeyError).
  - **Built instead:** an opt-in hook, `config.file_rows(key)`, "a file's
    rows as the city reads that file". `fetch_city` uses it for the count and
    the REQUIRED_COLUMNS check where a city defines it. Fukui and Toyama alias
    it to their `source_rows`, which each read one file as it stands. No
    other city defines it, so no other city's count can change.
- **Fukui's counts corrected without a download.** `fetch_sources.py city`
  keeps a file already on disk and re-records it, so it was re-run with
  `HEATMAP_NO_NETWORK=1`:
  - food 52,021 to 4,333, barber 3,257 to 268, beauty 9,432 to 788, laundry
    3,058 to 253: the newest sheet's rows, not all twelve sheets';
  - bytes, sha256, `how` and `retrieved` unchanged.
- **Toyama's recorded counts were already right.** Reading with and without
  `merged_header` gives the same row counts (5,616, 372, 1,052, 235, and
  MHLW's 8,168), so its provenance is unchanged. Only its header check now
  reads the way step 2 does.
- **Every other Japanese city checked:** the recorded count equals the
  default reading for all of them. Kyoto records through its portal path,
  Yokohama through its own `fetch_city`, and Sapporo's provenance holds no
  city files. None changes.
- **Fixed in passing:** `record()` wrote `provenance.json` in text mode (CRLF
  on Windows); it now writes bytes.
- **Okayama's sentence (owner: approved),** verified first in memory against
  the cached data (`japan_step2.run(write=False)`): 16 rows unplaced, 13 of
  them on the one point MHLW gives to filings in 13 different towns
  (34.6671, 133.9471 to 4 places), 0 of the 2 town-center rows. Added to the
  "Not placed" line of Okayama's What Is Excluded section, the section the
  proposal named; the page itself carries no unplaced count.
- **The default-point guard stays at 3 or more towns (owner: "OK as is").**
  Kitakyushu's 9 pins on points shared by fewer than 3 towns stay on the map.
  No code change.

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
