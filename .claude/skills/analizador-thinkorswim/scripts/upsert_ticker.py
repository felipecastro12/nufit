#!/usr/bin/env python3
"""Inserta o reemplaza datos dentro del bloque JSON de dashboard/index.html.

Uso:
    python3 -I upsert_ticker.py <index.html> <TICKER.json> [--default]
    python3 -I upsert_ticker.py <index.html> <contexto.json> --context <clave>

El JSON del ticker debe cumplir references/schema.md. Se valida lo mínimo
(campos obligatorios, probabilidades de escenarios = 100, fair value ordenado).
Con --context se guarda un bloque de contexto de mercado (por ejemplo "brasil").
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
    a = t["analysis"]
    sc = a.get("scenarios")
    if sc and sum(x["prob"] for x in sc) != 100:
        sys.exit("Las probabilidades de los escenarios deben sumar 100")
    f = a.get("fair")
    if f:
        if not (f["low"] <= f["base"] <= f["high"]):
            sys.exit("fair: se exige low <= base <= high")
        if sc and any("px" not in x for x in sc):
            sys.exit("Con fair, cada escenario necesita 'px' numérico")


def validate_context(c):
    for k in ("asOf", "headline", "summary", "stats", "points", "calendar", "portfolio", "sources", "disclaimer"):
        if k not in c:
            sys.exit(f"Falta el campo obligatorio del contexto: {k}")


def main():
    argv = sys.argv[1:]
    ctx_key = None
    if "--context" in argv:
        i = argv.index("--context")
        ctx_key = argv[i + 1]
        del argv[i:i + 2]
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 2:
        sys.exit(__doc__)
    html_path, json_path = Path(args[0]), Path(args[1])
    obj = json.loads(json_path.read_text(encoding="utf-8"))
    html = html_path.read_text(encoding="utf-8")
    m = BLOCK.search(html)
    if not m:
        sys.exit("No encontré el bloque tickers-data en el HTML")
    data = json.loads(m.group(2))
    if ctx_key:
        validate_context(obj)
        data.setdefault("contexts", {})[ctx_key] = obj
        msg = f"OK: contexto '{ctx_key}' guardado."
    else:
        validate(obj)
        data["tickers"][obj["ticker"]] = obj
        if "--default" in argv or not data.get("default"):
            data["default"] = obj["ticker"]
        msg = f"OK: {obj['ticker']} guardado. Tickers en el dashboard: {', '.join(data['tickers'])}"
    body = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html_path.write_text(html[: m.start(2)] + body + html[m.end(2):], encoding="utf-8")
    print(msg)


if __name__ == "__main__":
    main()
