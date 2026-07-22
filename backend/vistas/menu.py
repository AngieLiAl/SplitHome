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
    
    # ── PERSONAS ───────────────────────────────────────────────────
def agregar_persona(pdao):
    print("\n--- AGREGAR PERSONA ---")
    nombre = input("  Nombre : ")
    email  = input("  Email  : ")
    try:
        p = pdao.insertar(Persona(nombre, email))
        print(f"  OK Persona agregada con ID={p.id}")
    except EmailDuplicadoError as ex:
        print(f"  ERROR: {ex}")

def listar_personas(pdao):
    print("\n--- PERSONAS ---")
    personas = pdao.obtener_todos()
    if personas:
        for p in personas: print(f"  {p}")
    else:
        print("  (No hay personas registradas)")

def actualizar_persona(pdao):
    print("\n--- ACTUALIZAR PERSONA ---")
    try:
        persona_id = int(input("  ID de la persona a actualizar: "))
        nombre     = input("  Nuevo nombre (Enter para no cambiar): ").strip()
        email      = input("  Nuevo email  (Enter para no cambiar): ").strip()
        p = pdao.actualizar(persona_id, nombre or None, email or None)
        print(f"  OK Persona actualizada: {p}")
    except PersonaNoEncontradaError as ex:
        print(f"  ERROR: {ex}")
    except ValueError:
        print("  ERROR: El ID debe ser un número entero")

def eliminar_persona(pdao):
    print("\n--- ELIMINAR PERSONA ---")
    try:
        persona_id = int(input("  ID de la persona a eliminar: "))
        pdao.eliminar(persona_id)
        print(f"  OK Persona ID={persona_id} eliminada")
    except PersonaNoEncontradaError as ex:
        print(f"  ERROR: {ex}")
    except ValueError:
        print("  ERROR: El ID debe ser un número entero")
        
# ── CATEGORIAS ─────────────────────────────────────────────────
def agregar_categoria(cdao):
    print("\n--- AGREGAR CATEGORIA ---")
    nombre      = input("  Nombre      : ")
    icono       = input("  Icono (emoji, Enter para 📦): ").strip()
    descripcion = input("  Descripcion : ")
    try:
        c = cdao.insertar(Categoria(nombre, icono or "📦", descripcion))
        print(f"  OK Categoria agregada con ID={c.id}")
    except CategoriaDuplicadaError as ex:
        print(f"  ERROR: {ex}")

def listar_categorias(cdao):
    print("\n--- CATEGORIAS ---")
    categorias = cdao.obtener_todos()
    if categorias:
        for c in categorias: print(f"  {c}")
    else:
        print("  (No hay categorias registradas)")

def actualizar_categoria(cdao):
    print("\n--- ACTUALIZAR CATEGORIA ---")
    try:
        categoria_id = int(input("  ID de la categoria a actualizar: "))
        nombre       = input("  Nuevo nombre (Enter para no cambiar): ").strip()
        icono        = input("  Nuevo icono  (Enter para no cambiar): ").strip()
        c = cdao.actualizar(categoria_id, nombre or None, icono or None)
        print(f"  OK Categoria actualizada: {c}")
    except CategoriaNoEncontradaError as ex:
        print(f"  ERROR: {ex}")
    except ValueError:
        print("  ERROR: El ID debe ser un número entero")

def eliminar_categoria(cdao):
    print("\n--- ELIMINAR CATEGORIA ---")
    try:
        categoria_id = int(input("  ID de la categoria a eliminar: "))
        cdao.eliminar(categoria_id)
        print(f"  OK Categoria ID={categoria_id} eliminada")
    except CategoriaNoEncontradaError as ex:
        print(f"  ERROR: {ex}")
    except ValueError:
        print("  ERROR: El ID debe ser un número entero")