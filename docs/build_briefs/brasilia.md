# Brasília — build brief

**Step 0 measured 2026-09-23.** Run `python scripts/brief_check.py brasilia`
before writing any code. **Read `sao-paulo.md` first** — the national facts
(why CNEFE and not CNPJ, the free-text taxonomy, the privacy rule, the
licence, what every Brazilian page must say) are argued there once and hold
here unchanged. This brief carries what is Brasília's.

---

## The one-line summary

**The best coordinates in Brazil (99.9%) on the most unusual addresses: addresses name a block rather than a door, 9% of rows stand for more than one establishment, and the core loses half its trade names.**

---

## Business leg — IBGE's CNEFE 2022, MEASURED with `scripts/screen_cnefe.py`

| | |
|---|---|
| **File** | `Arquivos_CNEFE/CSV/Municipio/53_DF/5300108_BRASILIA.zip` — **19,814,371 bytes**, UTF-8, `;` |
| Establishment rows (`COD_ESPECIE = 6`) | **100,889** |
| **Mapped to the three buckets** | **35,824 (35.5%)** — Retail **19,706** · Food service **9,164** · Personal services **6,954** |
| Recorded **vacant** by the enumerator | 6,925 (6.9%) — excluded |
| **Unclassifiable** (catch-all + unmatched) | 26,958 (26.7%) |
| … by locality | 🚨 **16% in Sol Nascente → 48% in Asa Sul** (Asa Norte 39%, Núcleo Bandeirante 35%, Águas Claras 34%), median 25% — **the Plano Piloto, the city's core, is the most under-drawn place in Brazil** |
| Coordinate level 1 (the census's own point) | **99.9%** of mapped rows |
| One establishment per row | 91.0% of mapped rows |

**The unclassifiable rows are dropped, not assigned** — and where their share
rises, the map under-draws. The page must say so, as São Paulo's does.

---

## 🔒 Privacy — the decided rule applies unchanged

At an address that also holds a dwelling, the tooltip shows the **category,
never the description text**. On the old street + number key that reached 32,146 (89.7%) — **an artefact of block addressing, not the city**. **Keyed on the lot (decided by the owner 2026-09-23, now in `screen_cnefe.py`) it is 24,665 (68.9%)**; a
first name at a dwelling address is **706 (2.0%)**.

---

## 🚇 Rail — OpenStreetMap, counted 2026-09-23 (one query, Curitiba as the negative control)

**Metrô-DF, Linha Verde and Linha Laranja** — 4 relations, all coloured.

**Agency layers FOUND 2026-09-23 — stations AND lines, with status.**
IPEDF/Codeplan's GeoServer (`catalogo.ipe.df.gov.br/geoserver/geonode/wfs`):
`geonode:ESTACOES_METRO` — **24 stations**, `nome_estac` and `situacao` (all
*Em operação*), EPSG:4326, published 2023-10-27; `geonode:ESTACOES_EM_CONSTRUCAO`
— 5 (Onoyama, Estrada Parque, 110/106/104 Sul); `geonode:ESTACAO_EXPANSAO` — 13
planned; `geonode:LINHA_VERDE_LARANJA` — **one MultiLineString for both lines**
(`linha` = *verde e laranja*), so the two labels the invariant needs come from
a split or from OSM's per-line relations. Licence on the GeoNode item pages:
**"Public Domain (PD)"** as declared — **not read**. `dados.df.gov.br` timed out
in the TLS handshake; this catalogue is the way in. ⚠️ The status field is
from a **2023** file — cross-check it against OSM before trusting it.
**Recommendation: agency stations, whose status decides what is drawn; OSM
for the per-line geometry.**

## Scope

Município 5300108 **is the whole Federal District**, so Ceilândia and Samambaia at the lines' ends are inside it — no regional question.

## Region

Brazil's — the first Brazilian city adds it (see `sao-paulo.md`).

## Still unknown

- ✅ **DECIDED 2026-09-23 (owner): the dwelling test keys on the LOT where the door number is blank.** 98.5% of the old key's "shared" rows carried no door number (`SN`/`0`): the street field names a *quadra* or *conjunto* and the unit is the `LOTE` complement, so street + number merged whole blocks. `screen_cnefe.py` now appends the lot when the number is blank and the first complement is `LOTE`: **68.9%** of mapped rows share a lot with a dwelling (was 89.7%). Two other keys, measured for comparison: any first complement, 58.0%; the identical coordinate, 18.8% (Recife 20.3%) — rejected as least protective, since a home and a shop on one lot can carry different points.
- ⚠️ 9.0% of rows stand for 2+ establishments (`COD_INDICADOR_ESTAB_ENDERECO` 2/3/4)
- ⚠️ Whether the Asa Sul / Asa Norte skew needs a better classifier before this city is worth drawing

```brief-checks
[
  {
    "id": "brasilia-agency-stations",
    "claim": "IPEDF's GeoServer publishes Metro-DF's 24 operating stations with a status field - the station source, declared public domain",
    "kind": "http_contains",
    "url": "https://catalogo.ipe.df.gov.br/geoserver/geonode/wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=geonode:ESTACOES_METRO&resultType=hits",
    "present": [
      "numberMatched=\"24\""
    ]
  },
  {
    "id": "brasilia-cnefe-file-live",
    "claim": "The CNEFE 2022 file for Brasília is keyless and live - business leg and coordinate leg in one",
    "kind": "http_ok",
    "url": "https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/53_DF/5300108_BRASILIA.zip",
    "min_bytes": 1000000,
    "content_type_contains": "zip"
  },
  {
    "id": "brasilia-cnefe-not-re-released",
    "claim": "Every figure here was measured on the May-2024 release. When this FAILS, IBGE has re-released it: re-run scripts/screen_cnefe.py",
    "kind": "http_contains",
    "url": "https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/53_DF/",
    "present": [
      "5300108_BRASILIA.zip",
      "2024-05-2"
    ]
  },
  {
    "id": "brasilia-osm-rail",
    "claim": "OSM carries Brasília's rail refs as counted 2026-09-23 - the geometry source; agency layers searched 2026-09-23, see Rail",
    "kind": "osm_route_refs",
    "bbox": [
      -15.9,
      -48.15,
      -15.7,
      -47.85
    ],
    "routes": [
      "subway"
    ],
    "require_refs": {
      "subway": [
        "Laranja",
        "Verde"
      ]
    }
  },
  {
    "id": "brasilia-projected-crs",
    "claim": "Brasília projects to its own UTM zone, never a neighbour's",
    "kind": "utm_zone_from_longitude",
    "lon": -47.93,
    "north": false,
    "expect": "EPSG:32723"
  }
]
```
