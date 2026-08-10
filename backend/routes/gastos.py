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

router = APIRouter(
    prefix="/gastos",
    tags=["Gastos"],
    responses={404: {"description": "Gasto no encontrado"}}
)
dao    = GastoDAO()
pardao = ParticipacionDAO()

@router.get("/", response_model=list[GastoRespuesta], summary="Listar todos los gastos")
def listar_gastos():
    """
    Devuelve la lista completa de gastos ordenados del más reciente al más antiguo.
    """
    return [g.to_dict() for g in dao.obtener_todos()]

@router.get("/{gasto_id}", response_model=GastoRespuesta, summary="Obtener gasto por ID")
def obtener_gasto(gasto_id: int):
    """
    Busca y devuelve un gasto por su ID.
    Devuelve **404** si el ID no existe.
    """
    g = dao.buscar_por_id(gasto_id)
    if not g:
        raise HTTPException(status_code=404, detail=f"Gasto ID={gasto_id} no encontrado")
    return g.to_dict()

@router.get("/persona/{persona_id}", response_model=list[GastoRespuesta], summary="Gastos por persona")
def gastos_por_persona(persona_id: int):
    """
    Devuelve todos los gastos que pagó una persona específica.
    """
    return [g.to_dict() for g in dao.obtener_por_persona(persona_id)]

@router.post("/", response_model=GastoRespuesta, status_code=201, summary="Crear gasto simple")
def crear_gasto(datos: GastoCrear):
    """
    Crea un gasto simple pagado por un solo miembro del hogar.

    - El **monto** debe ser mayor a 0
    - La **fecha** es opcional — por defecto se usa la fecha de hoy
    - Si **es_compartido** es true se divide igualmente entre los miembros
    """
    g = dao.insertar(Gasto(
        datos.descripcion, datos.monto,
        datos.id_persona, datos.id_categoria,
        datos.fecha, datos.es_compartido
    ))
    return g.to_dict()

@router.post("/compartido", response_model=GastoRespuesta, status_code=201, summary="Crear gasto compartido")
def crear_gasto_compartido(datos: GastoCompartidoCrear):
    """
    Crea un gasto compartido entre dos miembros del hogar.
    Registra automáticamente las participaciones de cada uno según la proporción.

    - **proporcion** es el porcentaje que le toca al pagador (por defecto 50%)
    - El resto le corresponde al segundo miembro (**id_persona2**)
    - Las dos personas deben ser diferentes — devuelve **400** si son iguales
    """
    if datos.id_persona == datos.id_persona2:
        raise HTTPException(status_code=400, detail="Las dos personas deben ser diferentes")

    g = dao.insertar(GastoCompartido(
        datos.descripcion, datos.monto,
        datos.id_persona, datos.id_categoria,
        datos.fecha, datos.proporcion
    ))

    proporcion2 = round(100 - datos.proporcion, 2)
    monto1      = round(datos.monto * datos.proporcion  / 100, 2)
    monto2      = round(datos.monto * proporcion2       / 100, 2)

    pardao.insertar(g.id, datos.id_persona,  datos.proporcion, monto1)
    pardao.insertar(g.id, datos.id_persona2, proporcion2,      monto2)

    return g.to_dict()

@router.put("/{gasto_id}", response_model=GastoRespuesta, summary="Actualizar gasto")
def actualizar_gasto(gasto_id: int, datos: GastoActualizar):
    """
    Actualiza los datos de un gasto existente.
    Solo se actualizan los campos que se envíen.
    Devuelve **404** si el ID no existe.
    """
    try:
        g = dao.actualizar(
            gasto_id, datos.descripcion,
            datos.monto, datos.fecha, datos.id_categoria
        )
        return g.to_dict()
    except GastoNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.delete("/{gasto_id}", summary="Eliminar gasto")
def eliminar_gasto(gasto_id: int):
    """
    Elimina un gasto y sus participaciones asociadas.
    PostgreSQL elimina las participaciones automáticamente gracias al ON DELETE CASCADE.
    Devuelve **404** si el ID no existe.
    """
    try:
        dao.eliminar(gasto_id)
        return {"mensaje": f"Gasto ID={gasto_id} eliminado correctamente"}
    except GastoNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.get("/{gasto_id}/participaciones", summary="Ver participaciones de un gasto")
def ver_participaciones(gasto_id: int):
    """
    Devuelve quién participa en un gasto compartido y cuánto le toca pagar a cada uno.
    """
    return pardao.buscar_por_gasto(gasto_id)

@router.get("/balance/{persona_id}", summary="Balance de una persona")
def balance_persona(persona_id: int):
    """
    Devuelve el total que debe pagar una persona sumando todos sus montos asignados en participaciones.
    """
    resultado = pardao.calcular_balance([persona_id])
    return {
        "id_persona":    persona_id,
        "total_a_pagar": resultado[persona_id]
    }