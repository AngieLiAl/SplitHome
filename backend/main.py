# ──────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA — FastAPI
# Este archivo arranca el servidor del API y conecta
# todas las rutas (personas, categorias, gastos).
# También configura el CORS para que el frontend en React
# pueda comunicarse con el backend sin problemas.
# ──────────────────────────────────────────────────────────────
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.base_datos import inicializar
from routes import personas, categorias, gastos

# Creamos la aplicación FastAPI con información del proyecto
app = FastAPI(
    title="SplitHome API",
    version="1.0",
    description="API REST para gestionar gastos compartidos del hogar"
)

# ── CORS ──────────────────────────────────────────────────────
# CORS le permite al frontend en React (que corre en otro puerto)
# hacer peticiones al backend sin que el navegador las bloquee
app.add_middleware(
    CORSMiddleware,
    # Direcciones desde donde se puede acceder al API
    allow_origins=[
        "http://localhost:5173",  # Vite (React en desarrollo)
        "http://localhost:3000",  # Por si se usa otro puerto
    ],
    allow_credentials=True,
    allow_methods=["*"],    # Permite GET, POST, PUT, DELETE
    allow_headers=["*"],    # Permite cualquier cabecera
)

# ── INICIALIZAR BASE DE DATOS ─────────────────────────────────
# Crea las tablas en PostgreSQL si todavía no existen
# Esto se ejecuta cada vez que arranca el servidor
inicializar()

# ── REGISTRAR RUTAS ───────────────────────────────────────────
# Conectamos cada archivo de rutas al servidor
app.include_router(personas.router)
app.include_router(categorias.router)
app.include_router(gastos.router)

# ── RUTA PRINCIPAL ────────────────────────────────────────────
@app.get("/")
def inicio():
    # Cuando alguien entra a la raíz del API ve esta información
    return {
        "mensaje":  "API SplitHome — Gestor de Gastos Compartidos",
        "version":  "1.0",
        "autor":    "Lizarsaburu / Escobedo",
        "docs":     "/docs",
    }