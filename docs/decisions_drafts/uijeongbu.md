# DECISIONS drafts - branch `uijeongbu` (Band B build session)

Kept here under the owner's rule of 2026-09-30: build sessions keep their
entries in their own drafts file, and the cleanup session folds every drafts
file into `DECISIONS.md` in one pass. Newest first, each entry exactly as it
should land.

### 2026-09-30 - Uijeongbu built: a Gyeonggi satellite on SEMAS's register, the U Line drawn

**Built** on branch `uijeongbu` (from `origin/master`, `origin/macro-legend`
merged first), page 85, region Seoul Capital Area, not in the default frame,
from Bucheon's files and Namyangju's config. Downloads and page prose under the
owner's pre-approval (2026-09-30); the page is Bucheon's approved text with
Uijeongbu's lines. **13,103 storefronts** (food service 5,875, retail 5,090,
personal services 2,138), exactly the brief's; 11,178 within the rings
(85.3%, the brief's, the highest of any satellite). **20 stations** on three
lines (U Line 15, Line 1 5, Line 7 1: Jangam; Hoeryong shared by Line 1 and the
U Line), a 615 m median gap: standard rings, outside the spacing rule's
540-570 m band that would go to the owner (the brief read 622 m). `coverage`
full, `categories` "All three", `mode` metro, as the built satellites.

- **The U Line** (Uijeongbu LRT) in OSM's colour (#F0831E); Line 1 and Line 7 in
  the colours Bucheon draws. Line 7's one station is drawn by the satellites'
  rule.
- **Its two depot-shuttle relations** (no ref) are placed by name in
  `NOT_DRAWN_BY_NAME` (Incheon's pattern, as the brief said): the ref-U
  relation carries the whole line, and a drawn line is never matched on text.
- **Not drawn**: Line 4 and GTX-A, which reach the query box with no station in
  Uijeongbu.
- **Gate 3** exact on the U Line (15) and Line 7 (53); Line 1 left out of the
  whole-line gate, as in Incheon and Suwon.
- **Close pair read and kept**: the U Line's 경전철의정부 ("LRT Uijeongbu") and
  Korail's 의정부, 257 m apart, are separate stations.
- **Personal exposure: PASS.** `check_personal_exposure.py uijeongbu` (the
  Korean pass): a Korean personal name at a residential address still shown on
  0 of 13,103 rows; 11 withheld by step 2.
- **Licence**: notice 68 (SEMAS) gains Uijeongbu in its heading and text.
- **Macro label**: width 68.6 px (measured 2026-09-30, controls reproduced).
  Uijeongbu moves the Seoul Capital Area frame's centre north (37.450 to
  37.490 N; zoom unchanged, measured in memory); the default ("middle", 0, -22)
  scores clear, alone and on the combined tree with Namyangju's and Ansan's
  branches.
- **Master list**: the Gyeonggi satellites row stays a Band B candidate (Anyang,
  briefed on its ring share, is not built here); Uijeongbu adds to Built only.
  Namyangju, Ansan and Uijeongbu each call their city South Korea's tenth on
  their own branch: renumber in landing order.
