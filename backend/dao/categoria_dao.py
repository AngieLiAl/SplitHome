from config.logger import Logger
from modelos.categoria import Categoria

class CategoriaNoEncontradaError(Exception):
    def __init__(self, categoria_id):
        super().__init__(f"Categoría ID={categoria_id} no encontrada")

class CategoriaDuplicadaError(Exception):
    def __init__(self, nombre):
        super().__init__(f"Categoría '{nombre}' ya existe")

class CategoriaDAO:
    def __init__(self):
        self.__bd =[]
        self.__cid = 1
        self.__log = Logger()
        self._cargar_categorias_base()
        
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
        """Agrega una nueva categoría verificando que no esté duplicada."""
        if self.buscar_por_nombre(categoria.nombre):
            self.__log.warning(f"Categoría duplicada: {categoria.nombre}")
            raise CategoriaDuplicadaError(categoria.nombre)
        categoria.id = self.__cid
        self.__cid += 1
        self.__bd.append(categoria)
        self.__log.info(f"Categoría agregada: {categoria.nombre} (ID={categoria.id})")
        return categoria
    
    def buscar_por_nombre(self, nombre):
        """Devuelve la categoría con ese nombre o None si no existe."""
        for c in self.__bd:
            if c.nombre.lower() == nombre.lower():
                return c
        return None

    def buscar_por_id(self, categoria_id):
        """Devuelve la categoría con ese ID o None si no existe."""
        for c in self.__bd:
            if c.id == categoria_id:
                return c
        return None
    
    def obtener_todos(self):
        """Devuelve la lista de categorías ordenada por nombre."""
        return sorted(self.__bd, key=lambda c: c.nombre)

    def actualizar(self, categoria_id, nombre=None, icono=None):
        """Actualiza solo los campos que se envíen."""
        c = self.buscar_por_id(categoria_id)
        if not c:
            self.__log.error(f"Actualizar fallido: Categoría ID={categoria_id} no existe")
            raise CategoriaNoEncontradaError(categoria_id)
        if nombre: c.nombre = nombre
        if icono:  c.icono  = icono
        self.__log.info(f"Categoría actualizada: ID={categoria_id}")
        return c
