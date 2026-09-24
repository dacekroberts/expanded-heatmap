"""Read Roma Capitale's SUAP register, whose CSV is not valid CSV.

The file is comma-separated with NO quoting, and one field - SPECIALIZZAZIONE,
the twelfth of fourteen - carries commas of its own ("ALTRI ESERCIZI
SPECIALIZZATI NON ALIMENTARI (MACCHINE E ATTREZZATURE PER UFFICIO,OTTICA,
FOTOGRAFIA, ..."). 30,075 of 168,255 rows split into 15 to 24 fields
(measured 2026-09-24). A standard reader either refuses the file or shifts
every later column.

It is still unambiguous: the first eleven fields and the last two take no
commas, and the last two only ever hold ALIMENTARE / NON_ALIMENTARE or
nothing. So a row is its first eleven fields, its last two, and everything
between joined back with commas. Every row is VALIDATED against that shape,
and one that does not fit stops the read rather than being guessed at.
"""
import sys

import pandas as pd

HEAD = ["STRUTTURA_GESTIONE", "NUMERO_ESERCIZIO", "DATA_INIZIO", "CODICE_VIA", "DESCRIZIONE_VIA",
        "CIVICO", "ESP_CIVICO", "MUNICIPIO", "SUPERFICIE_TOTALE", "DESCRIZIONE_MACRO_ATTIVITA",
        "DESCRIZIONE", "SPECIALIZZAZIONE", "SUPERFICIE_ALIMENTARE", "SUPERFICIE_NON_ALIMENTARE"]


def read(path):
    rows, bad = [], []
    with open(path, encoding="utf-8-sig", newline="") as fh:
        header = fh.readline().rstrip("\r\n").split(",")
        if header != HEAD:
            sys.exit(f"SUAP header changed: {header}")
        for n, line in enumerate(fh, start=2):
            f = line.rstrip("\r\n").split(",")
            if len(f) < 14:
                bad.append((n, line[:120]))
                continue
            # A handful of street names carry a comma too, which shifts the
            # first eleven fields; take the street as whatever width leaves
            # MUNICIPIO a real municipio (1-15).
            row = None
            for k in range(0, 4):
                if len(f) < 14 + k:
                    break
                g = f[:4] + [",".join(f[4:5 + k])] + f[5 + k:]
                cand = g[:11] + [",".join(g[11:-2]), g[-2], g[-1]]
                if (cand[12] in ("", "ALIMENTARE") and cand[13] in ("", "NON_ALIMENTARE")
                        and cand[7].strip().isdigit() and 1 <= int(cand[7]) <= 15):
                    row = cand
                    break
            if row is None:
                bad.append((n, line[:120]))
                continue
            rows.append(row)
    if bad:
        sys.exit(f"{len(bad)} SUAP rows do not fit the fixed shape, e.g. {bad[:3]}")
    df = pd.DataFrame(rows, columns=HEAD)
    for c in df.columns:
        df[c] = df[c].map(_unmojibake).str.strip()
    return df.replace({"": None})


def _unmojibake(s):
    """Some values were UTF-8 encoded twice ("AttivitÃ\\xa0" for "Attività");
    undo it where - and only where - the round trip succeeds."""
    if s and "Ã" in s:
        try:
            return s.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return s
    return s
