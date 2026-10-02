# Data sources — Brazil

<!-- internal -->The Brazil part of the project's provenance record,
[`data_sources.md`](../data_sources.md), split out by country on 2026-09-27.
The numbered notices this project must display, the removal-request
commitment and the deploy gate apply to every country and are kept in
that record.<!-- /internal -->

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| São Paulo | **IBGE CNEFE 2022** - the census's walk of every block: one row per use-type per address, the enumerator's description of each establishment (`DSC_ESTABELECIMENTO`) and point; classified by this project's rules (free text, rules version 2) | All three categories: **219,578** storefronts placed; unreadable descriptions dropped, never guessed; at an address that also holds a dwelling the pin shows its category only | `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/35_SP/3550308_SAO_PAULO.zip` | none - the whole município file; `COD_ESPECIE` 6 read, 1-2 for the dwelling test, coordinate levels 1-4 kept | 2026-09-24 |
| Rio de Janeiro | **IBGE CNEFE 2022** - the census's walk of every block: one row per use-type per address, the enumerator's description of each establishment (`DSC_ESTABELECIMENTO`) and point; classified by this project's rules (free text, rules version 2) | All three categories: **106,652** storefronts placed; unreadable descriptions dropped, never guessed; at an address that also holds a dwelling the pin shows its category only | `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/33_RJ/3304557_RIO_DE_JANEIRO.zip` (94,594,981 bytes) | none - the whole município file; `COD_ESPECIE` 6 read, 1-2 for the dwelling test, coordinate levels 1-4 kept | 2026-09-24 |
| Belo Horizonte | **IBGE CNEFE 2022** - the census's walk of every block: one row per use-type per address, the enumerator's description of each establishment (`DSC_ESTABELECIMENTO`) and point; classified by this project's rules (free text, rules version 2) | All three categories: **45,582** storefronts placed; unreadable descriptions dropped, never guessed; at an address that also holds a dwelling the pin shows its category only | `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/31_MG/3106200_BELO_HORIZONTE.zip` (34,957,820 bytes) | none - the whole município file; `COD_ESPECIE` 6 read, 1-2 for the dwelling test, coordinate levels 1-4 kept | 2026-09-24 |
| Brasília | **IBGE CNEFE 2022** - the census's walk of every block: one row per use-type per address, the enumerator's description of each establishment (`DSC_ESTABELECIMENTO`) and point; classified by this project's rules (free text, rules version 2) | All three categories: **36,687** storefronts placed; unreadable descriptions dropped, never guessed; at an address that also holds a dwelling the pin shows its category only | `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/53_DF/5300108_BRASILIA.zip` (19,814,371 bytes) | none - the whole município file; `COD_ESPECIE` 6 read, 1-2 for the dwelling test, coordinate levels 1-4 kept | 2026-09-24 |
| Salvador | **IBGE CNEFE 2022** - the census's walk of every block: one row per use-type per address, the enumerator's description of each establishment (`DSC_ESTABELECIMENTO`) and point; classified by this project's rules (free text, rules version 2) | All three categories: **53,045** storefronts placed; unreadable descriptions dropped, never guessed; at an address that also holds a dwelling the pin shows its category only | `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/29_BA/2927408_SALVADOR.zip` (52,084,744 bytes) | none - the whole município file; `COD_ESPECIE` 6 read, 1-2 for the dwelling test, coordinate levels 1-4 kept | 2026-09-24 |
| Fortaleza (Regional) | **IBGE CNEFE 2022** - the census's walk of every block: one row per use-type per address, the enumerator's description of each establishment (`DSC_ESTABELECIMENTO`) and point; classified by this project's rules (free text, rules version 2) | All three categories: **62,969** storefronts placed; unreadable descriptions dropped, never guessed; at an address that also holds a dwelling the pin shows its category only | `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/23_CE/2304400_FORTALEZA.zip` (28,907,115 bytes); `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/23_CE/2303709_CAUCAIA.zip` (3,875,954 bytes); `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/23_CE/2307650_MARACANAU.zip` (2,340,410 bytes); `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/23_CE/2309706_PACATUBA.zip` (710,306 bytes) | none - the whole município file; `COD_ESPECIE` 6 read, 1-2 for the dwelling test, coordinate levels 1-4 kept | 2026-09-24 |
| Porto Alegre (Regional) | **IBGE CNEFE 2022** - the census's walk of every block: one row per use-type per address, the enumerator's description of each establishment (`DSC_ESTABELECIMENTO`) and point; classified by this project's rules (free text, rules version 2) | All three categories: **36,480** storefronts placed; unreadable descriptions dropped, never guessed; at an address that also holds a dwelling the pin shows its category only | `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/43_RS/4314902_PORTO_ALEGRE.zip` (17,172,345 bytes); `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/43_RS/4304606_CANOAS.zip` (3,546,253 bytes); `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/43_RS/4307708_ESTEIO.zip` (744,631 bytes); `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/43_RS/4320008_SAPUCAIA_DO_SUL.zip` (1,370,445 bytes); `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/43_RS/4318705_SAO_LEOPOLDO.zip` (2,436,268 bytes); `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/43_RS/4313409_NOVO_HAMBURGO.zip` (2,739,559 bytes) | none - the whole município file; `COD_ESPECIE` 6 read, 1-2 for the dwelling test, coordinate levels 1-4 kept | 2026-09-24 |
| Recife (Regional) | **IBGE CNEFE 2022** - the census's walk of every block: one row per use-type per address, the enumerator's description of each establishment (`DSC_ESTABELECIMENTO`) and point; classified by this project's rules (free text, rules version 2) | All three categories: **44,382** storefronts placed; unreadable descriptions dropped, never guessed; at an address that also holds a dwelling the pin shows its category only | `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/26_PE/2611606_RECIFE.zip` (17,729,524 bytes); `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/26_PE/2607901_JABOATAO_DOS_GUARARAPES.zip` (7,528,738 bytes); `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/26_PE/2602902_CABO_DE_SANTO_AGOSTINHO.zip` (2,470,937 bytes); `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/26_PE/2603454_CAMARAGIBE.zip` (1,592,566 bytes) | none - the whole município file; `COD_ESPECIE` 6 read, 1-2 for the dwelling test, coordinate levels 1-4 kept | 2026-09-24 |
| Santos (Regional) | **IBGE CNEFE 2022** - the census's walk of every block: one row per use-type per address, the enumerator's description of each establishment (`DSC_ESTABELECIMENTO`) and point; classified by this project's rules (free text, rules version 2) | All three categories: **11,813** storefronts placed; unreadable descriptions dropped, never guessed; at an address that also holds a dwelling the pin shows its category only | `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/35_SP/3548500_SANTOS.zip` (3,948,134 bytes); `https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/35_SP/3551009_SAO_VICENTE.zip` (3,189,142 bytes) | none - the whole município file; `COD_ESPECIE` 6 read, 1-2 for the dwelling test, coordinate levels 1-4 kept | 2026-09-24 |

## Transit feeds

### Rail geometry that is not a GTFS feed

| City | System / operator | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| São Paulo | **OpenStreetMap** - Metrô Linhas 1-5 (subway) and 15 (monorail), and CPTM Linha 9 (train; the rail test, owner 2026-09-24); **GeoSampa** `geoportal:estacao_metro` and `geoportal:estacao_trem` for STATUS and the gate-3 count only (the owner's 2026-09-23 rule), never drawn | every subway and monorail route relation, and separately every train relation, in the bbox, `out geom; node(r); out tags center;`; `https://wfs.geosampa.prefeitura.sp.gov.br/geoserver/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=geoportal:estacao_metro&outputFormat=application/json` and `https://wfs.geosampa.prefeitura.sp.gov.br/geoserver/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=geoportal:estacao_trem&outputFormat=application/json` | 2026-09-24 | Gate 3 exact on all eight counts (GeoSampa is stale by Jardim Colonial, recorded). CPTM Lines 7, 8 and 10-13 fail the rail test on spacing. OpenStreetMap, ODbL 1.0 - notice 1 |
| Rio de Janeiro | **IPP / DATA.RIO** (Prefeitura do Rio) - MetrôRio stations (layer 19, per-line flags) and lines (layer 18), **CC BY 4.0, a notice REQUIRED**; **OpenStreetMap** - the VLT Carioca's four lines and SuperVia Deodoro and Saracuruna (the rail test) | `https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Transporte_Trafego/Transporte_publico/MapServer/19/query?where=1%3D1&outFields=*&outSR=4326&f=geojson` and `.../MapServer/18/query?...`; OSM: every rail route relation in the bbox | 2026-09-24 | The agency's VLT layer (9) is NOT used: its line flags give 20/14/11/14 where pt.wikipedia lists 16/11/10/11 and OSM agrees. Gate 3: metro 20/26/6 and 41, VLT 30, Deodoro 19. The SIURB terms' liability clause accepted by the owner 2026-09-23 |
| Belo Horizonte | **OpenStreetMap** - Metrô BH Linha 1 and Linha 2 (opened 2026-07-03, peak hours; drawn, owner) | every rail route relation in the bbox | 2026-09-24 | Gate 3 against pt.wikipedia's text (22 in operation); its table is stale by Nova Suíça. The Vitória-Minas passenger train (intercity) left out. OpenStreetMap, ODbL 1.0 - notice 1 |
| Brasília | **OpenStreetMap** - Metrô-DF Linha Verde and Linha Laranja; **IPEDF** `geonode:ESTACOES_METRO` (public domain) read for status only | every rail route relation in the bbox; `https://catalogo.ipe.df.gov.br/geoserver/geonode/wfs?service=WFS&version=2.0.0&request=GetFeature&outputFormat=application/json&srsName=EPSG:4326&typeNames=geonode:ESTACOES_METRO` | 2026-09-24 | Gate 3 against pt.wikipedia's 27; the IPEDF layer (2023) is stale by 106 Sul, 110 Sul and Estrada Parque (opened 2020). OpenStreetMap, ODbL 1.0 - notice 1 |
| Salvador | **OpenStreetMap** - Metrô de Salvador Linha 1 and Linha 2 (CCR Metrô Bahia) | every rail route relation in the bbox | 2026-09-24 | OSM carries no colors; the operator's line NAMES (Vermelha, Azul) resolved through the CSS table. Aeroporto station is in Lauro de Freitas - excluded. OpenStreetMap, ODbL 1.0 - notice 1 |
| Fortaleza (Regional) | **OpenStreetMap** - Metrofor Linha Sul | every rail route relation in the bbox | 2026-09-24 | The diesel lines through the rail test: Linha Oeste and the Aeroporto branch fail; the Parangaba-Mucuripe VLT is borderline and out (owner, 2026-09-24). Metrofor's GTFS host has an expired certificate - not bypassed. OpenStreetMap, ODbL 1.0 - notice 1 |
| Porto Alegre (Regional) | **OpenStreetMap** - Trensurb Linha 1 | every rail route relation in the bbox | 2026-09-24 | The Aeromóvel airport connector not drawn (owner). OpenStreetMap, ODbL 1.0 - notice 1 |
| Recife (Regional) | **OpenStreetMap** - Metrô do Recife Linha Centro (both branches) and Linha Sul | every rail route relation in the bbox | 2026-09-24 | The diesel VLTs fail the rail test on spacing. The city's ODbL station file is a cross-check only, never read by a step. OpenStreetMap, ODbL 1.0 - notice 1 |
| Santos (Regional) | **OpenStreetMap** - VLT da Baixada Santista L1 and L2 (L2 in assisted operation since 2025-12-01) | every rail route relation in the bbox | 2026-09-24 | Three L2 stops named from their wikidata labels; the Bonde Turístico excluded; EMTU's CPGSTM layers a cross-check only. OpenStreetMap, ODbL 1.0 - notice 1 |

## Boundary layers

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| São Paulo | **OpenStreetMap** admin_level-8 relations carrying `IBGE:GEOCODIGO` in the bbox (-23.8, -46.83, -23.36, -46.36), polygonised from outer and inner ways, area-gated | The three Overpass mirrors in `pipeline/osm.py` | IBGE 3550308; the rest name excluded stations only. OpenStreetMap, ODbL 1.0 - notice 1 |
| Rio de Janeiro | **OpenStreetMap** admin_level-8 relations carrying `IBGE:GEOCODIGO` in the bbox (-23.08, -43.8, -22.75, -43.1), polygonised from outer and inner ways, area-gated | The three Overpass mirrors in `pipeline/osm.py` | IBGE 3304557; the rest name excluded stations only. OpenStreetMap, ODbL 1.0 - notice 1 |
| Belo Horizonte | **OpenStreetMap** admin_level-8 relations carrying `IBGE:GEOCODIGO` in the bbox (-20.1, -44.15, -19.75, -43.8), polygonised from outer and inner ways, area-gated | The three Overpass mirrors in `pipeline/osm.py` | IBGE 3106200; the rest name excluded stations only. OpenStreetMap, ODbL 1.0 - notice 1 |
| Brasília | **OpenStreetMap** admin_level-8 relations carrying `IBGE:GEOCODIGO` in the bbox (-16.06, -48.3, -15.49, -47.3), polygonised from outer and inner ways, area-gated | The three Overpass mirrors in `pipeline/osm.py` | IBGE 5300108 (the whole Federal District; OSM maps it as 35 administrative regions coded 5300108xxxx, assembled); the rest name excluded stations only. OpenStreetMap, ODbL 1.0 - notice 1 |
| Salvador | **OpenStreetMap** admin_level-8 relations carrying `IBGE:GEOCODIGO` in the bbox (-13.05, -38.6, -12.7, -38.25), polygonised from outer and inner ways, area-gated | The three Overpass mirrors in `pipeline/osm.py` | IBGE 2927408; the rest name excluded stations only. OpenStreetMap, ODbL 1.0 - notice 1 |
| Fortaleza (Regional) | **OpenStreetMap** admin_level-8 relations carrying `IBGE:GEOCODIGO` in the bbox (-4.05, -38.8, -3.68, -38.4), polygonised from outer and inner ways, area-gated | The three Overpass mirrors in `pipeline/osm.py` | IBGE 2304400, 2303709, 2307650, 2309706 (the owner's regional scope, 2026-09-23); the rest name excluded stations only. OpenStreetMap, ODbL 1.0 - notice 1 |
| Porto Alegre (Regional) | **OpenStreetMap** admin_level-8 relations carrying `IBGE:GEOCODIGO` in the bbox (-30.3, -51.35, -29.6, -50.95), polygonised from outer and inner ways, area-gated | The three Overpass mirrors in `pipeline/osm.py` | IBGE 4314902, 4304606, 4307708, 4320008, 4318705, 4313409 (the owner's regional scope, 2026-09-23); the rest name excluded stations only. OpenStreetMap, ODbL 1.0 - notice 1 |
| Recife (Regional) | **OpenStreetMap** admin_level-8 relations carrying `IBGE:GEOCODIGO` in the bbox (-8.4, -35.15, -7.92, -34.83), polygonised from outer and inner ways, area-gated | The three Overpass mirrors in `pipeline/osm.py` | IBGE 2611606, 2607901, 2602902, 2603454 (the owner's regional scope, 2026-09-23); the rest name excluded stations only. OpenStreetMap, ODbL 1.0 - notice 1 |
| Santos (Regional) | **OpenStreetMap** admin_level-8 relations carrying `IBGE:GEOCODIGO` in the bbox (-24.05, -46.6, -23.85, -46.2), polygonised from outer and inner ways, area-gated | The three Overpass mirrors in `pipeline/osm.py` | IBGE 3548500, 3551009 (the owner's regional scope, 2026-09-23); the rest name excluded stations only. OpenStreetMap, ODbL 1.0 - notice 1 |

## Licenses and terms of use

### Explicit and permissive — confirmed

| Source | License | Attribution declared |
|---|---|---|
| **Brazil — IBGE CNEFE 2022** (**built 2026-09-24**: nine cities, one national module) | **Free use by federal law** — Decree 8.777/2016 art. 4 and Lei 14.129/2021 art. 29 — subject to LGPD principles. **No IBGE license document exists.** Read 2026-09-23; four restrictive readings recorded in the Brazil section below | **Required** (the decree's definition of open data: *"limitando-se a creditar a autoria ou a fonte"*). No wording prescribed; use `Fonte: IBGE, Cadastro Nacional de Endereços para Fins Estatísticos (CNEFE), Censo Demográfico 2022.` |

### 🇧🇷 Brazil — IBGE's CNEFE 2022 (built 2026-09-24): the grant is a LAW, not a document

**Source:** *Cadastro Nacional de Endereços para Fins Estatísticos*, Censo
Demográfico 2022 — one CSV per município, keyless, at
`ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/`.
Every address in the country with a field-collected coordinate; rows with
`COD_ESPECIE = 6` carry `DSC_ESTABELECIMENTO`, the enumerator's
identification of the establishment. **It is Brazil's business leg AND its
coordinate leg** — no CNPJ, no geocoder. Read 2026-09-23 by the project's license
reader; its full working was not kept in the repository.

**PERMITTED WITH CONDITIONS — and no IBGE document grants it.** No license
exists anywhere machine-readable: the FTP is a bare listing, the zips hold
only the CSV, the dictionary is silent, and CNEFE is **not on dados.gov.br**.
The grant is federal law that binds IBGE as a public foundation:

- **Decree 8.777/2016, art. 4** (as reworded by Decree 9.903/2019): *"Os
  dados disponibilizados pelo Poder Executivo federal e as informações de
  transparência ativa são de livre utilização pelos Poderes Públicos e pela
  sociedade."*
- **Lei 14.129/2021, art. 29**: *"...são de livre utilização pela sociedade,
  observados os princípios dispostos no art. 6º da Lei nº 13.709 [LGPD]."*
- The FTP's own line: *"Todos os arquivos aqui disponíveis são públicos."*
  — a statement that they are public, not a license.

**Two conditions, neither of them an act owed to IBGE:**

1. **Credit the source.** No wording is prescribed. Use IBGE's own form:
   **`Fonte: IBGE, Cadastro Nacional de Endereços para Fins Estatísticos
   (CNEFE), Censo Demográfico 2022.`** It is displayed as notice 38 (Brazil).
2. **LGPD principles for any personal data published** (art. 29's proviso;
   LGPD art. 7 §3 — *finalidade, boa-fé e interesse público*). **This makes
   the privacy rule below a license condition, not house style.**

**Four restrictive readings were found and NOT resolved in this project's
favor by the reader. The owner decided on 2026-09-23 to proceed on the law**,
on a recorded reasoned position — the Philadelphia shape:

| | Reading | Why the project proceeds |
|---|---|---|
| **A** | A **2009 IBGE service-desk email**, surviving only in an OSM mailing-list archive: its dissemination policy *"não contempla a modalidade de disponibilizar o produto do seu trabalho em sites de terceiros"* | Informal, unpublished, about mirroring maps and orthophotos, and **predates both the 2016 decree and the 2021 law**. A second reply in the same thread allowed reuse with citation |
| **B** | The decree's **copyright waiver** (art. 4 §1) covers databases whose rights belong to **the União**; IBGE is a foundation and its PDFs say "© IBGE" | The **caput** and **Lei 14.129 art. 29** grant free use regardless; the CSVs carry no © notice |
| **C** | **Lei 5.534/1968**: informants' data are secret and *"usadas exclusivamente para fins estatísticos"* | The duty is **IBGE's**, and IBGE discharged it: its methodological note (Notas metodológicas n. 04) says establishment names were **published deliberately**, and its secrecy review withholds what identifies informants |
| **D** | CNEFE is **not in IBGE's open-data plan** and not on dados.gov.br | Art. 4 speaks of data *"disponibilizados"*, not only catalogued datasets |

**What may not be SAID** (from IBGE's own documentation, not its terms):
the names were **not checked against any register or standardized**, so never
present them as verified business names; **IBGE did not classify the
establishments** — the three categories are this project's reading of free text;
and **the data are not current** — they are the 2022 census fieldwork.

**Privacy rule, decided 2026-09-23:** at any address that also holds a
dwelling (`COD_ESPECIE` 1 or 2 at the same address), the tooltip shows the
**category, never the description text**. Structural rather than a name list.
Measured before deciding: a first name at a dwelling address is **2.1%** of
Rio's mapped rows and **1.1%** of São Paulo's; the structural rule reaches
**55.4%** and **37.3%**, which is the price of not trusting a name list —
and like Milan, where ~82% of pins carry no trade name, fewer published names
is a privacy asset rather than a loss.

#### Brazil's rail sources<!-- internal -->, read 2026-09-23 by the `licence-read` agent<!-- /internal -->

| Source | Verdict | What it requires |
|---|---|---|
| **Rio de Janeiro** — `pgeo3.rio.rj.gov.br/.../Transporte_Trafego/Transporte_publico/MapServer` layers 19, 18, 9, 10 (metro stations and lines, VLT stops and lines) | **PERMITTED WITH CONDITIONS — CC BY 4.0**, declared at SERVICE level (`info/iteminfo`: *"This work is licensed under a Creative Commons Attribution 4.0 International License"*) and on all four Data.Rio items | Credit **"Prefeitura da Cidade do Rio de Janeiro / Instituto Pereira Passos (IPP)"**, the license link, a link to the data, and **a statement that the data was modified** (CC BY §3(a)(1)(B) — required, not optional). Operator names and colors (MetrôRio, VLT Carioca) come from elsewhere and are **not licensed** by it |
| **São Paulo** — GeoSampa WFS `estacao_metro`, `linha_metro` | ⚠️ **AMBIGUOUS IN A WAY THAT MATTERS — owner decision** | See below |

**Rio: the "sem alteração" clause does NOT apply.** Data.Rio's *"Uso público,
citadas as fontes e sem alteração das informações originais"* is set **item by
item** — 2,727 of the PrefeituraRio account's 5,069 items, 2,671 of them PDFs,
2,722 last changed in 2018 — and is **absent from all four rail items, the
service record and its metadata.** Any OTHER Data.Rio source needs its own
check; the portal is split roughly in half.

**Rio: one clause RAISED, not resolved.** The IPP's *Termo de Uso do SIURB.RIO*
(v3.0, Aug 2025) governs the system that owns the server: §1 *"Ao utilizar o
Sistema, o usuário ... estará legalmente vinculado"*, and §6 iv makes the user
liable for *"todos e quaisquer danos, diretos ou indiretos"* caused to the
Administration or third parties. **Reading that binds:** fetching from the
server is using the System. **Reading that does not:** the Termo defines users
as *"pessoas naturais que utilizarem o Sistema por meio de login de acesso"*.
Even if it binds, it prohibits nothing the build does — it is **fault-based
liability for damage caused**, narrower than Hong Kong's indemnity, closer to
IBGE's portal clause. **Owner call — ✅ ACCEPTED 2026-09-23**: Rio's rail
comes from these layers, with OSM as the color source and cross-check.

**São Paulo: the license may not reach the layers.** GeoSampa declares
**CC BY-SA 4.0** on these layers, but its own *Créditos › Licença dos dados*
says: *"A licença CC BY-SA exibida no mapa aplica-se exclusivamente aos dados
geoespaciais das camadas, produzidos pelos órgãos da Prefeitura de São
Paulo."*

- **Reading A — covered:** the ISO lineage says the geometry is the
  Prefeitura's own photogrammetry (*"localizados por meio do Mapeamento Digital
  da Cidade de São Paulo - MDC"*); the portal attaches *"© Produzido por
  SMUL-PMSP-PRODAM - CC-BY-SA"* to exactly these layers; Lei 16.051/2014 art. 1
  §1 makes published Prefeitura data *"livremente utilizados, reutilizados e
  redistribuídos"*, including *"mapas"*.
- **Reading B — not covered:** both ISO records name the author as the **State's
  Companhia do Metropolitano (METRÔ)**; `sg_fonte_original = METRO` on all 94
  stations; the portal's attribution string is a blanket default on all 502
  layers; a municipal law cannot license a State company's work; Metrô's own
  portal says *"License Not Specified"*.
- **And if CC BY-SA applies, SHARE-ALIKE reaches the derived geometry**
  (§3(b)) — the repository is MIT. Narrow reading: only the station, line and
  ring geometry must be offered under CC BY-SA; broad: the rendered São Paulo
  map is Adapted Material.

**Not resolved in this project's favor.** The one party who can settle A
against B is `geosampa@prefeitura.sp.gov.br`.

✅ **DECIDED 2026-09-23 by the owner — the question is AVOIDED, not answered:
São Paulo's line and station geometry comes from OpenStreetMap**, as Mexico
City's and Barcelona's do, and **GeoSampa is used only to decide WHICH lines
operate** — a fact read from it, not a reproduction of its geometry. That also
keeps OSM's unbuilt Lines 6 and 17 off the map. OSM's terms are already
settled by precedent: under ODbL §4.5(b) the rendered map is a Produced Work,
so share-alike does not reach it; the committed station file carries an ODbL
notice and the linked public repository offers the method (§4.6) — the
Toulouse/Rennes discharge, `docs/licenses/odbl-toulouse-rennes.md`. **Why the
precedent does not simply carry over to GeoSampa:** CC BY-SA 4.0 has no
Produced Work carve-out, so its share-alike question stays open and is now
not this project's to answer. If São Paulo's build ever wants GeoSampa's
geometry, the email above comes first.

**Not a source here: CNPJ.** Receita Federal's CNPJ open data moved in early
2026 to a Nextcloud share (`arquivos.receitafederal.gov.br/index.php/s/YggdBLfdninEJX9`;
the old `dados_abertos_cnpj/` directory has returned **404 since 2026-01-30**)
and **the host refuses connections from outside Brazil** — measured
2026-09-23 from 16 check nodes: **the Brazilian one 200, all 15 others in 11
countries reset.** A publisher's access control, not an outage, so this
project does not route around it. Its terms were never read.
