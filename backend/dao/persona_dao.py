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
        
def insertar(self, persona):
    """Agrega una nueva persona verificando que el email no esté duplicado."""

    if self.buscar_por_email(persona.email):
        self.__log.warning(f"Email duplicado: {persona.email}")
        raise EmailDuplicadoError(persona.email)

    persona.id = self.__cid
    self.__cid += 1

    self.__bd.append(persona)

    self.__log.info(
        f"Persona agregada: {persona.nombre} (ID={persona.id})"
    )
    return persona

def buscar_por_email(self,email):
    """devuelve la persona con ese emaill o none si esta no existe"""
    for p in self.__bd:
        if p.email == email:
            return p
    return None 

def obtener_todos(self):
    """Devuelve la lista de personas ordenada por nombre"""
    return sorted(self.__bd, key=lambda p: p.nombre)

def actualizar(self, persona_id, nombre=None, email=None):
    """Actualiza solo los campos que se envíen."""

    p = self.buscar_por_id(persona_id)

    if not p:
        self.__log.error(
            f"Actualizar fallido: Persona ID={persona_id} no existe"
        )
        raise PersonaNoEncontradaError(persona_id)

    if nombre:
        p.nombre = nombre

    if email:
        p.email = email

    self.__log.info(
        f"Persona actualizada: ID={persona_id}"
    )

    return p

def eliminar(self, persona_id):
    """Elimina la persona con ese ID."""

    p = self.buscar_por_id(persona_id)

    if not p:
        self.__log.error(
            f"Eliminar fallido: Persona ID={persona_id} no existe"
        )
        raise PersonaNoEncontradaError(persona_id)

    self.__bd.remove(p)

    self.__log.info(
        f"Persona eliminada: {p.nombre} (ID={persona_id})"
    )

    return True

def total(self):
    return len(self.__bd)

