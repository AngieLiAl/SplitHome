from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.gasto import Gasto
import sqlite3

class GastoNoEncontradoError(Exception):
    def __init__(self, gasto_id):
        super().__init__(f"Gasto ID={gasto_id} no encontrado")

class GastoDAO:
    def __init__(self):
        self.__log = Logger()

    def insertar(self, gasto):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO gastos
            (descripcion, monto, fecha, es_compartido, id_persona, id_categoria)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (gasto.descripcion, gasto.monto, gasto.fecha,
            1 if gasto.es_compartido else 0,
            gasto.id_persona, gasto.id_categoria)
        )
        conn.commit()
        gasto.id = cursor.lastrowid
        conn.close()
        self.__log.info(f"Gasto agregado: {gasto.descripcion} S/.{gasto.monto:.2f} (ID={gasto.id})")
        return gasto

    def buscar_por_id(self, gasto_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gastos WHERE id = ?", (gasto_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_gasto(fila) if fila else None
    
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gastos ORDER BY fecha DESC")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_gasto(f) for f in filas]
        
    def obtener_por_persona(self, persona_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM gastos WHERE id_persona = ? ORDER BY fecha DESC",
            (persona_id,)
        )
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_gasto(f) for f in filas]