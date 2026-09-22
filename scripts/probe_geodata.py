"""Probe a candidate geodata or tabular endpoint and say what it ACTUALLY is.

The companion to `screen_rail.py`. That one answers "is there a GTFS feed";
this one answers the question the 2026-09-21 global screen discovered was the
real one: **does a national mapping agency publish station points and line
geometry**, and does a business register carry premises with coordinates.

    python scripts/probe_geodata.py targets.tsv
    python scripts/probe_geodata.py < targets.tsv

Input is tab-separated, `#` comments and blanks ignored:

    Japan-N02<TAB>https://nlftp.mlit.go.jp/ksj/gml/data/N02/N02-24/N02-24_GML.zip
    Korea-stations<TAB>https://data.kric.go.kr/rips/dataset/download.file?...

For each target it reports: reachability, real content type, and - for
anything geospatial or tabular - the row count, geometry types, CRS and
columns. It names the two things a screen must not confuse:

- **POINTS vs LINES.** This project draws and labels every transit line, so a
  station layer alone is not enough. Japan's N02 carries both (10,235 stations
  AND 21,932 line segments); Korea's station standard data carries 1,099
  stations and no lines at all. A screen that asks only about stations records
  a false pass.
- **PREMISES vs AGGREGATE.** A row that is a summary cannot be mapped. This
  killed Istanbul (counts per district), Japan's Economic Census (counts per
  area) and Seoul's 상권분석서비스 (per district per quarter) - the last of
  which was the best disguised, because its categories matched this project's
  three buckets exactly. The prober flags a coordinate column when it finds
  one, and its absence is the thing to look at.

Three transport traps it handles, all of which cost real time:

- **Python's TLS stack fails where curl succeeds.** `data.gcis.nat.gov.tw`
  refused `requests` with an SSLError and served curl a 4.5 MB CSV. A probe
  without the fallback would have recorded "unreachable", which is a statement
  about the client, not the data.
- **A transient outage is not a finding.** `www.data.go.kr` timed out at 21s
  from two independent networks and answered 200 an hour later. `--retry`
  re-probes failures after a delay so a blip is not written down as a fact.
- **A zip may hold several encodings.** Japan's N02 ships Shift-JIS and UTF-8
  copies of the same layers; the prober lists members rather than guessing.

Geospatial reporting needs geopandas (the pipeline environment has it). Without
it the prober still reports reachability, type and archive contents, which is
most of the screening value.
"""

import io
import subprocess
import sys
import time
import zipfile

REQUEST_TIMEOUT = 120
UA = "Mozilla/5.0 (compatible; transit-density-research/1.0)"
COORD_HINTS = (
    "lat", "lon", "lng", "latitude", "longitude", "x", "y", "geom", "geometry",
    "위도", "경도", "緯度", "経度", "latitud", "longitud", "coord",
)


def fetch(url):
    """-> (bytes, how). Tries requests, falls back to curl on any failure.

    The fallback is not defensive padding: curl and Python negotiate TLS
    differently, and at least one government host serves only curl.
    """
    try:
        import requests

        r = requests.get(url, headers={"User-Agent": UA}, timeout=REQUEST_TIMEOUT,
                         allow_redirects=True)
        r.raise_for_status()
        return r.content, f"requests {r.status_code}"
    except Exception as exc:
        first = f"{type(exc).__name__}"
    try:
        out = subprocess.run(
            ["curl", "-sSL", "-m", str(REQUEST_TIMEOUT), "-A", UA, url],
            capture_output=True, timeout=REQUEST_TIMEOUT + 30,
        )
        if out.returncode == 0 and out.stdout:
            return out.stdout, f"curl (requests failed: {first})"
        return None, f"both failed (requests: {first}; curl rc={out.returncode})"
    except Exception as exc2:
        return None, f"both failed (requests: {first}; curl: {type(exc2).__name__})"


def describe_frame(label, gdf):
    cols = list(gdf.columns)
    geom = ""
    if hasattr(gdf, "geom_type"):
        try:
            geom = f"  geometry={gdf.geom_type.value_counts().to_dict()}"
        except Exception:
            pass
    crs = f"  crs={gdf.crs}" if getattr(gdf, "crs", None) is not None else ""
    coordish = [c for c in cols if any(h in str(c).lower() for h in COORD_HINTS)]
    print(f"    {label}: rows={len(gdf)}{geom}{crs}")
    print(f"      columns: {cols[:18]}{' …' if len(cols) > 18 else ''}")
    if coordish:
        print(f"      COORDINATE-LIKE COLUMNS: {coordish}")
    else:
        print("      NO coordinate-like column found - check whether rows are "
              "premises or AGGREGATES before trusting this source")


def probe_geo(name, data):
    try:
        import geopandas as gpd
    except ImportError:
        print("    (geopandas not installed - skipping geometry inspection)")
        return
    try:
        gdf = gpd.read_file(io.BytesIO(data))
        describe_frame(name, gdf)
    except Exception as exc:
        print(f"    could not read as geodata: {type(exc).__name__}: {str(exc)[:120]}")


def probe(label, url, retry_after):
    print(f"\n{'=' * 72}\n{label}\n  {url}\n{'=' * 72}")
    data, how = fetch(url)
    if data is None and retry_after:
        print(f"  {how} - retrying in {retry_after}s "
              "(a transient outage is not a finding)")
        time.sleep(retry_after)
        data, how = fetch(url)
    if data is None:
        print(f"  UNREACHABLE: {how}")
        print("  Record as ASSERTED, not measured. Retry later and try the "
              "city portal; a national portal being down says nothing about "
              "the data.")
        return
    print(f"  fetched {len(data) // 1024} KB via {how}")

    head = data[:4]
    if head[:2] == b"PK":
        try:
            z = zipfile.ZipFile(io.BytesIO(data))
        except zipfile.BadZipFile:
            print("  looks like a zip and is not one (check the URL is a file, "
                  "not a landing page)")
            return
        names = z.namelist()
        print(f"  ZIP with {len(names)} members:")
        for n in names[:20]:
            print(f"    {n}")
        if any(n.lower().endswith(".xlsx") or n.startswith("xl/") for n in names):
            print("  (xlsx workbook - read with pandas/openpyxl)")
        geo = [n for n in names if n.lower().endswith((".shp", ".geojson"))]
        if geo:
            print(f"  geospatial members: {len(geo)}")
            import tempfile, os
            with tempfile.TemporaryDirectory() as td:
                z.extractall(td)
                for g in geo[:6]:
                    try:
                        import geopandas as gpd
                        describe_frame(g, gpd.read_file(os.path.join(td, g)))
                    except ImportError:
                        print("    (geopandas not installed)")
                        break
                    except Exception as exc:
                        print(f"    {g}: {type(exc).__name__}")
        return

    if head[:1] in (b"{", b"["):
        print("  JSON / GeoJSON")
        probe_geo("(geojson)", data)
        return

    if b"<html" in data[:600].lower() or b"<!doctype" in data[:600].lower():
        print("  HTML - this is a LANDING PAGE, not a data file.")
        print("  Find the real download URL before recording anything.")
        return

    # Tabular fallback: CSV in whatever encoding the publisher chose.
    for enc in ("utf-8-sig", "utf-8", "cp949", "big5", "cp950", "latin-1"):
        try:
            text = data.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        print("  binary of unknown type")
        return
    import csv as _csv
    sample = text[:400000]
    try:
        dialect = _csv.Sniffer().sniff(sample[:4000])
        delim = dialect.delimiter
    except Exception:
        delim = ","
    rows = list(_csv.reader(io.StringIO(sample), delimiter=delim))
    print(f"  TEXT/CSV decoded as {enc}, delimiter {delim!r}")
    if rows:
        print(f"  header: {rows[0][:18]}")
        coordish = [c for c in rows[0] if any(h in str(c).lower() for h in COORD_HINTS)]
        print(f"  COORDINATE-LIKE COLUMNS: {coordish}" if coordish else
              "  NO coordinate-like column - premises or AGGREGATE? check before trusting")
        for r in rows[1:3]:
            print(f"    {r[:8]}")


def read_targets(stream):
    for line in stream:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            sys.exit(f"Expected 'label<TAB>url', got: {line[:70]}")
        yield parts[0], parts[1]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    retry_after = 20 if "--retry" in sys.argv else 0
    if args:
        with open(args[0], encoding="utf-8") as fh:
            targets = list(read_targets(fh))
    else:
        targets = list(read_targets(sys.stdin))
    for label, url in targets:
        probe(label, url, retry_after)
    print(f"\n{len(targets)} probed. Reminders:")
    print("  - POINTS are not LINES. This project draws every transit line.")
    print("  - A row that is a summary is not a premises.")
    print("  - An unreachable host is a fact about today, not about the data.")


if __name__ == "__main__":
    main()
