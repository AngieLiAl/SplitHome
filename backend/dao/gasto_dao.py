# ──────────────────────────────────────────────────────────────
# DAO — GastoDAO
# Se encarga de todo lo relacionado con guardar, buscar,
# actualizar y eliminar gastos en PostgreSQL.
# Antes usaba una lista en memoria, ahora usa la base de datos
# real para que los datos no se pierdan al cerrar el programa.
# ──────────────────────────────────────────────────────────────
import psycopg2
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.gasto import Gasto

# Error personalizado cuando no se encuentra un gasto
class GastoNoEncontradoError(Exception):
    def __init__(self, gasto_id):
        super().__init__(f"Gasto ID={gasto_id} no encontrado")

class GastoDAO:
    def __init__(self):
        # Usamos el mismo historial de eventos que todo el sistema
        self.__log = Logger()

    def insertar(self, gasto):
        # Guardamos el gasto en PostgreSQL
        # es_compartido se guarda como True/False en PostgreSQL
        conn = obtener_conexion()
        cursor = conn.cursor()
        # RETURNING id_gasto le dice a PostgreSQL que nos devuelva
        # el id que generó automáticamente al insertar
        cursor.execute(
            """INSERT INTO gastos
            (descripcion, monto, fecha, es_compartido, id_persona, id_categoria)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_gasto""",
            (gasto.descripcion, gasto.monto, gasto.fecha,
            gasto.es_compartido,
            gasto.id_persona, gasto.id_categoria)
        )
        # Guardamos el id que PostgreSQL generó en el objeto gasto
        gasto.id = cursor.fetchone()["id_gasto"]
        conn.commit()
        conn.close()
        self.__log.info(
            f"Gasto agregado: {gasto.descripcion} "
            f"S/.{gasto.monto:.2f} (ID={gasto.id})"
            )
        return gasto

    def buscar_por_id(self, gasto_id):
        # Busca un gasto por su id, devuelve None si no existe
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gastos WHERE id = %s", (gasto_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_gasto(fila) if fila else None
    
    def obtener_todos(self):
        # Devuelve todos los gastos ordenados del más reciente al más antiguo
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gasto ORDER BY fecha DESC")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_gasto(f) for f in filas]
        
    def obtener_por_persona(self, persona_id):
        # Devuelve todos los gastos que pagó una persona específica
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT * FROM gasto WHERE id_persona = %s ORDER BY fecha DESC""",
            (persona_id,)
        )
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_gasto(f) for f in filas]
    
    def obtener_por_categoria(self, categoria_id):
        # Devuelve todos los gastos de una categoría específica
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT * FROM gasto WHERE id_categoria = %s
            ORDER BY fecha DESC""",
            (categoria_id,)
        )
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_gasto(f) for f in filas]
    
    def actualizar(self, gasto_id, descripcion=None, monto=None,
                fecha=None, id_categoria=None):
        # Solo actualiza los campos que se envíen
        # si no se manda un campo, se queda como estaba
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
            SET descripcion = %s, monto = %s, fecha = %s, id_categoria = %s
            WHERE id_gasto = %s""",
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
    
    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM gastos")
        total = cursor.fetchone()[0]
        conn.close()
        return total
    
    def __fila_a_gasto(self, fila):
        g = Gasto(
            fila["descripcion"],
            fila["monto"],
            fila["id_persona"],
            fila["id_categoria"],
            fila["fecha"],
            bool(fila["es_compartido"])
        )
        g.id = fila["id"]
        return g