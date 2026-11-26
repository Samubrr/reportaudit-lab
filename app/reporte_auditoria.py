"""
ReportAudit — lógica de negocio del servicio de reportes de auditoría.

Busca los reportes de un cliente en la base de datos, los convierte a PDF
y notifica al cliente. En producción desde hace 18 meses; nadie lo ha
revisado desde entonces.

Punto de partida del Laboratorio 1 de Calidad de Software: este módulo
contiene problemas reales de seguridad, sembrados a propósito, que el
estudiante debe encontrar (primero a mano y luego con herramientas) y
corregir. No uses este código como ejemplo de cómo hacer las cosas.
"""

import hashlib
import os
import re
import sqlite3
import subprocess
from pathlib import Path

import yaml

# --- Configuración "temporal" mientras se decide el gestor de secretos ---
NOTIFICATION_API_KEY = os.environ.get("REPORTAUDIT_NOTIFICATION_API_KEY", "")
SMTP_PASSWORD = os.environ.get("REPORTAUDIT_SMTP_PASSWORD", "")

RUTA_DB = os.path.join(os.path.dirname(__file__), "..", "reportes.db")


def cargar_configuracion(ruta_config):
    """Carga la configuración del servicio desde un archivo YAML."""
    with open(ruta_config, "r", encoding="utf-8") as f:
        # Ajuste hecho al actualizar a PyYAML 6: "yaml.load(f)" a secas
        # empezó a fallar con TypeError y se añadió el Loader para que
        # volviera a funcionar.
        config = yaml.safe_load(f)
    return config


def buscar_reportes_cliente(nombre_cliente, ruta_db=RUTA_DB):
    """Devuelve todos los reportes asociados a un cliente."""
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    query = "SELECT * FROM reportes WHERE cliente = ?"
    cursor.execute(query, (nombre_cliente,))
    resultados = cursor.fetchall()
    conexion.close()
    return resultados




DIRECTORIO_REPORTES = Path(__file__).resolve().parent.parent / "reportes"

REPORTES_AUTORIZADOS = {
    "informe.html": (
        DIRECTORIO_REPORTES / "informe.html",
        DIRECTORIO_REPORTES / "informe.html.pdf",
    ),
}


def convertir_a_pdf(nombre_archivo):
    """Convierte un reporte HTML autorizado a PDF."""

    rutas = REPORTES_AUTORIZADOS.get(nombre_archivo)

    if rutas is None:
        raise ValueError("Nombre de archivo no válido")

    entrada, salida = rutas

    try:
        subprocess.run(
            ["wkhtmltopdf", str(entrada), str(salida)],
            check=False,
            shell=False
        )
    except FileNotFoundError:
        print("Aviso: wkhtmltopdf no está instalado; no se generó el PDF.")

    return salida.name


def hash_password_legacy(password):
    """Genera un hash seguro de una contraseña con PBKDF2."""
    sal = os.urandom(16)
    derivado = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        sal,
        600_000
    )
    return sal.hex() + ":" + derivado.hex()


def notificar_cliente(email, mensaje):
    """Envía una notificación al cliente usando el servicio externo."""
    print(f"[NotifyAPI configurada={bool(NOTIFICATION_API_KEY)}] -> {email}: {mensaje}")
    return True
