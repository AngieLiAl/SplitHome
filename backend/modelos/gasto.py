# ──────────────────────────────────────────────────────────────
# MODELO — Gasto (clase base)
# Representa un pago realizado por un miembro del hogar.
# Aplica encapsulamiento en monto y descripcion.
# ──────────────────────────────────────────────────────────────
from datetime import date

class Gasto:
    def __init__(self, descripcion, monto, id_persona, id_categoria, fecha=None, compartido=False):
        self.id           = None  # el DAO asigna el ID al insertar
        self._descripcion = descripcion
        self._monto       = monto
        self.id_persona   = id_persona
        self.id_categoria = id_categoria
        self.fecha        = fecha or str(date.today())
        self.compartido   = compartido

    # ── Encapsulamiento: monto ─────────────────────────────────
    @property
    def monto(self): return self._monto
    @monto.setter
    def monto(self, v):
        if v < 0:
            raise ValueError("El monto no puede ser negativo")
        self._monto = round(v, 2)

    # ── Encapsulamiento: descripcion ───────────────────────────
    @property
    def descripcion(self): return self._descripcion
    @descripcion.setter
    def descripcion(self, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("La descripción no puede estar vacía")
        self._descripcion = v.strip()

    def calcular_deuda(self):
        """División igualitaria entre dos miembros por defecto."""
        return round(self._monto / 2, 2)

    def __str__(self):
        return (f"[{self.id}] {self._descripcion} | "
                f"S/.{self._monto:.2f} | {self.fecha} | "
                f"Persona:{self.id_persona} | Cat:{self.id_categoria} | "
                f"Compartido:{'Sí' if self.compartido else 'No'}")