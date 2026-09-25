"""Personal-data exposure check for a city's rendered map. Read-only.

Every `outputs/<city>/heatmap.html` is committed and meant to be served
publicly, and each pin carries a business NAME at a mapped COORDINATE. Where a
registry has no trade name for a row, the pipelines fall back to the owner or
registrant - which for a sole proprietor is a person's name, often at their
home address. Run this before publishing a city, and whenever a city's step 2
or its taxonomy changes.

    python scripts/check_personal_exposure.py                # every known city
    python scripts/check_personal_exposure.py los_angeles    # one city

It reports, per city:
  * pins whose displayed name can ONLY be the owner/registrant fallback
    (joined back to the raw trade-name column: the authoritative measure),
  * pins whose displayed name matches a conservative personal-name pattern
    (a heuristic - it flags "Jane Smith" and misses "J Smith Consulting"),
  * how many of those sit at an address with an APT/UNIT/STE/# indicator,
  * the classifications those pins carry, so a catch-all code sweeping in
    home-based registrants shows up by name.

Nothing here is a hard pass/fail: a trade name someone chose for their shop is
public commercial information, while a registrant name at a flat number is not.
Read the numbers, then decide per city and record the verdict in DECISIONS.md.
A new city must be added to REGISTRIES below (the columns are per registry).

Los Angeles is the worked example: excluding NAICS 812990 there (2026-09-21)
cut person-like pins from 3,998 to 1,803. See DECISIONS.md.
"""
import html
import json
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

# city slug -> how to find the trade name and the fallback in its RAW export.
# raw: file under data/<slug>/raw/; trade: the dba-style column; owner: what
# step 2 falls back to when trade is blank; processed/address: for the
# unit-indicator check (None to skip).
REGISTRIES = {
    # Dublin is the STRONGEST case in the project and the only one where the
    # answer is structural rather than measured: the Irish rateable valuation
    # register carries NO name column of ANY kind - no trade name, no occupier,
    # no ratepayer, no owner. 19 fields, all address, classification, valuation
    # and geometry, and step 2 ASSERTS that none matching
    # name|occupier|tenant|owner|ratepayer|proprietor|person|contact arrives,
    # exiting if a future refresh adds one.
    #
    # So there is no trade/owner fallback pair to join against, as for New York
    # and Philadelphia - but unlike those two the absence is a property of the
    # source rather than of what this project chose to download. Los Angeles'
    # failure mode (a blank trade name falling back to a registrant's own name
    # at their home) CANNOT occur here. The register is also non-domestic by
    # statute, so the residence question does not arise either.
    #
    # `business_name` holds the STREET ADDRESS, which is why the address
    # columns and the name column are the same field.
    "dublin": dict(raw=None, trade=None, owner=None, name_is_address=True,
                   processed="businesses_clean.csv",
                   address=("business_name",)),
    # Milan is a HYBRID, and the first one here: ~20% of pins carry a real
    # trade name (`insegna`) and the rest carry the street address, because
    # `insegna` is 17.6% populated on the retail register, 23.8% and 9.1% on
    # the two food ones, and ABSENT from three of the six registers entirely.
    #
    # None of the six carries a personal name - no titolare, ragione_sociale
    # or nominativo, confirmed against live headers, and step 2 EXITS if one
    # ever appears. So this is the France/Edmonton pattern (the publisher
    # stripped it) and the fallback is an address rather than an owner, which
    # is why Los Angeles' failure mode cannot occur.
    #
    # `name_is_address` is NOT set, unlike Dublin's: it is true of ~80% of
    # rows rather than all of them, so the heuristics below are measuring a
    # mixture. Read a person-like hit as "check whether this is an Italian
    # street name or a sole trader's shop sign" - both are present, and the
    # second is exactly what this script is for.
    "milan": dict(raw=None, trade=None, owner=None,
                  processed="businesses_clean.csv",
                  address=("business_name",)),
    # Paris is Milan's hybrid again, and the reasoning is worth keeping because
    # this city had the LARGEST measured temptation in the project to do
    # otherwise. SIRENE carries a premises name on only 37.2% of built rows, and
    # `StockUniteLegale` would have closed nine tenths of that gap by joining
    # `denominationUniteLegale` on siren. It is not joined, and the file is not
    # even downloaded.
    #
    # WHY: for a sole trader that column holds `nomUniteLegale` and
    # `prenomUsuelUniteLegale` - A PERSON'S NAME. Measured 2026-09-22, 8.7% of
    # Paris storefront rows are natural persons and 9.4% of the UNNAMED ones
    # are, so a blind fallback across the bucket would have published on the
    # order of TEN THOUSAND individuals' names, against the ~4,000 Los Angeles
    # nearly shipped. A guard on categorieJuridique == "1000" was measured as
    # safe and REJECTED anyway: "safe if the guard is built" does real work in
    # that sentence, and the hybrid needs no guard at all.
    #
    # So the fallback is the street address, as in Dublin and Milan, and step 2
    # ASSERTS that no personal-name column ever reaches it - a structural claim
    # rather than a measurement, which is what makes Los Angeles' failure mode
    # impossible here rather than merely unlikely. France also masks
    # non-diffusible records at source (name, address AND geolocation), which
    # removed 13.3% of active Paris rows before any of this ran.
    # ⚠ NOT name_is_address=True. That flag is Dublin's case - a register with
    # no name column at all - and Paris carries a real premises name on 37.2%
    # of built pins, so it is Milan's hybrid and takes Milan's shape. Setting
    # the flag also prints Dublin's own verification note (Irish streets named
    # after people, floor lists) as though it had been checked here, which it
    # had not.
    "paris": dict(raw=None, trade=None, owner=None,
                  processed="businesses_clean.csv",
                  address=("business_name",)),
    # Marseille is Paris's entry unchanged, and that is the point rather than
    # laziness: both read ONE national register through ONE shared step 2
    # (`pipeline/countries/france_register.py`), so the structural claim is the
    # same claim - no personal-name column is ever loaded, therefore no pin can
    # be one. The three remaining French cities will inherit it identically.
    #
    # What differs is only the fill rate: Marseille shows a premises name on
    # 43.8% of pins against Paris's 37.3%, so it falls back to the address less
    # often. Better data, same guarantee.
    "marseille": dict(raw=None, trade=None, owner=None,
                      processed="businesses_clean.csv",
                      address=("business_name",)),
    # Toulouse, the third on the same shared step 2 and so the same structural
    # guarantee again. Its fill rate is the best of the three at 51.9%, and
    # that is partly EARNED rather than given: excluding `96.09Z` removed 1,429
    # rows whose naming rate was the worst in the file, so the figure rose from
    # 50.6% to 51.9% as a side effect of a filter taken for other reasons.
    "toulouse": dict(raw=None, trade=None, owner=None,
                     processed="businesses_clean.csv",
                     address=("business_name",)),
    # Lille (Regional): the same shared French step 2 across eleven
    # communes rather than one, so the same structural guarantee - no
    # registrant-name column is ever loaded, in any of them.
    "lille": dict(raw=None, trade=None, owner=None,
                  processed="businesses_clean.csv",
                  address=("business_name",)),
    # Oslo: Enhetsregisteret's sub-units. NO owner column is loaded, but the
    # risk is not zero by construction the way France's is: a sub-unit's own
    # `navn` IS its owner's name for ~89% of sole traders (ENK parent). The
    # guard is norway_register.py's rule - an ENK row shows its ADDRESS, never
    # its name - so this check measures whether that rule held.
    "oslo": dict(raw=None, trade=None, owner=None,
                 processed="businesses_clean.csv",
                 address=("business_name",)),
    # Rennes, the fifth and last French city on the same shared step 2: the
    # same structural guarantee. Its premises-name rate is the best of the
    # five at 59.1%.
    "rennes": dict(raw=None, trade=None, owner=None,
                   processed="businesses_clean.csv",
                   address=("business_name",)),
    # Prague, the first Czech city: the structural guarantee again, from RES's
    # legal form. A natural person's (FORMA 101/105/107/424/425) or a v.o.s.
    # partnership's establishment shows its street address, never the
    # registered name, and a natural person's establishment at their own
    # registered seat is not on the map at all. No other name column is read.
    "prague": dict(raw=None, trade=None, owner=None,
                   processed="businesses_clean.csv",
                   address=("business_name",)),
    # Copenhagen, the first Danish city: Oslo's structural guarantee, from
    # CVR. The parent company's legal form is joined for every premises, and
    # a personally owned one (Enkeltmandsvirksomhed, PMV) - or any name with
    # the sole-trader marker "v/" - shows its address, never its name. CVR's
    # `coNavn` (c/o, a person on 25% of storefront rows) is never loaded and
    # step 2 asserts it. No registrant-name column exists to fall back to.
    # São Paulo, the first Brazilian city: IBGE's CNEFE has NO owner or
    # registrant column at all - a pin shows the census enumerator's
    # description of the establishment, or, at an address that also holds a
    # dwelling, only its category (the owner's decision of 2026-09-23,
    # structural, in pipeline/countries/brazil_register.py). So the fallback
    # failure cannot occur; the only route to a person's name is a first name
    # inside a description at a non-dwelling address (`BAR DO PAULO`), which
    # is a trade name there. No address column is carried, so the unit check
    # is skipped.
    "sao_paulo": dict(raw=None, trade=None, owner=None,
                      processed="businesses_clean.csv", address=None),
    # Every other Brazilian city reads CNEFE through the same national reader,
    # so São Paulo's structural answer holds for each; measured per city.
    "belo_horizonte": dict(raw=None, trade=None, owner=None,
                           processed="businesses_clean.csv", address=None),
    "brasilia": dict(raw=None, trade=None, owner=None,
                     processed="businesses_clean.csv", address=None),
    "salvador": dict(raw=None, trade=None, owner=None,
                     processed="businesses_clean.csv", address=None),
    "fortaleza": dict(raw=None, trade=None, owner=None,
                      processed="businesses_clean.csv", address=None),
    "porto_alegre": dict(raw=None, trade=None, owner=None,
                         processed="businesses_clean.csv", address=None),
    "recife": dict(raw=None, trade=None, owner=None,
                   processed="businesses_clean.csv", address=None),
    "santos": dict(raw=None, trade=None, owner=None,
                   processed="businesses_clean.csv", address=None),
    "rio_de_janeiro": dict(raw=None, trade=None, owner=None,
                           processed="businesses_clean.csv", address=None),
    "copenhagen": dict(raw=None, trade=None, owner=None,
                       processed="businesses_clean.csv",
                       address=("business_name",)),
    # Amsterdam, the first Dutch city, two layers. The BAG shop units carry NO
    # name at all - the pin shows the unit's address - and a unit also
    # registered as a dwelling is not on the map. The hospitality permits show
    # `zaaknaam`, the name the business trades under on its permit; the
    # register loads no owner or applicant column, so there is no fallback
    # to a registrant's name. What this check measures is whether a trade
    # name is itself a person's name.
    "amsterdam": dict(raw=None, trade=None, owner=None,
                      processed="businesses_clean.csv",
                      address=("address",)),
    # Rome: Roma Capitale's SUAP register carries NO name column at all, so
    # every pin shows its activity and street address and no person's name
    # can appear. Measured anyway, as a structural claim should be.
    "rome": dict(raw=None, trade=None, owner=None,
                 processed="businesses_clean.csv",
                 address=("business_name",)),
    # Rotterdam: neither layer carries a name. Permit premises show the fixed
    # label "Hospitality premises" (notice titles and abstracts sometimes hold a
    # trade name and are never read into a pin); BAG units show their address.
    "rotterdam": dict(raw=None, trade=None, owner=None,
                      processed="businesses_clean.csv",
                      address=("address",)),
    # Riga shows the KIND of place (excise) or the premise group's registered
    # name (cadastre); the excise holder (`Nodoklu_maksatajs`) is never read,
    # and the unit number is dropped from displayed addresses (owner).
    "riga": dict(raw=None, trade=None, owner=None,
                 processed="businesses_clean.csv",
                 address=("address",)),
    # FEHD's registers carry the SHOP SIGN (`SS`), the name on the licence
    # premises, and no licensee name at all - there is no owner column to
    # fall back to. The raw file is XML, so the processed file is read.
    "hong_kong": dict(raw=None, trade=None, owner=None,
                      processed="businesses_clean.csv",
                      address=("address",)),
    # Seoul's seventeen LOCALDATA registers carry the premises' trade name and
    # NO operator column (no 대표자, 성명 or 이름 in any of them); the telephone
    # column is never read, which step 2 asserts. So there is no fallback pair,
    # and the Latin heuristic cannot read Hangul: `korean` runs the Korean pass
    # (pipeline/korean_names.py) instead.
    # Taiwan's national tax register publishes no owner column; the risk is a
    # sole proprietor registered under the owner's own name. `taiwan` runs the
    # rule test above; the Latin heuristic cannot read Chinese.
    "taichung": dict(raw=None, trade=None, owner=None,
                     processed="businesses_clean.csv",
                     address=("address",), taiwan=True),
    "seoul": dict(raw=None, trade=None, owner=None,
                  processed="businesses_clean.csv",
                  address=("address",), korean=True, withheld="Name withheld"),
    "san_diego": dict(raw="sd_businesses_active_datasd.csv", trade="dba_name",
                      owner="business_owner_name", processed="businesses_clean.csv",
                      address=("address_no", "address_road", "address_suite")),
    "san_francisco": dict(raw="sf_business_locations.csv", trade="dba_name",
                          owner="ownership_name", processed="businesses_clean.csv",
                          address=("full_business_address",)),
    "los_angeles": dict(raw="la_active_businesses.csv", trade="dba_name",
                        owner="business_name", processed="businesses_geocoded.csv",
                        address=("street_address",)),
    "chicago": dict(raw="business_licenses_active.csv", trade="doing_business_as_name",
                    owner="legal_name", processed="businesses_clean.csv",
                    address=("address",)),
    # New York assembles four registries and NEVER loads a registrant-name
    # column (the salon file's license_holder_name is not even downloaded; its
    # step 2 asserts that). So there is no trade/owner fallback pair to join
    # against - raw and owner are None and the fallback measure is reported as
    # structurally absent, which is a stronger statement than a low count.
    # Its `unit` column is structured (DCA gives APT/STE/FL/RM as their own
    # values), so unlike San Diego the residence check here is real.
    "new_york": dict(raw=None, trade=None, owner=None,
                     processed="businesses_geocoded.csv",
                     address=("address", "unit")),
    # Philadelphia likewise never loads a registrant-name column (its step 2
    # asserts six of them stay absent), and its business_name is never blank,
    # so there is no fallback pair to join against either. What it adds that no
    # other city has is `legalentitytype`: Individual vs a corporate entity,
    # recorded by the registry itself. That is a STRUCTURAL signal, so here the
    # person-like-name regex is the cross-check and this column is the measure
    # - the other way round from every city above.
    "philadelphia": dict(raw=None, trade=None, owner=None,
                         processed="businesses_clean.csv",
                         address=("address", "unit_type", "unit_num"),
                         entity_type="legalentitytype",
                         entity_individual="Individual"),
    # Miami never loads a registrant-name column either: OWNERNAME is populated
    # on 100% of rows and is frequently a person, so fetch_sources.py does not
    # download it and step 2 asserts it and every MAIL* field stay absent.
    # There is therefore no trade/owner fallback pair to join against, and -
    # unlike Los Angeles (68% blank dba_name) and D.C. (49%) - none is needed,
    # because BUSNAME is present on every row. So `raw`, `trade` and `owner`
    # are None and the fallback measure reports as structurally absent, which
    # is a stronger statement than a low count.
    #
    # Its address is one free-text field, so the unit check is a regex over
    # BUSADDR rather than a structured column the way New York's is.
    "miami": dict(raw=None, trade=None, owner=None,
                  processed="businesses_clean.csv",
                  address=("address",)),
    # Boston never loads a personal-name column either: the ISD table carries
    # legalowner/namelast/namefirst and the Licensing Board table carries
    # applicant/manager/day_phone, and fetch_sources.py selects none of them -
    # step 2 asserts all eight stay absent. So the fallback measure reports as
    # structurally absent here too.
    #
    # READ ITS RESIDENCE FIGURE WITH CARE. Boston's addresses carry NO unit
    # designators at all - 0 of its person-like rows have an APT, UNIT, STE or
    # # - so a 0.00% residential reading is a MEASUREMENT GAP, not a verified
    # clean result. Same shape as San Diego's old 0.03%, which turned out to be
    # 2.80% once a parcel join replaced the address text. What limits the real
    # exposure here is the sources rather than the check: a food-service
    # licence and a package-store licence both require commercial premises, so
    # a home cannot hold one. The ISD table's `property_id` IS Boston's
    # assessing parcel id, so a parcel join against the city's Property
    # Assessment data (ODC-PDDL) is available if that is ever not enough.
    "boston": dict(raw=None, trade=None, owner=None,
                   processed="businesses_clean.csv",
                   address=("address",)),
    # MADRID IS THE STRONGEST STRUCTURAL CASE IN THIS PROJECT, and the reason
    # differs from every city above. New York, Philadelphia, Miami and Boston
    # all have a registrant-name column and decline to download it. Madrid's
    # register HAS NONE TO DECLINE: all 47 columns of the Censo de locales were
    # listed on 2026-09-22 and not one is an owner, titular, NIF/CIF, razon
    # social or contact field. The only name-shaped column is
    # `nombre_agrupacion`, which names a MARKET or SHOPPING CENTRE a unit sits
    # inside. Step 2 asserts twelve personal column names stay absent, so a
    # publisher widening the file raises rather than leaks.
    #
    # `rotulo` (the shop sign) is populated on 100% of kept premises and step 2
    # RAISES if any is blank, so there is no fallback path even in principle.
    #
    # READ THE RESIDENCE FIGURE AS STRUCTURAL, not as a measurement. Madrid
    # does not make this project infer whether a unit is a home: the register
    # carries `Uso vivienda` (8,486 premises) as its own status value, meaning
    # the unit reverted to residential use, and step 2 keeps only `Abierto`.
    # The address text here is street and number with no unit designator, so a
    # low unit-indicator count is the Boston measurement gap again - what
    # limits exposure is the source's own commercial/residential distinction,
    # not the regex.
    "madrid": dict(raw=None, trade=None, owner=None,
                   processed="businesses_clean.csv",
                   address=("address",)),
    # Barcelona: raw=None because the fallback pair does not exist to measure.
    # The Cens de locals is a FIELD SURVEY of premises, not a register of
    # registrants - `Nom_Local` is a shop sign and is populated on every row,
    # so step 2 has nothing to fall back TO and asserts as much. There is also
    # no address column: `USECOLS` never requests one, the map needs only
    # coordinates, and `Referencia_Cadastral` (a property-title reference) is
    # in FORBIDDEN_COLUMNS. So the unit-indicator check is skipped because
    # there is no address text in the pipeline at all, not because it was not
    # run.
    "barcelona": dict(raw=None, trade=None, owner=None,
                      processed="businesses_clean.csv", address=None),
    # Washington D.C. is the first city since Chicago where the trade/owner
    # fallback pair genuinely EXISTS and has to be measured rather than
    # reported as structurally absent. Its step 2 falls back from
    # ENTITYTRADENAME to ENTITYNAME, which is the legal entity's name - a
    # company name for a corporation, and sometimes a person's.
    #
    # Step 0 read that as "the Los Angeles trap at half LA's severity", on a
    # 49% blank-trade-name rate. That rate was measured before the category
    # exclusions, and General Business - 11,074 office rows, mostly with no
    # trade name - is most of it. On the rows that reach the map the gap is
    # 26.9%, and 85.6% of those carry a company-shaped ENTITYNAME.
    #
    # It also carries a STRUCTURAL entity-type signal, like Philadelphia's:
    # ENTITYTYPE names the legal form, and it spells sole trading two ways, so
    # entity_individual is a TUPLE here. That distinction is what the
    # measurement turns on - an LLC registered under its founder's name is a
    # deliberate public commercial act (San Diego's reasoning), whereas a sole
    # proprietorship displaying a person's name is the case to look at.
    "washington_dc": dict(raw="basic_business_licenses.csv",
                          trade="ENTITYTRADENAME", owner="ENTITYNAME",
                          processed="businesses_geocoded.csv",
                          address=("street_address",),
                          entity_type="ENTITYTYPE",
                          entity_individual=("Sole Proprietorship",
                                             "Domestic Sole Proprietor")),
    # Vancouver is REGIONAL (Vancouver + Surrey) and the only entry here whose
    # processed file mixes two registries. `raw` points at Vancouver's own
    # export, because Surrey's has no trade/owner pair to join against: it
    # publishes a single BusinessName and no second name column, so Surrey
    # rows cannot be a substituted fallback by construction.
    #
    # Vancouver's fallback pair genuinely exists, as D.C.'s does:
    # businesstradename -> businessname, blank on 49.6% of MAPPABLE rows (the
    # 63.0% in the build brief was measured before the coordinate and category
    # exclusions - the denominator error this project keeps re-learning).
    #
    # ITS STRUCTURAL SIGNAL IS A NAME FORMAT, NOT A COLUMN, which is why
    # entity_type is absent here even though the city has a structural signal
    # as good as Philadelphia's or D.C.'s: Vancouver WRAPS A SOLE PROPRIETOR'S
    # OWN NAME IN PARENTHESES - "(Christopher Colonia)", "(Qi Liu)". Step 2
    # uses it as the primary signal, unioned with the person-name regex, and
    # records the result in two columns of the processed file:
    # `registrant_name` and `name_suppressed`. Those are reported below
    # instead of an entity_type.
    #
    # So read this city's person-like-name percentage as a CROSS-CHECK of a
    # structural measure, the same way round as Philadelphia's.
    #
    # Its `sep` is ";" - see the read_csv note in check().
    # Montréal is the ONLY city here whose source is a field SURVEY rather
    # than a licence register, and it has the strongest privacy position of
    # the eleven. `NOM_ETAB` is the ESTABLISHMENT's name, populated on 100% of
    # rows, and the survey publishes no registrant, owner, agent or contact
    # column at all - so there is no fallback pair to join against and no pin
    # CAN be a person's name this pipeline substituted. Reported as
    # structurally absent, which is a stronger statement than a low count.
    #
    # The publisher did the privacy work upstream by surveying PREMISES rather
    # than licensees, which is the `read-licence` step-6b question answered in
    # the most favourable direction available.
    #
    # Its address is one free-text field (`ADRESSE`), so the unit check is a
    # regex over it as Miami's is - and SUITE, which the survey does carry, is
    # deliberately not joined in: a suite number in a shopping centre is
    # commercial, and 1,940 of these rows are in one.
    "montreal": dict(raw=None, trade=None, owner=None,
                     processed="businesses_clean.csv",
                     address=("address",)),
    # Calgary joins Montréal and Miami in the "structurally absent" group,
    # and for the cleanest reason yet: `tradename` is blank on ZERO of its
    # 23,203 rows and the register carries no second name column at all, so
    # there is no fallback pair to join against and no pin CAN be a
    # substituted name. `homeoccind` is `N` on every row, so the register also
    # asserts nothing about home occupation - what stands in for it is the
    # `(HOME BASED)` and `(MOBILE)` suffixes on individual categories, which
    # the taxonomy excludes.
    #
    # Its address is one free-text field, so the unit check is a regex over it
    # as Miami's and Montréal's are.
    "calgary": dict(raw=None, trade=None, owner=None,
                    processed="businesses_clean.csv",
                    address=("address",)),
    # Edmonton is the STRONGEST of the "structurally absent" group, and for a
    # reason none of the others have: the register publishes exactly ONE name
    # column and it is the business's. There is no registrant, owner or contact
    # field at all - so unlike Calgary (no blank tradenames) or Montreal (no
    # second name), there is not merely nothing to fall back ON, there is
    # nothing to fall back TO. No pin CAN be a person's name.
    #
    # Its own privacy work goes further than this project's: `<REDACTED FOR
    # PRIVACY>` replaces the address on 1,729 of the 25,105 Commercial rows,
    # and it takes the COORDINATES with it (redacted rows carrying coordinates:
    # zero), so those records cannot be mapped at all. `read-licence` step 6b.
    # Address is one free-text field, so the unit check is a regex over it as
    # Miami's, Montreal's and Calgary's are.
    "edmonton": dict(raw=None, trade=None, owner=None,
                     processed="businesses_clean.csv",
                     address=("address",)),
    # Toronto publishes THREE personal columns - `Client Name`, `Business
    # Phone` and `Business Phone Ext.` - and step 2 never reads any of them:
    # they are excluded at `usecols`, so they do not enter the process rather
    # than being dropped after. `Operating Name` is blank on 0.5% of storefront
    # rows and those rows are dropped rather than filled, so no pin can be a
    # registrant's name. Its processed file is the GEOCODED one, since the
    # register carries no coordinates.
    "toronto": dict(raw=None, trade=None, owner=None,
                    processed="businesses_geocoded.csv",
                    address=("address",)),
    "vancouver": dict(raw="vancouver_business_licences.csv", sep=";",
                      trade="businesstradename", owner="businessname",
                      processed="businesses_clean.csv",
                      address=("address",)),
    # Mexico City has the strongest structural position of any city here, and
    # it is the PUBLISHER's doing rather than this pipeline's. INEGI omits
    # `raz_social` entirely when the owner is a persona fisica - its own data
    # dictionary says "para proteger la confidencialidad de la informacion" -
    # and `nom_estab` is defined as the name on the shopfront, "visible y
    # escrito en rotulos, fachadas o anuncios luminosos", populated on 99.95%
    # of rows. So there is no registrant-name column to fall back to even in
    # principle, which is why raw/trade/owner are None: Los Angeles' failure
    # (68% blank dba_name -> ~4,000 individuals published at their premises)
    # has no mechanism here. Step 2 additionally forbids telefono, correoelec,
    # www and raz_social and asserts they never arrive.
    #
    # ADDRESS IS None AND THAT IS A MEASUREMENT GAP, NOT A PASS - recorded the
    # way San Diego's and Boston's gaps are. businesses_clean.csv carries no
    # address column because the map needs none, so the unit-indicator check
    # cannot run from here. DENUE does have `numero_int`, a STRUCTURED interior
    # number (better evidence than a regex over free text, per the
    # multi-source-city skill), and step 2 measures and prints its rate without
    # publishing the column - adding a unit number to the output to check for
    # unit numbers would be self-defeating.
    "mexico_city": dict(raw=None, trade=None, owner=None,
                        processed="businesses_clean.csv",
                        address=None),
    # Guadalajara is the same register as Mexico City, so the same structural
    # position applies unchanged: no registrant-name column is ever loaded,
    # INEGI withholds `raz_social` for a persona física, and `nom_estab` is the
    # shopfront sign. Address is None for the same reason - the clean CSV
    # carries none, and step 2 measures `numero_int` (7.1% here) without
    # publishing it. Read that as a measurement gap, not a pass.
    #
    # EXPECT A HIGH person-like READING AND DO NOT ACT ON IT. Mexico City's was
    # 32.2%, and a hand-sample of 26 found none that were a person presented as
    # a person - `looks_personal` is tuned for English "SMITH JOHN" forms and
    # misfires on the Spanish convention of trade type plus a given name
    # (ABARROTES LIZ, ESTETICA MARIFER), and even on two common nouns
    # (COCINA ECONOMICA).
    "guadalajara": dict(raw=None, trade=None, owner=None,
                        processed="businesses_clean.csv",
                        address=None),
}

# Unit designators that suggest a residence, as opposed to a commercial suite.
# Splitting these is why Los Angeles' jewellery district stopped reading as 42%
# "residential" (DECISIONS.md, 2026-09-21): STE in the Diamond District is an
# office, APT is someone's home.
#
# CORRECTED 2026-09-21. These lists contradicted their own source write-up,
# `docs/passover_name_filtering_skill.md`, on three designators, and the
# contradiction inflated every city's reported residential share:
#   FL / FLOOR and RM / ROOM were listed as RESIDENTIAL here and COMMERCIAL
#     there. "FL 3" and "RM 200" are an office floor and a room in a
#     commercial building; a dwelling is APT or UNIT. Moved to commercial.
#   SPC was listed as COMMERCIAL here and RESIDENTIAL there. A "space" is a
#     mobile-home or trailer space, which is a home. Moved to residential,
#     with SPACE and TRLR added alongside it.
# The source's list also includes a bare LOT as residential (a trailer lot).
# That is deliberately NOT adopted: in these registries "LOT" is at least as
# likely to appear in a parking-lot address, and it could not be verified
# either way, so adopting it would trade a known error for an unknown one.
# PH / BSMT / REAR / LOWR are kept as residential - secondary dwelling units,
# a refinement the source write-up predates rather than contradicts.
UNIT_RESIDENTIAL = re.compile(
    r"\b(APT|APARTMENT|UNIT|PH|BSMT|REAR|LOWR|SPC|SPACE|TRLR)\b")
UNIT_COMMERCIAL = re.compile(
    r"\b(STE|SUITE|BLDG|BUILDING|FRNT|LBBY|OFC|FL|FLOOR|RM|ROOM)\b")

# Tokens that make a name read as an organisation rather than a person. Kept
# broad on purpose: a false "organisation" only makes the report conservative.
ORG = re.compile(
    r"\b(INC|LLC|L\.?L\.?C|CORP|CORPORATION|CO|COMPANY|LTD|LP|LLP|PC|PLC|GROUP|"
    r"ENTERPRISE|ENTERPRISES|HOLDING|HOLDINGS|SERVICES|SERVICE|SALON|SHOP|STORE|"
    r"MARKET|CAFE|RESTAURANT|BAR|GRILL|PIZZA|LIQUOR|CLEANERS|CLEANER|BARBER|NAIL|"
    r"NAILS|SPA|STUDIO|BOUTIQUE|DELI|BAKERY|FOOD|FOODS|MART|CENTER|CENTRE|TRUST|"
    r"ASSOCIATION|ASSOC|PARTNERS|PARTNERSHIP|VENTURES|VENTURE|BROS|BROTHERS|THE|AND|"
    r"OF|DBA|USA|INTERNATIONAL|MANAGEMENT|PROPERTIES|REALTY|CONSTRUCTION|DESIGN|"
    r"SOLUTIONS|SYSTEMS|TECHNOLOGIES|CONSULTING|MEDICAL|DENTAL|CLINIC|CHURCH|SCHOOL|"
    r"ACADEMY|FOUNDATION|INSTITUTE|SUPPLY|WHOLESALE|RETAIL|AUTO|MOTORS|REPAIR|"
    r"PLUMBING|ELECTRIC|TRUCKING|TRANSPORT|LOGISTICS|BEAUTY|HAIR|SKIN|MASSAGE|"
    r"TATTOO|LAUNDRY|PET|DOG|KIDS|HOUSE|HOME|CITY|CLUB|LOUNGE|GIFTS)\b")
NOT_A_NAME = re.compile(r"[&/,\d\.]")
PERSON = re.compile(r"^[A-Z][A-Za-z'\-]{1,}(?:\s+[A-Z])?\s+[A-Z][A-Za-z'\-]{1,}$")
UNIT = re.compile(r"\b(APT|UNIT|STE|SUITE|SPC|#)\b")

# --- Contact details -------------------------------------------------------
# A different exposure from a name, and a worse one: a name at a commercial
# address identifies a business, while an email address or mobile number is a
# direct line to a person. Added 2026-09-21 after a repo grep - not this script
# - found a Gmail address published as a New York pin's business name. Neither
# test above could have caught it: an email fails PERSON and contains an "@",
# and NOT_A_NAME does not list "@", so it was reported as clean.
EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
# Conservative on purpose: a 10-digit run with separators, not any long number
# (a licence number or a street number must not match).
PHONE = re.compile(r"(?:\+?1[ .\-]?)?\(?\d{3}\)?[ .\-]\d{3}[ .\-]\d{4}")
# "C/O JOHN SMITH" names a person who is not the business. The separator is
# MANDATORY: an optional one (`C[/.]?O`) matches the bare abbreviation "CO" and
# flagged every "SAUSAGE CO" and "TYPEWRITER CO" in the project - 567 false
# positives across five cities before this was tightened.
CARE_OF = re.compile(r"\bC[/.]O\b|\bCARE\s+OF\b|\bATTN\b")

# "Andrew Polhemus (Molto Bene Ravioli Co)" - a registry that formats
# business_name as "LEGAL NAME (TRADE NAME)" publishes the licence holder's own
# name whenever the legal entity is an individual. PERSON cannot match it (the
# parenthesis and any digits fail NOT_A_NAME), so this form is invisible to
# every test above while displaying a person's name in full.
PERSON_THEN_TRADE = re.compile(
    r"^([A-Z][A-Za-z'\-]{1,}(?:\s+[A-Z]\.?)?\s+[A-Z][A-Za-z'\-]{1,})\s*\(")

# Registries record a licence holder surname-first, and NOT_A_NAME's comma rule
# treats that as evidence the string is NOT a person - backwards for exactly
# this form. Reported as its own number rather than folded into the PERSON
# count, so the older figures stay comparable across entries in DECISIONS.md.
PERSON_COMMA = re.compile(
    r"^[A-Z][A-Za-z'\-]{1,},\s*[A-Z][A-Za-z'\-]{1,}(?:\s+[A-Z]\.?)?$")


def mask_email(addr):
    local, _, domain = addr.partition("@")
    keep = local[:2] if len(local) > 2 else local[:1]
    return f"{keep}{'*' * max(len(local) - len(keep), 1)}@{domain}"


def mask_phone(num):
    digits = re.sub(r"\D", "", num)
    return f"***-***-{digits[-4:]}" if len(digits) >= 4 else "***"


def report_contact_details(rows, names):
    """Contact details and surname-first names in the DISPLAYED pin text.
    Prints masked values: the point is to find and count them, not reprint
    them."""
    emails, phones, commas, care_of = [], [], [], []
    for row, name in zip(rows, names):
        category = html.unescape(str(row[3])) if len(row) > 3 else ""
        for m in EMAIL.findall(name):
            emails.append((mask_email(m), category))
        # An email's digits must not also be counted as a phone number.
        stripped = EMAIL.sub("", name)
        for m in PHONE.findall(stripped):
            phones.append((mask_phone(m), category))
        if CARE_OF.search(name.upper()):
            care_of.append((name, category))
        if PERSON_COMMA.match(name) and not ORG.search(name.upper()):
            commas.append((name, category))

    print(f"  contact details in the displayed name: {len(emails)} email(s), "
          f"{len(phones)} phone number(s), {len(care_of)} 'c/o' marker(s)")
    for masked, cat in emails:
        print(f"    EMAIL {masked}  [{cat}]")
    for masked, cat in phones:
        print(f"    PHONE {masked}  [{cat}]")
    for name, cat in care_of[:5]:
        print(f"    C/O   {name!r}  [{cat}]")

    print(f"  surname-first names (\"Smith, John\"): {len(commas):,} "
          f"({100 * len(commas) / max(len(rows), 1):.1f}%)  "
          f"[NOT counted by the person-name heuristic - its comma rule "
          f"excludes them]")
    if commas:
        by_class = pd.Series([c for _, c in commas]).value_counts().head(5)
        print(f"    their top classifications: {by_class.to_dict()}")

    composite = []
    for row, name in zip(rows, names):
        m = PERSON_THEN_TRADE.match(name)
        if m and not ORG.search(m.group(1).upper()):
            composite.append((m.group(1), html.unescape(str(row[3]))
                              if len(row) > 3 else ""))
    print(f"  person's name followed by a trade name in brackets: "
          f"{len(composite):,} ({100 * len(composite) / max(len(rows), 1):.1f}%)"
          f"  [also invisible to the heuristic]")
    if composite:
        by_class = pd.Series([c for _, c in composite]).value_counts().head(5)
        print(f"    their top classifications: {by_class.to_dict()}")
    return len(emails) + len(phones), len(commas) + len(composite)


def pins(slug):
    """[lat, lon, name, classification, station, ring] for every pin in the map.

    row[3] IS AN INDEX INTO A PER-LAYER LOOKUP TABLE since 2026-09-22, not the
    classification string, because map_common indexes it to shrink the rendered
    file (Mexico City: 106 distinct values across 283,345 rows, ~7 MB inline).
    This resolves it back to the string so every caller below is unchanged.

    The pairing is positional: map_common emits the callback - and therefore
    `var CATEGORIES` - BEFORE its `var data`, once per category layer, so the
    Nth table belongs to the Nth data block. Verified against a rendered file
    rather than assumed.

    A bare string at row[3] is still accepted, so a map rendered before the
    change reads correctly instead of raising - which matters because these
    outputs are committed and are re-rendered city by city.
    """
    text = (ROOT / "outputs" / slug / "heatmap.html").read_text(encoding="utf-8")
    tables = [json.loads(t) for t in
              re.findall(r"var CATEGORIES = (\[.*?\]);", text, re.S)]
    blocks = re.findall(r"var data = (\[\[.*?\]\]);", text, re.S)
    if tables and len(tables) != len(blocks):
        raise SystemExit(
            f"{slug}: {len(tables)} CATEGORIES tables against {len(blocks)} "
            "data blocks - the positional pairing in pins() no longer holds. "
            "Do not guess; re-read how map_common.add_pin_layer emits them."
        )
    out = []
    for i, block in enumerate(blocks):
        table = tables[i] if i < len(tables) else None
        for r in json.loads(block):
            if table is not None and isinstance(r[3], int):
                r[3] = table[r[3]]
            out.append(r)
    return out


def looks_personal(name):
    upper = name.upper()
    return bool(PERSON.match(name)) and not ORG.search(upper) and not NOT_A_NAME.search(upper)


def check(slug):
    spec = REGISTRIES.get(slug)
    if spec is None:
        print(f"\n=== {slug}: NOT IN REGISTRIES - add its trade/owner columns to this script")
        return
    rows = pins(slug)
    names = [html.unescape(r[2]).strip() for r in rows]
    print(f"\n=== {slug}: {len(rows):,} pins, {len(set(names)):,} distinct names")

    if spec.get("name_is_address"):
        print("  ** THE DISPLAYED NAME IS THE STREET ADDRESS, NOT A BUSINESS "
              "NAME. **\n"
              "  This source publishes no name column of any kind, so every "
              "heuristic below\n"
              "  is being run over addresses and its output is not a privacy "
              "measurement.\n"
              "  Verified 2026-09-22: the person-like hits are Irish streets "
              "named after\n"
              "  people (Ashe Street, Thomas Street), the 'Surname, First' "
              "hits are floor\n"
              "  lists ('Basement, Ground & First floor'), and the "
              "'name (trade)' hits are\n"
              "  unit descriptors ('(Basement) 51 Henry Street'). READ THE "
              "NUMBERS BELOW AS\n"
              "  ZERO until a name column appears, which step 2 exits on.")

    if spec["raw"] is None:
        print("  no registrant-name fallback exists for this city: its step 2 "
              "never loads an owner/licence-holder column, so no pin can be "
              "one. Only registered trade names are displayed.")
        raw_path = None
    else:
        raw_path = ROOT / "data" / slug / "raw" / spec["raw"]
    if raw_path is not None and raw_path.exists():
        # `sep` per registry: Opendatasoft exports CSV SEMICOLON-delimited
        # (Vancouver), and read_csv's default comma parses such a file as one
        # single column, so every column lookup below would KeyError.
        raw = pd.read_csv(raw_path, dtype=str, low_memory=False,
                          sep=spec.get("sep", ","))
        trade = raw[spec["trade"]].fillna("").str.strip()
        owner = raw[spec["owner"]].fillna("").str.strip()
        fallback = set(owner[(trade == "") & (owner != "")].str.upper())
        trade_set = set(trade[trade != ""].str.upper())
        only_fb = [n for n in names if n.upper() in fallback and n.upper() not in trade_set]
        print(f"  blank trade name in raw: {int((trade == '').sum()):,} of {len(raw):,} "
              f"({100 * (trade == '').mean():.1f}%)")
        print(f"  pins that can ONLY be the {spec['owner']} fallback: {len(only_fb):,} "
              f"({100 * len(only_fb) / len(rows):.1f}%)")
    elif raw_path is not None:
        print(f"  raw file missing ({raw_path.name}); skipping the fallback join")

    report_contact_details(rows, names)

    personal = [(html.unescape(r[2]).strip(), html.unescape(str(r[3]))) for r in rows
                if looks_personal(html.unescape(r[2]).strip())]
    print(f"  pins whose name looks like a person: {len(personal):,} "
          f"({100 * len(personal) / len(rows):.1f}%)  [heuristic]")
    if personal:
        by_class = pd.Series([c for _, c in personal]).value_counts().head(5)
        print(f"  their top classifications: {by_class.to_dict()}")

    proc = ROOT / "data" / slug / "processed" / spec["processed"]

    # THE KOREAN PASS. The heuristic above reads Latin script only, so on a
    # Korean register its zero is not a finding (cjk-text section 5). A bare
    # Korean personal name is a surname and two syllables; the case that
    # matters is one at an address that reads residential. Shared with Seoul's
    # step 2, which withholds those names - so the residential count here
    # should be ZERO, and the withheld count is what step 2 caught.
    if spec.get("korean"):
        sys.path.insert(0, str(ROOT))
        from pipeline.korean_names import looks_like_personal_name, personal_name_at_home
        bare = [n for n in names if looks_like_personal_name(n)]
        print(f"  pins whose name is a bare Korean personal-name shape: {len(bare):,} "
              f"({100 * len(bare) / len(rows):.2f}%)  [Korean heuristic]")
        withheld = sum(n == spec["withheld"] for n in names)
        print(f"  pins whose name step 2 withheld: {withheld:,}")
        if proc.exists():
            d = pd.read_csv(proc, dtype=str, low_memory=False).fillna("")
            at_home = [personal_name_at_home(n, a) for n, a in zip(d.business_name, d.address)]
            print(f"    KOREAN PERSONAL NAME AT A RESIDENTIAL ADDRESS, still shown: "
                  f"{sum(at_home):,} of {len(d):,} rows (should be 0)")

    # THE TAIWAN PASS. The national tax register has no owner column, but for a
    # sole proprietor the registered NAME is often the owner's own, and the FIA
    # itself refuses to publish owners' names. The owner's rule (2026-09-23): a
    # name is shown only when it is a trade name (pipeline/countries/taiwan.py,
    # is_trade_name); otherwise the pin shows its industry. This tests the RULE
    # on what reached the map, not a name list - the count should be ZERO.
    if spec.get("taiwan") and proc.exists():
        sys.path.insert(0, str(ROOT))
        from pipeline.countries.taiwan import SOLE_PROPRIETOR, is_trade_name
        d = pd.read_csv(proc, dtype=str, low_memory=False).fillna("")
        sole = d.org.str.contains(SOLE_PROPRIETOR)
        shown = d.business_name != d.industry
        breach = [not is_trade_name(n, o) for n, o in zip(d.business_name[sole & shown],
                                                          d.org[sole & shown])]
        print(f"  sole proprietors: {int(sole.sum()):,} of {len(d):,} rows; name shown on "
              f"{int((sole & shown).sum()):,}, industry shown on {int((sole & ~shown).sum()):,}")
        print(f"    SOLE PROPRIETOR NAME SHOWN WITHOUT A BUSINESS MARKER: {sum(breach):,} "
              f"(should be 0)  [Taiwan rule]")

    # Where the registry records the entity type itself, report that first: it
    # is what the publisher asserts, not what a regex guesses.
    if spec.get("entity_type") and proc.exists():
        d = pd.read_csv(proc, dtype=str, low_memory=False)
        col, individual = spec["entity_type"], spec["entity_individual"]
        # A registry may spell one legal form several ways - D.C. has both
        # "Sole Proprietorship" and "Domestic Sole Proprietor" - so this
        # accepts a tuple as well as a single string.
        wanted = (individual,) if isinstance(individual, str) else tuple(individual)
        if col in d.columns:
            is_individual = d[col].fillna("").str.strip().isin(wanted)
            label = " / ".join(wanted)
            print(f"  {col}: {int(is_individual.sum()):,} of {len(d):,} mapped "
                  f"rows are {label!r} "
                  f"({100 * is_individual.mean():.1f}%)  [structural]")
            # The overlap is the population that actually matters: a row the
            # registry calls an individual AND whose displayed name reads as a
            # person's, rather than a trade name an individual registered.
            want = {n.upper() for n, _ in personal}
            named = d["business_name"].fillna("").str.strip().str.upper().isin(want)
            both = is_individual & named
            print(f"    {label} AND a person-like displayed name: "
                  f"{int(both.sum()):,} of {len(rows):,} pins "
                  f"({100 * int(both.sum()) / len(rows):.2f}%)")

    # A property register beats address text for "is this a home?": the unit
    # indicator below cannot see a detached house. Reported where a city's
    # step 2 carries the columns (Philadelphia joins the City's own parcel
    # data). See docs/data_sources.md and the add-city skill's Step 0.
    if proc.exists():
        d = pd.read_csv(proc, dtype=str, low_memory=False)
        if "parcel_landuse" in d.columns:
            occupied = d["parcel_owner_occupied"].astype(str).str.lower().eq("true")
            want = {n.upper() for n, _ in personal}
            named = d["business_name"].fillna("").str.strip().str.upper().isin(want)
            print(f"  parcel land use of mapped rows: "
                  f"{d['parcel_landuse'].value_counts(dropna=False).head(4).to_dict()}")
            print(f"    owner-occupied (homestead exemption): "
                  f"{int(occupied.sum()):,} of {len(d):,} "
                  f"({100 * occupied.mean():.1f}%)  [structural]")
            print(f"    person-like name AND owner-occupied parcel: "
                  f"{int((named & occupied).sum()):,}"
                  f"  - NOT filtered: most are mixed-use rowhouses where the "
                  f"owner lives above their own shop")

    if personal and spec["address"] and proc.exists():
        d = pd.read_csv(proc, dtype=str, low_memory=False)
        cols = [c for c in spec["address"] if c in d.columns]
        if cols and "business_name" in d.columns:
            addr = d[cols].fillna("").agg(" ".join, axis=1).str.upper()
            want = {n.upper() for n, _ in personal}
            hit = d["business_name"].fillna("").str.strip().str.upper().isin(want)
            if int(hit.sum()):
                unit_hits = addr[hit].map(lambda a: bool(UNIT.search(a)))
                print(f"  of {int(hit.sum()):,} matching processed rows, "
                      f"{int(unit_hits.sum()):,} ({100 * unit_hits.mean():.1f}%) have an "
                      "APT/UNIT/STE/# in the address (possible residence)")
                # Residential and commercial unit designators mean different
                # things; reported apart where the city carries a unit column.
                # Both are shares of the same base - the matching processed
                # rows - and NOT of the line above, whose regex is narrower
                # (it has no FL/RM/PH), so the residential count can exceed it.
                resid = addr[hit].map(lambda a: bool(UNIT_RESIDENTIAL.search(a)))
                comm = addr[hit].map(lambda a: bool(UNIT_COMMERCIAL.search(a)))
                print(f"    of the same {int(hit.sum()):,} rows: "
                      f"{int(resid.sum()):,} ({100 * resid.mean():.1f}%) at a "
                      f"residential unit (APT/UNIT/PH/SPC) and {int(comm.sum()):,} "
                      f"({100 * comm.mean():.1f}%) at a commercial one "
                      f"(STE/BLDG/FL/RM)")
                print(f"    PERSON-LIKE NAME AT A RESIDENTIAL UNIT: {int(resid.sum()):,} "
                      f"of {len(rows):,} pins ({100 * int(resid.sum()) / len(rows):.2f}%)")


def main():
    slugs = sys.argv[1:] or sorted(p.name for p in (ROOT / "outputs").iterdir() if p.is_dir())
    print("Personal-data exposure in the rendered maps (read-only).")
    print("A trade name is public commercial information; a registrant's name at a")
    print("flat number is not. Decide per city and record it in DECISIONS.md.")
    for slug in slugs:
        if (ROOT / "outputs" / slug / "heatmap.html").exists():
            check(slug)
        else:
            print(f"\n=== {slug}: no rendered map")


if __name__ == "__main__":
    main()
