# DECISIONS drafts - branch `namyangju` (Band B build session)

Kept here under the owner's rule of 2026-09-30: build sessions keep their
entries in their own drafts file, and the cleanup session folds every drafts
file into `DECISIONS.md` in one pass. Newest first, each entry exactly as it
should land.

### 2026-09-30 - Namyangju built: the sixth Gyeonggi satellite, on SEMAS's register

**Built** on branch `namyangju` (from `origin/master`, `origin/macro-legend`
merged first), page 83, region Seoul Capital Area, not in the default frame,
from Bucheon's files (the satellites' module: SEMAS through `korea_sbiz`, OSM
rail on Busan's step 1). Downloads and page prose under the owner's
pre-approval (2026-09-30); the page is Bucheon's approved text with
Namyangju's lines and one sentence on its spread. **18,344 storefronts**
(food service 8,069, retail 7,699, personal services 2,576), exactly the
brief's; 10,067 within the rings (54.9%, the brief's); **17 stations** on four
lines (Gyeongchun 7, Gyeongui-Jungang 6, Line 4 3, Line 8 2; Byeollae on Line 8
and Gyeongchun), a 2,294 m median gap, standard rings. `coverage` full,
`categories` "All three", `mode` metro, as the five built satellites.

- **Colours**: Seoul's for Line 4, Gyeongui-Jungang and Gyeongchun; Line 8 as
  Seoul and Seongnam draw it (#92144E).
- **Not drawn**: GTX-A and Seoul's Lines 2, 5, 6 and 9, which reach the query
  box with no station in Namyangju.
- **Gate 3**: no line takes the whole-line gate, each for a reason an earlier
  city recorded - Line 4's relations in the box carry 29 of its 51 stations
  (Line 1's case in Incheon and Suwon); Line 8 24 against 25 (Seongnam's);
  Gyeongui-Jungang 55 against 57 (Goyang's); Gyeongchun's relations carry 25
  with the Cheongnyangni and Kwangwoon University branches, its infobox 20 and
  its table 21 (read 2026-09-30). In its place, each line's in-city stations
  were read against its line table (English Wikipedia, 2026-09-30) and all four
  agree with step 1 (7, 6, 3, 2).
- **English names**: two overrides on Suwon's precedent, "Byeollaebyeolgaram"
  to "Byeollae Byeolgaram" and "PyeongnaeHopyeong" to "Pyeongnae-Hopyeong".
- **OSM**: the rail answer came from a mirror whose OSM base was 2026-07-28;
  nothing on Namyangju's four lines changed since (the brief's counts of
  2026-09-29 reproduce).
- **Personal exposure: PASS.** `check_personal_exposure.py namyangju` (the
  Korean pass): a Korean personal name at a residential address still shown on
  0 of 18,344 rows; 37 withheld by step 2 (30 of them inside the rings).
- **Licence**: notice 68 (SEMAS) gains Namyangju in its heading and text.
- **Macro label**: width 75.8 px (measured 2026-09-30, controls reproduced).
  Namyangju widens the Seoul Capital Area frame (zoom 8.21 to 8.10, measured in
  memory with and without it); the default ("middle", 0, -22) scores clear, and
  every other label there still does: PROBLEMS 0 on the combined tree.
- **Master list**: the Gyeonggi satellites row stays a Band B candidate until
  Ansan and Uijeongbu (and Anyang, briefed) are built; Namyangju adds to Built
  only.
- **For the cleanup session**: `brief_check.py gyeonggi` FAILS one claim, on
  Anyang's query box (Lines 1 and 4 and the Sillim Line by ref), a city this
  session is not building; the brief needs correcting there.
