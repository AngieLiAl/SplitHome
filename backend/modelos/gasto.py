# ──────────────────────────────────────────────────────────────
# MODELO — Gasto (clase base)
# Representa un pago realizado por un miembro del hogar.
# Solo guarda datos, el DAO se encarga de guardar en SQLite.
# ──────────────────────────────────────────────────────────────
from datetime import date

class Gasto:
    def __init__(self, descripcion, monto, id_persona,
                id_categoria, fecha="", es_compartido=False):
        self.id            = None
        self.descripcion   = descripcion
        self.monto         = monto
        self.id_persona    = id_persona
        self.id_categoria  = id_categoria
        self.fecha         = fecha or str(date.today())
        self.es_compartido = es_compartido

    def calcular_deuda(self):
        """División igualitaria entre dos miembros por defecto."""
        return round(self.monto / 2, 2)

    def __str__(self):
        return (f"[{self.id}] {self.descripcion} | "
                f"S/. {self.monto:.2f} | {self.fecha} | "
                f"Compartido: {'Sí' if self.es_compartido else 'No'}")