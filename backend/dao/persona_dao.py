from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.persona import Persona
from datetime import date
import sqlite3

class PersonaNoEncontradaError(Exception):
    def __init__(self, persona_id):
        super().__init__(f"Persona ID={persona_id} no encontrada")

class EmailDuplicadoError(Exception):
    def __init__(self, email):
        super().__init__(f"Email '{email}' ya registrado")

class PersonaDAO:
    def __init__(self):
        self.__log = Logger()
        
def insertar(self, persona):
    """Agrega una nueva persona verificando que el email no esté duplicado."""

    if self.buscar_por_email(persona.email):
        self.__log.warning(f"Email duplicado: {persona.email}")
        raise EmailDuplicadoError(persona.email)

    persona.fecha_registro = str(date.today())
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
            "INSERT INTO personas (nombre, email, fecha_registro) VALUES (?, ?, ?)",
            (persona.nombre, persona.email, persona.fecha_registro)
        )
    conn.commit()
    persona.id = cursor.lastrowid
    conn.close()
    self.__log.info(f"Persona agregada: {persona.nombre} (ID={persona.id})")
    return persona


def buscar_por_email(self, email):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM personas WHERE email = ?", (email,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_persona(fila) if fila else None

def buscar_por_id(self, persona_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM personas WHERE id = ?", (persona_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_persona(fila) if fila else None


def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM personas ORDER BY nombre")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_persona(f) for f in filas]


def actualizar(self, persona_id, nombre=None, email=None):
        p = self.buscar_por_id(persona_id)
        if not p:
            self.__log.error(f"Actualizar fallido: Persona ID={persona_id} no existe")
            raise PersonaNoEncontradaError(persona_id)
        nuevo_nombre = nombre if nombre is not None else p.nombre
        nuevo_email  = email  if email  is not None else p.email
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE personas SET nombre = ?, email = ? WHERE id = ?",
            (nuevo_nombre, nuevo_email, persona_id)
        )
        conn.commit()
        conn.close()
        self.__log.info(f"Persona actualizada: ID={persona_id}")
        return p

def eliminar(self, persona_id):
        p = self.buscar_por_id(persona_id)
        if not p:
            self.__log.error(f"Eliminar fallido: Persona ID={persona_id} no existe")
            raise PersonaNoEncontradaError(persona_id)
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM personas WHERE id = ?", (persona_id,))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            self.__log.warning(f"Persona ID={persona_id} tiene gastos asociados")
            raise
        conn.close()
        self.__log.info(f"Persona eliminada: {p.nombre} (ID={persona_id})")
        return True

def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM personas")
        total = cursor.fetchone()[0]
        conn.close()
        return total

