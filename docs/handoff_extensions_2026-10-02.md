# Handoff: four extensions to built cities (2026-10-02)

For the build session that extends four built cities with the municipalities
around them. Written by staging; the owner asked for the extensions to be
probed "first then we can push these all at once", then for their kit,
worktree and prompt (2026-10-02), in a worktree separate from Japan wave 2.

**✅ RELEASED by the owner, 2026-10-02**, to ONE build session. It works in
`.claude/worktrees/extensions` on branch `extensions-build`. There, `data/`
and `.venv-lean` are junctions to the main checkout's. The branch has no
upstream, so a plain `git push` can never reach master.

**These change LIVE pages.** Each extension re-renders a built city, so the
drift baseline moves on purpose and everything lands at review time. The
Japan wave 2 session runs beside this one and touches no code these do.

**Delete this file** once all four have landed.

---

## The four

| Built city | Becomes | Adds | Sources and state | Read first |
|---|---|---|---|---|
| **Rio de Janeiro** | Rio de Janeiro (Regional) | **Duque de Caxias**: SuperVia Saracuruna's three excluded stations, Duque de Caxias, Corte Oito and Gramacho | CNEFE, 18,698 storefronts, zip cached in `data/duque_de_caxias/raw/`. The rail test (2026-09-30) passes up to Gramacho. Beyond it (Campos Elíseos, Jardim Primavera, Saracuruna) it fails: the line is drawn to its end and those three are left unringed. | PLAN.md "Regional add-ons to built cities" and "Wave-2 follow-ups" (5); the `brazil-city` skill |
| **Belo Horizonte** | Belo Horizonte (Regional) | **Contagem**: Metrô BH Line 1's Eldorado and Novo Eldorado | CNEFE, 13,011, zip cached in `data/contagem/raw/` | PLAN.md, same section; `brazil-city` |
| **Los Angeles** | Los Angeles (Regional) | **Long Beach**: 8 A Line stations | "Business Licenses Public View", 20,264 active, in-city, not home-based at the probe (20,204 at build, 2026-10-03: 3,246 kept, Retail 1,327, Food 1,160, Personal 759). **PERMITTED WITH CONDITIONS**; the breach-only indemnity was accepted by the owner (2026-09-30). Never imply endorsement. Withhold `FULLNAME` where there is no `DBANAME` (12,854). Drop the Pacific placeholder points. | PLAN.md "Wave-2 follow-ups" (6); `docs/data_sources/united-states.md` |
| **Vancouver (Regional)** | (unchanged name) | **Burnaby (11), New Westminster (5), Coquitlam (4)**: 20 SkyTrain stations | Burnaby: 20,054 approved licences, every row a point, 2,143 in the buckets (probed 2026-10-02). New Westminster: 856 under today's rules (907 at the probe, before the 2026-09-29 caterer and catch-all exclusions), 853 placed. Coquitlam: 1,026 (the table listed twice; LAT/LONG in Web Mercator metres; 10 kiosks out). Build figures, 2026-10-03. All under OGL variants. Richmond (R) and Port Moody (no addresses) stay out. | `docs/build_briefs/vancouver_regional.md` |

**Vancouver's three small calls: APPROVED by the owner (2026-10-02, "approve
the three vancouver calls"), as recommended:**
1. Burnaby's credit: the BC wording as printed, "City of Burnaby", with a
   link.
2. `RETAIL SALE, RENTAL & REPAIR` (32 rows) goes to Retail.
3. Coquitlam's mall kiosks (about 9) are left out.

## How this session runs: one lead, sequential, Brazil first

The four do not split cleanly enough for parallel agents. Rio and Belo
Horizonte share the Brazil modules (`pipeline/countries/brazil*.py`), and
each extension is a careful edit of a live city. **Order:**
1. **Belo Horizonte + Contagem**, the simplest: two stations and one more
   município.
2. **Rio + Duque de Caxias**, which reuses the regional scoping Belo
   Horizonte just set up.
3. **Los Angeles + Long Beach.**
4. **Vancouver (Regional)**; its three calls are approved.

An agent may take a self-contained leg, such as Burnaby's step 2 filter or
Long Beach's withhold-and-drop. It returns the file and its counts, and never
commits, queries Overpass or edits a shared file.

**For each extension:**
1. **Prove the scoping change on the city alone first.** Re-render the built
   city with the new scope switched off and confirm zero drift.
2. **Then switch it on.** Record what moves: stations, storefronts, ring
   shares and macro facts.
3. **The page:**
   - It becomes "(Regional)" where the table says.
   - Its sections in What Is Excluded and About the Data name the new
     municipality (`docs/city_page_format.md`).
   - Every new source gets a licence row in `docs/data_sources/<country>.md`
     and its notice.
4. **Run the gates, then a deliberate baseline update.**
   `pipeline/drift_check.py` will report the change: confirm it is exactly
   the extension's, then re-record the baseline, as the built-city rescopes
   did.

## Visuals and analytics: what a build owes them (staging, 2026-10-02)

The visuals session is drafting presentation pieces on `visual-handoff`, not
yet on master: city cards, a title card, explainers. They are generated from
published files, so a city feeds them with nothing extra, as long as the
build keeps three things true:
1. **Native-script names stay in config.** The cards read each city's own
   name from its config: `MUNICIPALITY` (Japan), `BOUNDARY_NAME` (Korea),
   `CITY_NAME_ZH` (Taiwan). Keep the field the city's country uses; do not
   drop it as unused.
2. **Ring shares and bucket counts come from the gates.** Every card checks
   its pins against `app/ring_shares.json` and its layer counts against the
   bucket counts, so gate 9's ring shares must be recorded for the city.
3. **Every notice is registered where the page lists it.** Card credits are
   built from the per-page notice plan (`city_notices()`, on Cleanup's
   prose-pass branch, landing at review time). Register each new notice the
   same way as the city's other notices, so the card picks it up once both
   land.

**No analysis on any page.** AI-driven deep analysis is now permitted, but
it is private to the owner and always carries an AI-generated
acknowledgement. The rule is on `visual-handoff`, coming to `CLAUDE.md`. It
never goes on a city page, `outputs/` or any deployed file, so a build writes
none.

## Numbers

- **Pages:** none new. The four keep their pages.
- **Notices:** **129–136**, pre-assigned by staging, for:
  - New Westminster's, Coquitlam's and Burnaby's OGL statements;
  - Long Beach's;
  - any other the reads require.

  Japan wave 2 holds 115–128. Record the range in `docs/session_roles.md`'s
  numbers sentence.

## Gate order (Band B's, per city)

1. personal exposure and the privacy-verdict row (a re-run for the extended
   city);
2. provenance;
3. scope disclosure;
4. the inconsistency rows and `cities.py` fields;
5. the master list's add-ons section (the extension moves to the city's
   Built row);
6. macro facts and the macro label;
7. the decisions entry;
8. commit;
9. the drift check and the deliberate baseline update;
10. merge master, `check_all.py`, and push at 0 behind.

**Not to master** until the owner's review time.

## Session rules

- Decisions go to `docs/decisions_drafts/extensions.md`.
- **Overpass:** one query in flight per session; wait 60 s after a 504 or
  429. Only the lead queries.
- `data/` is one shared junction. Never re-run a city outside these four. A
  failing `check_macro_facts` or `check_ring_shares` on another city goes to
  Cleanup.
- **Personal data:**
  - Never fetch Burnaby's `ACCOUNT_NAME`, New Westminster's `LICENCEE_NAME`
    or `MAILING_ADDRESS`, or Coquitlam's `COL_BUSINESSPHONE` or
    `EMAILADDRESS`.
  - Withhold Long Beach's `FULLNAME`.
  - Select columns before printing anything.
- No backslash or backtick in a Bash command. Write a script file.
- Downloads named here or in the briefs are pre-permitted. Anything else
  goes to the owner.
