# Japan follow-ups

Detail moved verbatim from `PLAN.md` on 2026-10-08 (commit c75f4802); `PLAN.md` holds each item's one-line status and points here by heading.
This is open work, not a record: update an item here as it moves, and send a finished one to `docs/plan_done/`.

## From Analytics (2026-10-08)

  - From Analytics (2026-10-08, measured at 5507a4cb): `map_common._LETTER`
    has no full-width Latin, so a "?" between full-width letters still
    renders (Higashiyamato 6, Tachikawa 4, Ichinomiya 3; one Tachikawa Food
    service pin labelled "?"); Saitama's new-law food types show their layer
    code and padding ("01:飲食店営業 ") as the pin category, withheld names
    too, in Ageo (Regional), Kasukabe, Sōka and Tokorozawa (`japan_eigyo`
    has no `display_value()`); Ōita's "? そうざい製造業" category (a lost
    circled numeral?); Ōita's page does not say publisher-masked names (306
    before set-asides) show the permit type.

## Kept from the drafts' notes at the 2026-10-08 fold

  - Kept from the drafts' notes at the 2026-10-08 fold (the files are in
    `git show d121b2cc:docs/decisions_drafts/<name>.md`):
    - **Owner, review time: re-render the 34 built Japanese cities on
      `WAVE5_RULES`** (with `default_joined`), Toyota first (+177
      storefronts, the rest about 20 or fewer), each with a pinned
      `TERM_AS_OF`; call 158's reading goes to the owner with it
      (japan-foundation, "Review-time re-render proposal").
    - Japanese shared-code fixes (worktree-japan-regional-1, "Shared-code
      findings"): line labels anchored on in-city segments in `map_common`
      (retire Gifu's, Mito's and Morioka's `in_city_first` copies; Akita's
      Oga label), `wareki_date` YYYYMMDD, `rebuilt_register`'s ranking and
      種目 folding (re-measure Higashiōsaka), `city_rows` by magic bytes,
      the `oaza_cut` 大字 fallback, `SOURCE_LINKS` link text, Akita's yatai
      form, two `japan-city` skill lines, the `CLOSED_STATIONS` docstring.
    - Confirm five Japanese credits against their licence reads: notices
      157, 161, 178, 184, 186.
    - Correct three Kansai-1 briefs: Kakogawa (3 一円 vehicle rows name
      加古川市), Uji (the guard tests 宇治市), Toyonaka (files from June 2026
      drop 廃業年月日).

## The name-rule bullet's sign rule

- [ ] **Review time: the Japanese pages' name-rule bullet gains the sign rule**
  (owner, 2026-10-06; DECISIONS, "the name rule's version 2"). Proposal, every
  Japanese page's variant alike: "Where a business's trade name is its
  operator's own name, or is written as a bare personal name, the dot shows its
  permit type instead." The rule itself landed 2026-10-06.

## Japanese cities onto N02-25

  - [ ] **Japanese cities onto N02-25 (Band B session, 2026-09-30)**, one
    drift check per city. Hiroshima reads the 2025 edition because N02-24
    still draws Hiroden to the closed 猿猴橋町 stop; the six earlier cities
    stay on N02-24 (stations identical). `japan.n02(slug)` and
    `N02_EDITIONS` make it a per-city switch.

## Unticked publish steps

- [ ] **Unticked publish steps** (the pages exist on master; confirm and
  tick): Osaka's reboot and live check (pushed 2026-09-28); from the
  2026-09-28 builds, `publish-city` with deploy-verify `city-added` and a
  reboot for Buenos Aires (page 58, notice 60 (Buenos Aires), Fortaleza's
  and Porto Alegre's labels moved), Sapporo (notice 53 (Sapporo), Osaka's
  label right), Fukuoka (notice 54 (Fukuoka), Busan's label lower left) and
  Kyoto (notice 55 (Kyoto), its label far above its dot).

## Kyoto's August 2026 list

- [ ] **Kyoto:** when the city publishes its August 2026 list, add it to
  `config.PORTAL_RESOURCES`, move `AS_OF` to 2026-08-31, re-run (a rebuilt
  register goes stale a month a month).

## Osaka's Umekita stretch

- [ ] **Osaka's Umekita → 福島 stretch** (lines served only by limited
  expresses count, owner 2026-09-28): no station, so only the line changes;
  a re-render for review time.

## Kyoto before publishing

- [ ] **Kyoto:** pin `as_of` to the fetch date; before publishing, measure
  same-address successors and the factory share of 菓子 and そうざい (brief,
  "Still unknown").

## Tokyo: the missing wards

- [ ] **Tokyo: the missing wards** (built 2026-09-28 with 8 of 23). Chiyoda
  lifts urban station coverage from 45% to 56%; with Toshima and Bunkyō 67%;
  all 23 wards 98% (`tokyo.md`). Routes: Chiyoda's ledger (owner, gated item
  22); extract Ōta's, Kita's and Arakawa's PDF lists; Shinagawa's and
  Itabashi's partial files; requests to Toshima, Nerima and Edogawa.
  - [ ] ⏸ **PARKED, the last resort (owner, 2026-09-24): four requests**
    (`docs/gated_access.md` items 29–32), not sent and not the next step.
