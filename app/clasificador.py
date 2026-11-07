"""HU-03: sugerir la categoría de una incidencia y conservarla para revisión.

La fuente de la clasificación es inyectable para comprobar el contrato sin red.
"""
from collections.abc import Callable
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Incidencia:
    codigo: str
    descripcion: str
    categoria_sugerida: str | None = None
    estado: str = "PENDIENTE_REVISION"


@dataclass(frozen=True)
class ResultadoClasificacion:
    codigo: str
    categoria_sugerida: str | None
    mensaje: str


class ErrorProveedorIA(RuntimeError):
    """El servicio de IA respondió con un formato inservible."""


def clasificar_incidencia(
    incidencias: dict[str, Incidencia],
    codigo: str,
    servicio_ia: Callable[[str], str],
) -> ResultadoClasificacion:
    """Valida un reporte existente y guarda una categoría propuesta por IA."""
    incidencia = incidencias[codigo]  # La inexistencia debe levantar KeyError.
    descripcion = incidencia.descripcion.strip()
    if not 1 <= len(descripcion) <= 500:
        raise ValueError("La descripción debe contener entre 1 y 500 caracteres")

    try:
        respuesta = servicio_ia(descripcion)
    except (OSError, ErrorProveedorIA):
        return ResultadoClasificacion(
            codigo, None, "No fue posible clasificar; intente de nuevo"
        )

    if not isinstance(respuesta, str):
        return ResultadoClasificacion(codigo, None, "La IA devolvió una categoría no permitida")

    categoria_texto = respuesta.strip().casefold()
    if categoria_texto == "inventario":
        categoria = "Inventario"
    elif categoria_texto == "ventas":
        categoria = "Ventas"
    elif categoria_texto == "interfaz":
        categoria = "Interfaz"
    elif categoria_texto == "otro":
        categoria = "Otro"
    else:
        return ResultadoClasificacion(
            codigo, None, "La IA devolvió una categoría no permitida"
        )

    incidencias[codigo] = replace(incidencia, categoria_sugerida=categoria)
    return ResultadoClasificacion(codigo, categoria, "Categoría sugerida; pendiente de revisión")
