# ──────────────────────────────────────────────────────────────
# DAO — CategoriaDAO
# Se encarga de todo lo relacionado con guardar, buscar,
# actualizar y eliminar categorías en PostgreSQL.
# Antes usaba una lista en memoria, ahora usa la base de datos
# real para que los datos no se pierdan al cerrar el programa.
# ──────────────────────────────────────────────────────────────
import psycopg2
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.categoria import Categoria

# Error personalizado cuando no se encuentra una categoría
class CategoriaNoEncontradaError(Exception):
    def __init__(self, categoria_id):
        super().__init__(f"Categoría ID={categoria_id} no encontrada")

# Error personalizado cuando la categoría ya existe
class CategoriaDuplicadaError(Exception):
    def __init__(self, nombre):
        super().__init__(f"Categoría '{nombre}' ya existe")

class CategoriaDAO:
    def __init__(self):
        # Usamos el mismo historial de eventos que todo el sistema
        self.__log = Logger()

    def insertar(self, categoria):
        # Verificamos que no exista una categoría con el mismo nombre
        if self.buscar_por_nombre(categoria.nombre):
            self.__log.warning(f"Categoría duplicada: {categoria.nombre}")
            raise CategoriaDuplicadaError(categoria.nombre)
        conn = obtener_conexion()
        cursor = conn.cursor()
        # RETURNING id_categoria le dice a PostgreSQL que nos devuelva
        # el id que generó automáticamente al insertar
        cursor.execute(
            """INSERT INTO categorias (nombre, icono, descripcion) VALUES (%s, %s, %s) RETURNING id_categoria""",
            (categoria.nombre, categoria.icono, categoria.descripcion)
        )
        # Guardamos el id que PostgreSQL generó en el objeto categoria
        categoria.id = cursor.fetchone()["id_categoria"]
        conn.commit()
        conn.close()
        self.__log.info(f"Categoría agregada: {categoria.nombre} (ID={categoria.id})")
        return categoria
    
    def buscar_por_nombre(self, nombre):
        # Busca una categoría por su nombre, devuelve None si no existe
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categorias WHERE nombre = %s", (nombre,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_categoria(fila) if fila else None
    
    def buscar_por_id(self, categoria_id):
        # Busca una categoría por su id, devuelve None si no existe
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categorias WHERE id = %s", (categoria_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_categoria(fila) if fila else None
    
    def obtener_todos(self):
        # Devuelve todas las categorías ordenadas por nombre
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categoria ORDER BY nombre")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_categoria(f) for f in filas]

    def actualizar(self, categoria_id, nombre=None, icono=None):
        # Solo actualiza los campos que se envíen
        # si no se manda un campo, se queda como estaba
        c = self.buscar_por_id(categoria_id)
        if not c:
            self.__log.error(f"Actualizar fallido: Categoría ID={categoria_id} no existe")
            raise CategoriaNoEncontradaError(categoria_id)
        nuevo_nombre = nombre if nombre is not None else c.nombre
        nuevo_icono  = icono  if icono  is not None else c.icono
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE categoria SET nombre = %s, icono = %s WHERE id_categoria = %s",
            (nuevo_nombre, nuevo_icono, categoria_id)
        )
        conn.commit()
        conn.close()
        self.__log.info(f"Categoría actualizada: ID={categoria_id}")
        return c

    def eliminar(self, categoria_id):
        c = self.buscar_por_id(categoria_id)
        if not c:
            self.__log.error(f"Eliminar fallido: Categoría ID={categoria_id} no existe")
            raise CategoriaNoEncontradaError(categoria_id)
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM categorias WHERE id = ?", (categoria_id,))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            self.__log.warning(f"Categoría ID={categoria_id} tiene gastos asociados")
            raise
        conn.close()
        self.__log.info(f"Categoría eliminada: {c.nombre} (ID={categoria_id})")
        return True


    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM categorias")
        total = cursor.fetchone()[0]
        conn.close()
        return total
    
    def __fila_a_categoria(self, fila):
        c = Categoria(fila["nombre"], fila["icono"], fila["descripcion"])
        c.id = fila["id"]
        return c
