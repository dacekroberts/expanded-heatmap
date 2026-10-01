# DECISIONS drafts - branch `dallas` (Band B build session)

Kept here under the owner's rule of 2026-09-30: build sessions keep their
entries in their own drafts file, and the cleanup session folds every drafts
file into `DECISIONS.md` in one pass. Newest first, each entry exactly as it
should land.

### 2026-09-30 - Dallas: the Streetcar and the M-Line out, and coverage narrowed as Houston (owner)

Three calls at the build, each recommended:
- **The Dallas Streetcar and the M-Line trolley are not drawn** (owner): DART's
  four light-rail lines only, Houston's shape. Both are named in
  `config.NOT_DRAWN` so step 1 still stops on any relation it cannot place.
- **`mode` light_rail** (owner, as the brief proposed): DART has no metro.
- **`coverage` narrowed, `categories` "Personal services thin"** (owner). The
  brief proposed "full"; I first passed that on without weighing Houston,
  which uses the same register and is narrowed because Texas taxes few
  personal services, then corrected the question. Dallas's in-ring pins bear
  it out: 2,501 retail, 1,492 food service, 204 personal services. The brief is
  corrected to the calls.

### 2026-09-30 - Dallas built on Houston's register and rules, placed by the City's Address Points

**Built** on branch `dallas` (from `origin/master`, `origin/macro-legend` merged
first), page 86, region United States East, in the landing view (as Houston and
Sacramento). From Band A (owner, 2026-09-30), the last city in the Band B
session's queue. Downloads and page prose under the owner's pre-approval
(2026-09-30). **15,885 storefronts placed inside the city** (of 17,049
premises), 4,197 within the rings (26.4%; the brief's 400-row sample read
24.4%), **44 stations** on four lines.

- **Register**: the Comptroller's `jrea-zgmq`, 44,760 outlets flagged DALLAS
  inside city limits, Houston's explicit column list - `taxpayer_name`,
  `taxpayer_address` and `taxpayer_number` never requested, asserted twice.
  Houston's step 2 unchanged: 18,275 storefront NAICS; 97 not trading yet, 771
  at an apartment or trailer (homes), 21 with no house number; 17,049
  premises; 3,408 personally owned (IS 3,238, PI 170) show their address, never
  a name. Houston's measured reading that UNIT and SPC are commercial spaces
  held on Dallas's rows (NorthPark Center, DFW's concessions).
- **Placement** (`step3_place.py`, Houston's passes on Dallas's layer): the
  City's Address Points, 395,893 points pulled in pages of 2,000 (never per
  address): exact 14,363, canonical 158, unique street under any ZIP 560, and
  the brief's fourth tier, the nearest listed number on the same side within
  10, 225; the Census geocoder took 1,349 of the 1,743 left. **89.8% joined,
  7.9% geocoded, 2.3% unplaced**; 770 placed points with a Dallas postal address
  lie outside TIGER's city polygon and are dropped (no address-point placement
  among them). The indemnity was accepted by the owner (2026-09-30); the page
  calls the placement approximate, not surveyed.
- **Not run: Houston's "a person's permit at a Residential point is a home"**.
  The Address Points carry an `ADDRESSTYPE` code (T 250,622, B 61,683, A 47,722,
  P 23,855, and ten rarer) that neither the layer nor its ArcGIS item
  documents, so no code is read as Residential. Personally owned outlets still
  show an address rather than a name, and apartments and trailers are still
  left off. **For review time**: the codes' meaning (the City's GIS office) would
  let the rule run.
- **Personal exposure: PASS at Houston's level.** `check_personal_exposure.py
  dallas`: a person-like name at a residential unit on 4 of 4,197 pins (0.10%;
  Houston 0.31%), each a company outlet in a mall or airport space; no taxpayer
  column exists to fall back to.
- **Boundary**: TIGER's place polygon, GEOID 4819000, 993.8 km² (Houston's
  rule), not OSM's relation.
- **Rail**: OSM, 27 DART light-rail relations (network `DART`); 128 stop
  positions -> 64 stations, 44 inside the city, 20 beyond it excluded (Plano,
  Richardson, Garland, Rowlett, Carrollton, Farmers Branch, Irving, DFW
  Airport); median gap 1,388 m, standard rings. **Gate 3 exact** against
  English Wikipedia's line infoboxes (Red 26, Blue 23, Green 24, Orange 31) less
  two stations read at build: Convention Center, in OSM's Red and Blue
  relations with role `inactive` and closed while the convention centre is
  rebuilt, and Hidden Ridge, the Irving infill station OSM does not yet carry
  (outside the city: no ring lost).
- **Line colours**: the project's own. Red and Green are Houston's; Blue and
  Orange the smallest HLS move from DART's hues clearing CIE76 46 from the pins
  and 30 from the other lines, 3:1 on both pages: DART's blue sat 15.5 from
  Retail's pin, so #264ded (46.4); orange #d97c0e.
- **Page**: Houston's approved text with Dallas's facts, plus two sentences
  beyond the template, **flagged for review time**: the timetable (every 20
  minutes at peak, 20 to 30 at other times; Wikipedia's DART article, read
  2026-09-30), which the brief says to disclose, and that Texas taxes only some
  services, so salons and barbers mostly do not appear (the coverage call).
- **Macro label**: width 40.1 px (measured 2026-09-30, five controls
  reproduced). In the landing view Dallas's dot fell inside San Diego's pill,
  so **San Diego's label moved west of its dot**, ("start", 16, 0) to ("end",
  -16, -2), and Dallas sits left of its own dot, ("end", -10, -3), in a narrow
  clear window (dy -6 to 0); PROBLEMS 0 on the combined tree with every Band B
  branch.
- **Master list**: Dallas leaves Band A, which is now empty of candidates.
