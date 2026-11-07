"""Adaptador HTTP: simulado; ninguna prueba sale a Internet."""
from io import BytesIO
import json
from urllib.error import URLError

import pytest

from app.clasificador import ErrorProveedorIA
from app.proveedor_openai import ProveedorOpenAI


def test_adaptador_extrae_categoria_de_respuesta_openai(monkeypatch):
    import app.proveedor_openai as modulo
    peticiones = []

    def urlopen_simulado(peticion, timeout):
        peticiones.append((peticion, timeout))
        return BytesIO(json.dumps({
            "output": [{"type": "message", "content": [{"type": "output_text", "text": "Inventario"}]}]
        }).encode())

    monkeypatch.setattr(modulo, "urlopen", urlopen_simulado, raising=False)
    proveedor = ProveedorOpenAI("clave_de_ejemplo", model="modelo-prueba")
    assert proveedor("Las existencias no coinciden") == "Inventario"
    assert len(peticiones) == 1
    peticion, timeout = peticiones[0]
    assert peticion.full_url == "https://api.openai.com/v1/responses"
    cuerpo = json.loads(peticion.data.decode())
    assert cuerpo["model"] == "modelo-prueba"
    assert cuerpo["store"] is False
    assert timeout <= 10
    assert "clave_de_ejemplo" not in str(cuerpo)


def test_adaptador_rechaza_respuesta_sin_texto(monkeypatch):
    import app.proveedor_openai as modulo
    monkeypatch.setattr(modulo, "urlopen", lambda peticion, timeout: BytesIO(b'{"output":[]}'), raising=False)
    proveedor = ProveedorOpenAI("clave_de_ejemplo")
    with pytest.raises(ErrorProveedorIA):
        proveedor("Texto de prueba")


def test_adaptador_reporta_error_de_red_como_oserror(monkeypatch):
    import app.proveedor_openai as modulo

    def sin_red(peticion, timeout):
        raise URLError("sin conexion")

    monkeypatch.setattr(modulo, "urlopen", sin_red, raising=False)
    proveedor = ProveedorOpenAI("clave_de_ejemplo")
    with pytest.raises(OSError):
        proveedor("Problema en pantalla")
