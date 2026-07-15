import sqlite3

ARCHIVO_BD = "splithome.db"

def obtener_conexion():
    conn = sqlite3.connect(ARCHIVO_BD)
    conn.row_factory = sqlite3.Row
    return conn

def inicializar():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personas (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre          TEXT NOT NULL,
            email           TEXT UNIQUE NOT NULL,
            fecha_registro  TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre      TEXT NOT NULL UNIQUE,
            icono       TEXT,
            descripcion TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gastos (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion   TEXT NOT NULL,
            monto         REAL NOT NULL,
            fecha         TEXT NOT NULL,
            es_compartido INTEGER NOT NULL DEFAULT 0,
            id_persona    INTEGER NOT NULL,
            id_categoria  INTEGER NOT NULL,
            FOREIGN KEY (id_persona)   REFERENCES personas(id),
            FOREIGN KEY (id_categoria) REFERENCES categorias(id)
        )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS participacion (
        id_gasto       INTEGER NOT NULL,
        id_persona     INTEGER NOT NULL,
        proporcion     REAL NOT NULL DEFAULT 50.00,
        monto_asignado REAL NOT NULL,
        PRIMARY KEY (id_gasto, id_persona),
        FOREIGN KEY (id_gasto)   REFERENCES gastos(id),
        FOREIGN KEY (id_persona) REFERENCES personas(id)
    )
""")

    conn.commit()
    conn.close()