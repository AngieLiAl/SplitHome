class Categoria:

    def __init__(self, id_categoria=0, nombre="", icono="", descripcion=""):
        self.__id_categoria = id_categoria
        self.__nombre = nombre
        self.__icono = icono
        self.__descripcion = descripcion

    @property
    def id_categoria(self):
        return self.__id_categoria

    @id_categoria.setter
    def id_categoria(self, valor):
        self.__id_categoria = valor

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if valor.strip() == "":
            raise ValueError("El nombre es obligatorio")
        self.__nombre = valor

    @property
    def icono(self):
        return self.__icono

    @icono.setter
    def icono(self, valor):
        self.__icono = valor

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self.__descripcion = valor

    def __str__(self):
        return self.__nombre