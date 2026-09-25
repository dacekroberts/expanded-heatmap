"""Reading FEHD's licence registers: the daily XML (what is licensed) and the
same registers from the CSDI portal (FEHD's own point per licence). No network
here - fetch_sources.py downloads, this only reads.

Each XML is self-describing - `<GENERATION_DATE>`, and code->label lookups for
the licence type and the district inside the same file - so nothing here holds
a code list of its own.
"""
import json
import xml.etree.ElementTree as ET

from pipeline.hong_kong import config


def read_register(name):
    """(rows, generation_date, type_labels, district_labels) for one register."""
    path = config.DATA_RAW / config.FEHD_FILES[name]
    root = ET.parse(path).getroot()
    gen = (root.findtext("GENERATION_DATE") or "").strip()
    if not gen:
        raise ValueError(f"{path.name} carries no GENERATION_DATE - not the file the brief read")
    types = _codes(root, "TYPE_CODE")
    dists = _codes(root, "DIST_CODE")
    rows = [{k: (lp.findtext(k) or "").strip()
             for k in ("TYPE", "DIST", "LICNO", "SS", "ADR", "INFO", "EXPDATE")}
            for lp in root.iter("LP")]
    return rows, gen, types, dists


def _codes(root, block):
    el = root.find(block)
    if el is None:
        raise ValueError(f"no <{block}> lookup in the register")
    return {c.get("ID"): (c.text or "").strip() for c in el.iter("CODE") if c.get("ID")}


def read_points(name):
    """{licence number: (lat, lon, type code)} from the CSDI GeoJSON for one register."""
    path = config.DATA_RAW / f"csdi_{config.CSDI_LAYERS[name][1]}.geojson"
    feats = json.loads(path.read_text(encoding="utf-8"))["features"]
    out, dup = {}, 0
    for f in feats:
        p = f["properties"]
        lic = str(p.get(config.CSDI_LICENCE_NO) or "").strip()
        # The record's own WGS84 fields, not the geometry, whose CRS a file
        # export need not state.
        lat, lon = p.get("LATITUDE"), p.get("LONGITUDE")
        if lic in out:
            dup += 1
        if lat in (None, "", "None") or lon in (None, "", "None"):
            continue
        out[lic] = (float(lat), float(lon), str(p.get(config.CSDI_TYPE) or "").strip())
    return out, len(feats), dup
