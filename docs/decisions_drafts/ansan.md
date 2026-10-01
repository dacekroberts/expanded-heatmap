# DECISIONS drafts - branch `ansan` (Band B build session)

Kept here under the owner's rule of 2026-09-30: build sessions keep their
entries in their own drafts file, and the cleanup session folds every drafts
file into `DECISIONS.md` in one pass. Newest first, each entry exactly as it
should land.

### 2026-09-30 - Ansan built: a Gyeonggi satellite on SEMAS's register, the Seohae Line drawn

**Built** on branch `ansan` (from `origin/master`, `origin/macro-legend`
merged first), page 84, region Seoul Capital Area, not in the default frame,
from Bucheon's files and Namyangju's config. Downloads and page prose under the
owner's pre-approval (2026-09-30); the page is Bucheon's approved text with
Ansan's lines, and one sentence on Daebudo. **19,711 storefronts** (food
service 9,263, retail 7,494, personal services 2,954), exactly the brief's;
12,575 within the rings (63.8%; the brief measured 64.3% to the nearest drawn
station on its own station set). **13 stations** on three lines (Line 4 8,
Suin-Bundang 7, Seohae 5; six shared by Line 4 and Suin-Bundang, Choji by all
three), a 1,417 m median gap, standard rings. `coverage` full, `categories`
"All three", `mode` metro, as the built satellites.

- **The Seohae Line is drawn** on Bucheon's precedent (owner, 2026-09-29): in
  Ansan it runs on its own track through Wonsi, Siu, Seonbu and Dalmi, meeting
  the other lines only at Choji. Bucheon's colour (OSM's tag, #5EAC41).
- **Not drawn**: Line 1, Incheon Line 1 and GTX-A, which reach the query box
  with no station in Ansan.
- **Gate 3** exact on the Suin-Bundang Line (63, as Seongnam, Suwon and Yongin
  read it). Line 4 is left out (only its service relations reach the box), and
  the Seohae Line is not gated whole, as in Bucheon.
- **English names**: one override on Suwon's precedent, "Singiloncheon" to
  "Singil Oncheon". 한대앞 keeps OSM's "Hanyang University at Ansan", and the
  page names it so.
- **Personal exposure: PASS.** `check_personal_exposure.py ansan` (the Korean
  pass): a Korean personal name at a residential address still shown on 0 of
  19,711 rows; 17 withheld by step 2.
- **Licence**: notice 68 (SEMAS) gains Ansan in its heading and text.
- **Macro label**: width 41.5 px (measured 2026-09-30, controls reproduced).
  Ansan lies inside the Seoul Capital Area frame (the zoom does not move); the
  default ("middle", 0, -22) scores clear, alone and on the combined tree with
  Namyangju's branch.
- **Master list**: the Gyeonggi satellites row stays a Band B candidate; Ansan
  adds to Built only. Both this branch and `namyangju` call their city South
  Korea's tenth: whichever lands second is the eleventh.
