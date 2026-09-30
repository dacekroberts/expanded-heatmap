# Palma — build brief

**Step 0 measured 2026-09-28 (wave 2) and 2026-09-29 (the Band C audit;
this brief).** Band B (owner, 2026-09-29): **food only**, reopened as
Glasgow's twin. Run `python scripts/brief_check.py palma` before writing
code.

| | |
|---|---|
| Rail | Metro de Palma **M1** (Plaça d'Espanya ↔ ParcBit, `#f1b03e`) and **M2** (Plaça d'Espanya ↔ Marratxí, `#e93324`), operator SFM: 18 stations in OSM, about 16 inside the municipality (M2's outer stops are in Marratxí). OSM tags both `light_rail` |
| Spacing | 583 m median gap → **standard rings 0.1 / 0.2 / 0.3 / 0.6 mi** |
| Storefronts | **4,372 active food premises** (`Estat = Alta`): bars 1,461, restaurants 1,446, bar-cafeterias 710, cafeterias 664, and the rest |
| Placed | **74.0%**: 581 carry the register's own coordinates (13.3%), and 2,655 are joined to Catastro's INSPIRE addresses |
| In the rings | **37.3%** within 0.6 mi, 15.8% within 0.3 mi |
| CRS | EPSG:25831 (ETRS89 / UTM 31N; Palma is 2.65° E) |
| Region | `"Europe"` |

## Business leg — the Consell de Mallorca's register

The *Registre d'Establiments de Restauració i Entreteniment de Mallorca*,
on the GOIB catalogue (CKAN `empreses-restauracio-entreteniment-mallorca`):
`https://intranet.caib.es/opendatacataleg/files/dataset/empreses_restauracio_mallorca/empreses_restauracio_mallorca.csv`.
Cached at `data/palma/raw/`: 10,607 rows island-wide, **4,375 with
`Municipi = PALMA`**, and the resource last modified 2026-09-07.

- **Active = `Estat == "Alta"`** (4,372; 3 are `Baixa temporal`).
- **Never load `Explotador/s`**: it names the operator, sometimes a person
  (with a tax id). Display `Denominació comercial`; run
  `check_personal_exposure.py`.
- **Bucket: food.** `Grup` gives the type. Night venues (discoteca, sala
  de festes, sala de ball: ~31) are a category-rules question
  (`docs/category_rules.md`).
- **The page states**: food only, and the placement share.

## Coordinates — the register's own, then Catastro

1. **Use `latitude`/`longitude` where present** (581).
2. **Join the rest to Catastro's INSPIRE Addresses for Palma**
   (`https://www.catastro.hacienda.gob.es/INSPIRE/Addresses/07/07040-PALMA/A.ES.SDGC.AD.07040.zip`,
   2.3 MB, 55,609 points in EPSG:25831, from the province-07 ATOM feed). The
   key is **street + number**. Parse `Direcció` as `<street>, <number>…`,
   then normalise both sides:
   - strip Catastro's type codes (`CL`, `CM`, `AV`, `PZ`, `PS`, …) and the
     register's long forms (`Carrer`, `Avinguda`, `Plaça`, …);
   - drop Catalan and Castilian particles (`DE`, `DEL`, `DELS`, `D'`, `L'`,
     `SA`, `ES`, `SES`, `I`, `CAN`…);
   - ASCII-fold.
3. **Fallback: the nearest listed number on the same side within 6**
   (Incheon's precedent) adds about 8 points.
4. **Unplaced (~26%)**: `S/N` (no number, 12.7% of rows without coordinates)
   and street names Catastro spells differently. Read the misses at build,
   the `address-join` skill's step 5.
- ⚠️ **Catastro's certificate chain fails with Python's bundled store**:
  use `truststore` (the OS store), never verification off.

## Licences

| Source | Status |
|---|---|
| The Consell de Mallorca register (GOIB catalogue) | **READ 2026-09-29: PERMITTED WITH CONDITIONS, two owner calls.** GOIB's *Política i termes d'ús*: CC BY (3.0 ES linked). **Display**: *"Font de les dades: Govern de les Illes Balears"*, plus the author (Consell de Mallorca, Direcció Insular de Transició i Ordenació Turística), the title, the licence link and the dataset URI; **the date of last update** (2026-09-07); and **a statement that the data were modified** (filtered, classified, joined). **Must not** imply GOIB or the Consell endorses the map. Projects are "urged" (not required) to tell GOIB |
| Catastro INSPIRE Addresses | **READ 2026-09-29: PERMITTED WITH CONDITIONS.** The current metadata (IDEE `ES_SDGC_AD`, 2025-01-28; the EU high-value-dataset record, 2026-05-21) declares **CC BY 4.0 DG Catastro**. The ATOM feed's rights ask that the Dirección General del Catastro (Ministerio de Hacienda) be named "as author and owner of the information". **Display**: that credit, "CC BY 4.0" with the link, a statement that the data were joined and modified, and the access date. **Must not** present the map as Catastro information or imply endorsement |
| OSM | ODbL, notice 1 |

### ✅ The three licence calls — ANSWERED 2026-09-29 (owner)

**A: Barcelona's reading extended** (the no-alteration clause bars misrepresentation, not analysis; the page identifies the transformation). **B: the indemnity accepted**, for this source, as Hong Kong's and Sacramento's were. **C: the permissive reading of Catastro's terms** (CC BY 4.0, the current declaration; a joined business map is transformed and the address layer is never published). The questions as put:

- **A. "Que el contingut de la informació no sigui alterat"** (Ley 37/2007
  art. 8 wording). **Barcelona's precedent** (owner, 2026-09-22) reads it as
  a bar on misrepresentation, not on analysis. The same page grants
  modification and requires modifications to be identified. Extend it to
  Palma?
- **B. An uncapped indemnity** covering "el mer ús" (Hong Kong's, CSDI's and
  Sacramento's shape, each accepted one source at a time). Accept it for
  this source?
- **C. Catastro's 2016 INSPIRE licence PDF**, still linked as "Licencia de
  Acceso y Uso", bars distributing "información original" untransformed, and
  asks the reuser to bear third-party claims. The newer CC BY 4.0
  declarations never say they replace it. **Permissive reading (lean)**: CC
  BY 4.0 is the dated, current declaration, which the EU high-value-dataset
  rules require. The address layer is never published, and a business map
  built by a join is transformed. **Restrictive reading**: each pin sits at
  Catastro's exact coordinate. Your call, with A and B.

```brief-checks
[
  {
    "id": "palma-register-csv",
    "claim": "The GOIB catalogue serves the Consell de Mallorca's restaurant register as a keyless CSV (about 2 MB, 10,607 rows island-wide)",
    "kind": "http_ok",
    "url": "https://intranet.caib.es/opendatacataleg/files/dataset/empreses_restauracio_mallorca/empreses_restauracio_mallorca.csv",
    "min_bytes": 1000000
  },
  {
    "id": "palma-catastro-atom",
    "claim": "Catastro's province-07 ATOM feed lists Palma's INSPIRE address file (07040)",
    "kind": "http_contains",
    "url": "https://www.catastro.hacienda.gob.es/INSPIRE/Addresses/07/ES.SDGC.AD.atom_07.xml",
    "present": ["07040-PALMA"]
  },
  {
    "id": "palma-metro-osm",
    "claim": "OSM carries Metro de Palma M1 and M2 as light_rail relations",
    "kind": "osm_route_refs",
    "bbox": [39.55, 2.60, 39.65, 2.72],
    "routes": ["light_rail"],
    "require_refs": {"light_rail": ["M1", "M2"]}
  },
  {
    "id": "palma-utm-31",
    "claim": "Palma (2.65 E) is in UTM zone 31N (ETRS89 twin EPSG:25831)",
    "kind": "utm_zone_from_longitude",
    "lon": 2.65,
    "expect": "EPSG:32631"
  }
]
```
