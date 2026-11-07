"""Casos escritos ANTES de implementar HU-03. No cambiarlos para pasar pruebas."""
import pytest

from app.clasificador import Incidencia, clasificar_incidencia


def reporte(codigo="INC-001", descripcion="El sistema muestra 60 plantas y hay 48"):
    return {codigo: Incidencia(codigo=codigo, descripcion=descripcion)}


def test_normal_inventario_guarda_sugerencia_y_conserva_pendiente():
    incidencias = reporte()
    resultado = clasificar_incidencia(incidencias, "INC-001", lambda _: "Inventario")
    assert resultado.categoria_sugerida == "Inventario"
    assert incidencias["INC-001"].categoria_sugerida == "Inventario"
    assert incidencias["INC-001"].estado == "PENDIENTE_REVISION"
    assert incidencias["INC-001"].descripcion == "El sistema muestra 60 plantas y hay 48"


def test_normal_interfaz_guarda_categoria_del_proveedor():
    incidencias = reporte("INC-002", "No carga la pantalla de registrar ventas")
    resultado = clasificar_incidencia(incidencias, "INC-002", lambda _: "Interfaz")
    assert resultado.categoria_sugerida == "Interfaz"
    assert incidencias["INC-002"].categoria_sugerida == "Interfaz"


def test_normal_ventas_y_normaliza_espacios_y_mayusculas():
    incidencias = reporte("INC-004", "No se puede registrar la venta")
    resultado = clasificar_incidencia(incidencias, "INC-004", lambda _: "  vEnTaS  ")
    assert resultado.categoria_sugerida == "Ventas"


def test_limite_categoria_otro_es_valida_y_no_se_reinterpreta():
    incidencias = reporte("INC-005", "No encuentro la opción del reporte")
    resultado = clasificar_incidencia(incidencias, "INC-005", lambda _: "Otro")
    assert resultado.categoria_sugerida == "Otro"


def test_limite_descripcion_de_500_caracteres_aceptada():
    incidencias = reporte("INC-006", "a" * 500)
    recibido = []

    def ia(texto):
        recibido.append(texto)
        return "Inventario"

    clasificar_incidencia(incidencias, "INC-006", ia)
    assert recibido == ["a" * 500]
    assert incidencias["INC-006"].categoria_sugerida == "Inventario"


def test_limite_descripcion_de_501_caracteres_rechazada_sin_llamar_ia():
    incidencias = reporte("INC-007", "a" * 501)
    llamadas = []
    with pytest.raises(ValueError, match="1 y 500"):
        clasificar_incidencia(incidencias, "INC-007", lambda txt: llamadas.append(txt))
    assert llamadas == []
    assert incidencias["INC-007"].categoria_sugerida is None


def test_error_proveedor_no_disponible_conserva_reporte_sin_categoria():
    incidencias = reporte("INC-003", "No registra la salida de un lote")
    anterior = incidencias["INC-003"]

    def ia_no_disponible(_):
        raise TimeoutError("Servidor externo agotó el tiempo")

    resultado = clasificar_incidencia(incidencias, "INC-003", ia_no_disponible)
    assert resultado.categoria_sugerida is None
    assert resultado.mensaje == "No fue posible clasificar; intente de nuevo"
    assert incidencias["INC-003"] is anterior
    assert incidencias["INC-003"].estado == "PENDIENTE_REVISION"


def test_error_categoria_invalida_se_rechaza_en_vez_de_convertirla_a_otro():
    incidencias = reporte()
    resultado = clasificar_incidencia(incidencias, "INC-001", lambda _: "Urgente")
    assert resultado.categoria_sugerida is None
    assert resultado.mensaje == "La IA devolvió una categoría no permitida"
    assert incidencias["INC-001"].categoria_sugerida is None


def test_error_incidencia_inexistente_no_llama_al_modelo():
    incidencias = reporte()
    llamadas = []
    with pytest.raises(KeyError):
        clasificar_incidencia(incidencias, "INC-999", lambda txt: llamadas.append(txt))
    assert not llamadas


def test_error_descripcion_vacia_no_llama_al_modelo():
    incidencias = reporte("INC-010", "   ")
    llamadas = []
    with pytest.raises(ValueError, match="1 y 500"):
        clasificar_incidencia(incidencias, "INC-010", lambda txt: llamadas.append(txt))
    assert not llamadas


def test_reclasificacion_fallida_no_borra_categoria_ya_guardada():
    incidencia = Incidencia("INC-012", "Faltan plantas", "Inventario")
    incidencias = {"INC-012": incidencia}

    def ia_no_disponible(_):
        raise ConnectionError("Sin red")

    resultado = clasificar_incidencia(incidencias, "INC-012", ia_no_disponible)
    assert resultado.categoria_sugerida is None
    assert incidencias["INC-012"] is incidencia
    assert incidencia.categoria_sugerida == "Inventario"
