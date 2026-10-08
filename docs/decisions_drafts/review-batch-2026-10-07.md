# Review batch 2026-10-07: the integration branch (Cleanup)

Drafts for the fold. One branch, `review-batch-2026-10-07`, carries every
branch of the large review onto master as of bd0e9a8a: `japan-regions`
(with `europe-split` and the Abroad batch), the Abroad batch's drafts tip,
East-1, Kansai-1 and Regional-1, in that order; the pin-colours and
back-links branch joins before the pin.

### 2026-10-07 - The review batch integrated: four builds, the Europe split and Japan's views on one branch; how the overlaps were merged

- **Keep both, in notice order** (the builds' agreed protocol: East-1,
  Kansai-1, Regional-1): city entries in `app/cities.py`, the notice lists in
  `app/components.py` and `app/osm_notice.py`, `docs/data_sources.md` notices
  and source rows, `docs/data_sources/japan.md`, `docs/excluded_categories.md`,
  `docs/map_inconsistencies.md`, `docs/privacy_verdicts.md`,
  `scripts/check_personal_exposure.py`, `scripts/check_provenance.py`, and
  `pipeline/fingerprint_marks.json` (a union of keys; no key held two values).
- **WAVE5_RULES** keeps `name_city` (master) and `default_joined` (East-1);
  Regional-1's 届出者氏名 merged cleanly in OPERATOR_COLS_WAVE5.
- **Lines all three branches edited**, rebuilt rather than picked: the Japan
  row of the source table (the union of every side's cities); japan.md's
  "N cities built" sentence, which said "forty-one" on master's side because
  East-1 never updated it, now "sixty-four" with every city named; the
  notice-number sentence, every number from both sides in order. Regional-1's
  commented form of the `city_rules` one-liner, the same code on every side.
- **`docs/session_roles.md`**: master's paragraph (the A and B build plan's
  open claims) over `japan-regions`' older one; the claims are released at
  landing.
- **The notice blocks** in data_sources.md were reordered by number (Abroad's
  154-156 had landed after East-1's 157-168; check D of `check_provenance.py`
  requires number order).
- **The 30 new Japanese cities retagged** from "Japan West" or "Japan East"
  to the Japan views, from `docs/staged_cities.json`: 8 Tokyo Metropolis, 4
  Saitama Prefecture, 3 Osaka Prefecture, 3 Hyogo Prefecture, 2 Kansai (Uji,
  Tsu), 2 Kanto (Maebashi, Mito), 2 Chubu (Ichinomiya, Gifu), 4 Tohoku
  (Fukushima, Iwaki, Akita, Morioka), Chugoku (Fukuyama), Kyushu-Okinawa
  (Ōita).
- **Labels:** five widths measured in the browser (Fuchū (Tokyo), Fukuyama,
  Maebashi, Mito, Morioka; controls reproduced). Hino's label sits below its
  dot in Tokyo Metropolis: above it, the pill covered Tachikawa's dot 31 px
  away and Tachikawa was labelled in no view. `check_macro_labels.py`:
  PROBLEMS 0, 33 regions, 206 cities.
- **Drift on the 30** (`--jobs 3`, measured peak under the 6 GB declared):
  zero, except where another branch's rule now reaches a city. East-1's
  `default_joined` (owner, call 202) re-placed Uji (+3 storefronts),
  Ichinomiya (+1) and Mito (+4); Kansai-1's `name_city` withholds one more
  row in Tama, not on its map. Baselines updated; the privacy Japan pass
  prints 0 for all four.
- **Left for landing:** Staging's master-list rows (Built 170 -> 206, the
  only `check_provenance.py` failure); Kansai-1's seven maps need
  fingerprint marks, which only the owner's key makes (`fingerprint.py
  coverage` names Uji, the one re-rendered; the other six follow when
  re-rendered); a reboot (app/ changes throughout).
