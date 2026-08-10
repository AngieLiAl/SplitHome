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

router = APIRouter(
    prefix="/personas",
    tags=["Personas"],
    responses={404: {"description": "Persona no encontrada"}}
)
dao = PersonaDAO()

@router.get("/", response_model=list[PersonaRespuesta], summary="Listar todos los miembros")
def listar_personas():
    """
    Devuelve la lista completa de miembros del hogar ordenados por nombre.

    - **id_persona**: identificador único
    - **nombre**: nombre completo del miembro
    - **email**: correo electrónico único
    - **fecha_registro**: fecha en que se registró
    """
    return [p.to_dict() for p in dao.obtener_todos()]

@router.get("/{persona_id}", response_model=PersonaRespuesta, summary="Obtener un miembro por ID")
def obtener_persona(persona_id: int):
    """
    Busca y devuelve un miembro del hogar por su ID.
    Devuelve **404** si el ID no existe.
    """
    p = dao.buscar_por_id(persona_id)
    if not p:
        raise HTTPException(status_code=404, detail=f"Persona ID={persona_id} no encontrada")
    return p.to_dict()

@router.post("/", response_model=PersonaRespuesta, status_code=201, summary="Crear nuevo miembro")
def crear_persona(datos: PersonaCrear):
    """
    Crea un nuevo miembro del hogar.

    - El **email** debe ser único — devuelve **400** si ya está registrado
    - La **fecha_registro** se asigna automáticamente con la fecha de hoy
    """
    try:
        p = dao.insertar(Persona(datos.nombre, datos.email))
        return p.to_dict()
    except EmailDuplicadoError as ex:
        raise HTTPException(status_code=400, detail=str(ex))

@router.put("/{persona_id}", response_model=PersonaRespuesta, summary="Actualizar miembro")
def actualizar_persona(persona_id: int, datos: PersonaActualizar):
    """
    Actualiza los datos de un miembro existente.
    Solo se actualizan los campos que se envíen — los demás quedan igual.
    Devuelve **404** si el ID no existe.
    """
    try:
        p = dao.actualizar(persona_id, datos.nombre, datos.email)
        return p.to_dict()
    except PersonaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.delete("/{persona_id}", summary="Eliminar miembro")
def eliminar_persona(persona_id: int):
    """
    Elimina un miembro del hogar.
    Devuelve **404** si el ID no existe.
    Devuelve **409** si tiene gastos asociados y no se puede eliminar.
    """
    try:
        dao.eliminar(persona_id)
        return {"mensaje": f"Persona ID={persona_id} eliminada correctamente"}
    except PersonaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=409, detail=str(ex))