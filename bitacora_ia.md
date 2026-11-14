# Bitácora de uso de IA — Semana 5

**Proyecto:** Asistente de IA para clasificar incidencias en un sistema de inventario de vivero  
**Estudiante:** Juan Pablo Charry Herrera  
**Funcionalidad:** HU-03 · Obtener una categoría inicial sugerida por IA (Must)  
**Asistente usado:** ChatGPT, modalidad chat para diseño, pruebas, implementación y revisión.  
**Fecha de elaboración:** 2026-11-07  

**Cómo leer esta bitácora:** registra sugerencias y decisiones tomadas durante la preparación del prototipo en esta conversación. La plantilla permite registrar **«prompt o sugerencia»**; los textos siguientes son sugerencias concretas utilizadas en el proceso, no transcripciones inventadas de cinco conversaciones independientes. Los resultados de pruebas y el historial de commits sí se ejecutaron y se adjuntan. El estudiante debe revisar que el texto refleje su participación antes de presentarlo como bitácora personal.

## Entradas

### Entrada 1 — Contrato verificable para la HU-03

- **Fecha:** 2026-11-07.
- **Prompt o sugerencia:** «Separar la HU-03 en una sola función `clasificar_incidencia`, que reciba una incidencia existente y un clasificador inyectable; dejarla pendiente de revisión y evitar modificar existencias».
- **Decisión:** **Aceptada**.
- **Por qué:** el documento de requisitos exige una categoría propuesta, guardada como sugerencia inicial, y revisión humana; no exige resolver automáticamente la incidencia.
- **Verificación:** contrasté el contrato del README con los dos escenarios HU-03 y comprobé los casos con las pruebas de `tests/test_clasificador.py`.
- **Commit relacionado:** `93b10a4` · `test: registrar pruebas HU-03 en rojo`.

### Entrada 2 — Pruebas antes de la implementación

- **Fecha:** 2026-11-07.
- **Prompt o sugerencia:** «Escribir al menos cinco pruebas pytest: dos normales, dos límites y una de caída del clasificador; también validar entradas e impedir modificaciones del reporte cuando hay error».
- **Decisión:** **Aceptada con cambios**.
- **Por qué:** amplié el mínimo a 14 pruebas incluyendo categorías no permitidas, límite de 500 caracteres, ID inexistente, reclasificación fallida y comportamiento del adaptador HTTP sin Internet.
- **Verificación:** `evidencias/01_pruebas_rojo.txt` registra **14 pruebas fallidas** por `NotImplementedError` antes del código; el primer commit contiene las pruebas y los marcadores sin implementación.
- **Commit relacionado:** `93b10a4` · `test: registrar pruebas HU-03 en rojo`.

### Entrada 3 — No transformar una salida inválida en «Otro»

- **Fecha:** 2026-11-07.
- **Prompt o sugerencia:** «En el primer intento de implementación, tratar con `else` cualquier respuesta no reconocida de la IA como categoría `Otro`».
- **Decisión:** **Rechazada**.
- **Por qué:** una respuesta como `Urgente` no corresponde a una de las cuatro categorías. Convertirla a `Otro` ocultaría una salida inválida y guardaría una sugerencia que la IA no emitió.
- **Verificación:** `evidencias/02_intento_con_error_detectado.txt` documenta **1 fallo y 13 pruebas aprobadas**; falló `test_error_categoria_invalida_se_rechaza_en_vez_de_convertirla_a_otro`. Reemplacé la rama genérica por validación explícita. Después: **14/14** aprobadas (`evidencias/03_pruebas_verde.txt`).
- **Commit relacionado:** `7f877f0` · `feat: clasificar incidencias y pasar pruebas HU-03` (incluye la corrección que quedó aceptada).

### Entrada 4 — Integración de IA separada de la lógica del negocio

- **Fecha:** 2026-11-07.
- **Prompt o sugerencia:** «Permitir que la función use un servicio externo y, al mismo tiempo, ejecutar las pruebas con un doble de prueba para que sean repetibles y no necesiten claves de API».
- **Decisión:** **Aceptada con cambios**.
- **Por qué:** el módulo principal recibe `Callable[[str], str]`; el adaptador `ProveedorOpenAI` va en otro archivo y usa una API key solo en memoria. El programa también ofrece `demo.py` con respuesta simulada. No añadí dependencias de red para pytest ni una conexión automática.
- **Verificación:** tres pruebas en `tests/test_proveedor_openai.py` simulan la respuesta JSON, una respuesta vacía y una caída de red; todas pasaron sin solicitudes HTTP reales.
- **Commit relacionado:** `7f877f0` · `feat: clasificar incidencias y pasar pruebas HU-03`.

### Entrada 5 — Refactor de validación de categorías

- **Fecha:** 2026-11-07.
- **Prompt o sugerencia:** «Cambiar la secuencia `if/elif` usada para normalizar categorías por un catálogo centralizado y una función auxiliar que permita consultar las etiquetas válidas».
- **Decisión:** **Aceptada**.
- **Por qué:** el catálogo de cuatro opciones se define en un solo lugar, el cuerpo principal queda más corto y se reduce el riesgo de inconsistencias al mantener las etiquetas.
- **Verificación:** después del refactor se ejecutó `python -m pytest -v`: **14 passed** en `evidencias/05_pruebas_tras_refactor.txt`. No se cambió ningún archivo de `tests/` desde el primer commit.
- **Commit relacionado:** `cdedb58` · `refactor: simplificar normalizacion de categorias`.

## Resumen

| Decisión | Cantidad |
|---|---:|
| Aceptadas | 2 |
| Aceptadas con cambios | 2 |
| Rechazadas | 1 |
| **Total** | **5** |

## Errores que atraparon las pruebas

El primer intento del clasificador transformaba cualquier salida desconocida en `Otro`. La prueba `test_error_categoria_invalida_se_rechaza_en_vez_de_convertirla_a_otro` encontró el defecto: cuando la IA respondía `Urgente`, el código guardaba `Otro` en la incidencia. La ejecución registró **1 failed, 13 passed**. Corregí la validación para guardar únicamente una categoría perteneciente al catálogo y retornar `La IA devolvió una categoría no permitida` en otro caso. Después de corregirlo y, más tarde, refactorizar, las **14 pruebas aprobaron**.

## Reflexión final (7 líneas)

El asistente de IA me permitió estructurar la HU-03 y el contrato de la función.  
También ayudó a proponer las pruebas antes de escribir la implementación.  
Lo más útil fue poder probar el comportamiento sin conectarme a una API externa.  
La dificultad principal apareció al aceptar categorías que no estaban en el catálogo.  
Una prueba detectó que `Urgente` se convertía por error en `Otro`, por lo que se corrigió.  
Luego mejoré el código con un diccionario de categorías y comprobé que las 14 pruebas seguían pasando.  
En un próximo trabajo definiría primero más casos inválidos y validaría el contrato con el cliente del vivero.

## Evidencias verificables

- Rojo inicial: `evidencias/01_pruebas_rojo.txt`.
- Defecto real del primer intento: `evidencias/02_intento_con_error_detectado.txt`.
- Verde tras implementación: `evidencias/03_pruebas_verde.txt`.
- Demostración sin IA real: `evidencias/04_demo_simulada.txt`.
- Verde tras refactor: `evidencias/05_pruebas_tras_refactor.txt`.
- Historial: `git log --oneline --reverse` y `git show <hash>`.

**Límites declarados:** la API de IA real no se ha utilizado con credenciales en este entorno; las 14 pruebas son automatizadas con respuestas controladas. No hay verificación de exactitud de IA frente a incidencias auténticas del vivero, ni base de datos persistente en esta semana.

---

# Semana 6 — Revisión de código y seguridad (14/11/2026)

Estas entradas describen la revisión técnica realizada con asistencia de ChatGPT
sobre el ZIP del proyecto. El estudiante debe verificar el diff y los resultados
en su propio repositorio antes de presentar las decisiones como propias.

### Entrada S6-01 — Segunda revisión de seguridad con IA

- **Fecha:** 2026-11-14.
- **Consulta/sugerencia revisada:** «Examinar `app/clasificador.py`, `app/proveedor_openai.py`, las pruebas y la configuración; comprobar las advertencias Ruff, detectar problemas reales y separar falsos positivos» (síntesis de la solicitud y el intercambio de esta semana).
- **Decisión:** **Aceptada con ajustes**.
- **Razón:** Los 31 avisos `S101` son válidos en pytest; el `S310` se había justificado inicialmente por usar una URL fija, pero eso no resolvía redirecciones. Se hizo una comprobación más específica.
- **Verificación:** se leyó la implementación `urlopen()` y el manejo de redirecciones de `urllib.request`; se identificó que había que bloquear destinos externos. Los archivos del ZIP se contrastaron con la documentación.
- **Defecto de la IA detectado:** aceptar una anotación `# noqa: S310` sin analizar la posibilidad de redirección era insuficiente.
- **Corrección:** lista de URL permitida, bloqueo de redirecciones y pruebas nuevas. **Commit:** `21f7b32`.

### Entrada S6-02 — Corrección y pruebas de abuso

- **Fecha:** 2026-11-14.
- **Prompt/sugerencia:** «Limitar la respuesta de la API a una cantidad controlada de bytes y comprobar que una petición redirigida o una respuesta excesiva no cambie una incidencia».
- **Decisión:** **Aceptada**.
- **Razón:** `json.load()` leía sin límite el cuerpo de una respuesta externa; una respuesta descontrolada podía consumir recursos.
- **Verificación:** se agregaron cuatro pruebas en `tests/test_seguridad.py`, sin modificar las 14 originales. El resultado en el entorno de revisión fue **18 passed**.
- **Defectos encontrados:** lectura sin límite y ausencia de prueba contra direcciones no autorizadas.
- **Corrección:** límite de 65.536 bytes y validación del destino fijo. **Commit:** `21f7b32`.

### Entrada S6-03 — Dependencias, README y automatización

- **Fecha:** 2026-11-14.
- **Prompt/sugerencia:** «Actualizar la documentación con las ocho secciones exigidas, fijar versiones y hacer que GitHub Actions ejecute linter, pruebas y auditoría».
- **Decisión:** **Aceptada con ajustes**.
- **Razón:** el `README` anunciaba `demo_ia_real.py`, inexistente en el ZIP; además, pytest no estaba fijado a una versión exacta y la acción original mostraba un aviso de Node.js 20.
- **Verificación:** se cotejó el listado del ZIP con el README, se inspeccionó `requirements_auditoria.txt` y se observó una ejecución anterior de GitHub Actions con `No known vulnerabilities found` sobre `c1aab1b`.
- **Corrección:** demo opcional sin secretos, `pytest==9.2.0`, README de ocho secciones y flujo que reúne Ruff, pytest y pip-audit. **Commit:** `1c961da`.
- **Pendiente de verificar:** repetir el flujo de GitHub Actions con este nuevo commit antes de declarar aprobada la auditoría actualizada.

**Reflexión de semana 6 (6 líneas).**  
La IA ayudó a ubicar los controles de seguridad más relevantes para el módulo.  
La revisión recordó que un linter limpio no garantiza un cliente HTTP seguro.  
El riesgo de redirección obligó a corregir una justificación anterior demasiado rápida.  
Las nuevas pruebas comprobaron que los errores del proveedor no alteran el reporte.  
También fue necesario ajustar el README a los archivos realmente presentes.  
Antes de entregar, debo ejecutar el flujo actualizado en GitHub y revisar sus resultados.
