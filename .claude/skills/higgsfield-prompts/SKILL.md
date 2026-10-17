---
name: higgsfield-prompts
description: Crea prompts y configuraciones listas para pegar en Higgsfield (videos y anuncios de producto, UGC, try-on, escenas con modelo) para vender ropa deportiva de NuFit. Úsala siempre que el usuario mencione Higgsfield, video para Reels/TikTok/anuncios, "persona usando el producto", UGC, unboxing, prompt para video o imagen con IA, o quiera mejorar un resultado que no le gustó en Higgsfield, aunque no diga la palabra "prompt".
---

# Prompts para Higgsfield (NuFit)

Objetivo: que el usuario obtenga en Higgsfield exactamente lo que imagina, con pocos intentos y pocos créditos gastados. Un prompt vago produce videos genéricos y el producto se deforma; un prompt preciso, con el formato correcto y la imagen correcta de referencia, evita ambas cosas.

## Qué puede y qué no puede hacer el conector

El conector de Higgsfield en Claude solo permite ver créditos (`balance`), listar modelos (`models_list`, `models_get`), ver generaciones (`show_generations`) e importar videos de Claude Motion. **No genera ni sube archivos.** Por eso esta skill entrega un paquete que el usuario pega y ejecuta en Higgsfield. Nunca digas que ya generaste un video. Si el conector está disponible, consulta `models_get` del modelo elegido para confirmar parámetros vigentes, porque el catálogo cambia.

## Flujo

1. **Entender el pedido.** Define producto, objetivo (vender, mostrar ajuste, lanzar), plataforma (Reels, TikTok, anuncio, tienda), público, tono y qué imágenes tiene. Si el producto está en Shopify y hay conector, tómalo de ahí (título, colores, descripción). Pregunta solo lo que falte y que cambie el resultado, máximo 3 preguntas.
2. **Elegir herramienta y modelo** con la tabla de abajo.
3. **Escribir el prompt** con la estructura de abajo.
4. **Entregar el paquete** en el formato de salida.
5. **Iterar.** Si el resultado no gustó, pregunta qué falló y cambia **una sola variable** por intento (encuadre, luz, movimiento o duración). Cambiar todo a la vez impide saber qué ayudó y gasta créditos.

## Elegir herramienta (verificado en el catálogo de video)

| Necesidad | Opción | Notas |
|---|---|---|
| Anuncio de producto listo para Reels/TikTok | **Marketing Studio** (`marketing_studio_video`) | 12-15 s. Presets como UGC, Unboxing, Product Review, Tutorial y UGC Virtual Try On. Acepta avatar (máx. 1), producto, `hook_id` (gancho) y `setting_id` (lugar). |
| Persona usando la prenda | Marketing Studio, preset **UGC Virtual Try On** | Es el camino más directo para "modelo con el short". |
| Producto fiel y consistente, varias referencias | **Seedance 2.0** | Referencias de imagen/video/audio, identidad consistente, pensado para e-commerce y varios SKU. 4-15 s, hasta 4k. Hay versión Mini, más barata, hasta 720p. |
| Escena cinematográfica de marca | **Cinema Studio Video 3.0** | Mejor calidad, más créditos. |
| Imagen a video rápido y barato | Grok Video 1.5 Lite, Seedance 2.0 Mini | Para probar ideas antes de gastar en el modelo caro. |

Regla práctica: probar la idea en un modelo barato o Mini y pasar al modelo premium solo cuando el prompt ya funciona.

## Estructura del prompt

Escribe el prompt en **inglés** (los modelos de video suelen responder mejor) y da al usuario un resumen en español. Si hay voz o texto en pantalla, ese contenido va en español de Colombia. Incluye, en este orden:

1. **Sujeto y acción:** quién o qué aparece y qué hace, en una acción simple por toma.
2. **Fidelidad del producto:** color exacto, tela, logo y dónde está, detalles clave. Es lo que más se rompe, así que descríbelo siempre y pide mantenerlo sin cambios.
3. **Escenario y luz:** lugar, hora, tipo de luz.
4. **Cámara y movimiento:** plano (general, medio, detalle), movimiento (fijo, travelling lento, giro), ritmo.
5. **Estilo:** limpio, comercial, UGC natural, cinematográfico.
6. **Audio:** música, sonido ambiente o voz, o "sin audio".
7. **Restricciones:** qué evitar (texto inventado, logos distintos, manos deformes, cambios de color).

Principios: una idea clara por video; la imagen del producto debe ir como **imagen de referencia o primer cuadro**, no solo descrita; prefiere acciones concretas ("la modelo se ata el cordón y sale a correr") a adjetivos vagos ("dinámico, increíble").

## Formato de salida

Entrega siempre este bloque:

- **Herramienta y modelo:** nombre exacto, y por qué.
- **Parámetros:** duración, proporción (9:16 para Reels/TikTok), resolución, audio, preset/gancho/lugar si aplica.
- **Imágenes a subir:** cuáles y con qué rol (primer cuadro, referencia de producto, avatar).
- **Prompt (EN):** listo para copiar.
- **Resumen (ES):** qué va a pasar en el video.
- **Variante B:** una alternativa distinta, para probar.
- **Texto para el post:** gancho, copia y llamado a la acción en español.
- **Revisar al recibir el video:** ¿el color y el logo coinciden con el producto real?, ¿la prenda mantiene la forma?, ¿manos y proporciones normales?, ¿el movimiento es natural?

## Antes de generar

Recuerda al usuario revisar sus créditos (el conector puede consultarlos) y que la prenda que se muestra debe ser el producto real que vende: no uses el video para sugerir características que la prenda no tiene.
