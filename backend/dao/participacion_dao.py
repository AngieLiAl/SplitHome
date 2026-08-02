# ──────────────────────────────────────────────────────────────
# DAO — ParticipacionDAO
# Se encarga de registrar quién participa en cada gasto
# compartido y cuánto le toca pagar a cada uno.
# Antes usaba una lista en memoria, ahora usa la base de datos
# real de PostgreSQL para guardar esa información.
# ──────────────────────────────────────────────────────────────
import psycopg2
from config.logger import Logger
from config.base_datos import obtener_conexion

# Error personalizado cuando no se encuentra una participación
class ParticipacionNoEncontradaError(Exception):
    def __init__(self, id_gasto, id_persona):
        super().__init__(f"Participacion Gasto ID= {id_gasto} "
            f"Persona ID={id_persona} no encontrada")

class ParticipacionDAO:
    def __init__(self):
        # Usamos el mismo historial de eventos que todo el sistema
        self.__log = Logger()

    def insertar(self, id_gasto, id_persona, proporcion, monto_asignado):
        # Registra que una persona participa en un gasto compartido
        # y cuánto le corresponde pagar según la proporción acordada
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO participacion
            (id_gasto, id_persona, proporcion, monto_asignado)
            VALUES (%s, %s, %s, %s)""",
            (id_gasto, id_persona, proporcion, monto_asignado)
        )
        conn.commit()
        conn.close()
        self.__log.info(
            f"Participacion registrada: Gasto ID={id_gasto} "
            f"Persona ID={id_persona} "
            f"S/. {monto_asignado:.2f}"
        )
        
    def buscar_por_gasto(self, id_gasto):
        # Devuelve todas las personas que participan en un gasto
        # junto con su proporción y monto asignado
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT p.id_gasto, p.id_persona, pe.nombre, 
                    p.proporcion, p.monto_asignado
            FROM participacion p
            JOIN persona pe ON p.id_persona = pe.id_persona
            WHERE p.id_gasto = %s""",
            (id_gasto,)
        )
        filas = cursor.fetchall()
        conn.close()
        # Convertimos cada fila a diccionario para poder usarla fácilmente
        return [dict(f) for f in filas]
    
    def buscar_por_persona(self, id_persona):
        # Devuelve todos los gastos compartidos en los que
        # participa una persona específica
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT p.id_gasto, g.descripcion, g.monto,
                    p.proporcion, p.monto_asignado
            FROM participacion p
            JOIN gasto g ON p.id_gasto = g.id_gasto
            WHERE p.id_persona = %s
            ORDER BY g.fecha DESC""",
            (id_persona,)
        )
        filas = cursor.fetchall()
        conn.close()
        return [dict(f) for f in filas]
    
    def eliminar_por_gasto(self, id_gasto):
        # Elimina todas las participaciones de un gasto
        # Esto se usa antes de eliminar el gasto manualmente
        # aunque PostgreSQL también lo hace automáticamente
        # gracias al ON DELETE CASCADE
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM participacion WHERE id_gasto = %s",
            (id_gasto,)
        )
        conn.commit()
        conn.close()
        self.__log.info(f"Participaciones eliminadas del Gasto ID={id_gasto}")
        
    def calcular_balance(self, persona_ids):
        # Calcula cuánto debe pagar cada persona en total
        # sumando todos sus montos asignados en participaciones
        conn = obtener_conexion()
        cursor = conn.cursor()
        balance = {}
        for pid in persona_ids:
            cursor.execute(
                """SELECT SUM(monto_asignado) AS total FROM participacion WHERE id_persona = %s""",
                (pid,)
            )
            resultado = cursor.fetchone()["total"]
            # Si no tiene participaciones devuelve 0
            balance[pid] = round(resultado or 0.0, 2)
        conn.close()
        return balance
    
    def total(self):
        # Devuelve cuántas participaciones hay registradas en total
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM participacion")
        total = cursor.fetchone()["total"]
        conn.close()
        return total