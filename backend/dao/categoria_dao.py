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

    def buscar_por_id(self, categoria_id):
        """Devuelve la categoría con ese ID o None si no existe."""
        for c in self.__bd:
            if c.id == categoria_id:
                return c
        return None
    
    def obtener_todos(self):
        """Devuelve la lista de categorías ordenada por nombre."""
        return sorted(self.__bd, key=lambda c: c.nombre)

    