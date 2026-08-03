# ──────────────────────────────────────────────────────────────
# RUTAS — Gastos
# Define los endpoints del API para gestionar gastos.
# Incluye endpoints especiales para gastos compartidos
# que también registran las participaciones de cada miembro.
# ──────────────────────────────────────────────────────────────
from fastapi import APIRouter, HTTPException
from dao.gasto_dao import GastoDAO, GastoNoEncontradoError
from dao.participacion_dao import ParticipacionDAO
from modelos.gasto import Gasto
from modelos.gasto_compartido import GastoCompartido
from schemas.gasto_schemas import (
    GastoCrear, GastoActualizar,
    GastoRespuesta, GastoCompartidoCrear
)

# Agrupamos todas las rutas de gastos bajo /gastos
router = APIRouter(prefix="/gastos", tags=["Gastos"])
dao    = GastoDAO()
pardao = ParticipacionDAO()

@router.get("/", response_model=list[GastoRespuesta])
def listar_gastos():
    # Devuelve todos los gastos registrados
    return [g.to_dict() for g in dao.obtener_todos()]

@router.get("/{gasto_id}", response_model=GastoRespuesta)
def obtener_gasto(gasto_id: int):
    # Busca un gasto por su id
    # Si no existe devuelve error 404
    g = dao.buscar_por_id(gasto_id)
    if not g:
        raise HTTPException(
            status_code=404,
            detail=f"Gasto ID={gasto_id} no encontrado"
        )
    return g.to_dict()

@router.get("/persona/{persona_id}", response_model=list[GastoRespuesta])
def gastos_por_persona(persona_id: int):
    # Devuelve todos los gastos que pagó una persona específica
    return [g.to_dict() for g in dao.obtener_por_persona(persona_id)]

@router.post("/", response_model=GastoRespuesta, status_code=201)
def crear_gasto(datos: GastoCrear):
    # Crea un gasto simple (no compartido)
    g = dao.insertar(Gasto(
        datos.descripcion,
        datos.monto,
        datos.id_persona,
        datos.id_categoria,
        datos.fecha,
        datos.es_compartido
    ))
    return g.to_dict()

@router.post("/compartido", response_model=GastoRespuesta, status_code=201)
def crear_gasto_compartido(datos: GastoCompartidoCrear):
    # Crea un gasto compartido y registra automáticamente
    # las participaciones de cada miembro según la proporción
    if datos.id_persona == datos.id_persona2:
        raise HTTPException(
            status_code=400,
            detail="Las dos personas deben ser diferentes"
        )

    # Creamos el gasto compartido usando la clase GastoCompartido
    g = dao.insertar(GastoCompartido(
        datos.descripcion,
        datos.monto,
        datos.id_persona,
        datos.id_categoria,
        datos.fecha,
        datos.proporcion
    ))

    # Calculamos cuánto le toca a cada uno según la proporción
    proporcion2   = round(100 - datos.proporcion, 2)
    monto1        = round(datos.monto * datos.proporcion  / 100, 2)
    monto2        = round(datos.monto * proporcion2       / 100, 2)

    # Registramos la participación de cada miembro
    pardao.insertar(g.id, datos.id_persona,  datos.proporcion, monto1)
    pardao.insertar(g.id, datos.id_persona2, proporcion2,      monto2)

    return g.to_dict()

@router.put("/{gasto_id}", response_model=GastoRespuesta)
def actualizar_gasto(gasto_id: int, datos: GastoActualizar):
    # Actualiza los datos de un gasto
    # Solo se actualizan los campos que se manden
    try:
        g = dao.actualizar(
            gasto_id,
            datos.descripcion,
            datos.monto,
            datos.fecha,
            datos.id_categoria
        )
        return g.to_dict()
    except GastoNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.delete("/{gasto_id}")
def eliminar_gasto(gasto_id: int):
    # Elimina un gasto y sus participaciones
    # PostgreSQL elimina las participaciones automáticamente
    # gracias al ON DELETE CASCADE
    try:
        dao.eliminar(gasto_id)
        return {"mensaje": f"Gasto ID={gasto_id} eliminado correctamente"}
    except GastoNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.get("/{gasto_id}/participaciones")
def ver_participaciones(gasto_id: int):
    # Devuelve quién participa en un gasto compartido
    # y cuánto le toca pagar a cada uno
    return pardao.buscar_por_gasto(gasto_id)

@router.get("/balance/{persona_id}")
def balance_persona(persona_id: int):
    # Devuelve el total que debe pagar una persona
    # sumando todos sus montos asignados en participaciones
    resultado = pardao.calcular_balance([persona_id])
    return {
        "id_persona":   persona_id,
        "total_a_pagar": resultado[persona_id]
    }