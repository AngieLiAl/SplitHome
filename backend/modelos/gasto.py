# ──────────────────────────────────────────────────────────────
# MODELO — Gasto (clase base)
# Representa un pago realizado por un miembro del hogar.
# Es la clase padre de GastoCompartido.
# Solo guarda los datos, el DAO se encarga de guardarlos
# en la base de datos PostgreSQL.
# ──────────────────────────────────────────────────────────────
from datetime import date

class Gasto:
    def __init__(self, descripcion, monto, id_persona,
                id_categoria, fecha="", es_compartido=False):
        # El id lo asigna PostgreSQL automáticamente al insertar
        self.id            = None
        self.descripcion   = descripcion
        self.monto         = monto
        self.id_persona    = id_persona
        self.id_categoria  = id_categoria
        # Si no se manda fecha se usa la de hoy
        self.fecha         = fecha or str(date.today())
        self.es_compartido = es_compartido

    def calcular_deuda(self):
        # Divide el monto entre 2 cuando el gasto es compartido
        return round(self.monto / 2, 2)

    def __str__(self):
        return (f"[{self.id}] {self.descripcion} | "
                f"S/. {self.monto:.2f} | {self.fecha} | "
                f"Compartido: {'Sí' if self.es_compartido else 'No'}")

    # Convierte el objeto a diccionario para poder enviarlo como respuesta del API
    def to_dict(self):
        return {
            "id_gasto":      self.id,
            "descripcion":   self.descripcion,
            "monto":         self.monto,
            "fecha":         self.fecha,
            "es_compartido": self.es_compartido,
            "id_persona":    self.id_persona,
            "id_categoria":  self.id_categoria
        }