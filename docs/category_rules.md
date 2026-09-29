# Category rules — what counts as a storefront, the same in every city

**Read this before recommending that any category be kept or left out.** A new
city's taxonomy must reach the same answer as the built cities for the same
trade, or say plainly why it cannot. The owner's standing rules are below, each
with the cities it was measured on. A new register's category is matched to a
rule by what the premises IS, not by the register's word for it.

**How to use it (the `premises-taxonomy` and `add-city` skills point here):**

1. For every category you would keep or drop, find its row below.
2. If there is no row, grep `pipeline/taxonomies/` for the trade in the
   languages already built (massage: `massag|masaje|massaggi|마사지`) and
   read what each city did.
3. Recommend the precedent. **A departure is an owner call**: bring it with
   the precedent it breaks, the count, and the reason this register differs.
   "It seems risky" is not a reason; "the register names it as adult" is.
4. When the owner makes a new cross-city call, add a row here in the same
   change as its DECISIONS entry.
5. **`python scripts/check_category_continuity.py` enforces this table**
   (it runs in `check_all.py`). Its table,
   `scripts/category_continuity_table.py`, locates each rule's trade in
   every taxonomy and asserts `classify()` reaches the rule's verdict. A new
   row here, or a new taxonomy, fails the check until every taxonomy has
   answered it. A departure is listed there as a DECISIONS-backed exception
   or as pending for the owner, never fixed to make the check pass.
   `--matrix` prints the rule-by-taxonomy grid.

Why this file exists (2026-09-29): Korea's SEMAS taxonomy was first proposed
with massage left out, which would have made Korea the only country to drop
commercial massage, and the fringe-category rules below lived only in a
DECISIONS entry that a build session does not read before recommending.

## The rules

| Trade | Rule | Precedent (where measured or decided) | Source |
|---|---|---|---|
| Funeral homes, crematoria, cemeteries | **Out**. Shops selling funeral goods stay Retail | NAICS 8122, SCIAN 8123, NAF 96.03Z, Rev. 2.1 96.30, Madrid, Taiwan 9630, Brazil, the local types in six more cities; about 4,180 pins | DECISIONS 2026-09-29 "Funeral exclusions coded" |
| Food with no counter of its own: institutional and staff canteens, contract catering, event caterers, mobile food, street and market stalls | **Out** (R1). A market building of fixed shops is kept (Seoul's 시장, Riga's pavilions); its stalls and stands are not | Madrid's 1,157 canteens; France's traiteurs 56.21Z and Montréal's caterers KEPT (usually a shop) | same entry, R1; DECISIONS 2026-09-29 "the owner's calls on the pending departures" |
| The "other personal services" catch-all (NAICS 812990 and its equivalents: wedding halls, matchmaking, tarot, public toilets, shoe-shine stands) | **Out** (R2). Tattoo stays where it has its own code, except Berlin's, which goes with its 969 catch-all (owner, confirmed 2026-09-29) | San Diego, Montréal, Mexico, Madrid, Taiwan; ten more cities had already dropped it | same entry, R2 |
| Adult and hostess venues: cabarets, hostess bars (Korea's 유흥주점), body-rub premises, premises the register names as adult | **Out** (R3), wherever the register names them | Tokyo's cabarets and snack bars (2,536), San Diego's "massage parlors" (144), Calgary's body-rub centres, Seoul's 유흥주점 | same entry, R3 |
| Korean karaoke bars (단란주점) | **Kept**, Food service | Seoul, Daegu, Busan | R3 (owner) |
| Sex shops | **Kept**, Retail | | R3 (owner) |
| Commercial massage (not named as adult, not regulated health care) | **Kept**, Personal services | NAICS 812199; D.C., Miami, Chicago, Calgary, Dublin, Milan, Buenos Aires, Brazil, Korea (SEMAS) | korea_sbiz.py (owner, 2026-09-29) |
| Regulated massage therapy (a registered health profession) | **Out** (health care, NAICS 621) | Vancouver's and Toronto's RMTs | vancouver.py, toronto_mlscategory.py |
| Car dealers, petrol and LPG stations | **Kept**, Retail (R4). Vehicle repair and wholesale stay out. A type that merges fuel with repair or a car wash goes whole (Edmonton, Philadelphia), and a forecourt with no shop is out (Dublin) | about 40 cities; France the disclosed exception (division 45 left out: mostly one-person traders registered at home, owner 2026-09-29) | R4; DECISIONS 2026-09-29 "Exclusions batch: the owner's eight follow-ups" |
| Gambling: betting shops, lottery sellers, casinos | **Out** (R5) | Dublin's 176 betting shops | R5 |
| Pawnbrokers | **Kept**, Retail. New York and Chicago are disclosed exceptions. Where a classification files pawnshops with every other lender (NAICS 522298/522299, NACE 64.92) none can be kept | Mexico, Berlin, Taiwan and D.C. brought in (owner, 2026-09-29) | R5 |
| Nightclubs (not adult) | **Kept**, Food service | Toronto and Edmonton aligned 2026-09-29; Madrid, Taiwan and Brazil to align (owner, 2026-09-29) | R5 |
| Veterinary clinics | **Out** (professional, NAICS 541940) | six cities; Barcelona's `Veterinaris / Mascotes` kept and disclosed (one value mixed with pet shops, owner 2026-09-29) | R5; DECISIONS 2026-09-29 "Exclusions batch: the owner's eight follow-ups" |
| Nonstore retail: e-commerce, mail order, direct selling, vending machines, fuel dealers | **Out**, heating-fuel and bottled-gas dealers included | NAICS 454 in every NAICS city, and its 2022 recodes 445132 and 457210 (owner, 2026-09-29); Korea, Brazil | naics.py |
| Parking | **Out** | NAICS 81293 | naics.py |
| Repairs (vehicles, appliances, phones, clothing alterations) | **Out** (NAICS 811, not 812), shoe repair, key cutting, tailoring and alterations included. Miami's one dry-cleaning-and-alterations type stays whole | the NAICS cities and most others; Chicago, Dublin, Buenos Aires and Barcelona aligned (owner, 2026-09-29) | naics.py |
| Lodging: hotels, motels, guest houses | **Out** | every city; Barcelona's and Mexico's accommodation inside food service carved out | premises-taxonomy Step 5 |
| Recreation (NAICS 71): gyms, karaoke rooms, PC rooms, sports venues | **Out** | the NAICS cities | naics.py |
| Pharmacies, opticians | **Kept**, Retail (NAICS 44-45) where the register covers general retail. A food-only register's pharmacies are out (not food shops), except the FSA cities', which are kept. Melbourne's opticians are out: ANZSIC files them in health (owner, confirmed 2026-09-29) | the NAICS cities; Stockholm (food-only) | naics.py; DECISIONS 2026-09-29 Stockholm |
| Health-food sellers | **In-store only**; e-commerce, door-to-door and multilevel sellers out, and never at an apartment unit | Seoul, Daegu, Busan, Incheon | korea_localdata.py |
| Mobile units, kiosk carts, vending machines | **Out** | Bucharest, Seoul (food trucks), Glasgow (mobile caterers) | romania_dsvsa.py, korea_localdata.py |
