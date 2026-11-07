# Informe de verificación — HU-03

**Proyecto:** Asistente de IA para incidencias del inventario de vivero  
**Entorno de ejecución:** Python 3.13.5, pytest 9.0.2 (la implementación está escrita para Python 3.11 o superior)  
**Fecha:** 7 de noviembre de 2026  

## Matriz de pruebas automatizadas

| ID | Prueba | Tipo | Resultado final |
|---|---|---|---|
| P-01 | Clasificación Inventario y sugerencia guardada | Normal | Aprobada |
| P-02 | Clasificación Interfaz | Normal | Aprobada |
| P-03 | Clasificación Ventas con espacios y mayúsculas | Normal | Aprobada |
| P-04 | Categoría `Otro` | Límite de catálogo | Aprobada |
| P-05 | Descripción de 500 caracteres | Límite superior válido | Aprobada |
| P-06 | Descripción de 501 caracteres | Límite superior inválido | Aprobada |
| P-07 | Servicio de IA indisponible | Error HU-03 | Aprobada |
| P-08 | Categoría `Urgente` no permitida | Error de salida | Aprobada |
| P-09 | Incidencia inexistente | Error de entrada | Aprobada |
| P-10 | Descripción vacía | Error de entrada | Aprobada |
| P-11 | Reintento fallido conserva sugerencia anterior | Integridad | Aprobada |
| P-12 | Extraer categoría de respuesta HTTP simulada | Integración simulada | Aprobada |
| P-13 | Rechazar respuesta HTTP sin texto | Integración simulada | Aprobada |
| P-14 | Manejar caída de red en adaptador HTTP | Integración simulada | Aprobada |

## Secuencia TDD comprobada

1. **Pruebas rojas:** 14 fallaron por `NotImplementedError` (sin implementación), archivo `evidencias/01_pruebas_rojo.txt`.
2. **Intento preliminar:** 13 aprobaron y 1 falló por categoría no reconocida almacenada como `Otro`, archivo `evidencias/02_intento_con_error_detectado.txt`.
3. **Implementación:** 14 aprobaron, archivo `evidencias/03_pruebas_verde.txt`.
4. **Refactor:** 14 aprobaron sin cambiar las pruebas, archivo `evidencias/05_pruebas_tras_refactor.txt`.

## Qué NO comprueban estas pruebas

No miden precisión ni calidad predictiva de un modelo de IA real; validan la integración lógica y el tratamiento de sus salidas simuladas. No se probaron consultas HTTP reales ni persistencia en base de datos. Por eso **no corresponde afirmar que la clasificación real por IA está validada en producción**.
