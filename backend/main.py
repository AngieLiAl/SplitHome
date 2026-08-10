from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.base_datos import inicializar
from routes import personas, categorias, gastos

# Descripción completa que aparece en el Swagger
descripcion = """
## SplitHome — API REST

Sistema para gestionar los gastos compartidos del hogar.

### Funcionalidades principales:
- 👥 **Personas** — Gestión de miembros del hogar
- 🏷️ **Categorías** — Clasificación de gastos por tipo
- 🧾 **Gastos** — Registro y seguimiento de pagos
- ⚖️ **Balance** — Cálculo automático de quién debe a quién

### Pilares POO aplicados:
- **Encapsulamiento** — Atributos privados con validación
- **Herencia** — GastoCompartido hereda de Gasto
- **Polimorfismo** — calcular_deuda() se comporta diferente según el tipo
- **Abstracción** — Gasto define la interfaz común
"""

app = FastAPI(
    title="SplitHome API",
    version="1.0.0",
    description=descripcion,
    contact={
        "name": "Angie Lizarsaburu Alfaro / Angela Escobedo Quispe",
        "email": "angie.lizarsaburua@istpargentina.edu.pe",
    },
    license_info={
        "name": "Proyecto Académico — IESTP Argentina 2026-I",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

inicializar()

app.include_router(personas.router)
app.include_router(categorias.router)
app.include_router(gastos.router)

@app.get("/", tags=["Inicio"])
def inicio():
    """
    Ruta principal del API.
    Devuelve información general del sistema y links útiles.
    """
    return {
        "sistema":    "SplitHome — Gestor de Gastos Compartidos",
        "version":    "1.0.0",
        "autoras":    "Lizarsaburu / Escobedo",
        "institucion":"IESTP Argentina 2026-I",
        "docs":       "http://localhost:8000/docs",
        "endpoints":  "http://localhost:8000/openapi.json",
    }