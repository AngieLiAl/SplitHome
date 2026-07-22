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
        
# ── GASTOS ─────────────────────────────────────────────────────
def agregar_gasto(gdao, pdao, cdao, pardao):
    print("\n--- AGREGAR GASTO ---")
    listar_personas(pdao)
    listar_categorias(cdao)
    try:
        descripcion  = input("  Descripcion  : ")
        monto        = float(input("  Monto        : "))
        id_persona   = int(input("  ID persona que pago: "))
        id_categoria = int(input("  ID categoria : "))
        compartido   = input("  Es compartido? (s/n): ").strip().lower()

        if not pdao.buscar_por_id(id_persona):
            print(f"  ERROR: Persona ID={id_persona} no existe")
            return
        if not cdao.buscar_por_id(id_categoria):
            print(f"  ERROR: Categoria ID={id_categoria} no existe")
            return

        if compartido == "s":
            # Listar personas para elegir quienes participan
            print("\n  Personas disponibles para participar:")
            listar_personas(pdao)
            id_persona2 = int(input("  ID de la otra persona que participa: "))

            if not pdao.buscar_por_id(id_persona2):
                print(f"  ERROR: Persona ID={id_persona2} no existe")
                return
            if id_persona2 == id_persona:
                print("  ERROR: La otra persona debe ser diferente al pagador")
                return

            proporcion = float(
                input("  Proporcion del pagador % (Enter para 50): ").strip() or "50"
            )
            proporcion2 = round(100 - proporcion, 2)

            # Insertar el gasto compartido
            g = gdao.insertar(GastoCompartido(descripcion, monto,
                                            id_persona, id_categoria,
                                            proporcion=proporcion))

            # Calcular montos de cada uno
            monto1 = round(monto * proporcion  / 100, 2)
            monto2 = round(monto * proporcion2 / 100, 2)

            # Registrar participaciones
            pardao.insertar(g.id, id_persona,  proporcion,  monto1)
            pardao.insertar(g.id, id_persona2, proporcion2, monto2)

            print(f"  OK Gasto compartido agregado ID={g.id}")
            print(f"  Persona ID={id_persona}  debe S/. {monto1:.2f} ({proporcion}%)")
            print(f"  Persona ID={id_persona2} debe S/. {monto2:.2f} ({proporcion2}%)")
        else:
            g = gdao.insertar(Gasto(descripcion, monto, id_persona, id_categoria))
            print(f"  OK Gasto agregado con ID={g.id}")

    except ValueError:
        print("  ERROR: Monto e IDs deben ser numeros")

def listar_gastos(gdao):
    print("\n--- GASTOS ---")
    gastos = gdao.obtener_todos()
    if gastos:
        for g in gastos: print(f"  {g}")
    else:
        print("  (No hay gastos registrados)")

def actualizar_gasto(gdao):
    print("\n--- ACTUALIZAR GASTO ---")
    try:
        gasto_id    = int(input("  ID del gasto a actualizar: "))
        descripcion = input("  Nueva descripcion (Enter para no cambiar): ").strip()
        monto_str   = input("  Nuevo monto       (Enter para no cambiar): ").strip()
        fecha       = input("  Nueva fecha       (Enter para no cambiar): ").strip()
        monto       = float(monto_str) if monto_str else None
        g = gdao.actualizar(gasto_id, descripcion or None, monto, fecha or None)
        print(f"  OK Gasto actualizado: {g}")
    except GastoNoEncontradoError as ex:
        print(f"  ERROR: {ex}")
    except ValueError:
        print("  ERROR: ID debe ser entero y monto debe ser numero")

def eliminar_gasto(gdao, pardao):
    print("\n--- ELIMINAR GASTO ---")
    try:
        gasto_id = int(input("  ID del gasto a eliminar: "))
        # Primero eliminar participaciones asociadas
        pardao.eliminar_por_gasto(gasto_id)
        gdao.eliminar(gasto_id)
        print(f"  OK Gasto ID={gasto_id} eliminado")
    except GastoNoEncontradoError as ex:
        print(f"  ERROR: {ex}")
    except ValueError:
        print("  ERROR: El ID debe ser un número entero")

def gastos_por_persona(gdao, pdao):
    print("\n--- GASTOS POR PERSONA ---")
    listar_personas(pdao)
    try:
        persona_id = int(input("  ID de la persona: "))
        gastos = gdao.obtener_por_persona(persona_id)
        if gastos:
            for g in gastos: print(f"  {g}")
        else:
            print("  (Esta persona no tiene gastos registrados)")
    except ValueError:
        print("  ERROR: El ID debe ser un número entero")

def ver_total_gastado(gdao):
    print("\n--- TOTAL GASTADO ---")
    total = gdao.calcular_total()
    print(f"  Total registrado: S/. {total:.2f}")