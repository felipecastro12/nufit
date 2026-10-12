#!/usr/bin/env python3
"""Inserta o reemplaza un ticker dentro del bloque JSON de dashboard/index.html.

Uso:
    python3 -I upsert_ticker.py <ruta/al/index.html> <ruta/al/TICKER.json> [--default]

El JSON del ticker debe cumplir references/schema.md. Se valida lo mínimo
(campos obligatorios, probabilidades de escenarios = 100) antes de escribir.
"""
import json
import re
import sys
from pathlib import Path

BLOCK = re.compile(r'(<script type="application/json" id="tickers-data">)(.*?)(</script>)', re.S)


def validate(t):
    for k in ("ticker", "name", "asOf", "periods", "sections", "analysis"):
        if k not in t:
            sys.exit(f"Falta el campo obligatorio: {k}")
    for s in t["sections"]:
        for r in s["rows"]:
            for k in ("key", "label", "v", "fmt"):
                if k not in r:
                    sys.exit(f"Fila sin '{k}' en la sección {s.get('id')}: {r}")
            if r.get("hist") and len(r["hist"]) != len(t["periods"]):
                sys.exit(f"{r['key']}: hist tiene {len(r['hist'])} valores y periods {len(t['periods'])}")
    sc = t["analysis"].get("scenarios")
    if sc and sum(x["prob"] for x in sc) != 100:
        sys.exit("Las probabilidades de los escenarios deben sumar 100")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        sys.exit(__doc__)
    html_path, json_path = Path(args[0]), Path(args[1])
    ticker = json.loads(json_path.read_text(encoding="utf-8"))
    validate(ticker)
    html = html_path.read_text(encoding="utf-8")
    m = BLOCK.search(html)
    if not m:
        sys.exit("No encontré el bloque tickers-data en el HTML")
    data = json.loads(m.group(2))
    data["tickers"][ticker["ticker"]] = ticker
    if "--default" in sys.argv or not data.get("default"):
        data["default"] = ticker["ticker"]
    body = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html_path.write_text(html[: m.start(2)] + body + html[m.end(2):], encoding="utf-8")
    print(f"OK: {ticker['ticker']} guardado. Tickers en el dashboard: {', '.join(data['tickers'])}")


if __name__ == "__main__":
    main()
