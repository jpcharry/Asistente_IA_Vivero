# Informe de revisión de código y seguridad — Semana 6

**Proyecto:** Asistente de IA para incidencias del inventario de vivero  
**Estudiante:** Juan Pablo Charry Herrera · **Fecha:** 14/11/2026  
**Base revisada:** `c1aab1b` · **Commits de mejora:** `21f7b32`, `1c961da`

## 1. Herramientas y criterios

- **Linter:** Ruff 0.17.5 en el equipo del estudiante, reglas `E,F,B,S` configuradas en `pyproject.toml`. Antes de esta revisión reportó 37 avisos: 31 `S101` en pytest, cinco `E501` y un `S310`. Se formatearon las líneas largas, se justificó `S101` solo en `tests/` y se reemplazó la apertura HTTP original. **La ejecución definitiva de Ruff en el ZIP actualizado queda pendiente de GitHub Actions o del equipo del estudiante.**
- **Dependencias:** `pip-audit` en GitHub Actions registró `No known vulnerabilities found` sobre `c1aab1b`, antes de fijar la versión. El archivo actual contiene `pytest==9.2.0`; **debe revisarse de nuevo en el flujo actualizado**. El fallo local Windows `0xC0000005` fue del proceso de auditoría, no una vulnerabilidad identificada.
- **Pruebas:** se conservaron las 14 originales y se agregaron cuatro de abuso: **18/18 aprobadas** en el entorno de revisión. No se probó la conexión con credenciales reales.
- **Criterios:** legibilidad, entradas, errores, exposición de secretos, inyección, accesos, dependencias y envío de datos a terceros.

| Punto de seguridad | ¿Aplica? | Resultado |
|---|---|---|
| Inyección SQL | No: sin base de datos ni consultas SQL | No se construyen consultas con texto del usuario; se valida una etiqueta cerrada. |
| Secretos | Sí | Clave solo en parámetro/memoria; `.env` ignorado, `.env.example` ficticio. Búsqueda básica de patrones en cinco commits previos sin coincidencias sospechosas. |
| Contraseñas | No | El módulo no registra usuarios ni almacena contraseñas. |
| Control de acceso | No en este prototipo | No hay sesiones ni operaciones administrativas; la autenticación será requisito al integrar el módulo al sistema web. |
| Dependencias | Sí | Solo pytest como dependencia declarada y ahora fijada; auditoría remota anterior sin hallazgos conocidos. |

## 2. Hallazgos verificados y correcciones

| Id | Archivo y línea actual | Hallazgo, categoría y severidad | Corrección | Commit |
|---|---|---|---|---|
| H-01 | `app/proveedor_openai.py:16-34` | La apertura HTTP anterior podía seguir redirecciones que involucraran el encabezado Authorization. **Seguridad / CWE-918, media.** | Lista de destino HTTPS exacto y manejador que rechaza redirecciones; pruebas de abuso. | `21f7b32` |
| H-02 | `app/proveedor_openai.py:76-79` | Lectura de JSON externo sin límite de bytes. **Consumo de recursos / CWE-400, media.** | Tope de 65.536 bytes; al excederlo se conserva la incidencia. | `21f7b32` |
| H-03 | `requirements.txt:1` | Versión no fijada (`pytest>=8,<10`). **Dependencias / baja.** | Fijar `pytest==9.2.0`, versión identificada en el entorno entregado. | `21f7b32` |
| H-04 | `demo_ia_real.py:1` | El README anunciaba un archivo de demo real que no venía en el ZIP. **Omisión documental / baja.** | Agregar demo opcional que exige API key, sin incluir secretos. | `1c961da` |
| H-05 | `.github/workflows/auditoria.yml:14-37` | Acción de GitHub con aviso sobre Node.js 20 y sin ejecutar pruebas/linter. **CI/mantenimiento / baja.** | Usar acciones compatibles con Node 24 y ejecutar Ruff, pytest y pip-audit. | `1c961da` |

**Aviso descartado:** `S101` en `tests/*.py` es normal en pytest; se ignora solo allí, nunca en `app/`. **Advertencia revisada:** la URL fija impedía esquemas introducidos por usuarios, pero **no justificaba ignorar las redirecciones**; por eso se implementó H-01 en lugar de dejar únicamente `# noqa: S310`.

## 3. Segunda revisión con IA

**Consulta de revisión (síntesis del encargo en el chat):** «Examinar el ZIP de la Semana 5: validar la configuración Ruff, revisar peticiones externas y claves, comprobar dependencias, buscar fallos verificables, distinguir problemas reales de falsos positivos y mantener los tests anteriores».

| Sugerencia o hallazgo | Clasificación | Verificación |
|---|---|---|
| `S101` significa que los tests son inseguros | **Falso positivo** | Las aserciones son parte de pytest y las 14 pruebas originales pasan. |
| URL HTTPS fija elimina todos los riesgos de `urlopen` | **Conclusión incompleta** | Se detectó riesgo de redirecciones; se añadió prueba para impedir reenviar la petición. |
| Respuesta HTTP sin límite | **Real** | El código anterior llamaba `json.load()` sin tope; se añadió prueba de 65.537 bytes. |
| Declaración de pytest con rango de versiones | **Real** | Comparación directa con `requirements.txt` original. |

**Algo omitido en revisiones anteriores:** el README referenciaba `demo_ia_real.py` y ese archivo no estaba en el ZIP; se comprobó el listado real y se agregó. Se revisaron además los cinco commits anteriores en busca de patrones obvios de claves, sin hallazgos de exposición; ello no sustituye una auditoría completa de secretos.

## 4. Pendientes

| Pendiente | Razón | Plan |
|---|---|---|
| Confirmar ejecución actual de Ruff y pip-audit | El primer pase de pip-audit fue sobre el commit previo a los cambios; Ruff no se ejecutó en el entorno donde se preparó el ZIP. | Subir cambios, abrir Actions y comprobar los tres pasos; guardar captura. |
| Prueba real de API y privacidad | No se usó una clave ni datos auténticos del vivero. | Con autorización, probar datos ficticios, minimizar información personal y medir la calidad de las categorías. |
| Autorización por roles y almacenamiento | No forman parte de HU-03 aislada. | Definir permisos y pruebas de abuso antes de integrar el módulo con una API y BD. |

**Claves expuestas detectadas:** ninguna en la revisión de patrones realizada. No se incluyó `.env` ni una clave real en el archivo entregado.
