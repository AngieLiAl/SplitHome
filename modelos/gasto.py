class Gasto:

    def __init__(self,
                id_gasto=0,
                descripcion="",
                monto=0.0,
                fecha="",
                es_compartido=False,
                id_persona=0,
                id_categoria=0):

        self.__id_gasto = id_gasto
        self.__descripcion = descripcion
        self.__monto = monto
        self.__fecha = fecha
        self.__es_compartido = es_compartido
        self.__id_persona = id_persona
        self.__id_categoria = id_categoria

    @property
    def id_gasto(self):
        return self.__id_gasto

    @id_gasto.setter
    def id_gasto(self, valor):
        self.__id_gasto = valor

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor):
        if valor.strip() == "":
            raise ValueError("La descripción es obligatoria")
        self.__descripcion = valor

    @property
    def monto(self):
        return self.__monto

    @monto.setter
    def monto(self, valor):
        if valor < 0:
            raise ValueError("El monto no puede ser negativo")
        self.__monto = valor

    @property
    def fecha(self):
        return self.__fecha

    @fecha.setter
    def fecha(self, valor):
        self.__fecha = valor

    @property
    def es_compartido(self):
        return self.__es_compartido

    @es_compartido.setter
    def es_compartido(self, valor):
        self.__es_compartido = valor

    @property
    def id_persona(self):
        return self.__id_persona

    @id_persona.setter
    def id_persona(self, valor):
        self.__id_persona = valor

    @property
    def id_categoria(self):
        return self.__id_categoria

    @id_categoria.setter
    def id_categoria(self, valor):
        self.__id_categoria = valor

    def calcular_deuda(self):
        if self.__es_compartido:
            return self.__monto / 2
        return self.__monto

    def __str__(self):
        return f"{self.__descripcion} - S/. {self.__monto}"