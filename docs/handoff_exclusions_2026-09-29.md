# Handoff - the exclusions batch (cleanup role, 2026-09-29)

For a FRESH cleanup session. This batch has two parts: funeral services come off
every map, and the fringe-category rules. The owner approved the rules and the
wording on 2026-09-29. What is left is running them, writing the approved text
and landing the result. Read this file, `docs/handoff_2026-09-28.md` (the role),
and DECISIONS 2026-09-29 ("Funeral exclusions coded; fringe-category audit..."
and "Record the funeral exclusions...").

## Before starting

- Work in `.claude/worktrees/cleanup` on `worktree-cleanup`. Check with
  `git branch --show-current` and `git worktree list`. **The previous cleanup
  session must be CLOSED first.**
- `get_usage`. The weekly limit was past 64% on 2026-09-29, which is why this
  batch moved to a fresh session.
- This worktree's `data/` is now a JUNCTION to the main checkout's shared
  `data/`. Before 2026-09-29 it was a real, stale folder; that folder is kept as
  `data.stale-2026-09-29/`, excluded from git in `.git/info/exclude`. It holds 7
  older `stations.csv` and line files for Madrid, Rome, Montréal, Paris and San
  Francisco, whose shared copies are newer. Delete it only on the owner's word.

## State of the branch

- The taxonomy code for the whole batch is COMMITTED on `worktree-cleanup`, in
  the commit that added this file, and **NOT pushed**. Pushing it before the
  outputs are re-rendered would put code on master that no committed map
  matches, which is drift for every other session. **Do not push
  `worktree-cleanup` until the re-rendered outputs are committed with it, at
  review time.** A docs-only fix meant for master in the meantime goes on a
  separate branch from `origin/master`.
- **Files, 26 plus a new one** (`git show --stat` on that commit):
  - `pipeline/taxonomies/`: `naics.py`, the new `naics_montreal.py` (Montréal
    keeps its caterers, 722320), `scian.py`, `france_naf.py` (funeral only;
    division 45 stays out, with the owner's reason in a comment),
    `norway_sn2025.py`, `denmark_db25.py`, `czech_nace2025.py`, `ihk_wz2025.py`,
    `madrid_epigrafe.py`, `brazil_cnefe.py`, `vancouver.py`,
    `edmonton_licencecategory.py`, `miami_catgryname.py`,
    `dc_businessactivity.py`, `dublin_uses.py`, `ba_usos_suelo.py`,
    `japan_eigyo.py`, `calgary_licencetype.py`, `phl_licensetype.py`,
    `chicago_license.py`, `toronto_mlscategory.py`, and `__init__.py` (it
    registers `naics_montreal`).
  - `pipeline/countries/taiwan.py`.
  - City files: `pipeline/montreal/config.py`,
    `pipeline/san_diego/config.py` and `step2_clean_businesses.py`
    (`NAICS_EXCLUDE_CODES` 8129, 72234, 81295, 812959), and
    `pipeline/prague/config.py`.
  - Import-time asserts guard every near miss. For example, SCIAN's 8122 is
    LAUNDRIES, so Mexico excludes funeral services as 8123, and San Diego's
    81291 and 81292 stay.
- `check_all.py` passed 24/24 on the working tree with this code.

## The run: 41 cities, step 2 then step 3, ONE AT A TIME

The cities: Los Angeles, San Diego, San Francisco, Montréal, Mexico City,
Guadalajara, Monterrey, Paris, Marseille, Toulouse, Lille, Rennes, Oslo,
Copenhagen, Prague, Berlin, Madrid, Taichung, Taipei, Taoyuan, Tokyo, Fukuoka,
Vancouver, Edmonton, Miami, Washington D.C., Dublin, Buenos Aires, Calgary,
Chicago, Philadelphia, Toronto, and the nine Brazilian cities (São Paulo, Rio
de Janeiro, Belo Horizonte, Brasília, Salvador, Fortaleza, Porto Alegre,
Recife, Santos). The Brazilian cities change for funeral services only.
Barcelona does NOT change; its vets are disclosed only. Kobe, Osaka, Sapporo
and Kyoto use the changed Japanese module but lose 0 rows: run
`drift_check.py` on them to prove it.

For each city:
1. **Announce the heavy job** to every live session (`ListAgents`), and
   announce its end. One heavy job on the machine at a time. Group a few small
   cities under one announcement if that suits.
2. **Back up master's shared processed files first:** copy
   `data/<slug>/processed/` to the scratchpad (`master_processed/<slug>/`).
   Step 2 rewrites the SHARED data, and other sessions'
   `check_macro_facts.py` reads it. On 2026-09-28 cleanup broke every other
   session's pre-push hook this way (London) and had to restore master's
   file.
3. Run `python pipeline/<slug>/step2_clean_businesses.py`, then its step 3
   (the map). **Toronto** has a geocode step before its map: its nightclubs
   (about 32 new pins) need geocoding, which may fetch. A step may fetch when a
   person runs it.
4. Copy the NEW processed files to the scratchpad
   (`new_processed/<slug>/`), then **restore master's** from
   `master_processed/<slug>/`. The shared data is back to master's state.
5. Record the counts the step printed. Commit that city's `outputs/<slug>/`
   (after each green step; stage by name; `git checkout -- outputs/` for any
   other city's churn). Then run `python scripts/check_personal_exposure.py
   <slug>`; the rule is to run it after any change to a city's step 2 or
   taxonomy.

After all 41: `python scripts/check_ring_shares.py --write` (it reads the
committed maps, so the shared data does not matter). Then run
`check_macro_labels.py`. Last, `check_all.py`.

`app/macro_facts.json` needs the new storefront counts, but
**`check_macro_facts.py --write` DROPS every city whose processed data is
absent or stale in the data it reads.** Do it only at landing:
1. Copy every `new_processed/<slug>/` into the shared `data/`.
2. Run `check_macro_facts.py --write` in this worktree, whose `data/` is the
   shared folder.
3. Commit, fetch, merge, and push in the same breath (CLAUDE.md
   `[#fetch-before-push]`).

## Expected counts (measured read-only; the re-run may shift them a little)

Storefronts before → after, funeral plus all rules:

| City | Before → after | City | Before → after |
|---|---|---|---|
| Los Angeles | 58,173 → 57,525 | Taipei | 133,335 → 128,949 |
| San Diego | 10,955 → 9,124 | Taichung | 66,115 → 63,731 |
| San Francisco | 17,837 → 16,495 | Taoyuan | 45,014 → 43,603 |
| Montréal | 17,231 → 17,162 | Tokyo | 63,989 → 61,370 |
| Mexico City | 283,345 → 279,804 | Fukuoka | 30,062 → 29,920 |
| Guadalajara | 117,454 → 116,657 | Dublin | 13,123 → 12,904 |
| Monterrey | 58,564 → 58,049 | Miami | 29,878 → 29,540 (may shift) |
| Madrid | 53,355 → 52,035 | Philadelphia | 8,504 → 8,301 (may shift) |
| Vancouver | 11,724 → 11,517 | Calgary | 15,099 → 15,072 (may shift) |
| Chicago | 20,686 → 20,552 (may shift) | Buenos Aires | 63,596 → 63,443 |
| Prague | 25,275 → 25,206 | Toronto | 18,186 → about 18,218 (after geocoding) |
| Edmonton | 10,721 → 10,702 | | |

**Funeral only:**
- Paris 87,164 → 86,903; Marseille 18,177 → 18,029; Toulouse 8,635 → 8,596;
  Lille 11,833 → 11,739; Rennes 3,479 → 3,448.
- Oslo 10,718 → 10,678; Copenhagen 14,978 → 14,922; Berlin 60,313 → 60,269;
  Washington D.C. 5,230 → 5,201.
- Brazil, removed: São Paulo 25, Rio 74, Belo Horizonte 48, Brasília 52,
  Fortaleza 84, Porto Alegre 83, Recife 77, Salvador 106, Santos 1 (550 in
  all).

Calgary, Philadelphia, Miami and Chicago collapse several licences into one
premises, so a removed pin can come back under another licence.

**If a re-run count differs from the approved wording below, use the re-run
count.** The owner approved the wording knowing counts might shift. A
difference of more than a few percent goes back to the owner.

## The APPROVED wording (owner, 2026-09-29): write it as given

### (i) `docs/excluded_categories.md`: a new paragraph right after "## Which businesses are counted"

> **Five kinds of business are left off every map, wherever a register names them.** Funeral homes, crematoria and cemeteries, which are not places a passer-by walks into. Food with no counter of its own: canteens inside schools, offices, hospitals and care homes, event caterers, food trucks, and street and market stalls. The "other personal services" catch-all that registers keep for whatever fits nowhere else, which mostly holds people working from home or at the customer's door, fortune-tellers and dating agencies among them. Adult and hostess venues, left off for the sake of the people who work there; sex shops are shops and stay. And gambling: betting shops, casinos, arcades and lottery agencies. Where a register files one of these under the same label as ordinary businesses, it cannot be separated and stays on the map; each city's section says where. Newsstands and kiosks, pawnbrokers, karaoke bars and nightclubs are kept, and car dealers count as shops everywhere except France.

### (ii) `docs/excluded_categories.md`, per city (quoted text is the text being replaced)

**Los Angeles.** Add: "Also left out: funeral services (93) and food with no counter of its own — mobile food (348), caterers (147) and food-service contractors (60). **Kept because it cannot be split:** `722300` "special food services" (3,013 pins), which this registry uses for caterers, concession stands and food trucks alike, but also for taquerias and cafés; all of it counts as food service." After the heading of the "other personal services" catch-all section, add: "Since 2026-09-29 this catch-all is left out in every city."

**San Diego** (a new section, "San Diego - its own codes for massage parlours, cottage kitchens and kiosks"): "San Diego's registry extends NAICS with codes of its own, and four are left out: `812193` massage parlours (144; massage therapy, `812198`, stays), `72234` cottage-food operators (192, a licensed home kitchen), `81295`/`812959` kiosk businesses (26, ecoATM phone-recycling machines), and `8129` "other personal services" filed at group level (569; calibration labs, waste haulers, remodellers). With the `81299` catch-all (585), caterers, mobile food and food contractors (296) and funeral services (19), 1,831 pins leave the map. Pet care and photofinishing stay."
In "Kept, and why", replace "**San Diego's personal services.** San Diego shows no comparable exposure: its registry always carries a trade name, so no registrant name was ever substituted. Its residual is small and it was left in." with "**San Diego's personal services, apart from its catch-alls.** Its registry always carries a trade name, so no registrant name was ever substituted. The two catch-all codes were left in on that ground until 2026-09-29, when the catch-all left every map."

**San Francisco.** Add: "Also left out: funeral services (21); food with no counter of its own (1,300) — food-service contractors (537), caterers (417) and mobile food (325); and the remaining catch-all rows filed as `81299` (21). The contractor code goes whole, although the city's own licences show it also holds 139 stadium and convention-centre concession stands, 21 bars on San Francisco Bay ferries and a few restaurants."

**Montréal.** Add: "**Caterers are kept here (107), unlike in every other NAICS city.** The survey records premises a surveyor walked past, and they are traiteur shops with a counter, as in France. Left out, as everywhere: funeral services (39) and the "other personal services" catch-all (30)."

**Chicago.** Add: "Licences whose only listed activity is "Miscellaneous Personal Services", the city's catch-all, are left out (134); a licence that also names a specific service is counted by that service." Also add the funeral DISCLOSURE (owner, 2026-09-28): Chicago has no funeral licence type; about 63 pins carry funeral words in their names (26 of them sell funeral items), and they stay because nothing in the register separates them.

**Philadelphia.** Add to "Also left out": "event caterers (`Food Caterer`, 193) and curb markets (10). Newsstands are kept, as small walk-in shops."

**Miami.** Add to the mobile paragraph: "`CATERING BUSINESS` (276) and `FUNERAL HOME` (62) are out too. `NIGHT CLUB` and `DANCING OR ENTERTAINMENT` are kept as food service."

**Washington D.C.** Add: "`Funeral Establishment` (29) is excluded, as funeral services are everywhere."

**Vancouver and Surrey.** Replace "**A funeral parlour counts; a cemetery does not.** … on storefront grounds." with "**Neither a funeral parlour nor a cemetery counts.** Surrey's `Funeral Parlour` (4) and `Cemetery` (2) are left out: funeral services are off every map." Append to the mobile-trade paragraph: "Both registers' `Caterer` (148 and 49), Surrey's `Concession Stand` (5) and `Flea Market` (1) are out too. Surrey's one `Adult Entertainment Store` is a sex shop and stays."

**Calgary.** Add: "`MARKET` (27) is out: a market is where stalls stand, not a shop." Also add the funeral DISCLOSURE: about 12 pins with funeral words in their names sit under the general retail licence and stay.

**Edmonton.** Replace "…carnivals (2) and one after-hours dance club that holds no alcohol category." with "…and carnivals (2). `After Hours Dance Club` (1) counts as food service, as a nightclub does everywhere here; that premises was already a pin through its retail licence." Add: "`Funeral, Cremation, and Cemetery Service` (19 pins) is out."

**Toronto.** In "Also excluded", delete "`ENTERTAINMENT ESTABLISHMENT/NIGHTCLUB` 170 - merged and leading with entertainment, so the same treatment as Edmonton's after-hours dance club -". Add: "**Nightclubs count as food service** — 36 active premises, about 32 new pins once geocoded — as in every other city. Adult entertainment clubs stay out."

**Mexico City.** Add: "Also excluded: public toilets and shoe-shine stands (`812130`, 1,646), the "other personal services" catch-all (`812990`, 977), funeral services (629), event caterers (146), institutional canteens (82) and food trucks (61)." **Guadalajara:** the same sentence with 227 / 238 / 207 / 77 / 34 / 14. **Monterrey:** 72 / 125 / 156 / 78 / 51 / 33.

**Madrid.** Add: "So are canteens in schools, care homes, social centres, offices, sports grounds and hospitals (1,157), banquet halls and event caterers (90), the register's "other personal services (astrology, contact agencies)" catch-all (43) and funeral parlours (30)."

**Barcelona.** Add: "**Kept, although part of it is clinics:** `Veterinaris / Mascotes` (395) puts vets under one value with pet shops and groomers; about 160 read as veterinary clinics by name, and the census cannot separate them."

**Dublin.** Add: "**Betting shops are left out (175)**, with a casino and an amusement centre that had reached the map through a "shop" use beside them. So are markets (4) and funeral homes (38). Kiosks stay: a kiosk is a small walk-in shop."

**Paris.** Add: "**Funeral services (`96.03Z`) are excluded** — 261 here." And: "**Car dealers are not on the French maps, unlike every other city here.** SIRENE files vehicle sales in their own division, not with retail. Four selling codes would add about 9,500 pins across the five cities (5,384 in Paris), but 95% record no employees and about a quarter carry a premises name: mostly one-person traders, probably registered at home. Left off on that ground (owner, 2026-09-29)."
**Marseille, Toulouse, Lille, Rennes.** Replace "the four no-premises trades, the wholesale laundry, and the same two catch-alls" with "the four no-premises trades, the wholesale laundry, funeral services, and the same two catch-alls" (funeral counts 148 / 39 / 94 / 31).

**Oslo, Copenhagen, Berlin.** Add "Funeral services are excluded too, as everywhere: 40 / 56 / 44 premises."

**Prague.** Replace "**No catch-all is excluded.** The "other personal services" category that other cities leave out holds three rows here; the 2025 classification already sorts that work into specific classes." with "**The "other personal services" catch-all is excluded, as in every city — three rows here**; the 2025 classification already sorts that work into specific classes." Add "funeral services (66)".

**Milan.** Add the funeral DISCLOSURE: Milan's registers carry no funeral code; about 29 funeral services reach the non-food shop layer through the shop register, and they stay.

**Amsterdam, Rotterdam, Riga.** Add the funeral DISCLOSURE: the building register records only a shop unit, so a funeral home there cannot be identified or removed.

**Buenos Aires.** Add to "Excluded by use": "funeral homes and wake parlours (143); fortune-tellers and astrologers (10)".

**São Paulo** (and "as in São Paulo" for the other eight Brazilian cities): "**Funeral homes, wakes, crematoria and cemeteries are excluded** (550 across the nine cities)." And: "**Not excluded, because the census cannot say it:** food trucks, trailers, kiosks and stalls. About 325 descriptions across the nine cities mention a trailer or food truck, and about 1,400 start with quiosque, barraca or banca, but a beach kiosk is a fixed premises and a trailer may stand in one spot for years. They count as whatever the rest of the description names."

**Taichung.** Replace "**Left out** - online shopping (industry code 487); every industry…" with "**Left out** - online shopping (industry code 487); funeral services (443); street and market stalls (1,101) and caterers, banquet cooks and school-lunch contractors (266); the "other personal services" catch-all, fortune-telling and marriage introduction (574); every industry…". **Taoyuan:** 288 / 553 / 182 / 388. **Taipei:** 634 / 2,669 / 272 / 811. All three: add "Drinking places and restaurants with shows are kept: their register names claim no hostess service."

**Tokyo.** Add to "Left out": "- 2,536 bars and snack bars filed under the permit sub-types バー・キャバレー (bars and cabarets, one sub-type) and スナック (hostess-staffed snack bars)" and "- 83 caterers (仕出し)". After the list: "**Kept, though possibly the same sub-type:** Meguro abbreviates its bar permits as 飲食バー (102), without the cabaret or snack detail."

**Fukuoka.** Add to "Left out": "- 103 snack bars (スナック). - 39 caterers (仕出し)."

**London, Glasgow, Newcastle:** "**Not measured: canteens.**" already stands. No change.

### (iii) City-page sentences (`app/pages/*_Heatmap.py`), published wording, approved

- **London, Glasgow, Newcastle:** "Caterers working from home, mobile traders, and kitchens in schools, hospitals and workplaces are left out." → "Caterers working from home, mobile traders, and kitchens in schools, hospitals and care homes are left out; a workplace canteen registered as a restaurant or café cannot be told apart and may appear."
- **Taichung, Taoyuan, Taipei:** "Shops, food service and personal services are read from the code; online sellers are left out." → "…; online sellers, street and market stalls, caterers, funeral services and the "other personal services" catch-all are left out."
- **Tokyo:** "Food trucks, stalls and temporary permits are left out." → "Food trucks, stalls, temporary permits and caterers are left out, and so are the bar permit types that take in cabarets and hostess-staffed snack bars; Meguro's bars, listed without that detail, are kept."
- **Fukuoka:** "Food trucks, festival stalls, school and hospital kitchens and staff canteens are not." → "Food trucks, festival stalls, caterers, school and hospital kitchens, staff canteens and snack bars are not."
- **Paris:** "…contract catering for institutions, and the two "other services" catch-alls…" → "…contract catering for institutions, funeral services, and the two…". Add: "Car dealers are not counted here, unlike on other cities' maps: most are one-person traders registered at home."
- **Madrid:** add to "So are wholesale, vehicle repair…": "canteens in schools, care homes and offices, event caterers, funeral parlours".
- A page sentence that states a storefront count or a ring share: re-check it after the re-run (`check_ring_shares.py`; Washington D.C.'s "roughly 5,200" still holds at 5,201).

## Also to update

- `docs/map_inconsistencies.md`:
  - Theme 11 (category edges: funeral, caterers, catch-all, adult and hostess
    venues, gambling, nightclubs, the France car-dealer reason) and theme 2
    where categories change.
  - The table B in-ring counts, from each re-rendered map's layer menu.
  - The car-dealer list in theme 11, which was already out of date: Prague,
    the Canadian cities, D.C., Dublin, Taiwan, Brazil, Sydney and Melbourne
    also keep dealers.
- `DECISIONS.md`: one entry for the run (counts before and after per city,
  drift results, the personal-exposure verdicts), then `decisions_index.py`.
- `PLAN.md`: tick the exclusions batch at landing. The next item is the
  cross-city audits 1-3 (owner, 2026-09-29).

## Landing (review time; only the owner calls it)

- The data-bound gate steps run here, because this worktree now sees the
  shared data: drift checks, the personal-exposure verdicts, and
  `check_all.py`.
- A FULL `deploy-verify` (`scope: full`), because about 41 maps change.
- Then swap the new processed files into the shared data,
  `check_macro_facts.py --write`, commit, fetch, merge, push, and the owner
  reboots. Check the live site, including one city that did not change.
- Stockholm (branch `stockholm`, frozen at `9d58123`) may be landing in the
  same batch: see `docs/handoff_2026-09-28.md`.

## State after the run (2026-09-29, second cleanup session)

- **Done and committed on `worktree-cleanup`, not pushed:** all 41 maps,
  baselines, `app/ring_shares.json`, the Brazil funilaria fix, the approved
  wording (with the owner's re-run substitutions: Los Angeles 3,145; Chicago
  133 and a rewritten funeral disclosure; Brazil 558 and about 320),
  `docs/map_inconsistencies.md`, the info pages renumbered to 200-202, and
  DECISIONS. `check_all.py` 24/24. Counts and verdicts are in DECISIONS
  2026-09-29 "Exclusions batch re-run".
- **The new processed files are in that session's scratchpad**,
  `new_processed/<slug>/` (41 cities; the Brazilian ones are the final
  re-run), under
  `C:/Users/dacek/AppData/Local/Temp/claude/C--Users-dacek-Documents-Portfolio-expanded-heatmap--claude-worktrees-cleanup/b47d2f67-189e-4346-a6f0-718eed9272c2/scratchpad/`.
  Master's copies are beside them in `master_processed/` (Brazil:
  `master_processed_run2/`). If that folder is gone, the landing re-runs
  step 2 onward for the 41 cities instead; the committed maps say what the
  result must be.
- **Waiting for the owner:** the "Why the maps differ" page
  (`app/pages/202_Why_the_Maps_Differ.py`) still says "Street stalls are
  left out in Mexico." A replacement is drafted in chat.
- **Not traced, internal only:** a few in-ring Retail counts rose (Chicago
  +15, Madrid +8, D.C. +2, Miami +1), consistent with multi-use premises
  re-bucketing when one of their uses is excluded; Madrid's multi-bucket
  premises fell 1,535 -> 1,488.
- **The landing branch is `review-2026-09-29`** (local, in the cleanup
  worktree; owner pre-approved every change at review time). It is
  `worktree-cleanup` + origin/master + `stockholm` + `bucharest`, with
  Bucharest's three merge fixes done (DSVSA București's notice renumbered 67, `REGION_ZOOM_WITHOUT` with
  Riga, Stockholm and Bucharest, master-list counts 64 built / B 2 / 78
  candidates / 23 countries), ring shares for 64 cities, and a Stockholm
  disclosure (its restaurant type also holds about 39 caterers and 15 mobile
  units). `check_macro_labels.py` PROBLEMS 0, `check_all.py` 24/24.
- **Review time** (owner: once the two Korean cities are in): merge them and
  origin/master into `review-2026-09-29`, then the full `deploy-verify`, the
  processed-data swap, `check_macro_facts.py --write`, tick PLAN's
  exclusions item, fetch, merge, push.
- **Push only when a reboot can follow.** The info pages moved from 90-92 to
  200-202; until the app reboots, the cached `components.py` still links to
  `pages/90_...`, which no longer exists, so every info-page link would break
  on the live site. If the owner cannot reboot, hold the push.
- **Later the same day:** Incheon and the Gyeonggi satellites (Goyang,
  Seongnam, Yongin) merged too (the Small Enterprise and Market Service's notice 68, the Seoul Capital Area
  region, 68 built / B 1 / 77 candidates); `app/macro_facts.json` written with
  the new processed files swapped in and master's restored; PLAN ticked; the
  full `deploy-verify` PASSED on c50615b (68 maps at five sizes, the app, the
  renumbered info pages, notices; three pre-existing label overlaps in
  Madrid, Oslo and Osaka, none from this batch). `check_macro_facts.py` fails
  on this branch until the swap is redone - expected.
- **The push, when the owner can reboot:**
  1. `python <scratchpad>/swap_processed.py in` (it refuses unless the shared
     data is still master's).
  2. `git fetch`, merge origin/master into `review-2026-09-29` if behind
     (`merge_append_only.py DECISIONS.md` for a conflict there).
  3. `check_all.py` (the pre-push hook runs it, `check_macro_facts.py`
     included) and `check_deploy_imports.py`.
  4. `git push origin review-2026-09-29:master`, gated on 0 behind.
  5. The owner reboots; check the live site, including an unchanged city.
  The shared data stays swapped in after the push: it is then master's.
- **For the owner, not decided:** Stockholm's caterers and mobile units could
  be excluded by name, as its institutional kitchens are; today's rule keeps
  them because the register's type cannot split them.
- **LANDED 2026-09-29** as 95e04c4 and live after the owner's reboot
  (DECISIONS "Review batch live after the owner's reboot"). The four city
  branches were deleted locally and on origin (owner, confirmed in the
  cleanup chat).

## Next review time

**When (owner, 2026-09-29):** after the last light-rail builds are on their
branches: Bergen, then Houston, Sacramento, Buffalo and Aarhus. That review is
a deliberate stopping point for builds; the owner's remaining edits before the
tram cities are mostly prose. If the light-rail builds slip past 2026-10-01,
run the review with what is ready. Every queued branch stays off master, is
pushed to its own origin branch as a backup, and sends the cleanup session a
READY notice (commit, counts it assumes, exposure verdict). The shared counts
(Built, Band A, notices, page numbers) are reconciled once, in the review
merge. Suggested order: stockholm-catering, category-continuity, suwon,
bucheon, bergen, then the four light-rail cities; one `deploy-verify` scope
`full`, one push, one reboot.

- **`stockholm-catering`** (origin, one commit on master; owner-approved):
  the name filter now also drops caterers and mobile units, 5,262 -> 5,218
  placed (85 unplaced). The committed map, macro_facts and ring_shares already
  carry 5,218, but the shared `data/stockholm/processed/` holds master's
  5,262. **Right after merging it, run
  `python pipeline/stockholm/step2_clean_businesses.py`**, or
  `check_macro_facts.py` (and so the pre-push hook) disagrees. It touches
  `app/cities.py` and the Stockholm page: reboot after the push. It edits
  `docs/excluded_categories.md` too; confirm the 2026-09-29 "Kept because the
  register cannot split it" Stockholm disclosure no longer claims the
  caterers are on the map.
- **`category-continuity`** (local branch in worktree
  `quizzical-lamarr-4c765b`, 60d23ff, waiting for the owner) adds
  `check_category_continuity.py` to `check_all.py`. Its table in
  `scripts/category_continuity_table.py` lists Stockholm's "Westers Catering"
  and "Tommys Farstaplan, Food truck" as `pending(...)`. **Whichever of the two
  branches lands second, turn those two into `loc(...)` in the
  sweden_livsmedel column in that merge**, or the check reports them stale
  and the pre-push hook fails. **Correction (category session, 2026-09-29):
  the edit is `pending(` -> `fixed(`, not `loc(`** (same arguments), on the
  Westers Catering and Tommys Farstaplan rows (~1549, ~1557); delete the
  `("sweden_livsmedel", "mobile_unit")` entry from QUEUED_ELSEWHERE (~1572) and
  reword its no_counter_food entry to the torghandel stall, a name rule now
  that stockholm-catering has landed. The torghandel stall row stays
  `pending`. Then `python scripts/check_category_continuity.py` and its
  `--selftest`: 2 queued plus Boston's pending row, OK.
- **category-continuity's new processed files** (40 cities, 8 identical to
  master) are in `data/_review_category-continuity_2026-09-29/new_processed/`,
  with master's copies in `master_processed/` beside them (585 MB, local
  only). Swap them in for `check_macro_facts.py --write`, swap master's back,
  and swap in again at the push. Branch at 41b44cf; exposure verdicts clean
  for all 32 moved cities (DECISIONS "Category fix batch re-run"). Its
  per-city `docs/excluded_categories.md` wording still needs the owner's
  approval.
- The Stockholm worktree was removed 2026-09-29 (owner); `stockholm-catering`
  is kept, locally and on origin.
- **`suwon`** (page 69; 33,433 storefronts, 14 stations) and **`bucheon`**
  (page 70; 22,512, 14 stations, Seohae drawn per the owner), both on origin,
  each cut from master and counting 69 built. **The second to land
  reconciles:** master list Built 70, South Korea 9, Seoul Capital Area (7);
  the Small Enterprise and Market Service's notice 68 names both cities; both
  cities' rows follow Yongin's in `docs/data_sources/south-korea.md`,
  `docs/map_inconsistencies.md` and `docs/excluded_categories.md`; `app/cities.py`,
  `macro_facts.json`, `ring_shares.json`, README, `check_macro_labels.py`
  TEXT_WIDTH and `check_personal_exposure.py` REGISTRIES take both. `bucheon`
  also moves Incheon's macro label below its dot. Re-run
  `check_macro_labels.py` with both merged.
- **The category-fix batch** (`category-continuity`, 17 taxonomies and their
  re-renders, owner-approved) bases its Stockholm fix on `stockholm-catering`:
  land it after, or in one merge.
