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

def inicializar():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS persona (
            id_persona      SERIAL PRIMARY KEY,
            nombre          VARCHAR(100) NOT NULL,
            email           VARCHAR(150) UNIQUE,
            fecha_registro  TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categoria (
            id_categoria INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            nombre       VARCHAR(80) NOT NULL UNIQUE,
            icono        VARCHAR(10) NULL,
            descripcion  TEXT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gasto (
            id_gasto      SERIAL PRIMARY KEY,
            descripcion   VARCHAR(200) NOT NULL,
            monto         DECIMAL(10,2) NOT NULL CHECK (monto >= 0),
            fecha         DATE NOT NULL DEFAULT CURRENT_DATE,
            es_compartido BOOLEAN NOT NULL DEFAULT FALSE,
            id_persona    INT NOT NULL REFERENCES persona(id_persona) ON DELETE NO ACTION,
            id_categoria  INT NOT NULL REFERENCES categoria(id_categoria) ON DELETE NO ACTION
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS participacion (
            id_gasto       INT NOT NULL REFERENCES gasto(id_gasto) ON DELETE CASCADE,
            id_persona     INT NOT NULL REFERENCES persona(id_persona) ON DELETE NO ACTION,
            proporcion     DECIMAL(5,2) NOT NULL DEFAULT 50.00
                        CHECK (proporcion > 0 AND proporcion <= 100),
            monto_asignado DECIMAL(10,2) NOT NULL,
            PRIMARY KEY (id_gasto, id_persona)
        )
    """)

    conn.commit()
    conn.close()