# São Paulo — build brief

**Step 0 measured 2026-09-23.** Run `python scripts/brief_check.py sao-paulo`
before writing any code. Brazil has never been built, so read the Brazil
section of `docs/global_country_shortlist.md` first — this brief carries the
city, that section carries the country.

---

## The one-line summary

**216,037 storefronts from the census's own walk of every block, with the
enumerator's coordinate on 98.5% of them — no register, no geocoder — and a
metro whose agency layer already separates what runs from what is planned.**

---

## Business leg — IBGE's CNEFE 2022, MEASURED

**Not CNPJ.** Receita Federal's CNPJ open data is geo-blocked outside Brazil
(16 check nodes: the Brazilian one 200, the other 15 reset) and this project
does not route around an access control. São Paulo's own portals hold no
business register: **483 CKAN packages** read by eye, **483 GeoSampa layers**
enumerated (`aprovacao-de-alvaras` is building permits, discontinued 2019).

| | |
|---|---|
| **File** | `Arquivos_CNEFE/CSV/Municipio/35_SP/3550308_SAO_PAULO.zip` on `ftp.ibge.gov.br` — **185,731,999 bytes**, last modified **2024-05-20** |
| Member | `3550308_SAO_PAULO.csv`, **UTF-8**, **`;`** — verified, not assumed |
| Establishment rows (`COD_ESPECIE = 6`) | **570,229** |
| `DSC_ESTABELECIMENTO` filled | **100.0%** (one blank) |
| **Mapped to the three buckets** | **216,037** — Retail **108,265** · Food service **66,467** · Personal services **41,305** |
| Recorded **vacant** by the enumerator | 32,653 (5.7%) — excluded, and a signal no register carries |
| Coordinate level 1 (*"coordenada original do Censo 2022"*) | **98.5%** of mapped rows |
| One establishment per row | **97.4%** of mapped rows |

### ⚠️ What a row IS

*"Cada registro representa uma espécie existente no endereço"* — **one row per
use-type per address, not one per business.** `COD_INDICADOR_ESTAB_ENDERECO`
says whether a row stands for 1, 2–10, more than 10, or an unknown number of
establishments. On mapped rows: 1 = 97.4%, 2 = 1.1%, 3 = 0.1%, 4 = 1.3%.
**A shopping centre collapses to one to a few rows** — decided 2026-09-23:
accept and disclose.

---

## Taxonomy — free text, classified by `scripts/screen_cnefe.py`

**This is a new shape for `premises-taxonomy`.** 261,417 distinct descriptions
cannot each get an explicit home, so the screen uses **ordered keyword rules
on the NAICS bucket boundaries every built city uses** — car washes, auto
repair, gyms and repair shops OUT; a **bakery is Retail** (Dublin / Vancouver /
Milan precedent) — plus two rules pinned by import-time checks:

- **The head noun wins** — the earliest match in the string decides, so
  `BAR DO CLUBE` is a bar and `SALAO DE FESTAS` is an events hall, not a salon.
- **Vacancy wins wherever it appears** — `LOJA FECHADA` is a closed shop.

An edit-distance pass rescued **8,188** misspelled rows (`RESTAUTANTE`,
`CABELEIRO`, `GARRAGEM`).

**Build it as ONE shared national module** under `pipeline/taxonomies/` (the
`france_naf.py` pattern), lifted from the screen's `RULES` — **never a
per-city copy**. It is shared code, so per `docs/session_roles.md` it belongs
to the app/chrome owner, or to staging when no third window exists.

### 🚨 The catch-all is 19.7%, and it is not evenly spread

| | Rows | Share |
|---|---|---|
| Unmatched — mostly bare trade names with no category word (`BURITI NATIVO`, `VIA VENEZA`, `ROLATEL`) | 105,475 | 18.5% |
| Generic catch-all (`COMERCIO`, `LOJA`, `BARRACA`) | 6,650 | 1.2% |

**There is no deeper level to key on** — the skill's remedy for a >5% share
does not exist here. The rows are **dropped, not assigned to Retail**, which
would be a guess wearing a number's clothes. **But the drop is not uniform**:
**13% in Lageado and 14% in Cidade Tiradentes, 31% in Pinheiros, 28% in
Moema.** Affluent commercial districts use brand names, so **the map
under-draws them**, and the page must say so. A better classifier reduces
this; nothing hides it.

---

## ✅ Coordinates — there is NO geocoding leg

`LATITUDE`/`LONGITUDE` on **100%** of rows, the enumerator's own point on
98.5% of mapped ones. ⚠️ The dictionary names no datum; IBGE's standard is
**SIRGAS 2000** (EPSG:4674), which sits within centimetres of WGS84 — ASSERTED,
harmless at ring scale. **Project to EPSG:32723 (UTM 23S) for distances.**

---

## 🔒 Privacy — DECIDED 2026-09-23, and a licence condition

At any address that **also holds a dwelling** (`COD_ESPECIE` 1 or 2 at the same
setor / quadra / face / street / number), **the tooltip shows the category,
never the description text.** Measured: **37.3%** of mapped rows share an
address with a dwelling (an upper bound — a shop under flats shares its
number), and **1.1%** carry a first name at one (`BAR DO PAULO`, `MERCEARIA
DA SONIA`). Structural rather than a name list, because a list misses names.
**LGPD applies by the licence's own terms**, so this is not house style.
`check_personal_exposure.py` needs a CNEFE entry: there is **no owner or
registrant column at all**, so Los Angeles' fallback failure cannot occur —
the only route is a name inside the description.

---

## Licence — free use by federal law, credit required

Decree 8.777/2016 art. 4 and Lei 14.129/2021 art. 29; **no IBGE document
licenses CNEFE.** Four restrictive readings recorded in `docs/data_sources.md`;
the owner decided to proceed on the law. **Notice:** `Fonte: IBGE, Cadastro
Nacional de Endereços para Fins Estatísticos (CNEFE), Censo Demográfico 2022.`
— add it to the numbered notices when this page ships.

---

## 🚇 Rail — GeoSampa WFS, the agency's own layers

| Layer | Features | |
|---|---|---|
| `geoportal:estacao_metro` | **94** station-line records, **85 distinct stations** | EPSG:31983, all `OPERANDO`, all `cd_tipo_transporte = 1` |
| `geoportal:linha_metro` | **6** lines | 1 Azul · 2 Verde · 3 Vermelha · 4 Amarela · 5 Lilás · **15 Prata** |
| `geoportal:estacao_trem` / `linha_trem` | 109 / 26 | **CPTM — `cd_tipo_transporte = 2`, commuter rail, EXCLUDED** by the standing rule |
| `geoportal:estacao_metro_projetada` | **142** | **Planned** — never request it |

**Interchanges** (on two lines): Sé, República, Paraíso, Ana Rosa, Chácara
Klabin, Vila Prudente, Vila Mariana, Luz, Santa Cruz. Collapse by name.

🚨 **OSM disagrees, and the agency is right to win.** OSM carries **subway refs
1–6 and monorail refs 15 and 17** — but GeoSampa has **Linha 6-Laranja (21
stations) and Linha 17-Ouro (18) only in the PLANNED layer.** OSM would draw
two lines GeoSampa does not list as operating — Tel Aviv's trap. **Verify both
lines' status at build time**; if either has opened since GeoSampa's last
edit, the agency layer is stale, not OSM right by default. OSM's box also
catches the **Aeromóvel GRU** people mover, which is in Guarulhos.

⚠️ **Line 15 is a MONORAIL** typed as metro. Draw it — Toulouse's cable car
is the precedent for a non-rail mode that is part of the network.
⚠️ **No colour field in GeoSampa.** Line names ARE colours (`AZUL`,
`VERMELHA`); OSM's relations carry hex colours on all 12 — use those, and say
which.

**Scope:** all six operating lines lie inside the município, so the commune
is the natural scope — Marseille's shape, not Dublin's.

---

## Region

**None exists.** `app/cities.py` raises on a city outside every leaf region,
so the first Brazilian city adds one — `"Brazil"`, or a South American region
if more countries follow. **Owner call at build**, measured with
`check_macro_labels.py`.

## What the page must say

1. The IBGE source notice above.
2. **The data are 2022 census fieldwork**, not current.
3. **The categories are this project's reading of free text** — IBGE did not
   classify establishments, and names were not checked against any register.
4. **About a fifth of establishments could not be classified and are not
   drawn — more in affluent commercial districts**, which are under-drawn.
5. **Shopping centres appear as a single point.**
6. At addresses that also hold a home, only the category is shown.

## Still unknown

- 🚨 **GeoSampa's licence — READ 2026-09-23 and AMBIGUOUS; owner decision.**
  The portal shows CC BY-SA 4.0, but its own text limits that to data
  *"produzidos pelos órgãos da Prefeitura"*, and these layers' metadata names
  the **State's Metrô company** as author. If it does apply, share-alike
  reaches the derived geometry. Full record in `docs/data_sources.md`. **The
  alternative that sidesteps it:** draw lines from OSM (Mexico City's and
  Barcelona's route) and use GeoSampa only to decide WHICH lines operate — a
  fact, not its geometry.
- ⚠️ **Lines 6 and 17** — operating or not, at build time.
- ⚠️ **Neighbourhood bias** — measured by locality; not yet by distance from a
  station, which is what the map actually shows.
- ⚠️ **CPTM exclusion** — standing rule, but Lines 8 and 9 run at metro
  frequencies. Not re-litigated here; noted.

```brief-checks
[
  {
    "id": "sp-cnefe-file-live",
    "claim": "The CNEFE 2022 file for Sao Paulo (3550308) is keyless and live - 185,731,999 bytes, a zip. It is BOTH the business leg and the coordinate leg",
    "kind": "http_ok",
    "url": "https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/35_SP/3550308_SAO_PAULO.zip",
    "min_bytes": 1000000,
    "content_type_contains": "zip"
  },
  {
    "id": "sp-cnefe-not-re-released",
    "claim": "Every figure in this brief was measured on the file dated 2024-05-20. When this FAILS, IBGE has re-released it: re-run scripts/screen_cnefe.py before trusting any number here",
    "kind": "http_contains",
    "url": "https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/35_SP/",
    "present": ["3550308_SAO_PAULO.zip", "2024-05-20 19:54"]
  },
  {
    "id": "cnpj-still-geo-blocked",
    "claim": "Receita's CNPJ share refuses connections from outside Brazil, which is why this brief uses CNEFE. When this FAILS, the share answers from here: CNPJ becomes a possible cross-check, and its terms still need reading",
    "kind": "endpoint_absent",
    "url": "https://arquivos.receitafederal.gov.br/index.php/s/YggdBLfdninEJX9"
  },
  {
    "id": "geosampa-metro-layers-and-planned-layer-separate",
    "claim": "GeoSampa serves operating metro stations and lines as layers SEPARATE from planned ones, so a build that never requests *_projetada cannot draw an unbuilt line",
    "kind": "http_contains",
    "url": "https://wfs.geosampa.prefeitura.sp.gov.br/geoserver/ows?service=WFS&version=2.0.0&request=GetCapabilities",
    "present": ["geoportal:estacao_metro", "geoportal:linha_metro", "geoportal:estacao_metro_projetada"]
  },
  {
    "id": "geosampa-lines-6-and-17-not-operating",
    "claim": "Linha 6-Laranja and Linha 17-Ouro are NOT in the operating station layer, though OSM carries both as routes. When this FAILS, one has opened: add it deliberately",
    "kind": "http_contains",
    "url": "https://wfs.geosampa.prefeitura.sp.gov.br/geoserver/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=geoportal:estacao_metro&outputFormat=application/json&propertyName=nm_linha_metro_trem",
    "present": ["PRATA", "LILAS", "AZUL"],
    "absent": ["LARANJA", "OURO"]
  },
  {
    "id": "sp-projected-crs",
    "claim": "Sao Paulo projects to UTM 23S; GeoSampa's EPSG:31983 is SIRGAS 2000 / UTM 23S, the same zone",
    "kind": "utm_zone_from_longitude",
    "lon": -46.63,
    "north": false,
    "expect": "EPSG:32723"
  }
]
```
