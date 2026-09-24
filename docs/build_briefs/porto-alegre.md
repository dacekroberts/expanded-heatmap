# Porto Alegre — build brief

**Step 0 measured 2026-09-23.** Run `python scripts/brief_check.py porto-alegre`
before writing any code. **Read `sao-paulo.md` first** — the national facts
(why CNEFE and not CNPJ, the free-text taxonomy, the privacy rule, the
licence, what every Brazilian page must say) are argued there once and hold
here unchanged. This brief carries what is Porto Alegre's.

---

## The one-line summary

**One metropolitan line that spends most of its length outside the city, and the lowest mapped share of the nine (30.8%).**

---

## Business leg — IBGE's CNEFE 2022, MEASURED with `scripts/screen_cnefe.py`

| | |
|---|---|
| **File** | `Arquivos_CNEFE/CSV/Municipio/43_RS/4314902_PORTO_ALEGRE.zip` — **17,172,345 bytes**, UTF-8, `;` |
| Establishment rows (`COD_ESPECIE = 6`) | **61,068** |
| **Mapped to the three buckets** | **18,798 (30.8%)** — Retail **10,576** · Food service **4,599** · Personal services **3,623** |
| Recorded **vacant** by the enumerator | 6,055 (9.9%) — excluded |
| **Unclassifiable** (catch-all + unmatched) | 17,030 (27.9%) |
| … by locality | 23% (Rubem Berta, Centro) → 40% (Navegantes), median 27% |
| Coordinate level 1 (the census's own point) | **98.1%** of mapped rows |
| One establishment per row | 95.9% of mapped rows |

**The unclassifiable rows are dropped, not assigned** — and where their share
rises, the map under-draws. The page must say so, as São Paulo's does.

---

## 🔒 Privacy — the decided rule applies unchanged

At an address that also holds a dwelling, the tooltip shows the **category,
never the description text**. Here that reaches **6,849 (36.4%)** of mapped rows; a
first name at a dwelling address is **166 (0.9%)**.

---

## 🚇 Rail — OpenStreetMap, counted 2026-09-23 (one query, Curitiba as the negative control)

**Trensurb** — `route=subway`, 6 relations, ref `1`, all coloured — plus the **Aeromóvel airport connector** (`Conexão Metrô-Aeroporto`), a people mover. ⚠️ Trensurb is a *trem metropolitano*: confirm it is urban rail, not commuter, under the standing rule — its frequency and electrification argue urban.

**Agency layers searched 2026-09-23 — none found (MEASURED, four methods).**
Trensurb's own domains (`trensurb.gov.br`, `.com.br`) refuse or time out; the
city's and the state's CKAN portals return nothing for any rail term
(nonsense control: zero on both); the Mobility Database has no Trensurb, CBTU
or Aeromóvel feed; ArcGIS Online has nothing in the box. A secondary source
says Trensurb falls outside Decree 8.777's open-data duty — ASSERTED. **OSM is
the geometry source.**

## Scope

**MEASURED 2026-09-23** (OSM route members, by município): **23 stations — only 7 in Porto Alegre (30%)**, Canoas 6, Novo Hamburgo 4, São Leopoldo 3, Sapucaia do Sul 2, Esteio 1. **The city holds under a third of its own network: regional, or not built** — the owner's call. The five neighbours' CNEFE files total 10,837,156 B, not yet downloaded.

## Region

Brazil's — the first Brazilian city adds it (see `sao-paulo.md`).

## Still unknown

- ⚠️ Scope — regional or not built, **owner's call**; the corridor's storefronts are unmeasured
- ⚠️ Trensurb's classification (urban vs commuter)
- ⚠️ Whether the Aeromóvel is drawn (Toulouse's cable-car precedent says a non-rail mode can be)

```brief-checks
[
  {
    "id": "porto-alegre-cnefe-file-live",
    "claim": "The CNEFE 2022 file for Porto Alegre is keyless and live - business leg and coordinate leg in one",
    "kind": "http_ok",
    "url": "https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/43_RS/4314902_PORTO_ALEGRE.zip",
    "min_bytes": 1000000,
    "content_type_contains": "zip"
  },
  {
    "id": "porto-alegre-cnefe-not-re-released",
    "claim": "Every figure here was measured on the May-2024 release. When this FAILS, IBGE has re-released it: re-run scripts/screen_cnefe.py",
    "kind": "http_contains",
    "url": "https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/43_RS/",
    "present": [
      "4314902_PORTO_ALEGRE.zip",
      "2024-05-2"
    ]
  },
  {
    "id": "porto-alegre-osm-rail",
    "claim": "OSM carries Porto Alegre's rail refs as counted 2026-09-23 - the geometry source; agency layers searched 2026-09-23, see Rail",
    "kind": "osm_route_refs",
    "bbox": [
      -30.27,
      -51.31,
      -29.93,
      -51.05
    ],
    "routes": [
      "subway"
    ],
    "require_refs": {
      "subway": [
        "1"
      ]
    }
  },
  {
    "id": "porto-alegre-projected-crs",
    "claim": "Porto Alegre projects to its own UTM zone, never a neighbour's",
    "kind": "utm_zone_from_longitude",
    "lon": -51.2,
    "north": false,
    "expect": "EPSG:32722"
  }
]
```
