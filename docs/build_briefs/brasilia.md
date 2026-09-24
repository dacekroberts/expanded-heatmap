# Brasília — build brief

**Step 0 measured 2026-09-23.** Run `python scripts/brief_check.py brasilia`
before writing any code. **Read `sao-paulo.md` first** — the national facts
(why CNEFE and not CNPJ, the free-text taxonomy, the privacy rule, the
licence, what every Brazilian page must say) are argued there once and hold
here unchanged. This brief carries what is Brasília's.

---

## The one-line summary

**The best coordinates in Brazil (99.9%) on the most unusual addresses: 90% of storefronts share an address with a home, 9% of rows stand for more than one establishment, and the core loses half its trade names.**

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
never the description text**. Here that reaches **32,146 (89.7%)** of mapped rows; a
first name at a dwelling address is **824 (2.3%)**.

---

## 🚇 Rail — OpenStreetMap, counted 2026-09-23 (one query, Curitiba as the negative control)

**Metrô-DF, Linha Verde and Linha Laranja** — 4 relations, all coloured.

⚠️ **Agency layers have NOT been searched.** `osm-rail` puts them first, and
Rio's metro and VLT layers turned up only when its city's ArcGIS org was
enumerated. **Enumerate Brasília's own portals before building from OSM.**

## Scope

Município 5300108 **is the whole Federal District**, so Ceilândia and Samambaia at the lines' ends are inside it — no regional question.

## Region

Brazil's — the first Brazilian city adds it (see `sao-paulo.md`).

## Still unknown

- ⚠️ 🚨 **Superquadra addressing**: 89.7% of mapped rows share an address with a dwelling and 9.0% stand for 2+ establishments (`COD_INDICADOR_ESTAB_ENDERECO` 2/3/4) — look at the addresses before trusting any Brasília figure; the privacy rule strips description text from nearly every pin
- ⚠️ Whether the Asa Sul / Asa Norte skew needs a better classifier before this city is worth drawing

```brief-checks
[
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
    "claim": "OSM carries Brasília's rail refs as counted 2026-09-23 - the geometry source until agency layers are found",
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
