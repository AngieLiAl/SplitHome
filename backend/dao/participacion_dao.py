# ──────────────────────────────────────────────────────────────
# DAO — ParticipacionDAO
# Encapsula el acceso a la tabla participacion.
# Registra qué personas participan en un gasto compartido
# y cuánto le corresponde pagar a cada una.
# ──────────────────────────────────────────────────────────────
from config.logger import Logger
from config.base_datos import obtener_conexion

class ParticipacionNoEncontradaError(Exception):
    def __init__(self, id_gasto, id_persona):
        super().__init__(f"Participacion Gasto ID={id_gasto} Persona ID={id_persona} no encontrada")

class ParticipacionDAO:
    def __init__(self):
        self.__log = Logger()

    def insertar(self, id_gasto, id_persona, proporcion, monto_asignado):
        """Registra que una persona participa en un gasto compartido."""
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO participacion
            (id_gasto, id_persona, proporcion, monto_asignado)
            VALUES (?, ?, ?, ?)""",
            (id_gasto, id_persona, proporcion, monto_asignado)
        )
        conn.commit()
        conn.close()
        self.__log.info(
            f"Participacion registrada: Gasto ID={id_gasto} "
            f"Persona ID={id_persona} S/. {monto_asignado:.2f}"
        )