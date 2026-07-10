class Persona:

    def __init__(self, id_persona=0, nombre="", email="", fecha_registro=""):
        self.__id_persona = id_persona
        self.__nombre = nombre
        self.__email = email
        self.__fecha_registro = fecha_registro

    @property
    def id_persona(self):
        return self.__id_persona

    @id_persona.setter
    def id_persona(self, valor):
        self.__id_persona = valor

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if valor.strip() == "":
            raise ValueError("El nombre no puede estar vacío")
        self.__nombre = valor

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        if valor and "@" not in valor:
            raise ValueError("Correo electrónico inválido")
        self.__email = valor

    @property
    def fecha_registro(self):
        return self.__fecha_registro

    @fecha_registro.setter
    def fecha_registro(self, valor):
        self.__fecha_registro = valor

    def __str__(self):
        return f"{self.__nombre} ({self.__email})"