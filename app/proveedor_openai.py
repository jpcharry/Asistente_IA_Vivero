"""Adaptador opcional a una IA real. No se utiliza red en las pruebas."""
from app.clasificador import ErrorProveedorIA


class ProveedorOpenAI:
    """Invoca Responses API y devuelve una categoría como texto."""

    def __init__(self, api_key: str, model: str = "gpt-6-luna") -> None:
        self.api_key = api_key
        self.model = model

    def __call__(self, descripcion: str) -> str:
        raise NotImplementedError("Se implementa después de las pruebas")
