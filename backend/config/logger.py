# ──────────────────────────────────────────────────────────────
# HISTORIAL DE EVENTOS — Patrón Singleton
#
# Este archivo registra todo lo que pasa en el sistema:
# cuando se agrega un gasto, cuando hay un error, etc.
# También existe una SOLA instancia del historial en todo
# el programa, así todos los módulos comparten el mismo registro.
# ──────────────────────────────────────────────────────────────
import datetime

class Logger:

    # Variable que guarda la única instancia del historial
    _instancia = None

    def __new__(cls):
        # Si todavía no existe el historial, lo creamos
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            # Lista donde se guardarán todos los eventos
            cls._instancia._logs = []
        # Si ya existe, devolvemos el mismo
        return cls._instancia

    def _registrar(self, nivel, mensaje):
        # Guardamos la hora exacta en que ocurrió el evento
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        # Cada evento se guarda con su hora, nivel e información
        entrada = {"hora": hora, "nivel": nivel, "msg": mensaje}
        self._logs.append(entrada)

    # Registra un evento normal (todo salió bien)
    def info(self, msg):
        self._registrar("INFO", msg)

    # Registra una advertencia (algo raro pasó pero no es grave)
    def warning(self, msg):
        self._registrar("WARNING", msg)

    # Registra un error (algo salió mal)
    def error(self, msg):
        self._registrar("ERROR", msg)

    def mostrar_logs(self):
        # Muestra todo el historial de eventos
        print(f"\n=== HISTORIAL DEL SISTEMA ({len(self._logs)} eventos) ===")
        for log in self._logs:
            # :7 alinea las columnas aunque los niveles tengan diferente largo
            print(f"  [{log['hora']}] {log['nivel']:7} | {log['msg']}")

    def limpiar(self):
        # Borra todos los eventos del historial
        self._logs.clear()
        print("  OK Historial de logs limpiado")