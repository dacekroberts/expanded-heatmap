# DECISIONS drafts - Korea sweep (`korea-sweep-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-04 - korea_sbiz: a 시군구코드 filter beside the 시군구명 prefix, zero drift on the ten built SEMAS cities

- **The change** (`docs/handoff_korea_sweep_2026-10-03.md`, Phase 1):
  `pipeline/countries/korea_sbiz.py` now reads `시군구코드` and
  `storefronts()` takes `sigungu_codes`. Given codes, they decide the rows;
  given prefixes as well, the two must pick identical rows or the step
  exits. An unknown code exits rather than silently matching nothing. The
  built cities pass prefixes only and are read exactly as before; the output
  columns are unchanged (the code is read, never written).
- **Why:** 시군구명 is not unique within a SEMAS member. Gwangju's 동구,
  서구, 남구 and 북구 recur in other metropolitan cities, and 경기도 광주시
  is another city; the 2026 merger put Gwangju in the member
  전남광주통합특별시 with all of South Jeolla. A code is unambiguous.
- **Verified:** `python pipeline/drift_check.py` over the ten built SEMAS
  cities (Incheon, Goyang, Suwon, Yongin, Seongnam, Bucheon, Ansan, Anyang,
  Namyangju, Uijeongbu), under `heavy_job.py`: **zero drift** in every
  output, and the four cities with a `baseline.json` (Ansan, Anyang,
  Namyangju, Uijeongbu) report 10 figures unchanged. Measured peaks: Goyang
  alone 0.38 GB, the other nine two at a time 0.75 GB.
- **Session setup, 2026-10-03:** branch 0 behind `origin/master` at
  `fafec401`; registered in `docs/session_roles.md`; `brief_check.py
  daejeon gwangju gimhae` 13/13 claims hold.
