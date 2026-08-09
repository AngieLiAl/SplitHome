# ──────────────────────────────────────────────────────────────
# SCHEMAS — Persona
# Define cómo deben verse los datos que llegan y salen
# del API para las personas.
# Pydantic valida automáticamente que los datos sean correctos
# antes de que lleguen al DAO.
# ──────────────────────────────────────────────────────────────
import re
from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional

class PersonaCrear(BaseModel):
    # Datos que se necesitan para crear una nueva persona
    nombre: str
    email:  str

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor):
        # El nombre no puede estar vacío ni tener solo espacios
        if not valor.strip():
            raise ValueError("El nombre no puede estar vacío")
        return valor.strip()

    @field_validator("email")
    @classmethod
    def validar_email(cls, valor):
        # Verificamos que el email tenga el formato correcto
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
            raise ValueError("El email no tiene un formato válido")
        return valor

class PersonaActualizar(BaseModel):
    # Todos los campos son opcionales para poder actualizar
    # solo lo que se necesite
    nombre: Optional[str] = None
    email:  Optional[str] = None

class PersonaRespuesta(BaseModel):
    # Así se verán los datos cuando el API los devuelva
    id_persona:     int
    nombre:         str
    email:          str
    fecha_registro: datetime