# Belo Horizonte — build brief

**Step 0 measured 2026-09-23.** Run `python scripts/brief_check.py belo-horizonte`
before writing any code. **Read `sao-paulo.md` first** — the national facts
(why CNEFE and not CNPJ, the free-text taxonomy, the privacy rule, the
licence, what every Brazilian page must say) are argued there once and hold
here unchanged. This brief carries what is Belo Horizonte's.

---

## The one-line summary

**The highest vacancy of the nine (10.3%) and a metro whose second line may exist only in OpenStreetMap.**

---

## Business leg — IBGE's CNEFE 2022, MEASURED with `scripts/screen_cnefe.py`

| | |
|---|---|
| **File** | `Arquivos_CNEFE/CSV/Municipio/31_MG/3106200_BELO_HORIZONTE.zip` — **34,957,820 bytes**, UTF-8, `;` |
| Establishment rows (`COD_ESPECIE = 6`) | **125,268** |
| **Mapped to the three buckets** | **44,923 (35.9%)** — Retail **22,518** · Food service **13,127** · Personal services **9,278** |
| Recorded **vacant** by the enumerator | 12,939 (10.3%) — excluded |
| **Unclassifiable** (catch-all + unmatched) | 28,617 (22.8%) |
| … by locality | 22% (Padre Eustáquio) → 30% (Carlos Prates), median 29% — but **BH's `DSC_LOCALIDADE` is coarse**: few localities reach 1,500 rows, so this spread under-describes the city |
| Coordinate level 1 (the census's own point) | **98.8%** of mapped rows |
| One establishment per row | 94.6% of mapped rows |

**The unclassifiable rows are dropped, not assigned** — and where their share
rises, the map under-draws. The page must say so, as São Paulo's does.

---

## 🔒 Privacy — the decided rule applies unchanged

At an address that also holds a dwelling, the tooltip shows the **category,
never the description text**. Here that reaches **16,193 (36.0%)** of mapped rows; a
first name at a dwelling address is **608 (1.4%)**.

---

## 🚇 Rail — OpenStreetMap, counted 2026-09-23 (one query, Curitiba as the negative control)

**Metrô BH**: `route=subway`, 4 relations, refs `1` (Linha 1 – Laranja) and `2`, **3 of 4 coloured**. 🚨 **Linha 2 (Barreiro–Nova Suíça) is, on this project's knowledge, still under construction** — OSM carrying it as a plain `subway` route is **Tel Aviv's trap**. Verify operating status before drawing it. The EFVM intercity train in the box is excluded by the standing rule.

⚠️ **Agency layers have NOT been searched.** `osm-rail` puts them first, and
Rio's metro and VLT layers turned up only when its city's ArcGIS org was
enumerated. **Enumerate Belo Horizonte's own portals before building from OSM.**

## Scope

Linha 1 lies within the município; commune scope likely holds.

## Region

Brazil's — the first Brazilian city adds it (see `sao-paulo.md`).

## Still unknown

- ⚠️ 🚨 Linha 2's operating status
- ⚠️ Linha 2's missing colour
- ⚠️ Locality granularity for the skew measurement

```brief-checks
[
  {
    "id": "belo-horizonte-cnefe-file-live",
    "claim": "The CNEFE 2022 file for Belo Horizonte is keyless and live - business leg and coordinate leg in one",
    "kind": "http_ok",
    "url": "https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/31_MG/3106200_BELO_HORIZONTE.zip",
    "min_bytes": 1000000,
    "content_type_contains": "zip"
  },
  {
    "id": "belo-horizonte-cnefe-not-re-released",
    "claim": "Every figure here was measured on the May-2024 release. When this FAILS, IBGE has re-released it: re-run scripts/screen_cnefe.py",
    "kind": "http_contains",
    "url": "https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/31_MG/",
    "present": [
      "3106200_BELO_HORIZONTE.zip",
      "2024-05-2"
    ]
  },
  {
    "id": "belo-horizonte-osm-rail",
    "claim": "OSM carries Belo Horizonte's rail refs as counted 2026-09-23 - the geometry source until agency layers are found",
    "kind": "osm_route_refs",
    "bbox": [
      -20.06,
      -44.07,
      -19.78,
      -43.85
    ],
    "routes": [
      "subway"
    ],
    "require_refs": {
      "subway": [
        "1",
        "2"
      ]
    }
  },
  {
    "id": "belo-horizonte-projected-crs",
    "claim": "Belo Horizonte projects to its own UTM zone, never a neighbour's",
    "kind": "utm_zone_from_longitude",
    "lon": -43.94,
    "north": false,
    "expect": "EPSG:32723"
  }
]
```
