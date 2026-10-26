# Estructura del JSON de un ticker

Ejemplo completo: `dashboard/data/BSX.json`. El script `upsert_ticker.py` valida lo mínimo.

```jsonc
{
  "ticker": "BSX",
  "name": "Boston Scientific",
  "exchange": "NYSE · USD",
  "asOf": "2026-10-12",                 // fecha del análisis
  "source": "thinkorswim (pestaña Fundamentals)",
  "type": "company",                    // company | etf
  "tags": ["brasil"],                   // opcional: agrupa tickers en una vista de contexto
  "periods": ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"],   // más antiguo primero, 5 valores; [] si no hay captura
  "sections": [
    {
      "id": "shares",                   // shares, profit, activity, fin, valuation, growth, owners
      "title": "Valores por acción",
      "rows": [
        {
          "key": "eps",                 // clave del diccionario CONCEPTS del HTML
          "label": "Earnings Per Share - TTM",   // nombre original de thinkorswim
          "v": 2.47,                    // valor actual; null si es N/A; texto si fmt = "txt"
          "chg": 55.20,                 // opcional: columna de crecimiento a 5 años, en %
          "hist": [0.69, 0.45, 1.07, 1.25, 1.94],  // opcional: 5 valores (null si falta uno)
          "extras": [{"l": "Promedio 5 años", "v": 59.698, "fmt": "x"}],  // opcional
          "fmt": "usd",                 // usd | pct | x | num | int | txt
          "tone": "good",               // good | ok | warn | bad
          "note": "Una o dos frases sencillas sobre este número en esta empresa."
        }
      ]
    }
  ],
  "analysis": {
    "verdict": {"rating": "Acumular en tramos", "tone": "warn", "headline": "Una frase."},
    "summary": "Un párrafo: qué dicen los números, qué descuenta el mercado, por qué esa acción.",
    "range": {"low": 42.20, "high": 105.65, "price": 42.73, "label": "Rango de 52 semanas"},
    "fair": {                           // obligatorio en análisis nuevos
      "price": 11.24, "priceTag": "premarket 26-oct",
      "low": 9.5, "base": 13.5, "high": 17.5,        // deben coincidir con los px de los escenarios
      "method": "Qué método se usó, en una frase.",
      "assumptions": [{"label": "EPS", "value": "..."}],
      "caveat": "Qué es estimación propia."
    },
    "brazil": {"level": "Muy alta", "summary": "...", "points": [{"label": "Tipo de cambio", "text": "..."}]},   // sensibilidad al contexto
    "next": "Q3: 12-nov",                // próximo evento, aparece en la tabla comparativa
    "tiles": [{"label": "Precio", "value": "$42.73", "sub": "Cierre del 9-oct-2026", "tone": "good"}],
    "scores": [{"label": "Crecimiento", "score": 8, "text": "Una frase con el dato."}],
    "strengths": ["..."],
    "risks": ["..."],
    "scenarios": [{"name": "Bajista", "prob": 25, "px": 9.5, "tone": "bad", "text": "..."}],   // px numérico; price (texto) es opcional
    "plan": [{"label": "Acción", "value": "..."}],
    "sources": [{"t": "Título", "u": "https://..."}],
    "disclaimer": "Análisis con fines educativos..."
  }
}
```

## Claves de `key` que ya tienen explicación en el HTML

Valores por acción: `eps`, `dps`, `bvps`, `cfps`, `fcfps`, `sps`.
Rentabilidad: `roe`, `roa`, `gross`, `opm`, `tax`, `interest`, `npm`.
Actividad: `assetturn`, `invturn`.
Salud financiera: `ltdebt`, `leverage`, `fixedcov`, `payout`, `quick`, `current`.
Valoración: `pe`, `pcf`, `pb`, `mcapeq`, `divyield`, `divpayout`.
Crecimiento: `g_rev`, `g_ni`, `g_eps`, `g_dps`, `g_bvps`.
Acciones y propiedad: `shares`, `float`, `mcap`, `borrow`, `inst`.

## Notas

- Los porcentajes de thinkorswim ya vienen en %, guárdalos así (15.339 es 15.3%).
- Los escenarios deben sumar 100.
- `hist` debe tener el mismo largo que `periods`.

## Contexto de mercado (`contexts.<clave>`)

Se guarda con `upsert_ticker.py <index.html> <archivo.json> --context <clave>`. Campos obligatorios: `asOf`, `headline`, `summary`, `stats` (tiles), `points` (`h` y `t`), `calendar` (`when`, `what`, `why`), `portfolio` (lista de reglas de cartera), `sources`, `disclaimer`. Ejemplo: `dashboard/data/context-brasil.json`.
