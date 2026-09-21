"""Screen candidate cities on rail, by reading their real GTFS `routes.txt`.

Run this BEFORE any business-data research. Rail is the cheapest disqualifier
this project has: a city with no urban rail is out regardless of how good its
business registry turns out to be, and finding that out first saves the whole
Step 0. Screening 13 Canadian cities on 2026-09-21 removed 6 of them in one
pass, before a single catalogue was opened.

    python scripts/screen_rail.py feeds.tsv
    python scripts/screen_rail.py < feeds.tsv

Input is tab-separated, one agency per line, `#` comments and blanks ignored:

    Toronto<TAB>TTC<TAB>https://.../toronto-ttc-gtfs.zip
    Montreal<TAB>STM<TAB>https://.../montreal-stm-gtfs.zip

Feed URLs come from the Mobility Database catalogue, which is one CSV listing
most of the world's public feeds - far quicker than hunting agency sites:

    curl -sL https://bit.ly/catalogs-csv -o catalog.csv
    # then filter on location.country_code / location.municipality,
    # and take `urls.latest`

What it reports, per agency: the GTFS `route_type` counts, split into urban
rail (0 tram/LRT, 1 subway, 5 cable, 7 funicular, 12 monorail) and everything
else. **route_type 2 is commuter rail and is deliberately NOT urban rail** -
this project excludes it in every city built so far, so a city whose only rail
is type 2 reads as "no urban rail" here, which is the intended answer.

Two traps this exists to catch, both real:

- **An agency may code its subway as type 0.** Toronto does: its 4 subway
  lines and ~13 streetcar routes are indistinguishable by type, which is San
  Francisco's shape and means `docs/sub_transit_line_filters.md` applies and
  lines must be picked by route id. A high type-0 count is a prompt to look at
  route names, not a finished answer.
- **A regional agency's feed covers cities that have no rail of their own.**
  TransLink's feed carries Surrey's SkyTrain stations; Vancouver's own city
  screen would miss that. Check whether rail physically reaches a candidate
  before ruling it out - or in.

Read-only: nothing is written, and feeds are fetched to memory, never to disk.
"""

import csv
import io
import sys
import urllib.request
import zipfile

URBAN_RAIL = {0: "tram/LRT", 1: "subway", 5: "cable", 7: "funicular", 12: "monorail"}
OTHER = {2: "commuter rail", 3: "bus", 4: "ferry", 6: "aerial", 11: "trolleybus"}
UA = "Mozilla/5.0 (compatible; transit-density-research/1.0)"


class HttpFile(io.RawIOBase):
    """A seekable file over HTTP range requests.

    A GTFS zip is mostly `stop_times.txt`, which this never needs - so where
    the host supports ranges, only the central directory and `routes.txt` are
    transferred instead of tens of megabytes. Hosts that do not advertise
    `Accept-Ranges` (Google's storage API among them) fall back to a full
    download, which still works, just slower.
    """

    def __init__(self, url):
        self.url = url
        self.pos = 0
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            self.size = int(r.headers["Content-Length"])
            if r.headers.get("Accept-Ranges") != "bytes":
                raise OSError("no range support")

    def seek(self, off, whence=0):
        self.pos = {0: off, 1: self.pos + off, 2: self.size + off}[whence]
        return self.pos

    def tell(self):
        return self.pos

    def seekable(self):
        return True

    def readable(self):
        return True

    def read(self, n=-1):
        if n < 0:
            n = self.size - self.pos
        if n == 0 or self.pos >= self.size:
            return b""
        end = min(self.pos + n, self.size) - 1
        req = urllib.request.Request(
            self.url, headers={"User-Agent": UA, "Range": f"bytes={self.pos}-{end}"}
        )
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        self.pos += len(data)
        return data


def open_feed(url):
    try:
        return HttpFile(url), "range"
    except Exception:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=300) as r:
            buf = io.BytesIO(r.read())
        buf.size = len(buf.getvalue())
        return buf, "full download"


def route_types(url):
    """-> (counts by route_type, how it was fetched, zip size in bytes)."""
    handle, mode = open_feed(url)
    with zipfile.ZipFile(handle) as z:
        name = next((n for n in z.namelist() if n.endswith("routes.txt")), None)
        if name is None:
            return None, mode, handle.size
        raw = z.read(name).decode("utf-8-sig", errors="replace")
    counts = {}
    for row in csv.DictReader(io.StringIO(raw)):
        value = (row.get("route_type") or "").strip()
        if value.isdigit():
            counts[int(value)] = counts.get(int(value), 0) + 1
    return counts, mode, handle.size


def read_targets(stream):
    for line in stream:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            sys.exit(f"Expected 3 tab-separated fields, got {len(parts)}: {line[:70]}")
        yield parts


def main():
    if len(sys.argv) > 2:
        sys.exit(__doc__)
    if len(sys.argv) == 2:
        with open(sys.argv[1], encoding="utf-8") as fh:
            targets = list(read_targets(fh))
    else:
        targets = list(read_targets(sys.stdin))

    passed = []
    for city, agency, url in targets:
        try:
            counts, mode, size = route_types(url)
        except Exception as exc:
            print(f"{city:<14} {agency:<30} ERROR {type(exc).__name__}: {exc}")
            continue
        if counts is None:
            print(f"{city:<14} {agency:<30} no routes.txt in the zip")
            continue
        rail = {k: v for k, v in counts.items() if k in URBAN_RAIL}
        rail_desc = ", ".join(f"{URBAN_RAIL[k]}:{v}" for k, v in sorted(rail.items())) or "-"
        other = ", ".join(
            f"{OTHER.get(k, k)}:{v}" for k, v in sorted(counts.items()) if k not in URBAN_RAIL
        )
        if rail:
            passed.append(city)
        verdict = "URBAN RAIL" if rail else "no urban rail"
        print(
            f"{city:<14} {agency:<30} {verdict:<14} [{rail_desc}]  "
            f"other: {other}  ({size // 1024} KB, {mode})"
        )

    print(f"\n{len(passed)} of {len(targets)} have urban rail: {', '.join(passed) or 'none'}")
    print("Commuter rail (route_type 2) is not counted - this project excludes it.")
    print("A high tram/LRT count may hide a subway: check route names before concluding.")


if __name__ == "__main__":
    main()
