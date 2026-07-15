# ──────────────────────────────────────────────────────────────
# MODELO — GastoCompartido (hereda de Gasto)
# Aplica HERENCIA y POLIMORFISMO:
#   - Hereda todos los atributos de Gasto
#   - Sobreescribe calcular_deuda() según proporción pactada
# ──────────────────────────────────────────────────────────────
from modelos.gasto import Gasto

class GastoCompartido(Gasto):
    def __init__(self, descripcion, monto, id_persona,
                id_categoria, fecha="", proporcion=50.0):
        # super() llama al constructor de Gasto
        super().__init__(descripcion, monto, id_persona,
                        id_categoria, fecha, es_compartido=True)
        self.proporcion = proporcion

    def calcular_deuda(self):
        """Polimorfismo: calcula la deuda según la proporción pactada."""
        return round(self.monto * (1 - self.proporcion / 100), 2)

    def __str__(self):
        base = super().__str__()
        return f"{base} | Proporción: {self.proporcion}%"