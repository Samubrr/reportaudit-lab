import sqlite3

import pytest

from app import reporte_auditoria as ra


def test_cargar_configuracion(tmp_path):
    archivo = tmp_path / "config.yaml"
    archivo.write_text("servicio:\n  puerto: 8080\n", encoding="utf-8")

    resultado = ra.cargar_configuracion(archivo)

    assert resultado["servicio"]["puerto"] == 8080


def test_buscar_reportes_cliente(tmp_path):
    db = tmp_path / "reportes.db"

    conexion = sqlite3.connect(db)
    conexion.execute(
        "CREATE TABLE reportes (id INTEGER, cliente TEXT, monto REAL)"
    )
    conexion.execute(
        "INSERT INTO reportes VALUES (1, 'acme_corp', 1500)"
    )
    conexion.commit()
    conexion.close()

    resultado = ra.buscar_reportes_cliente("acme_corp", str(db))

    assert len(resultado) == 1
    assert resultado[0][1] == "acme_corp"


def test_buscar_reportes_cliente_inyeccion_sql(tmp_path):
    db = tmp_path / "reportes.db"

    conexion = sqlite3.connect(db)
    conexion.execute(
        "CREATE TABLE reportes (id INTEGER, cliente TEXT, monto REAL)"
    )
    conexion.execute(
        "INSERT INTO reportes VALUES (1, 'acme_corp', 1500)"
    )
    conexion.commit()
    conexion.close()

    resultado = ra.buscar_reportes_cliente(
        "' OR '1'='1",
        str(db)
    )

    assert resultado == []


def test_convertir_a_pdf_autorizado(monkeypatch):
    llamadas = []

    def ejecutar_comando(*args, **kwargs):
        llamadas.append((args, kwargs))

    monkeypatch.setattr(ra.subprocess, "run", ejecutar_comando)

    resultado = ra.convertir_a_pdf("informe.html")

    assert resultado == "informe.html.pdf"
    assert len(llamadas) == 1
    assert llamadas[0][1]["shell"] is False


def test_convertir_a_pdf_no_autorizado():
    with pytest.raises(ValueError):
        ra.convertir_a_pdf("../../archivo.html")


def test_convertir_a_pdf_sin_wkhtmltopdf(monkeypatch):
    def comando_no_disponible(*args, **kwargs):
        raise FileNotFoundError

    monkeypatch.setattr(
        ra.subprocess,
        "run",
        comando_no_disponible
    )

    resultado = ra.convertir_a_pdf("informe.html")

    assert resultado == "informe.html.pdf"


def test_hash_password_legacy():
    hash1 = ra.hash_password_legacy("MiPassword123")
    hash2 = ra.hash_password_legacy("MiPassword123")

    assert ":" in hash1
    assert hash1 != hash2


def test_notificar_cliente(capsys):
    resultado = ra.notificar_cliente(
        "cliente@example.com",
        "Informe disponible"
    )

    salida = capsys.readouterr().out

    assert resultado is True
    assert "cliente@example.com" in salida
    assert "Informe disponible" in salida
    assert "configurada=False" in salida
