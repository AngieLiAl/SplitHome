# ──────────────────────────────────────────────────────────────
# CONFIGURACIÓN GENERAL DEL SISTEMA — Patrón Singleton
#
# Este archivo guarda los datos generales del sistema como
# el nombre, versión y quiénes lo hicieron.
# Solo existe UNA sola configuración en todo el programa,
# eso es lo que hace el patrón Singleton.
# ──────────────────────────────────────────────────────────────
from config.logger import Logger

class SistemaConfig:

    # Esta variable guarda la única instancia que existirá
    _inst = None

    def __new__(cls):
        # Solo se crea la configuración UNA sola vez
        # Si ya existe, devuelve la misma que ya había
        if cls._inst is None:
            cls._inst = super().__new__(cls)

            # Datos generales del sistema
            cls._inst.nombre  = "SplitHome"
            cls._inst.version = "1.0"
            cls._inst.empresa = "IESTP Argentina"
            cls._inst.autor   = "Lizarsaburu / Escobedo"

            # Registramos en el historial que el sistema arrancó
            Logger().info(
                f"Sistema iniciado: {cls._inst.nombre} "
                f"v{cls._inst.version} | "
                f"{cls._inst.empresa} | "
                f"{cls._inst.autor}"
            )

        # Siempre devolvemos la misma configuración
        return cls._inst