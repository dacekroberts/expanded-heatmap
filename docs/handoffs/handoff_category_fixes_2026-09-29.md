# Handoff: the category fix batch (owner-approved 2026-09-29)

For a fresh session. `scripts/check_category_continuity.py` found departures
from `docs/category_rules.md`. On 2026-09-29 the owner approved every
recommended fix, including "align" for repairs and "fix all" for the probable
bugs. The reasoning is in DECISIONS 2026-09-29, "Category check: the owner's
calls on the pending departures". This file is the work list. Read it together
with the check's table, `scripts/category_continuity_table.py`, and
`docs/handoff_exclusions_2026-09-29.md`, whose run procedure this batch
repeats.

## Before starting

- **Weekly usage was 81% on 2026-09-29**, with the reset on 2026-10-04. The
  owner decides whether this runs before or after the reset. Call
  `get_usage` first.
- **Base it on the branch that holds the check**: `category-continuity`,
  in worktree `quizzical-lamarr-4c765b`, or master once it has landed.
- **Taxonomy modules are shared code** (`docs/session_roles.md`). Claim the
  role that owns them for this batch, and announce it to every live session.

## How the check drives the work

Every item below is a `pending(...)` row in the table, printed as `QUEUED FIX`.
When a fix lands, its row becomes stale and the check **fails** until that row
is turned into a `loc(...)`. So each code change and its table edit go in the
same commit. Where a fix works through a config filter rather than
`classify()`, make the row an `outside(path, token, what)`. When the batch is
done, `python scripts/check_category_continuity.py` should show no `QUEUED FIX`
lines and exactly one `PENDING OWNER` line (Boston, below).

## The fixes, by taxonomy

Each item gives what to change, then the cities to re-render. Counts come from
the check's agents or the raw files; re-measure them after step 2.

1. **`naics.py`**: add `445132` (vending machine operators, NAICS 2022) and
   `457210` (fuel dealers, NAICS 2022) to `NAICS_EXCLUDE_PREFIXES`, each with
   a near-miss assert. Raw rows: Los Angeles 52 + 1, San Francisco 29 + 15.
   *Re-render: Los Angeles, San Francisco, San Diego, Montréal.*
2. **`scian.py`**: `522452` casas de empeño to Retail (381 in Mexico City).
   It needs an explicit carve-in, because 5224 is not a bucket prefix.
   *Re-render: Mexico City, Guadalajara, Monterrey.*
3. **`dc_businessactivity.py`**: `Pawnbroker` to Retail. *Re-render:
   Washington D.C.*
4. **`chicago_license.py`**: remove `CLOTHING ALTERATIONS` from the
   personal-service activities. Keep the module's asserts true. *Re-render:
   Chicago.*
5. **`dublin_uses.py`**:
   - Move `SHOE REPAIR / KEY CUT`, `ALTERATIONS` and `TAILORING` out of
     personal services. Rewrite the "TWO DELIBERATE DEPARTURES" comment to cite
     this decision.
   - Stop a generic `SHOP` / `STORE` segment from rescuing recreation uses,
     the way `_OVERRIDES_GENERIC` already stops it for betting and markets.
     This affects `GYMNASIUM / FITNESS CENTRE` and `SNOOKER HALL` (5 pins),
     and any other recreation use found.
   - Take `INTERNET CAFE` (27) out of food service, since a PC room counts as
     recreation.
   - `SERVICE STATION (NO SHOP)` stays out: it is a declared exception.
   - The funeral-home-beside-a-shop case stays Retail (owner, earlier).

   *Re-render: Dublin.*
6. **`ba_usos_suelo.py` and Buenos Aires step 2**:
   - Admit TIPO1 `ESTACION DE SERVICIO` (266 active) as Retail. Its TIPO2 is
     blank, so this needs a step-2 change beside the UNICOMERCIAL filter plus
     a classify mapping.
   - Move `COMPOSTURA DE CALZADO`, `ARREGLO DE ROPA` and `SASTRERIA` out of
     personal services.
   - `CERRAJERIA` (locksmith, key cutting) was not ruled on. It follows
     Dublin's "key cut", so bring it to the owner with that precedent.

   *Re-render: Buenos Aires.*
7. **`brazil_cnefe.py`**. Verify each with `classify_description()`, and on
   real CNEFE descriptions, not only the table's samples.
   - `CANTINA ESCOLAR` and `RESTAURANTE INDUSTRIAL` (canteens) out.
   - `BOATE` (nightclub) to Food service.
   - `ESTUDIO DE TATUAGEM`: give `ESTUDIO` the same tattoo lookahead that
     `STUDIO` has.
   - `LOJA VIRTUAL` (online shop) out.

   *Re-render: the nine Brazilian cities.*
8. **`japan_eigyo.py`**: add `露店` to the form rules' temporary words, about
   34 rows. `ろ店` (Fukuoka's yatai) must stay Food service; add an assert
   for it. *Re-render: Fukuoka and Tokyo, which hold MHLW-format rows. Run
   `drift_check.py` on Kobe, Osaka, Sapporo and Kyoto to prove they are
   unchanged.*
9. **`taiwan_fia.py` / `pipeline/countries/taiwan.py`**:
   - `649611` pawnbrokers to Retail.
   - `932918` nightclubs and `932917` dance halls without hostesses to Food
     service.
   - `969014` shoe-shine out.
   - `482912` bottled gas and `482911` kerosene out.

   *Re-render: Taichung, Taipei, Taoyuan.*
10. **`france_naf.py`**: `47.78B` heating-fuel dealers out. *Re-render:
    Paris, Marseille, Toulouse, Lille, Rennes.*
11. **Berlin**:
    - `477893` fuel dealers out, as an exact `ihk_branch_id` exclusion in
      `pipeline/berlin/config.py` beside `47122`. `classify()` reads only the
      4-digit class, and 4778 holds other retail. Its row becomes an
      `outside()`.
    - Leihhäuser `64922` in as Retail. This needs `classify()` to read
      `ihk_branch_id` for that one branch, or a step-2 carve-in.

    *Re-render: Berlin.*
12. **Prague** (`pipeline/countries/czechia_register.py`, line 153): make
    `CATCH_ALL_EXCLUDE` match by prefix, as Berlin does, so the 21 bare `969`
    rows go. Any other Czech city on the same module inherits the fix.
    *Re-render: Prague.*
13. **`madrid_epigrafe.py`**:
    - `DISCOTECAS Y SALAS DE BAILE` (233) to Food service.
    - Every `SITUADOS: ...` street pitch (about 163) out.
    - `ESTABLECIMIENTO DE RESTAURACION MOVIL` (18) and `VENDEDOR AMBULANTE
      DE ALIMENTOS PREPARADOS...` (3) out.

    *Re-render: Madrid.*
14. **`barcelona_activitat.py`**: `Arranjaments` (649) out. *Re-render:
    Barcelona.*
15. **Riga** (`pipeline/riga/config.py` name rules):
    - Keep fuel stations as shops.
    - Move `remont|darbnīc|apavu|atslēg` out of the kept personal-service
      class.
    - Drop stands (`stends`, `^lete`).
    - Market pavilions (`tirgus`, `paviljon`) and kiosks stay: they are
      declared exceptions.

    *Re-render: Riga.*
16. **`romania_dsvsa.py`**: add `rulota` and `unitate mobila` to
    `NOT_STOREFRONT_CATEGORY` (7 A19 rows). *Re-render: Bucharest.*
17. **Stockholm**: drop the `torghandel` market-square stall by name. Its
    caterer and food-truck rows are fixed by branch `stockholm-catering`,
    which is already owner-approved. Land that first, then add this.
    *Re-render: Stockholm.*

**Not in this batch.** Boston's General On Premise licences are a measurement
first: count the bars and clubs holding no ISD food permit, then bring that
number to the owner. That is the check's one `PENDING OWNER` row.

## The run

Follow `docs/handoff_exclusions_2026-09-29.md`, "The run":
- one city at a time, announced as a heavy job;
- master's processed data saved and restored around each city;
- step 2 then step 3, with the counts recorded;
- that city's `outputs/` committed;
- `check_personal_exposure.py <slug>` after each city.

Then `check_ring_shares.py --write`, `check_macro_labels.py` and
`check_all.py`. `app/macro_facts.json` is written only at landing, after the
processed-data swap, exactly as before. Landing is review time: a full
`deploy-verify`, a push, and a reboot by the owner.

## Wording the owner still has to approve

The per-city lines in `docs/excluded_categories.md` (what left and what
joined each map, with the re-run counts), and any city-page sentence that
names a category or a count. Draft them from the re-run counts and bring them
to the owner in one message, as the exclusions batch did.
