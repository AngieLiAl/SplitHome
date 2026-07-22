# ──────────────────────────────────────────────────────────────
# Funciones del menú
# Pedir datos con input() y mostrar
# resultados con print(). 
# ──────────────────────────────────────────────────────────────
from config.logger import Logger
from modelos.persona import Persona
from modelos.categoria import Categoria
from modelos.gasto import Gasto
from modelos.gasto_compartido import GastoCompartido
from dao.persona_dao import PersonaDAO, PersonaNoEncontradaError, EmailDuplicadoError
from dao.categoria_dao import CategoriaDAO, CategoriaNoEncontradaError, CategoriaDuplicadaError
from dao.gasto_dao import GastoDAO, GastoNoEncontradoError
from dao.participacion_dao import ParticipacionDAO

def mostrar_menu(cfg):
    print(f"\n{'=' * 45}")
    print(f"  {cfg.nombre} v{cfg.version}")
    print(f"  {cfg.empresa}")
    print(f"{'=' * 45}")
    print("  -- PERSONAS ------------------")
    print("  1. Agregar persona")
    print("  2. Listar personas")
    print("  3. Actualizar persona")
    print("  4. Eliminar persona")
    print("  -- CATEGORIAS ----------------")
    print("  5. Agregar categoria")
    print("  6. Listar categorias")
    print("  7. Actualizar categoria")
    print("  8. Eliminar categoria")
    print("  -- GASTOS --------------------")
    print("  9.  Agregar gasto")
    print("  10. Listar gastos")
    print("  11. Actualizar gasto")
    print("  12. Eliminar gasto")
    print("  13. Ver gastos por persona")
    print("  14. Ver total gastado")
    print("  -- PARTICIPACIONES -----------")
    print("  15. Ver participaciones de un gasto")
    print("  16. Ver gastos de una persona")
    print("  17. Ver balance entre miembros")
    print("  -- LOGS ----------------------")
    print("  18. Ver historial de logs")
    print("  19. Limpiar historial de logs")
    print("  0. Salir")
    print(f"{'=' * 45}")