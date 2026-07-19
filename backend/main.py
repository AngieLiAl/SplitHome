from config.base_datos import inicializar
from config.sistema_config import SistemaConfig
from config.logger import Logger
from dao.persona_dao import PersonaDAO
from dao.categoria_dao import CategoriaDAO
from dao.gasto_dao import GastoDAO
from dao.participacion_dao import ParticipacionDAO

from vistas.menu import (
    mostrar_menu,
    agregar_persona, listar_personas,
    actualizar_persona, eliminar_persona,
    agregar_categoria, listar_categorias,
    actualizar_categoria, eliminar_categoria,
    agregar_gasto, listar_gastos,
    actualizar_gasto, eliminar_gasto,
    gastos_por_persona, ver_total_gastado,
    ver_participaciones_gasto, ver_gastos_persona,
    ver_balance
)

