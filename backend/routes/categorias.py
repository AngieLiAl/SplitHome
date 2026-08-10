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

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"],
    responses={404: {"description": "Categoría no encontrada"}}
)
dao = CategoriaDAO()

@router.get("/", response_model=list[CategoriaRespuesta], summary="Listar todas las categorías")
def listar_categorias():
    """
    Devuelve la lista completa de categorías de gasto ordenadas por nombre.
    Ejemplos: 🏠 Alquiler, 💡 Luz, 💧 Agua, 📶 Internet, 🍛 Comida.
    """
    return [c.to_dict() for c in dao.obtener_todos()]

@router.get("/{categoria_id}", response_model=CategoriaRespuesta, summary="Obtener categoría por ID")
def obtener_categoria(categoria_id: int):
    """
    Busca y devuelve una categoría por su ID.
    Devuelve **404** si el ID no existe.
    """
    c = dao.buscar_por_id(categoria_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Categoría ID={categoria_id} no encontrada")
    return c.to_dict()

@router.post("/", response_model=CategoriaRespuesta, status_code=201, summary="Crear nueva categoría")
def crear_categoria(datos: CategoriaCrear):
    """
    Crea una nueva categoría de gasto.

    - El **nombre** debe ser único — devuelve **400** si ya existe
    - El **icono** es un emoji opcional — por defecto se usa 📦
    """
    try:
        c = dao.insertar(Categoria(datos.nombre, datos.icono, datos.descripcion))
        return c.to_dict()
    except CategoriaDuplicadaError as ex:
        raise HTTPException(status_code=400, detail=str(ex))

@router.put("/{categoria_id}", response_model=CategoriaRespuesta, summary="Actualizar categoría")
def actualizar_categoria(categoria_id: int, datos: CategoriaActualizar):
    """
    Actualiza los datos de una categoría existente.
    Solo se actualizan los campos que se envíen.
    Devuelve **404** si el ID no existe.
    """
    try:
        c = dao.actualizar(categoria_id, datos.nombre, datos.icono)
        return c.to_dict()
    except CategoriaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.delete("/{categoria_id}", summary="Eliminar categoría")
def eliminar_categoria(categoria_id: int):
    """
    Elimina una categoría de gasto.
    Devuelve **404** si el ID no existe.
    Devuelve **409** si tiene gastos asociados y no se puede eliminar.
    """
    try:
        dao.eliminar(categoria_id)
        return {"mensaje": f"Categoría ID={categoria_id} eliminada correctamente"}
    except CategoriaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=409, detail=str(ex))