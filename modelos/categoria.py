# ──────────────────────────────────────────────────────────────
# MODELO — Categoria
# Clasificación temática de los gastos del hogar.
# ──────────────────────────────────────────────────────────────
class Categoria:
    def __init__(self, nombre, icono="📦"):
        self.id     = None  # el DAO asigna el ID al insertar
        self._nombre = nombre
        self.icono   = icono

    @property
    def nombre(self): return self._nombre
    @nombre.setter
    def nombre(self, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("El nombre de categoría no puede estar vacío")
        self._nombre = v.strip()

    def __str__(self):
        return f"[{self.id}] {self.icono} {self._nombre}"