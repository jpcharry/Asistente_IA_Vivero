"""Pruebas nuevas de seguridad incorporadas durante la semana 6."""

from io import BytesIO
from urllib.request import HTTPRedirectHandler, Request, build_opener

import pytest

import app.proveedor_openai as modulo
from app.clasificador import ErrorProveedorIA, Incidencia, clasificar_incidencia
from app.proveedor_openai import (
    MAX_BYTES_RESPUESTA,
    ProveedorOpenAI,
    _BloquearRedirecciones,
)


def test_abuso_redireccion_externa_no_se_sigue():
    """Una respuesta 302 no puede reenviar Authorization a otra dirección."""
    opener = build_opener(_BloquearRedirecciones())
    manejadores = [
        h for h in opener.handlers if isinstance(h, HTTPRedirectHandler)
    ]
    assert len(manejadores) == 1
    solicitud = Request("https://api.openai.com/v1/responses", method="POST")
    nueva = manejadores[0].redirect_request(
        solicitud,
        None,
        302,
        "Found",
        {"Location": "https://ejemplo-no-autorizado.invalid/"},
        "https://ejemplo-no-autorizado.invalid/",
    )
    assert nueva is None


def test_abuso_url_no_autorizada_se_rechaza():
    """No admite esquemas file: ni destinos externos."""
    with pytest.raises(ValueError, match="Destino HTTP no permitido"):
        modulo.urlopen(Request("file:///etc/passwd"), timeout=1)


def test_abuso_respuesta_excesiva_se_rechaza(monkeypatch):
    """Una respuesta HTTP grande no puede consumirse sin límite."""
    monkeypatch.setattr(
        modulo,
        "urlopen",
        lambda solicitud, timeout: BytesIO(b"x" * (MAX_BYTES_RESPUESTA + 1)),
    )
    proveedor = ProveedorOpenAI("clave_de_ejemplo")
    with pytest.raises(ErrorProveedorIA, match="demasiado grande"):
        proveedor("Diferencia de existencias")


def test_abuso_respuesta_excesiva_no_modifica_incidencia(monkeypatch):
    """Una falla del proveedor no debe modificar el registro original."""
    monkeypatch.setattr(
        modulo,
        "urlopen",
        lambda solicitud, timeout: BytesIO(b"x" * (MAX_BYTES_RESPUESTA + 1)),
    )
    original = Incidencia("INC-011", "Faltan plantas", categoria_sugerida="Ventas")
    incidencias = {original.codigo: original}
    resultado = clasificar_incidencia(
        incidencias, original.codigo, ProveedorOpenAI("clave_de_ejemplo")
    )
    assert resultado.categoria_sugerida is None
    assert incidencias[original.codigo] is original
