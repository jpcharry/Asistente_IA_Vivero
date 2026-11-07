# Asistente de IA para incidencias en inventario de vivero

**Estudiante:** Juan Pablo Charry Herrera  
**Curso:** Seminario Inteligencia Artificial Aplicada al Ciclo de Vida del Software  
**Entrega:** Semana 5 · Primera funcionalidad con pruebas y bitácora de IA  
**Lenguaje:** Python 3.11+ · **Pruebas:** pytest

## 1. Funcionalidad de la semana 5

### Historia seleccionada — HU-03 (Must), necesidad N-03

> Como empleado del vivero, quiero obtener una categoría inicial sugerida por IA para identificar el área del problema sin clasificarlo manualmente.

Criterios Gherkin (del documento de requisitos, semana 3):

- **Escenario normal:** Dado que INC-001 contiene «El sistema muestra 60 plantas, pero el conteo físico es 48», cuando se solicita clasificar el reporte, entonces el asistente devuelve «Inventario» y guarda esa sugerencia inicial en INC-001.
- **Escenario de error:** Dado que INC-003 existe y el servicio clasificador no responde, cuando se solicita la clasificación, entonces INC-003 conserva el reporte, queda sin categoría sugerida y se muestra «No fue posible clasificar; intente de nuevo».

**Alcance de este corte:** clasificar un reporte existente, validar la categoría, guardar la sugerencia en un repositorio **en memoria** y conservar el estado `PENDIENTE_REVISION`. El módulo no cambia existencias, ventas ni prioridades, y no reemplaza la revisión humana. Una base de datos persistente queda fuera de esta primera función.

### Contrato de la función

```python
def clasificar_incidencia(
    incidencias: dict[str, Incidencia],
    codigo: str,
    servicio_ia: Callable[[str], str],
) -> ResultadoClasificacion:
    ...
```

- **Entrada `incidencias`:** diccionario donde las claves son los códigos de las incidencias (por ejemplo, `INC-001`). Cada `Incidencia` tiene `codigo`, `descripcion`, `categoria_sugerida` y `estado`.
- **Entrada `codigo`:** identificador de una incidencia existente.
- **Entrada `servicio_ia`:** función o adaptador que recibe la descripción y devuelve una sola categoría textual. Puede ser una respuesta simulada durante las pruebas o el proveedor real opcional.
- **Salida:** `ResultadoClasificacion(codigo, categoria_sugerida, mensaje)`.
- **Efecto permitido:** si la categoría es válida, se **reemplaza solo el registro del diccionario** con una copia que incluye la sugerencia. Su `descripcion` y `estado` se conservan. No hay escritura en bases de datos ni ajuste de inventario.
- **Categorías válidas:** `Inventario`, `Ventas`, `Interfaz`, `Otro`. Se toleran espacios al inicio/final y diferencias entre mayúsculas/minúsculas; **no** se aceptan categorías fuera del catálogo.
- **Longitud admitida:** entre **1 y 500 caracteres** de descripción, excluyendo espacios laterales. El máximo corresponde a la condición de 500 caracteres usada para las pruebas de rendimiento propuestas en la semana 3; debe validarse con el cliente.
- **Incidencia inexistente:** se lanza `KeyError`; no se consulta la IA.
- **Descripción vacía o de más de 500 caracteres:** se lanza `ValueError`; no se consulta la IA.
- **Servicio no disponible:** si el proveedor lanza un error de red, tiempo de espera o formato, el registro **no se modifica** y se devuelve una respuesta sin nueva categoría y el mensaje del escenario de error.
- **Categoría devuelta fuera de catálogo:** se rechaza sin guardar nada y se retorna `La IA devolvió una categoría no permitida`. La respuesta `Urgente` **no** debe convertirse automáticamente en `Otro`.

Los nombres de clases y los supuestos técnicos son decisiones de implementación de la semana 5; no equivalen a nuevos requisitos validados por el cliente.

### Ejemplos de entrada y salida

| Caso | Entrada | Salida esperada |
|---|---|---|
| 1. Inventario | `INC-001` con discrepancia de plantas; IA devuelve `Inventario` | `categoria_sugerida="Inventario"`; queda almacenada y en estado pendiente |
| 2. Interfaz | `INC-002` con error de pantalla; IA devuelve `Interfaz` | `categoria_sugerida="Interfaz"`; queda almacenada |
| 3. Otro | `INC-005`; IA devuelve `Otro` | `categoria_sugerida="Otro"` sin reinterpretación |
| 4. Falla del servicio | `INC-003`; IA lanza `TimeoutError` | `categoria_sugerida=None`, mensaje de error; reporte intacto |
| 5. Respuesta inválida | `INC-001`; IA devuelve `Urgente` | `categoria_sugerida=None`, mensaje de categoría no permitida |

## 2. Preparación en Windows (PowerShell)

```powershell
cd ruta\a\Charry_JuanPablo_S5_AsistenteIA_Vivero
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si `py -3` no está disponible, usa `python -m venv .venv`. Si PowerShell bloquea el script, puedes omitir la activación y ejecutar `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` y luego las pruebas con ese mismo ejecutable.

### Cómo ejecutar las pruebas

Desde la **raíz** del proyecto (donde está `requirements.txt`):

```powershell
python -m pytest -v
```

Para ejecutar una demostración sin clave de API ni Internet:

```powershell
python demo.py
```

La demo usa una **respuesta simulada**; no prueba que un modelo de IA real acierte la categoría. Los tests automatizados simulan el comportamiento del proveedor y comprueban que la aplicación acepta o rechaza su salida conforme al contrato.

## 3. Proveedor real opcional

El archivo `app/proveedor_openai.py` incluye un adaptador a la **Responses API** por HTTPS usando solo la librería estándar. Esta conexión es opcional y **no se ha ejecutado contra una cuenta real**: requeriría una API key del usuario y puede generar costos. La integración se comprueba con pruebas que simulan HTTP, sin Internet.

En PowerShell (solo en tu equipo, nunca publiques la clave):

```powershell
$env:OPENAI_API_KEY = "TU_API_KEY"
$env:OPENAI_MODEL = "gpt-6-luna"
python demo_ia_real.py
```

El nombre del modelo puede ajustarse según los modelos habilitados en tu cuenta. No se envían números de teléfono, contraseñas ni otros datos personales en los ejemplos.

## 4. Evidencia TDD y control de versiones

El historial de Git contiene, en orden:

1. `test: registrar pruebas HU-03 en rojo` — pruebas diseñadas antes de la implementación; la función era un marcador que lanzaba `NotImplementedError`.
2. `feat: clasificar incidencias y pasar pruebas HU-03` — implementación y pruebas en verde.
3. `refactor: simplificar normalizacion de categorias` — mejora de estructura sin modificar las pruebas.
4. `docs: documentar bitacora y verificaciones` — bitácora con decisiones y evidencias.

Consulta el historial con `git log --oneline --reverse` y las diferencias de cada etapa con `git show <hash>`. Los archivos en `evidencias/` guardan resultados de las ejecuciones. **Las pruebas no se modificaron después del primer commit.**

## 5. Límites y uso responsable

- No se entrenó un modelo con datos reales del vivero ni se midió precisión del proveedor; la clasificación de ejemplo depende de la respuesta simulada o, si se configura, de un servicio externo.
- `dict` es almacenamiento de demostración y pierde datos al terminar el programa; integración con una base de datos persistente queda para otra semana.
- Una categoría propuesta por IA siempre queda pendiente de revisión humana. No se modifican existencias.
- No subas `.env`, claves privadas, contraseñas ni registros reales de clientes. El `.gitignore` evita versionar archivos de entorno comunes.
- El documento de semana 3 marca las citas de entrevista como simuladas. No se presentan como transcripción verificada ni como requisitos ya validados.

## 6. Entrega

Subir este repositorio a GitHub y pegar la URL en Moodle. Si no se puede usar GitHub, entregar el ZIP **con la carpeta `.git` incluida** para que el docente revise los commits. Consulta `GUIA_ENTREGA.md`.
