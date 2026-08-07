# ──────────────────────────────────────────────────────────────
# RUTAS — Categorias
# Define los endpoints del API para gestionar categorías.
# Cada función responde a una petición del frontend:
# GET para obtener, POST para crear, PUT para actualizar
# y DELETE para eliminar.
# ──────────────────────────────────────────────────────────────
from fastapi import APIRouter, HTTPException
from dao.categoria_dao import CategoriaDAO, CategoriaNoEncontradaError, CategoriaDuplicadaError
from modelos.categoria import Categoria
from schemas.categoria_schemas import CategoriaCrear, CategoriaActualizar, CategoriaRespuesta

# Agrupamos todas las rutas de categorías bajo /categorias
router = APIRouter(prefix="/categorias", tags=["Categorias"])
dao = CategoriaDAO()

@router.get("/", response_model=list[CategoriaRespuesta])
def listar_categorias():
    # Devuelve todas las categorías registradas
    return [c.to_dict() for c in dao.obtener_todos()]

@router.get("/{categoria_id}", response_model=CategoriaRespuesta)
def obtener_categoria(categoria_id: int):
    # Busca una categoría por su id
    # Si no existe devuelve error 404
    c = dao.buscar_por_id(categoria_id)
    if not c:
        raise HTTPException(
            status_code=404,
            detail=f"Categoría ID={categoria_id} no encontrada"
        )
    return c.to_dict()

@router.post("/", response_model=CategoriaRespuesta, status_code=201)
def crear_categoria(datos: CategoriaCrear):
    # Crea una nueva categoría con los datos que manda el frontend
    # Si ya existe una categoría con el mismo nombre devuelve error 400
    try:
        c = dao.insertar(
            Categoria(datos.nombre, datos.icono, datos.descripcion)
        )
        return c.to_dict()
    except CategoriaDuplicadaError as ex:
        raise HTTPException(status_code=400, detail=str(ex))

@router.put("/{categoria_id}", response_model=CategoriaRespuesta)
def actualizar_categoria(categoria_id: int, datos: CategoriaActualizar):
    # Actualiza los datos de una categoría
    # Solo se actualizan los campos que se manden
    try:
        c = dao.actualizar(categoria_id, datos.nombre, datos.icono)
        return c.to_dict()
    except CategoriaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.delete("/{categoria_id}")
def eliminar_categoria(categoria_id: int):
    # Elimina una categoría
    # Si tiene gastos asociados devuelve error 409
    try:
        dao.eliminar(categoria_id)
        return {"mensaje": f"Categoría ID={categoria_id} eliminada correctamente"}
    except CategoriaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=409, detail=str(ex))