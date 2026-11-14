# Asistente de IA para clasificar incidencias de inventario de vivero

**Autor:** Juan Pablo Charry Herrera  
**Asignatura:** Seminario Inteligencia Artificial Aplicada al Ciclo de Vida del Software  
**Entrega:** Semana 6 — revisión del primer incremento funcional

## 1. ¿Qué es el proyecto?

Prototipo académico que permite recibir una incidencia ya registrada de un vivero y guardar una **categoría sugerida** por un clasificador. Las categorías son **Inventario, Ventas, Interfaz y Otro**. La sugerencia queda en estado `PENDIENTE_REVISION`; ninguna decisión de IA modifica las existencias o las ventas.

**Historia de usuario HU-03 (Must, necesidad N-03):** Como empleado del vivero, quiero obtener una categoría inicial sugerida por IA para identificar el área del problema sin clasificarlo manualmente.

**Criterio normal:** Dado un reporte `INC-001` sobre diferencias entre el conteo físico y las plantas registradas, cuando el clasificador propone `Inventario`, entonces se guarda esa sugerencia y la incidencia permanece pendiente de revisión.

**Criterio de error:** Dado que `INC-003` existe, cuando el servicio no responde, entonces la incidencia se conserva sin nueva clasificación y se informa que es necesario reintentar.

**Alcance:** un módulo Python con incidencias guardadas en un diccionario en memoria, un proveedor de IA opcional y pruebas automatizadas. No incluye base de datos, aplicación web, autenticación ni clasificación real medida con datos del vivero.

### Contrato verificable

```python
def clasificar_incidencia(
    incidencias: dict[str, Incidencia],
    codigo: str,
    servicio_ia: Callable[[str], str],
) -> ResultadoClasificacion:
    ...
```

Recibe el repositorio en memoria, el identificador del reporte y un clasificador que acepta texto y devuelve una etiqueta. Retorna `ResultadoClasificacion(codigo, categoria_sugerida, mensaje)`. Acepta descripciones de **1 a 500 caracteres** sin contar espacios laterales. Normaliza mayúsculas y espacios de la categoría; rechaza etiquetas desconocidas sin cambiarlas automáticamente a `Otro`. Lanza `KeyError` si el código no existe y `ValueError` si la descripción es inválida. Una falla de red o formato deja la incidencia intacta y devuelve un mensaje de reintento.

| Ejemplo | Entrada | Resultado esperado |
|---|---|---|
| Normal 1 | Descripción de conteo erróneo, respuesta `Inventario` | Guarda `Inventario`, mantiene `PENDIENTE_REVISION` |
| Normal 2 | Problema de pantalla, respuesta `Interfaz` | Guarda `Interfaz` |
| Límite | Descripción de 500 caracteres, respuesta `Otro` | Admite el texto y guarda `Otro` |
| Error | Descripción de 501 caracteres | Lanza `ValueError`, no llama a la IA |
| Error del servicio | `TimeoutError` del proveedor | Conserva el registro y avisa que se reintente |

## 2. Requisitos

- Python **3.11 o superior**, Git y acceso a terminal.
- Dependencia de pruebas: `pytest==9.2.0` definida en `requirements.txt`.
- Herramientas de revisión: Ruff y pip-audit (se instalan aparte, no son necesarias para ejecutar la demo).
- **Opcional:** una clave de API de OpenAI y acceso a Internet para ejecutar `demo_ia_real.py`. La demo local no requiere clave.

## 3. Instalación

Desde una carpeta recién descargada o clonada, en **PowerShell**:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

En Linux/macOS: `python3 -m venv .venv`, `source .venv/bin/activate` y `python -m pip install -r requirements.txt`. Si PowerShell bloquea la activación, usa directamente `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` y el mismo ejecutable en los siguientes comandos.

## 4. Ejecución

**Demostración local (sin consumo real de IA):**

```powershell
python demo.py
```

**Demostración opcional con API real** (puede generar cargos y no fue probada con una clave real en esta entrega):

```powershell
$env:OPENAI_API_KEY = "TU_CLAVE_PRIVADA"
$env:OPENAI_MODEL = "gpt-6-luna"
python demo_ia_real.py
```

No publiques la clave ni la almacenes en un commit. `.env.example` solo muestra nombres de variables. La solicitud de red usa una URL fija HTTPS, bloquea redirecciones y limita el tamaño máximo de su respuesta.

## 5. Pruebas y revisión de seguridad

```powershell
python -m pytest -v
python -m pip install ruff
python -m ruff check .
python -m pip install pip-audit
python -m pip_audit -r requirements.txt
```

Se ejecutaron **18 pruebas en un entorno aislado:** 14 existentes de la semana 5 y 4 nuevas de seguridad (redirección, destino no autorizado, respuesta excesiva e integridad del reporte). Los 18 casos aprobaron. **El linter debe comprobarse de nuevo con Ruff en el equipo local o en GitHub Actions tras publicar estos cambios**; esta revisión no ejecutó Ruff en ese entorno aislado.

La auditoría anterior de GitHub Actions, sobre el commit `c1aab1b`, terminó con `No known vulnerabilities found`; al fijar versiones para semana 6, hay que volver a revisar la ejecución nueva. La auditoría solo evalúa vulnerabilidades **conocidas** en dependencias, no certifica la seguridad general del programa.

Historial TDD de la semana 5: `93b10a4` (pruebas en rojo), `7f877f0` (implementación verde), `cdedb58` (refactor), `977a1a9` (documentación). La semana 6 agrega las pruebas de abuso y el informe `revision_seguridad.md`.

## 6. Estructura del repositorio

```text
app/
  clasificador.py         Lógica de clasificación y validaciones
  proveedor_openai.py     Adaptador HTTPS opcional con controles de seguridad
tests/
  test_clasificador.py    Comportamientos originales de HU-03
  test_proveedor_openai.py   Pruebas simuladas del proveedor
  test_seguridad.py       Nuevas pruebas de abuso, semana 6
.github/workflows/
  auditoria.yml           Ruff, pytest y pip-audit en GitHub Actions
evidencias/              Registros de pruebas y comprobaciones previas
demo.py                   Ejemplo sin red
demo_ia_real.py           Ejemplo opcional con API
pyproject.toml            Reglas E, F, B y S de Ruff
requirements.txt          Dependencia fijada
revision_seguridad.md     Informe de revisión de seguridad
bitacora_ia.md           Decisiones sobre uso de IA
```

`.venv`, `.pytest_cache`, `.ruff_cache`, `__pycache__` y `.env` son archivos de entorno local y no deben subirse al repositorio.

## 7. Uso de inteligencia artificial

Se utilizó ChatGPT como apoyo para el contrato, la propuesta de pruebas, la implementación, la revisión y la refactorización. La **bitácora `bitacora_ia.md`** documenta las decisiones aceptadas, ajustadas y rechazadas, y separa los resultados de pruebas de la precisión real del modelo. En semana 6 se revisó el manejo de redirecciones, el límite de respuestas HTTP y los avisos del linter. **La clasificación automática no se validó con incidencias reales ni con una evaluación de precisión.**

## 8. Autor y licencia

**Juan Pablo Charry Herrera**, proyecto académico de Ingeniería de Software. **Licencia:** sin licencia de reutilización declarada; se reserva la decisión de publicar una licencia posteriormente. El código se conserva para evaluación educativa y las credenciales no se incluyen en el repositorio.
