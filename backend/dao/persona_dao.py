from config.logger import Logger
from modelos.persona import Persona

class PersonaNoEncontradaError(Exception):
    def __init__(self, persona_id):
        super().__init__(f"Persona ID={persona_id} no encontrada")

class EmailDuplicadoError(Exception):
    def __init__(self, email):
        super().__init__(f"Email '{email}' ya registrado")

class PersonaDAO:
    def __init__(self):
        self.__bd = []
        self.__cid = 1
        self.__log = Logger()
        
