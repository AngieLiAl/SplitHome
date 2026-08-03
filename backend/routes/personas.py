# ──────────────────────────────────────────────────────────────
# RUTAS — Personas
# Define los endpoints del API para gestionar personas.
# Cada función responde a una petición del frontend:
# GET para obtener, POST para crear, PUT para actualizar
# y DELETE para eliminar.
# ──────────────────────────────────────────────────────────────
from fastapi import APIRouter, HTTPException
from dao.persona_dao import PersonaDAO, PersonaNoEncontradaError, EmailDuplicadoError
from modelos.persona import Persona
from schemas.persona_schemas import PersonaCrear, PersonaActualizar, PersonaRespuesta

# Agrupamos todas las rutas de personas bajo /personas
router = APIRouter(prefix="/personas", tags=["Personas"])
dao = PersonaDAO()

@router.get("/", response_model=list[PersonaRespuesta])
def listar_personas():
    # Devuelve todas las personas registradas
    return [p.to_dict() for p in dao.obtener_todos()]

@router.get("/{persona_id}", response_model=PersonaRespuesta)
def obtener_persona(persona_id: int):
    # Busca una persona por su id
    # Si no existe devuelve error 404
    p = dao.buscar_por_id(persona_id)
    if not p:
        raise HTTPException(
            status_code=404,
            detail=f"Persona ID={persona_id} no encontrada"
        )
    return p.to_dict()

@router.post("/", response_model=PersonaRespuesta, status_code=201)
def crear_persona(datos: PersonaCrear):
    # Crea una nueva persona con los datos que manda el frontend
    # Si el email ya existe devuelve error 400
    try:
        p = dao.insertar(Persona(datos.nombre, datos.email))
        return p.to_dict()
    except EmailDuplicadoError as ex:
        raise HTTPException(status_code=400, detail=str(ex))

@router.put("/{persona_id}", response_model=PersonaRespuesta)
def actualizar_persona(persona_id: int, datos: PersonaActualizar):
    # Actualiza los datos de una persona
    # Solo se actualizan los campos que se manden
    try:
        p = dao.actualizar(persona_id, datos.nombre, datos.email)
        return p.to_dict()
    except PersonaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.delete("/{persona_id}")
def eliminar_persona(persona_id: int):
    # Elimina una persona
    # Si tiene gastos asociados devuelve error 409
    try:
        dao.eliminar(persona_id)
        return {"mensaje": f"Persona ID={persona_id} eliminada correctamente"}
    except PersonaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=409, detail=str(ex))