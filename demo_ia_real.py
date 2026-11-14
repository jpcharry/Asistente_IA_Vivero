"""Demostración opcional con un modelo real; requiere OPENAI_API_KEY."""

import os

from app.clasificador import Incidencia, clasificar_incidencia
from app.proveedor_openai import ProveedorOpenAI


def principal() -> None:
    """Clasifica un reporte de ejemplo o termina si no se configuró la clave."""
    clave = os.getenv("OPENAI_API_KEY", "").strip()
    if not clave:
        raise SystemExit("Configura OPENAI_API_KEY antes de ejecutar esta demo")
    modelo = os.getenv("OPENAI_MODEL", "gpt-6-luna")
    incidencias = {
        "INC-DEMO": Incidencia(
            codigo="INC-DEMO",
            descripcion="El inventario muestra 60 plantas y contamos 48",
        )
    }
    resultado = clasificar_incidencia(
        incidencias, "INC-DEMO", ProveedorOpenAI(clave, model=modelo)
    )
    print(f"Incidencia: {resultado.codigo}")
    print(f"Categoría propuesta: {resultado.categoria_sugerida}")
    print(f"Estado: {incidencias['INC-DEMO'].estado}")
    print(f"Mensaje: {resultado.mensaje}")


if __name__ == "__main__":
    principal()
