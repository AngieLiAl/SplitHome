from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.categoria import Categoria
import sqlite3


class CategoriaNoEncontradaError(Exception):
    def __init__(self, categoria_id):
        super().__init__(f"Categoría ID={categoria_id} no encontrada")

class CategoriaDuplicadaError(Exception):
    def __init__(self, nombre):
        super().__init__(f"Categoría '{nombre}' ya existe")

class CategoriaDAO:
    def __init__(self):
        self.__log = Logger()

        
    def _cargar_categorias_base(self):
        """Carga las categorías predeterminadas del hogar al iniciar."""
        bases = [
            ("Alquiler", "🏠"), ("Luz",      "💡"),
            ("Agua",     "💧"), ("Internet", "📶"),
            ("Comida",   "🍛"), ("Limpieza", "🧹"),
            ("Otros",    "📦"),
        ]
        for nombre, icono in bases:
            c = Categoria(nombre, icono)
            c.id = self.__cid
            self.__cid += 1
            self.__bd.append(c)
            
    def insertar(self, categoria):
        if self.buscar_por_nombre(categoria.nombre):
            self.__log.warning(f"Categoría duplicada: {categoria.nombre}")
            raise CategoriaDuplicadaError(categoria.nombre)
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO categorias (nombre, icono, descripcion) VALUES (?, ?, ?)",
            (categoria.nombre, categoria.icono, categoria.descripcion)
        )
        conn.commit()
        categoria.id = cursor.lastrowid
        conn.close()
        self.__log.info(f"Categoría agregada: {categoria.nombre} (ID={categoria.id})")
        return categoria

    
    def buscar_por_nombre(self, nombre):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categorias WHERE nombre = ?", (nombre,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_categoria(fila) if fila else None


    def buscar_por_id(self, categoria_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categorias WHERE id = ?", (categoria_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_categoria(fila) if fila else None

    
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categorias ORDER BY nombre")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_categoria(f) for f in filas]


    def actualizar(self, categoria_id, nombre=None, icono=None):
        c = self.buscar_por_id(categoria_id)
        if not c:
            self.__log.error(f"Actualizar fallido: Categoría ID={categoria_id} no existe")
            raise CategoriaNoEncontradaError(categoria_id)
        nuevo_nombre = nombre if nombre is not None else c.nombre
        nuevo_icono  = icono  if icono  is not None else c.icono
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE categorias SET nombre = ?, icono = ? WHERE id = ?",
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
