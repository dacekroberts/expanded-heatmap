# Decisions drafts: Regional-2 (branch worktree-japan-regional-2)

The Regional-2 build session of the A and B build plan
(`docs/build_plan_2026-10-07.md`), phase 2: Shizuoka, Kanazawa, Okazaki,
Aomori, Matsue, Fuji, Matsumoto, Tottori, Yamagata, Kure and Kurashiki, on
pages 258-267 and 306 and notices 205-214 and 216. Newest first; Cleanup folds
these into `DECISIONS.md`.

## Parked calls

None yet.

## Proposals for review time (sentences no template covers)

- **Shizuoka, the source bullet** (the owner asked for each list's date on
  the page, 2026-10-04): "From Shizuoka City's registers of barbers, beauty
  salons and laundries: the complete lists as of March 31, 2026 and the new
  premises listed each month since, to August 31, 2026 for barbers and
  September 30, 2026 for beauty salons and laundries."
- **Shizuoka, the food bullet** (Kōchi's sentence with Shizuoka's share):
  "Restaurants, cafés and shops are not on this map: the national list of
  food businesses gives an address for only about six in ten of Shizuoka's
  restaurants."
- **Shizuoka, the sightseeing bullet** fills the template's slot for a line
  rather than cable cars: "The Oigawa Railway's Ikawa Line, which is a
  sightseeing line, is not drawn."

## Downstream inputs this branch changes

- New cities (Visuals, Analytics): Shizuoka (`shizuoka`, notice 205; English
  station names from OpenStreetMap, rail from MLIT N02). Notice 205: caption
  only (CC BY 4.0 asks for attribution with the work, no placement named).
  No open terms question.
- `pipeline/line_registry.py`: `jr-central-tokaido-line` gains Shizuoka.

## Changes

### 2026-10-11 - Shizuoka built, the city's barber, beauty-salon and laundry registers with their monthly new permits, personal services only

- **Shizuoka built (page 258, notice 205), Kōchi's shape (full lists plus
  monthly openings) on Hamamatsu's three-ward precedent: 2,752 storefronts,
  all Personal services, around 24 stations on 2 lines, 44.2% of them in a
  ring (1,216) on the standard rings.** Sources: Shizuoka City's three BODIK
  datasets (organization 221007), CC BY 4.0 under the city's terms (read
  2026-10-05 by staging, the barber list the same day; calls 10, 11, 39 and
  40): each full list as of 2026-03-31 (686 barbers, 1,752 beauty salons, 306
  laundry rows) and 41 monthly rows since. Food stays off (owner,
  2026-10-04). Built by the Regional-2 lead; the brief passed 10 of 10.
- **The brief's dates moved forward.** BODIK gained R8.9 files for beauty
  salons (3 rows) and laundries (1 row) on 2026-10-06, after the brief; the
  brief says to fetch the newest monthly files at build and re-pin each date.
  Beauty salons and laundries are as of 2026-09-30, barbers 2026-08-31 (no
  barber file for R8.9). Three BODIK downloads on 2026-10-11, 21 s apart: the
  barber full list (re-fetched under the owner's approval of call 39, as the
  brief says) and the two September files; three `package_show` calls before
  them, 21 s apart.
- **Two laundry vehicles the brief did not see.** Step 2 sets aside 2 rows of
  the laundry list whose address ends 県内全域 after a vehicle's plate number:
  mobile laundry vehicles, caught by the foundation's area-wide rule. With the
  1 無店舗 row out, laundries are 306 premises (the brief counted 307 before
  the September row, vehicles included).
- **Step 2:** rows 689, 1,787 and 309; storefront rows 2,782. The join: block
  2,713 (97.5%), town-chōme 68 (2.4%), unplaced 1 (三保宮方, a beauty salon;
  MLIT has no 宮方 under 三保). The foundation's ッ / ツ rule placed the 3
  七ッ新屋 rows the brief left unplaced. 29 repeat rows shown once, so 2,752
  pins (the brief expected 2,750 before the September files). The name rule
  flags 0 rows.
- **Independent check (GSI's address search, 150 block-tier rows, 1 request a
  second, 2026-10-11):** 150 answered; median 26 m from MLIT's block point,
  148 within 100 m, all within 250 m.
- **Rail:** step 1 reproduces the brief: 15 of 15 on the Shizuoka-Shimizu
  Line (gate 3 exact), 10 of 89 on JR's Tokaido Line, 草薙 one group (176 m),
  the Ikawa Line left out by `LEFT_OUT_LINES` (owner, 2026-10-04), 2 stations
  beyond the city line listed (富士, 富士川, both in Fuji). The median
  nearest-station gap is 610 m, where the brief read 624 m: standard rings
  either way (the halving threshold is about 550 m).
- **Station names stand as OpenStreetMap writes them (a judgment call, on the
  operator's own signs):** "Pref. Art Museum" and "Pref. Sports Park" are the
  Shizuoka Railway's own English names for 県立美術館前 and 県総合運動場, not
  OSM's translation, so Fukuoka's trap does not apply; "Shin-shizuoka" and
  "Shin-shimizu" keep OSM's lowercase beside JR's "Shin-Kambara" (Maebashi's
  precedent: OSM's spellings stand). No override, alias or tie.
- **Line colours:** JR Central's Tokaido Line takes `#E86810` from
  `pipeline/line_registry.py` (the registry's `maps` gains Shizuoka); the
  Shizuoka-Shimizu Line is `#0068B8`, `line_colour_search.py`'s nearest to the
  operator's blue. Against the Personal services pin: 88.5 and 106.4 (CIE76);
  `check_line_identity.py` PROBLEMS 0.
- **Line names:** "Shizuoka-Shimizu Line" (the operator's own name for its
  one line, as "Jomo Line" in Maebashi) and "JR Tokaido Line" (the registry's
  name).
- **Privacy verdict: publish.** `check_personal_exposure.py shizuoka`: the
  Japan pass prints 0 of 2,752; no trade name in the raw files is an
  operator's own name. The name rule compares 開設者氏名, 開設者法人, 営業者氏名
  and 法人代表者 in memory only; the operators' own addresses and the phone
  column are never selected.
- **No Economic Census control was run:** the control measures restaurants
  (industry 76) and this page has no food leg. The brief's census ratios for
  the registers (1.22, 1.57 and 1.12 per establishment) stand as measured at
  Step 0.
- **The notice's credit form** follows the licence read's "CC BY 4.0 改変
  form" in Hamamatsu's wording (the three register titles, 静岡市, the CC BY
  4.0 deed, the three dataset pages linked). The city's own terms were not
  re-read at the build.
- Files: `pipeline/shizuoka/`, `outputs/shizuoka/`,
  `app/pages/258_Shizuoka_Heatmap.py`, `app/cities.py`, `app/components.py`
  (notice 205, `_OSM_STATION_NAMES`), `pipeline/countries/japan.py` (the
  batch's eleven `CITIES` entries), `pipeline/line_registry.py`,
  `scripts/check_personal_exposure.py` (the batch's eleven entries), the
  docs rows.
