# ──────────────────────────────────────────────────────────────
# MODELO — Persona
# Representa a un miembro del hogar que participa en los gastos.
# Solo guarda los datos, el DAO se encarga de guardarlos
# en la base de datos PostgreSQL.
# ──────────────────────────────────────────────────────────────
from datetime import date

class Persona:
    def __init__(self, nombre, email, fecha_registro=""):
        # El id empieza en None porque PostgreSQL lo asigna
        # automáticamente cuando se inserta en la base de datos
        self.id             = None
        self.nombre         = nombre
        self.email          = email
        # Si no se manda fecha, se usa la de hoy
        self.fecha_registro = fecha_registro or str(date.today())

    def __str__(self):
        return f"[{self.id}] {self.nombre} | {self.email} | {self.fecha_registro}"

    # Convierte el objeto a diccionario para poder enviarlo como respuesta del API
    def to_dict(self):
        return {
            "id_persona":     self.id,
            "nombre":         self.nombre,
            "email":          self.email,
            "fecha_registro": self.fecha_registro
        }