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

