# Fortaleza (Regional) — build brief

**Step 0 measured 2026-09-23.** Run `python scripts/brief_check.py fortaleza`
before writing any code. **Read `sao-paulo.md` first** — the national facts
(why CNEFE and not CNPJ, the free-text taxonomy, the privacy rule, the
licence, what every Brazilian page must say) are argued there once and hold
here unchanged. This brief carries what is Fortaleza's.

---

## The one-line summary

**Three lines, two modes and all coloured — and Meireles, the city's premier commercial district, loses 43% of its establishments to unclassifiable trade names.**

---

## Business leg — IBGE's CNEFE 2022, MEASURED with `scripts/screen_cnefe.py`

| | |
|---|---|
| **File** | `Arquivos_CNEFE/CSV/Municipio/23_CE/2304400_FORTALEZA.zip` — **28,907,115 bytes**, UTF-8, `;` |
| Establishment rows (`COD_ESPECIE = 6`) | **132,638** |
| **Mapped to the three buckets** | **49,503 (37.3%)** — Retail **29,239** · Food service **11,470** · Personal services **8,794** |
| Recorded **vacant** by the enumerator | 10,253 (7.7%) — excluded |
| **Unclassifiable** (catch-all + unmatched) | 34,299 (25.9%) |
| … by locality | **20% in Genibaú → 43% in Meireles** (Aldeota 33%, Centro 30%), median 23% — the beachfront commercial district is the most under-drawn |
| Coordinate level 1 (the census's own point) | **98.5%** of mapped rows |
| One establishment per row | 97.9% of mapped rows |

**The unclassifiable rows are dropped, not assigned** — and where their share
rises, the map under-draws. The page must say so, as São Paulo's does.

---

## 🔒 Privacy — the decided rule applies unchanged

At an address that also holds a dwelling, the tooltip shows the **category,
never the description text**. Here that reaches **26,186 (52.9%)** of mapped rows; a
first name at a dwelling address is **502 (1.0%)**.

---

## 🚇 Rail — OpenStreetMap, counted 2026-09-23 (one query, Curitiba as the negative control)

**Metrofor**: `route=subway` **Linha Sul** (2 relations); `route=light_rail` **Linha Oeste**, **Parangaba–Mucuripe** and ref `5` (6 relations). **All 8 coloured.** ⚠️ Linha Oeste is a **diesel** light-rail line — confirm service frequency before treating it as urban rail rather than commuter.

**Agency layers searched 2026-09-23 — none reachable (MEASURED, three methods).**
The city's CKAN (`dados.fortaleza.ce.gov.br`) returns only a discount-zone
dataset and bike-share stations for every rail term (nonsense control: zero).
ArcGIS Online holds no government item in the box. **Metrofor's own GTFS page
fails TLS because its certificate has EXPIRED** — not bypassed — and the
Mobility Database lists all three Metrofor feed versions as deprecated, the
last as of 2025-02-24. `dados.ce.gov.br` does not resolve. **OSM is the
geometry source.**

## Scope

**MEASURED 2026-09-23** (OSM route members, by município): **41 stations — 31 in Fortaleza (76%)**, Maracanaú 5, Caucaia 3, Pacatuba 1 (Carlito Benevides, Linha Sul's terminus), and Conjunto São Miguel on the boundary. Every outside station is at a line's end. **REGIONAL — decided by the owner 2026-09-23: Fortaleza (Regional)** = Fortaleza + Caucaia + Maracanaú + Pacatuba. Measured the same night: **Caucaia 6,790** storefronts · **Maracanaú 5,158** · **Pacatuba 1,341** — **62,792 with Fortaleza's 49,503**. Coordinate level 1 ≥ 97.0% (Caucaia the lowest, 2.6% at level 2); catch-all 25.9–28.2%.

## Region

Brazil's — the first Brazilian city adds it (see `sao-paulo.md`).

## Still unknown

- ⚠️ Linha Oeste's service pattern (diesel)
- ⚠️ OSM ref `5` is the **Ramal Aeroporto–Castelão** (Expedicionários ⇒ Castelão, light rail) — whether it carries passengers is unverified: Tel Aviv's trap

```brief-checks
[
  {
    "id": "fortaleza-cnefe-file-live",
    "claim": "The CNEFE 2022 file for Fortaleza is keyless and live - business leg and coordinate leg in one",
    "kind": "http_ok",
    "url": "https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/23_CE/2304400_FORTALEZA.zip",
    "min_bytes": 1000000,
    "content_type_contains": "zip"
  },
  {
    "id": "fortaleza-cnefe-not-re-released",
    "claim": "Every figure here was measured on the May-2024 release. When this FAILS, IBGE has re-released it: re-run scripts/screen_cnefe.py",
    "kind": "http_contains",
    "url": "https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/23_CE/",
    "present": [
      "2304400_FORTALEZA.zip",
      "2307650_MARACANAU.zip",
      "2303709_CAUCAIA.zip",
      "2309706_PACATUBA.zip",
      "2024-05-2"
    ]
  },
  {
    "id": "fortaleza-osm-rail",
    "claim": "OSM carries Fortaleza's rail refs as counted 2026-09-23 - the geometry source; agency layers searched 2026-09-23, see Rail",
    "kind": "osm_route_refs",
    "bbox": [
      -3.89,
      -38.64,
      -3.69,
      -38.4
    ],
    "routes": [
      "subway",
      "light_rail"
    ],
    "require_refs": {
      "subway": [
        "Sul"
      ],
      "light_rail": [
        "Oeste",
        "Parangaba-Mucuripe"
      ]
    }
  },
  {
    "id": "fortaleza-projected-crs",
    "claim": "Fortaleza projects to its own UTM zone, never a neighbour's",
    "kind": "utm_zone_from_longitude",
    "lon": -38.5,
    "north": false,
    "expect": "EPSG:32724"
  }
]
```
