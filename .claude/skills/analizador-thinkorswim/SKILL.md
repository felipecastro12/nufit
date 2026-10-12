---
name: analizador-thinkorswim
description: Analiza los datos fundamentales de una empresa copiados de thinkorswim (captura de pantalla de la pestaña Fundamentals o texto pegado), saca conclusiones sobre su estado financiero y si conviene comprar la acción, y agrega el análisis al dashboard "Radar de Fundamentales". Úsala siempre que el usuario comparta una captura o tabla de thinkorswim con Share Values, Profitability, Financial Ratios, Valuation o Growth Rates, o pida "analiza esta empresa", "¿es buena compra?" con esos datos, aunque no nombre la skill.
---

# Analizador thinkorswim

Convierte una pantalla de Fundamentals de thinkorswim en un análisis de inversión y lo guarda en el dashboard compartido (`dashboard/index.html`, publicado como Artifact). Respondes siempre en español.

## Archivos del proyecto

- `dashboard/index.html`: dashboard. Los datos viven en el bloque `<script type="application/json" id="tickers-data">`. No lo edites a mano.
- `dashboard/data/<TICKER>.json`: copia legible de cada empresa. Es la fuente de verdad que editas.
- `dashboard/ARTIFACT_URL.txt`: URL del Artifact publicado. Si no existe, publica y guárdala.
- `scripts/upsert_ticker.py`: valida el JSON e inserta o reemplaza el ticker en el HTML.
- `references/schema.md`: estructura exacta del JSON. Léela antes de escribir uno nuevo.
- `references/rubrica.md`: umbrales para dar tono (good/ok/warn/bad) y notas a cada ratio, y cómo calcular las notas de 0 a 10.

## Flujo

1. **Transcribir.** Pasa cada fila de la captura al JSON, tal cual, sin redondear. `N/A` es `null`. Las columnas de la captura son: valor actual (TTM), crecimiento a 5 años, mini gráfico, y cinco años fiscales del más antiguo al más reciente. Pon en `periods` los cinco años fiscales (el más reciente es el último cerrado; confírmalo con el filing si dudas). Valoración y Crecimiento usan `extras` para los promedios de 3 y 5 años. Si un número es ilegible, pregunta al usuario en vez de adivinar.
2. **Verificar en vivo.** Invoca la skill `anthropic-skills:financial-advisor-pro` y sigue su filosofía: precio actual con fecha, rango de 52 semanas, fecha del próximo resultado, guía vigente (EPS y ventas), consenso de analistas, noticias de las últimas semanas. Usa WebSearch. Si las fuentes se contradicen (fechas, precios), dilo en el análisis. Nunca cites cifras de memoria como actuales.
3. **Cruzar con la captura.** Comprueba que precio ≈ P/E × EPS TTM y que capitalización ≈ precio × acciones. Si no cuadra, el precio de la captura puede estar desfasado: dilo.
4. **Calcular derivados** (anótalos en `tiles`): rendimiento FCF (FCF por acción ÷ precio), P/E sobre EPS ajustado de la guía, P/E con tasa de impuestos normalizada (EPS × (1 − 0.15) ÷ (1 − tasa actual)), valor esperado ponderado por escenarios.
5. **Analizar** con `references/rubrica.md`. Revisa siempre, en este orden: crecimiento y su ritmo frente al promedio, márgenes y su estabilidad, calidad de las utilidades (impuestos bajos, base baja, EPS contable frente a ajustado), caja libre, balance (deuda, cobertura, liquidez), valoración frente a su historia y frente al consenso, y el catalizador más cercano.
6. **Recomendar** en el formato de `financial-advisor-pro` (modo B): acción (Comprar, Acumular, Mantener, Recortar, Vender o Evitar), zona de entrada, invalidación, objetivos a 3 y 12 meses, tamaño de posición (mandato moderado: tope individual de 5% de la cartera total, 8% si es core), y tres escenarios (bajista, base, alcista) cuyas probabilidades sumen 100. No hay certeza: si es cara o cruz, dilo.
7. **Guardar y publicar.**
   ```bash
   python3 -I .claude/skills/analizador-thinkorswim/scripts/upsert_ticker.py dashboard/index.html dashboard/data/<TICKER>.json [--default]
   ```
   Luego publica `dashboard/index.html` con la herramienta Artifact pasando la URL de `dashboard/ARTIFACT_URL.txt` en `url`. Si el archivo no existe, publica sin `url` (icon `chart`) y guarda la URL nueva en `ARTIFACT_URL.txt`. Si la publicación avisa de un conflicto, lee la versión viva, fusiona y publica de nuevo.
8. **Responder** con un resumen corto: veredicto, tres razones, el riesgo principal, el plan (entrada, invalidación, tamaño) y el enlace al dashboard. Cierra con el disclaimer breve de `financial-advisor-pro`.
9. **Commit** de `dashboard/` en la rama de trabajo cuando el usuario lo pida o la sesión lo exija. No abras un pull request sin que lo pidan.

## Reglas

- Si el ticker ya existe, reemplázalo entero y conserva los demás tickers.
- Cada nota de ratio (`note`) explica el número de esa empresa en una o dos frases sencillas. El significado general del concepto vive en el diccionario `CONCEPTS` del HTML. Si aparece un concepto que no está ahí, agrégalo a `CONCEPTS` con `n`, `que` y `lectura`, usando la misma clave que pongas en `key`.
- Lenguaje sencillo, sin jerga innecesaria. Los términos estándar (P/E, FCF, ROE) se quedan en inglés.
- No inventes datos. Todo número del análisis sale de la captura o de una fuente con enlace en `sources`.
- Una captura es una foto de un momento: indica siempre la fecha del análisis (`asOf`).
