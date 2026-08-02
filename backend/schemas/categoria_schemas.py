# ──────────────────────────────────────────────────────────────
# SCHEMAS — Categoria
# Define cómo deben verse los datos que llegan y salen
# del API para las categorías.
# Pydantic valida automáticamente que los datos sean correctos
# antes de que lleguen al DAO.
# ──────────────────────────────────────────────────────────────
from pydantic import BaseModel, field_validator
from typing import Optional

class CategoriaCrear(BaseModel):
    # Datos que se necesitan para crear una nueva categoría
    nombre:      str
    icono:       Optional[str] = "📦"
    descripcion: Optional[str] = ""

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor):
        # El nombre no puede estar vacío ni tener solo espacios
        if not valor.strip():
            raise ValueError("El nombre de la categoría no puede estar vacío")
        return valor.strip()

class CategoriaActualizar(BaseModel):
    # Todos los campos son opcionales para poder actualizar
    # solo lo que se necesite
    nombre:      Optional[str] = None
    icono:       Optional[str] = None
    descripcion: Optional[str] = None

class CategoriaRespuesta(BaseModel):
    # Así se verán los datos cuando el API los devuelva
    id_categoria: int
    nombre:       str
    icono:        Optional[str] = None
    descripcion:  Optional[str] = None