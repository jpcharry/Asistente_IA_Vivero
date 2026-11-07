"""Ejemplo opcional de integración real; necesita API key y acceso a Internet."""
import os

from app.clasificador import Incidencia, clasificar_incidencia
from app.proveedor_openai import ProveedorOpenAI


def principal() -> None:
    clave = os.getenv("OPENAI_API_KEY")
    if not clave:
        raise SystemExit("Falta OPENAI_API_KEY; usa 'python demo.py' para una demo sin red.")

    modelo = os.getenv("OPENAI_MODEL", "gpt-6-luna")
    proveedor = ProveedorOpenAI(clave, model=modelo)
    incidencias = {
        "INC-001": Incidencia("INC-001", "El conteo físico es 48 y el sistema muestra 60 plantas")
    }
    resultado = clasificar_incidencia(incidencias, "INC-001", proveedor)
    print("Prueba con proveedor externo configurado:")
    print(f"Categoría: {resultado.categoria_sugerida}")
    print(f"Estado: {incidencias['INC-001'].estado}")
    print(resultado.mensaje)


if __name__ == "__main__":
    principal()
