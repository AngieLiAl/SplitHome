# ──────────────────────────────────────────────────────────────
# SCHEMAS — Gasto
# Define cómo deben verse los datos que llegan y salen
# del API para los gastos.
# Pydantic valida automáticamente que los datos sean correctos
# antes de que lleguen al DAO.
# ──────────────────────────────────────────────────────────────
from datetime import date
from pydantic import BaseModel, field_validator
from typing import Optional

class GastoCrear(BaseModel):
    # Datos que se necesitan para registrar un nuevo gasto
    descripcion:   str
    monto:         float
    id_persona:    int
    id_categoria:  int
    fecha:         Optional[str]  = None
    es_compartido: Optional[bool] = False

    @field_validator("descripcion")
    @classmethod
    def validar_descripcion(cls, valor):
        # La descripción no puede estar vacía
        if not valor.strip():
            raise ValueError("La descripción no puede estar vacía")
        return valor.strip()

    @field_validator("monto")
    @classmethod
    def validar_monto(cls, valor):
        # El monto debe ser mayor a 0
        if valor <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        return round(valor, 2)

class GastoActualizar(BaseModel):
    # Todos los campos son opcionales para poder actualizar
    # solo lo que se necesite
    descripcion:  Optional[str]   = None
    monto:        Optional[float] = None
    fecha:        Optional[str]   = None
    id_categoria: Optional[int]   = None

class GastoRespuesta(BaseModel):
    # Así se verán los datos cuando el API los devuelva
    id_gasto:      int
    descripcion:   str
    monto:         float
    fecha:         date
    es_compartido: bool
    id_persona:    int
    id_categoria:  int

class GastoCompartidoCrear(BaseModel):
    # Datos adicionales para registrar un gasto compartido
    # con su proporción entre los miembros
    descripcion:  str
    monto:        float
    id_persona:   int
    id_categoria: int
    fecha:        Optional[str]   = None
    proporcion:   Optional[float] = 50.0
    id_persona2:  int

    @field_validator("monto")
    @classmethod
    def validar_monto(cls, valor):
        if valor <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        return round(valor, 2)

    @field_validator("proporcion")
    @classmethod
    def validar_proporcion(cls, valor):
        # La proporción debe estar entre 1 y 99
        if valor <= 0 or valor >= 100:
            raise ValueError("La proporción debe estar entre 1 y 99")
        return valor