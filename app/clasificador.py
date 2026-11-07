"""HU-03: sugerir la categoría de una incidencia y conservarla para revisión."""
from collections.abc import Callable
from dataclasses import dataclass


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
    """Implementación pendiente: las pruebas deben fallar antes de programarla."""
    raise NotImplementedError("Primero se escriben las pruebas (TDD rojo)")
