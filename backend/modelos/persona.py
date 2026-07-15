# ──────────────────────────────────────────────────────────────
# MODELO — Persona
# Representa a un miembro del hogar que participa en los gastos.
# Solo guarda datos, el DAO se encarga de guardar en SQLite.
# ──────────────────────────────────────────────────────────────
from datetime import date

class Persona:
    def __init__(self, nombre, email, fecha_registro=""):
        self.id             = None
        self.nombre         = nombre
        self.email          = email
        self.fecha_registro = fecha_registro or str(date.today())

    def __str__(self):
        return f"[{self.id}] {self.nombre} | {self.email} | {self.fecha_registro}"