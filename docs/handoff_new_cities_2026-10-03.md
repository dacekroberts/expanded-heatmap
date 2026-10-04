# Handoff: Mendoza, Tacoma and Liverpool (Regional) (2026-10-03)

For the build session that builds the three non-Korean, non-Belgian cities
the coverage sweep found. Written by staging; the owner set three build
sessions on 2026-10-03 ("one korean, one belgium, one for the other cities").

**NOT YET RELEASED.** The owner releases this kit to ONE build session,
which works in its own worktree (suggested: `.claude/worktrees/new-cities`
on branch `new-cities-build`, cut from origin/master; `data/` and
`.venv-lean` are junctions to the main checkout's). The branch has no
upstream, so a plain `git push` can never reach master. Everything lands at
the owner's review time.

**Two other build sessions may run beside this one:** Korea
(`docs/handoff_korea_sweep_2026-10-03.md`) and Belgium (its kit follows the
KBO measurement). All three edit `app/cities.py`, `docs/data_sources.md` and
`docs/excluded_categories.md` in their own sections.

**Delete this file** once all three cities have landed.

---

## The three

| City | Page | Business leg | Rail | Brief |
|---|---|---|---|---|
| **Mendoza** 🇦🇷 | 193 | The capital's "Listado Comercios por Actividad 2025": **8,309 businesses**, all active June 2025, **100% placed** from `comercios_limpio.json` (cached, `data/mendoza/raw/`, Gauss-Krüger zone 2). CC BY 4.0 | LIGHT RAIL: the Metrotranvía, **drawn to its end** (owner), **7 of 25 stations** counted in the capital | `docs/build_briefs/mendoza.md` |
| **Tacoma** 🇺🇸 | 194 | The City's business licences: **11,812 in the city** (Council_District 1-5), NAICS, daily; the point layer is item `2fa3b14b4de44c16b44893fee2cadefd` (EPSG:2927, lower-case fields), not the table. Permitted with conditions | TRAM: the T Line, **12 stops**, every 12 minutes; median spacing 452 m, halved rings | `docs/build_briefs/tacoma.md` |
| **Liverpool (Regional)** 🇬🇧 | 195 | Food only: the FSA register for Liverpool, Sefton, Knowsley and Wirral, **about 7,400 storefronts**, OGL v3, the UK six's shared steps | Merseyrail, **59 stations**, a **commuter-rail exception** (owner): every branch every 15 minutes by day; the City Line named, not drawn | `docs/build_briefs/liverpool.md` |

**Owner calls already made (2026-10-03):** all three banded (Mendoza and
Tacoma A, Liverpool (Regional) B); Mendoza the capital alone, its line drawn
to its end; Tacoma's licence accepted on Chicago's template; Merseyrail as a
commuter-rail exception on the "by day" reading.

**Settled by the owner later the same evening ("1. metro 2. reword"):**
1. Liverpool (Regional)'s map mode is `metro`.
2. The Department for Transport, NaPTAN notice 86 is reworded to cover
   Merseyrail; no new notice. Its current text reads "the UK's tram and
   light-rail maps". **The owner approved the new first sentence
   (2026-10-03):** "Stop and station counts on the UK's tram, light-rail and
   Merseyrail maps are checked against NaPTAN, the National Public Transport
   Access Nodes dataset published by the Department for Transport." The
   licence sentence and the no-endorsement sentence stay. Write it in
   `app/components.py` and `docs/data_sources.md` together.

## Per-city traps the briefs record

- **Mendoza:** the JSON carries only `desc_full` (418 distinct types), not
  the CSV's `desc_breve`: the taxonomy is written on `desc_full` and the
  bucket counts re-measured (`premises-taxonomy` skill). A business has up
  to 30 activity rows: one bucket per business, by a measured rule.
  `nombre_fantasia` holds some sole traders' own names, surname first:
  Vancouver's name rule (2026-09-21) and `check_personal_exposure.py`. The
  notice needs a modification statement and no endorsement. The boundary
  source is open (the portal's `seccionales-ciudaddemendoza` is a candidate,
  its licence unread: a new source goes to the owner).
- **Tacoma:** the City's 115-word disclaimer is shown site-wide, like
  Chicago's and Kansas City's (`render_site_notices()`), verbatim as the
  brief quotes it; the City may require any use to end, which the removal
  rule honours. Cite data.tacoma.gov, never the dead data.cityoftacoma.org.
  The pins are "active business license accounts", never "currently
  licensed". 712 trade names equal the entity name; mailing fields never
  place or label a pin. Rail from OSM (the owner ruled out Sound Transit's
  GTFS for Seattle); gate 3 against the operator's own stop count.
- **Liverpool:** `pipeline/countries/uk.py`'s NaPTAN gate matches tram stops
  only (type MET, area 940); Merseyrail's stations are rail stops (RLY,
  910). Make the stop type configurable once and **prove zero drift on the
  six built UK cities** before scaffolding. The FSA authority API returns
  404 without its version header; the build keys on the file codes (FHRS414,
  424, 412, 435), which the brief checks. Station spacing is measured at
  build.

## How this session runs: one lead, agents for self-contained legs

**Phase 0, setup.** Confirm the worktree and branch, `git fetch`, merge
`origin/master`, register the session in `docs/session_roles.md`'s table,
and run `python scripts/brief_check.py mendoza tacoma liverpool` (16
checks, no Overpass).

**Phase 1, shared code first:** the `uk.py` stop-type change and its
zero-drift proof on the UK six.

**Phase 2, the cities:** Liverpool (Regional) (closest to built code), then
Tacoma (NAICS and a Kansas City-shaped page), then Mendoza (a new taxonomy).
An agent may take a self-contained leg (Mendoza's taxonomy measurement,
Tacoma's privacy pass); it returns files and counts and never commits,
queries Overpass or edits a shared file.

## Visuals and analytics: what a build owes them

1. **Native-language names stay in config** where the country uses a field
   for them.
2. **Ring shares and bucket counts come from the gates**: record gate 9's
   ring shares (`scripts/check_ring_shares.py --write`).
3. **Every notice is registered where the page lists it** (`city_notices()`
   in `app/components.py`).
4. **Record each notice's card face or caption, and any open terms question,
   in the drafts file** (`docs/session_roles.md`, "Downstream sessions").
   Tacoma's disclaimer is long and site-wide: say whether a card can carry
   it or only a caption pointing to it.

**No analysis on any page.**

## Numbers

- **Pages: 193 (Mendoza), 194 (Tacoma), 195 (Liverpool (Regional))**,
  claimed in `docs/session_roles.md`'s numbers sentence.
- **Notices: 141 (Mendoza), 142 (Tacoma), 143 (Liverpool's FSA notice,
  Manchester's 84 with the city and date changed)**, claimed there too.
  The Department for Transport, NaPTAN notice 86's wording is the owner's call above.

## Gate order (Band A's and B's, per city)

1. personal exposure and a row in `docs/privacy_verdicts.md`;
2. provenance;
3. scope disclosure, written to `docs/city_page_format.md`;
4. the inconsistency rows and `cities.py` fields;
5. the master list (each city leaves its band for Built);
6. macro facts and the macro label;
7. the decisions entry;
8. commit;
9. the drift check, its baseline and ring shares;
10. merge master, `check_all.py`, and push at 0 behind (to the build branch).

## Session rules

- Decisions go to `docs/decisions_drafts/new-cities.md`.
- Overpass: one query in flight per session, one per city; wait 60 s after a
  504 or 429. Only the lead queries.
- Memory: every heavy job through `scripts/heavy_job.py run` with a real
  label and `--session new-cities`; the owner gives Cleanup and the map-dot
  session priority.
- `data/` is one shared junction. Never re-run another city's step from this
  branch; the UK six's zero-drift proof is the drift check, as the
  extensions proved their cities off (2026-10-03).
- Personal data: select columns before printing anything; never print,
  store or quote a person's name, ID, phone or address.
- No backslash or backtick in a Bash command; write a script file.
- Downloads named in a brief or skill are pre-permitted; anything else goes
  to the owner.
- One browser-using agent at a time: the built-in browser pane is shared.
- A failing brief claim goes to the staging session.
