# ──────────────────────────────────────────────────────────────
# MODELO — GastoCompartido (hereda de Gasto)
# Cuando un gasto se divide entre los miembros del hogar
# se usa esta clase en vez de Gasto directamente.
# Aplica HERENCIA (hereda de Gasto) y POLIMORFISMO
# (sobreescribe calcular_deuda con su propia lógica)
# ──────────────────────────────────────────────────────────────
from modelos.gasto import Gasto

class GastoCompartido(Gasto):
    def __init__(self, descripcion, monto, id_persona,
                id_categoria, fecha="", proporcion=50.0):
        # Llama al constructor de Gasto para heredar todos sus atributos
        super().__init__(descripcion, monto, id_persona,
                        id_categoria, fecha, es_compartido=True)
        # Porcentaje del gasto que le toca al pagador
        self.proporcion = proporcion

    def calcular_deuda(self):
        # Calcula cuánto le toca pagar al otro miembro
        # según la proporción que se definió al crear el gasto
        return round(self.monto * (1 - self.proporcion / 100), 2)

    def __str__(self):
        # Muestra la información del gasto más la proporción
        base = super().__str__()
        return f"{base} | Proporción: {self.proporcion}%"