# ──────────────────────────────────────────────────────────────
# MODELO — GastoCompartido (hereda de Gasto)
# Aplica HERENCIA y POLIMORFISMO:
#   - Hereda todos los atributos y métodos de Gasto
#   - Sobreescribe calcular_deuda() para distribuir por proporción
# ──────────────────────────────────────────────────────────────
from modelos.gasto import Gasto

class GastoCompartido(Gasto):
    def __init__(self, descripcion, monto, id_persona, id_categoria,
                fecha=None, proporcion=50.0):
        # super() llama al constructor de la clase padre (Gasto)
        super().__init__(descripcion, monto, id_persona, id_categoria,
                        fecha, compartido=True)
        self.proporcion = proporcion  # porcentaje que le corresponde al pagador

    def calcular_deuda(self):
        """Polimorfismo: calcula la deuda según la proporción pactada."""
        parte_otro = round(self._monto * (1 - self.proporcion / 100), 2)
        return parte_otro

    def __str__(self):
        base = super().__str__()
        return f"{base} | Proporción:{self.proporcion}%"