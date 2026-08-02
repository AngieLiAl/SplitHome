# ──────────────────────────────────────────────────────────────
# CONEXIÓN A POSTGRESQL
# Usa psycopg2 para conectarse a la base de datos.
# Las credenciales se leen desde el archivo .env
# para no exponer contraseñas en el código.
# ──────────────────────────────────────────────────────────────

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def obtener_conexion():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "splithome_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "")
    )
    conn.cursor_factory = RealDictCursor
    return conn