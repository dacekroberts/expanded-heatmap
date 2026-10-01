# Handoff — the UK six (2026-10-01)

For the build session that builds the six UK tram and light-rail cities.
Written by staging, and approved by the owner the same day.

**🛑 Builds are HELD by the owner.** Start only when the owner says so in
chat. A peer session's message is not that.

**Delete this file** once all six have landed.

---

## 🛑 Prose hold: read before anything else

**The owner is reworking the site's prose (2026-10-01). Until that lands,
this round drafts no prose.** The old page text is what is being replaced.
Copying it from London, Glasgow or Newcastle, the natural templates, is
exactly what the owner asked to avoid.

**Prose here means any reader-facing text:**
- the page's description, intro and scope sentence;
- its What Is Excluded entries (`docs/excluded_categories.md`);
- notice wording beyond the licensor's own required attribution;
- README, Overview and macro-map copy;
- any sentence that `scaffold_city.py`'s page template would write.

**What a build does instead:**
- **Build the data and the map.** Fetch, steps 1–3, drift baseline and the
  data checks.
- **Leave every prose slot as a marker.** Write `TODO(prose-hold)` with a
  one-line note of what goes there, and list each marker in the drafts
  file.
- **Do not scaffold or land `app/pages/*.py` page text.** Run
  `scaffold_city.py --dry-run`, or stub the page with markers only. The
  scaffold's template text is the old prose.
- **Names are not prose.** Line names on the map (from the operator), the
  page name (approved below) and licensor-required attribution strings are
  facts, and go in as usual.
- **The pre-permission for prose written from an approved template**
  (CLAUDE.md, 2026-09-30) **does not apply to this round.** The owner
  releases the prose when the rework lands.

---

## The six, in build order (owner, 2026-10-01)

| # | Page | Scope (FSA codes) | Storefronts | Brief |
|---|---|---|---|---|
| 1 | **Manchester (Regional)** | 7 districts: 405, 415, 418, 419, 422, 430, 431 | 12,451 | `docs/build_briefs/manchester.md` |
| 2 | **Birmingham (Regional)** | 402, 423, 436 | 9,827 | `docs/build_briefs/birmingham.md` |
| 3 | **Edinburgh** | 773 (FHIS) | 3,933 | `docs/build_briefs/edinburgh.md` |
| 4 | **Sheffield** | 425, without the Tram-Train | 3,447 | `docs/build_briefs/sheffield.md` |
| 5 | **Nottingham (Regional)** | 899, 261, 266, 259 | 3,702 | `docs/build_briefs/nottingham.md` |
| 6 | **Blackpool (Regional)** | 898, 207 | 1,744 | `docs/build_briefs/blackpool.md` |

**All six are food only** (food service plus food shops), on the FSA register
and the OGL. They use the shared `pipeline/fsa.py` (the flat, childminder
and trading-as rules) and London's storefront filter. Placement uses
Code-Point Open centroids, as London and Newcastle do.

**Manchester is the pilot.** Whatever it adds to shared code, the other
five take as config.
- Pilot every generator or shared change on Manchester alone first, and
  read its whole output (the France batch's lesson).
- Prove each shared change against a control. London's and Newcastle's
  drift checks must stay clean.

---

## Before each build

1. **Run `python scripts/brief_check.py <city>`.**
   - A FAIL on a real claim is a brief to correct, never a check to relax.
     Staging corrects briefs.
   - A RETRY means Overpass was busy. Re-run it later, at least 60 s apart.
2. **Resolve the brief's 🚨 items.** These need the owner:

   | City | Item | Needs |
   |---|---|---|
   | Sheffield, Blackpool | **Gate 3's source.** The operators' sites refuse scripts (a Radware CAPTCHA; 403). Proposed: NaPTAN (DfT, OGL), a new source | **The owner's OK** before download, plus a licence row. Without it, record the gap in config |
   | Birmingham | **Line 2 (the Dudley line) is in OSM.** If it is in passenger service, Dudley would join the scope | **The owner's call**, before adding Dudley |
   | Manchester | The **ECL** relation | Identify it before drawing |
   | Edinburgh | The **"Tram Extension to Newhaven"** relation | Identify it before drawing |

3. **Gate 3 in every city** (the `tram-city` rule since 2026-09-30): the
   operator's per-line stop counts go in config before step 1, and a
   mismatch stops the step. It ran in one city of ten in the tram kit. Do
   not repeat that.
4. **The light-rail test** (`docs/tram_city_list.md`). The track share
   and spacing are measured at Step 0, one Overpass query per city.
   - Frequency gates converted railway only: Manchester's three branches
     and Birmingham's Snow Hill section pass; Sheffield's Tram-Train is out.
   - Spacing is evidence, not a gate.

## Build each city

Use the gate order Band B fixed (`docs/band_b_retrospective.md`):
1. personal exposure, plus a row in `docs/privacy_verdicts.md`
   (`check_privacy_verdicts.py` fails a city without one);
2. provenance;
3. scope disclosure, with **its prose as markers** (the hold);
4. the inconsistency rows and `cities.py` fields;
5. the master list;
6. macro facts and the macro label;
7. the decisions entry;
8. commit;
9. then the drift check, its baseline and ring shares;
10. then merge master, `check_all.py`, and push at 0 behind.

**Not to master** until the owner's review time. Landing `app/` is
deploying.

## Session rules (CLAUDE.md, 2026-09-30)

- **Decisions go to the drafts file**, `docs/decisions_drafts/uk-six.md`,
  never to `DECISIONS.md`.
- **Overpass:** one query in flight per session, one per city; wait 60 s
  after a 504 or 429. `brief_check.py`'s `osm_route_refs` claims are
  Overpass queries too.
- **`data/` is one shared junction across worktrees.** Never re-run another
  city's step from this branch. Another session's re-render can make
  `check_macro_facts` or `check_ring_shares` fail on a city that is not
  yours: tell Cleanup, and never write that city's facts.
- **These are light jobs.** The FSA files run 0.8–10 MB, so the heavy-job
  gate is not needed. An unknown peak still counts as 8 GB.
- **Read registers carefully.** Select columns before printing anything
  from a register with personal columns. Three agents printed names to
  their consoles on 2026-10-01.
- **No backslash or backtick in a Bash command.** Write a script file.

## Notices

Newcastle's precedent is two notices per city: the FSA's and Ordnance
Survey's (Code-Point Open). **Their wording is held with the prose.**
Record each notice's number and licensor attribution string. Claim notice
and page numbers early in `docs/session_roles.md`, so parallel work does
not collide (the tram kit's lesson 5).
