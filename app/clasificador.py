"""HU-03: sugerir una categoría de incidencia y dejarla para revisión.

Se inyecta el clasificador para probar la función sin conexión a Internet.
"""

from collections.abc import Callable
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Incidencia:
    """Reporte en memoria con código, descripción, sugerencia y estado."""

    codigo: str
    descripcion: str
    categoria_sugerida: str | None = None
    estado: str = "PENDIENTE_REVISION"


@dataclass(frozen=True)
class ResultadoClasificacion:
    """Resultado que la operación de clasificación devuelve al solicitante."""

    codigo: str
    categoria_sugerida: str | None
    mensaje: str


class ErrorProveedorIA(RuntimeError):
    """El proveedor de IA respondió con un formato no utilizable."""


CATEGORIAS_PERMITIDAS = {
    "inventario": "Inventario",
    "ventas": "Ventas",
    "interfaz": "Interfaz",
    "otro": "Otro",
}


def _categoria_valida(respuesta: object) -> str | None:
    """Normaliza una categoría válida o devuelve ``None`` si no coincide."""
    if not isinstance(respuesta, str):
        return None
    return CATEGORIAS_PERMITIDAS.get(respuesta.strip().casefold())


def clasificar_incidencia(
    incidencias: dict[str, Incidencia],
    codigo: str,
    servicio_ia: Callable[[str], str],
) -> ResultadoClasificacion:
    """Clasifica un reporte existente sin modificar existencias del vivero.

    Recibe un diccionario de incidencias, un código y un clasificador.
    Devuelve una sugerencia con su mensaje, o un error recuperable sin
    modificar el registro. Conserva el estado pendiente de revisión.

    Lanza ``KeyError`` para códigos inexistentes y ``ValueError`` para
    descripciones vacías o mayores de 500 caracteres (sin espacios laterales).
    """
    incidencia = incidencias[codigo]
    descripcion = incidencia.descripcion.strip()
    if not 1 <= len(descripcion) <= 500:
        raise ValueError("La descripción debe contener entre 1 y 500 caracteres")

    try:
        respuesta = servicio_ia(descripcion)
    except (OSError, ErrorProveedorIA):
        return ResultadoClasificacion(
            codigo, None, "No fue posible clasificar; intente de nuevo"
        )

    categoria = _categoria_valida(respuesta)
    if categoria is None:
        return ResultadoClasificacion(
            codigo, None, "La IA devolvió una categoría no permitida"
        )

    incidencias[codigo] = replace(incidencia, categoria_sugerida=categoria)
    return ResultadoClasificacion(
        codigo,
        categoria,
        "Categoría sugerida; pendiente de revisión",
    )
