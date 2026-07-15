# ──────────────────────────────────────────────────────────────
# MODELO — Categoria
# Clasificación temática de los gastos del hogar.
# Solo guarda datos, el DAO se encarga de guardar en SQLite.
# ──────────────────────────────────────────────────────────────
class Categoria:
    def __init__(self, nombre, icono="📦", descripcion=""):
        self.id          = None
        self.nombre      = nombre
        self.icono       = icono
        self.descripcion = descripcion

    def __str__(self):
        return f"[{self.id}] {self.icono} {self.nombre}"