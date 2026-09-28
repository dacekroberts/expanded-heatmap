# Tram rescope of built cities — estimated load and recommendations

**Saved 2026-09-27 for later (owner). Nothing is rescoped, and nothing here
is decided.** The rescopes are held by the owner (PLAN, "Trams left off built
maps"), and Band T's group decision is deferred until the full tram list and
the second-wave screens are done. The tram-list count itself now runs **with
wave 2** (owner, 2026-09-27).

## How the load was estimated

No per-build usage has ever been recorded, so this is calibrated from one
session. On 2026-09-27, two build briefs (Daegu and Busan), Daegu's correction
and a 32-file encoding fix used about **32 points of the 5-hour window and 4
of the weekly limit, roughly 8:1**. The per-city figures are judgement from
that anchor, with wide ranges. **Read `get_usage` before and after the first
batch and re-scale the rest** before trusting them.

## The table (% of one 5-hour window)

| Work | Cities | Each | Subtotal |
|---|---|---|---|
| **Complete the tram list** (read-only, cached OSM plus small fetches) — **moved into wave 2** | Barcelona TRAM, Hong Kong Tramways, Seoul's Wirye Line, D.C. Streetcar's service status, Mexico City's Cablebús | 1–2% | 5–8% |
| Light rescopes (1 line, data cached) | Rome tram 8, Madrid ML1, SF F Market, Montréal REM, D.C. Streetcar | 2–4% | 10–20% |
| Medium | Paris T3a/T3b plus the edges of T2/T9 | 4–6% | 4–6% |
| Heavy (many routes; every drawn line needs its own label and legend entry) | Toronto (18 routes, 476 stops), Milan (17 routes, no published colours), Prague (37 routes) | 6–10% | 18–30% |
| Blind spots, if rescoped | Barcelona (6 lines), Hong Kong Tramways | 4–5% | 8–10% |
| Once per batch | drift check, map checks, disclosure docs, one deploy check, publish | — | 8–12% |
| **Total** | | | **about 55–85% of one 5-hour window, roughly 7–11% of the weekly limit** |

Left out: Fortaleza's diesel VLT (failed the rail test, every 40 minutes), and
every "reason still stands" case in PLAN (heritage lines, no stop in scope,
works routes).

## Recommendations, by category

1. **Complete the tram list: YES, first.** It is the cheapest line and the
   Band T decision now waits on it. It runs with wave 2 (owner). It is
   read-only, so it costs no build or deploy.
2. **Light rescopes: YES, as one batch**, in this order:
   - **Montréal REM first.** It is an automated light metro, not a street
     tram, and its omission was silent. It is arguably a scope error rather
     than a tram question.
   - **Rome tram 8** and **Madrid ML1**: one line each, stops outside the
     metro's reach, colours published.
   - **SF F Market: yes, but low priority.** It overlays Muni Metro on Market
     Street, and its Embarcadero stretch to Fisherman's Wharf is the only rail
     there. The "heritage" objection fell with "trams count".
   - **D.C. Streetcar: only after its service status is verified** (the
     tram-list count does that).
3. **Paris T3a/T3b: YES.** The ring trams run the périphérique corridor the
   metro crosses but does not follow. IDFM publishes colours, and 62 stops is
   a modest map change.
4. **Heavy cities: NOT YET. Decide a design rule first, then pilot ONE.**
   - The invariant (every drawn line gets a permanent label and a legend
     entry) makes 17–37 street routes a map-readability question before it is
     a data one.
   - **Pilot Toronto**: TTC publishes colours, and the streetcars are the
     downtown network. If the pilot map stays readable, Milan and Prague
     follow with the same rule.
   - **Milan also needs a colour decision** (ATM publishes none), and
     **Prague probably needs a frequency or core-network filter**
     (`docs/sub_transit_line_filters.md`) before 37 routes are drawn.
5. **Blind spots: decide after the count.**
   - **Barcelona TRAM: likely yes.** Trambaix and Trambesòs reach districts
     beyond the metro.
   - **Hong Kong Tramways: recommend it stays out.** The owner excluded it on
     2026-09-24, and it runs beside the Island Line for most of its length:
     the pure-overlay case.
   - **Seoul's Wirye Line: count only**; draw it if it is open and inside
     Seoul.
   - **Mexico City's Cablebús: yes.** Toulouse's drawn Téléo cable car is the
     precedent.
6. **Batch overhead: pay it once.** Land every approved rescope together at
   the owner's review time, under one deploy check and one reboot.

**If only part of it is affordable**: the tram list plus light rescopes plus
Paris is about 25–40% of one window and covers eight cities. The heavy three
are most of the rest.
