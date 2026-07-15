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
    
    def actualizar(self, gasto_id, descripcion=None, monto=None,
                fecha=None, id_categoria=None):
        g = self.buscar_por_id(gasto_id)
        if not g:
            self.__log.error(f"Actualizar fallido: Gasto ID={gasto_id} no existe")
            raise GastoNoEncontradoError(gasto_id)
        nueva_desc  = descripcion   if descripcion   is not None else g.descripcion
        nuevo_monto = monto         if monto         is not None else g.monto
        nueva_fecha = fecha         if fecha         is not None else g.fecha
        nueva_cat   = id_categoria  if id_categoria  is not None else g.id_categoria
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE gastos
            SET descripcion = ?, monto = ?, fecha = ?, id_categoria = ?
            WHERE id = ?""",
            (nueva_desc, nuevo_monto, nueva_fecha, nueva_cat, gasto_id)
        )
        conn.commit()
        conn.close()
        self.__log.info(f"Gasto actualizado: ID={gasto_id}")
        return g
    
    def eliminar(self, gasto_id):
        g = self.buscar_por_id(gasto_id)
        if not g:
            self.__log.error(f"Eliminar fallido: Gasto ID={gasto_id} no existe")
            raise GastoNoEncontradoError(gasto_id)
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM gastos WHERE id = ?", (gasto_id,))
        conn.commit()
        conn.close()
        self.__log.info(f"Gasto eliminado: {g.descripcion} (ID={gasto_id})")
        return True
    
    def calcular_total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(monto) FROM gastos")
        resultado = cursor.fetchone()[0]
        conn.close()
        return resultado or 0.0
    