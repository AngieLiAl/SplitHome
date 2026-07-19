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

def main():
    inicializar()

    cfg    = SistemaConfig()
    pdao   = PersonaDAO()
    cdao   = CategoriaDAO()
    gdao   = GastoDAO()
    pardao = ParticipacionDAO()
    
    while True:
        mostrar_menu(cfg)
        opcion = input("  Elige una opción: ").strip()
        
        match opcion:
            case "1":  agregar_persona(pdao)
            case "2":  listar_personas(pdao)
            case "3":  actualizar_persona(pdao)
            case "4":  eliminar_persona(pdao)
            case "5":  agregar_categoria(cdao)
            case "6":  listar_categorias(cdao)
            case "7":  actualizar_categoria(cdao)
            case "8":  eliminar_categoria(cdao)
            case "9":  agregar_gasto(gdao, pdao, cdao, pardao)
            case "10": listar_gastos(gdao)
            case "11": actualizar_gasto(gdao)
            case "12": eliminar_gasto(gdao, pardao)
            case "13": gastos_por_persona(gdao, pdao)
            case "14": ver_total_gastado(gdao)
            case "15": ver_participaciones_gasto(pardao)
            case "16": ver_gastos_persona(pardao, pdao)
            case "17": ver_balance(pardao, pdao)
            case "18": Logger().mostrar_logs()
            case "19": Logger().limpiar()
            case "0":
                Logger().info("Sistema cerrado por el usuario")
                print("\n  Hasta luego.")
                break
            case _:
                print("  Opción no válida, elige entre 0 y 19")
            