"""Demostración local sin red: utiliza un clasificador de respuesta simulada."""
from app.clasificador import Incidencia, clasificar_incidencia


def principal() -> None:
    incidencias = {
        "INC-001": Incidencia(
            codigo="INC-001",
            descripcion="El sistema muestra 60 plantas pero el conteo físico es 48",
        )
    }
    resultado = clasificar_incidencia(incidencias, "INC-001", lambda _: "Inventario")
    print("Tipo de prueba: DEMOSTRACIÓN SIMULADA (sin modelo de IA real)")
    print(f"Incidencia: {resultado.codigo}")
    print(f"Categoría sugerida: {resultado.categoria_sugerida}")
    print(f"Estado: {incidencias['INC-001'].estado}")
    print(f"Resultado: {resultado.mensaje}")


if __name__ == "__main__":
    principal()
