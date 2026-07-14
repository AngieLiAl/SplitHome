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
        