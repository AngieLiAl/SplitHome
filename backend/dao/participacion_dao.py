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
        
    def buscar_por_gasto(self, id_gasto):
        """Devuelve todas las participaciones de un gasto compartido."""
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT p.id_gasto, p.id_persona, pe.nombre, 
                    p.proporcion, p.monto_asignado
            FROM participacion p
            JOIN personas pe ON p.id_persona = pe.id
            WHERE p.id_gasto = ?""",
            (id_gasto,)
        )
        filas = cursor.fetchall()
        conn.close()
        return filas
    
    def buscar_por_persona(self, id_persona):
        """Devuelve todos los gastos en los que participa una persona."""
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT p.id_gasto, g.descripcion, g.monto,
                    p.proporcion, p.monto_asignado
            FROM participacion p
            JOIN gastos g ON p.id_gasto = g.id
            WHERE p.id_persona = ?
            ORDER BY g.fecha DESC""",
            (id_persona,)
        )
        filas = cursor.fetchall()
        conn.close()
        return filas