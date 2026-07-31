# ──────────────────────────────────────────────────────────────
# PATRÓN SINGLETON — SistemaConfig
# Centraliza la configuración del sistema. Al ser Singleton, todos los módulos leen los mismos datos sin pasarlos como parámetros cada vez.
# ──────────────────────────────────────────────────────────────
from config.logger import Logger

class SistemaConfig:
    _inst = None

    def __new__(cls):
        if cls._inst is None:
            cls._inst = super().__new__(cls)
            cls._inst.nombre  = "SplitHome"
            cls._inst.version = "1.0"
            cls._inst.empresa = "IESTP Argentina"
            cls._inst.autor   = "Lizarsaburu / Escobedo"
            Logger().info(
                f"Sistema iniciado: {cls._inst.nombre} "
                f"v{cls._inst.version} | "
                f"{cls._inst.empresa} | "
                f"{cls._inst.autor}"
            )
        return cls._inst