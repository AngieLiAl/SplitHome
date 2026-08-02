# ──────────────────────────────────────────────────────────────
# MODELO — Categoria
# Representa una categoría de gasto del hogar
# como Alquiler, Luz, Agua, etc.
# Solo guarda los datos, el DAO se encarga de guardarlos
# en la base de datos PostgreSQL.
# ──────────────────────────────────────────────────────────────
class Categoria:
    def __init__(self, nombre, icono="📦", descripcion=""):
        # El id lo asigna PostgreSQL automáticamente al insertar
        self.id          = None
        self.nombre      = nombre
        self.icono       = icono
        self.descripcion = descripcion

    def __str__(self):
        return f"[{self.id}] {self.icono} {self.nombre}"

    # Convierte el objeto a diccionario para poder enviarlo como respuesta del API
    def to_dict(self):
        return {
            "id_categoria": self.id,
            "nombre":       self.nombre,
            "icono":        self.icono,
            "descripcion":  self.descripcion
        }