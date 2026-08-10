# SplitHome
Este repositorio contiene la app web SplitHome para el trabajo final de POO (Lizarsaburu/Escobedo)
# 🏠 SplitHome — Gestor de Gastos Compartidos del Hogar

Aplicación Full Stack para registrar, dividir y balancear los gastos entre los miembros de un hogar.  
Desarrollado como proyecto final del curso de **Programación Orientada a Objetos con Python**.
 y **Programación en Legnguajes Relevantes**
**Integrantes:** Angie Diorela Lizarsaburu Alfaro · Angela Yadira Escobedo Quispe  
**Docente:** Ing. Giovanni Ramírez Berrocal  
**Institución:** IESTP "Argentina" — 2026-I

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología |
|---|---|
| Backend | Python 3.12 · FastAPI · psycopg2 |
| Base de datos | PostgreSQL 16 |
| Frontend | React 18 · Bootstrap 5 · Axios |
| Control de versiones | Git · GitHub |

---

## 📁 Estructura del Proyecto

```
SplitHome/
├── backend/
│   ├── config/
│   │   ├── base_datos.py          # Conexión a PostgreSQL
│   │   ├── logger.py              # Registro de eventos (Singleton)
│   │   └── sistema_config.py      # Configuración general (Singleton)
│   ├── dao/
│   │   ├── persona_dao.py         # CRUD de personas
│   │   ├── categoria_dao.py       # CRUD de categorías
│   │   ├── gasto_dao.py           # CRUD de gastos
│   │   └── participacion_dao.py   # CRUD de participaciones
│   ├── modelos/
│   │   ├── persona.py             # Modelo Persona
│   │   ├── categoria.py           # Modelo Categoria
│   │   ├── gasto.py               # Modelo Gasto (clase base)
│   │   └── gasto_compartido.py    # Modelo GastoCompartido (hereda de Gasto)
│   ├── routes/
│   │   ├── personas.py            # Endpoints /personas
│   │   ├── categorias.py          # Endpoints /categorias
│   │   └── gastos.py              # Endpoints /gastos
│   ├── schemas/
│   │   ├── persona_schemas.py     # Validación de datos de personas
│   │   ├── categoria_schemas.py   # Validación de datos de categorías
│   │   └── gasto_schemas.py       # Validación de datos de gastos
│   ├── .env                       # Variables de entorno (NO está en Git)
│   ├── main.py                    # Punto de entrada del servidor
│   └── requirements.txt           # Dependencias Python
│
├── frontend/
│   └── src/
│       ├── componentes/
│       │   ├── api/axios.jsx      # Configuración de Axios
│       │   ├── panel/             # Página de inicio con KPIs
│       │   ├── persona/           # Gestión de miembros
│       │   ├── categoria/         # Gestión de categorías
│       │   ├── gasto/             # Gestión de gastos
│       │   └── balance/           # Balance entre miembros
│       ├── App.jsx                # Rutas y layout principal
│       └── main.jsx               # Punto de entrada de React
│
├── database/
│   └── splithome.sql              # Script SQL completo (DDL + DML)
│
└── README.md
```

---

## ⚙️ Variables de Entorno

Crea un archivo `.env` dentro de la carpeta `backend/` con este contenido:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=splithome_db
DB_USER=postgres
DB_PASSWORD=tu_contraseña_aqui
```

> ⚠️ El archivo `.env` no está en el repositorio por seguridad. Se debe crear manualmente en cada PC.

---

## 🚀 Instalación y ejecución

### Requisitos previos

- Python 3.10 o superior
- Node.js 18 o superior
- PostgreSQL 16
- Git

### 1. Clonar el repositorio

```bash
git clone https://github.com/AngieLiAl/SplitHome.git
cd SplitHome
```

### 2. Crear la base de datos

Abre **pgAdmin 4**, crea una base de datos llamada `splithome_db` y ejecuta el script:

```
database/splithome.sql
```

### 3. Configurar el backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
# Si python no funciona usa: py -m venv venv

# Activar el entorno virtual
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Crear el archivo .env

Crea el archivo `backend/.env` con tus credenciales de PostgreSQL (ver sección Variables de Entorno arriba).

### 5. Levantar el backend

```bash
uvicorn main:app --reload
```

El servidor estará disponible en: `http://localhost:8000`  
Documentación Swagger: `http://localhost:8000/docs`

### 6. Configurar e instalar el frontend

Abre una nueva terminal:

```bash
cd frontend
npm install
```

### 7. Levantar el frontend

```bash
npm run dev
```

El sistema estará disponible en: `http://localhost:5173`

---

## 📡 Endpoints del API

| Método | Endpoint | Descripción |
|---|---|---|
| GET | /personas/ | Listar todos los miembros |
| POST | /personas/ | Crear nuevo miembro |
| PUT | /personas/{id} | Actualizar miembro |
| DELETE | /personas/{id} | Eliminar miembro |
| GET | /categorias/ | Listar todas las categorías |
| POST | /categorias/ | Crear nueva categoría |
| PUT | /categorias/{id} | Actualizar categoría |
| DELETE | /categorias/{id} | Eliminar categoría |
| GET | /gastos/ | Listar todos los gastos |
| POST | /gastos/ | Crear nuevo gasto |
| POST | /gastos/compartido | Crear gasto compartido con participaciones |
| PUT | /gastos/{id} | Actualizar gasto |
| DELETE | /gastos/{id} | Eliminar gasto |
| GET | /gastos/{id}/participaciones | Ver participaciones de un gasto |
| GET | /gastos/balance/{id} | Ver balance de una persona |

---

## 🧱 Pilares POO aplicados

| Pilar | Dónde se aplica |
|---|---|
| **Encapsulamiento** | Atributos privados en modelos con validación |
| **Herencia** | `GastoCompartido` hereda de `Gasto` |
| **Polimorfismo** | `calcular_deuda()` se comporta diferente en cada clase |
| **Abstracción** | `Gasto` define la interfaz común para todos los gastos |

---

## 📝 Gracias ❤️

Proyecto académico — IESTP "Argentina" 2026-I