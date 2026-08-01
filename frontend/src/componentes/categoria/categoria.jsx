import { useState } from "react"
import { FaTags } from "react-icons/fa"

function Categoria() {
    const [nombre,      setNombre]      = useState("")
    const [icono,       setIcono]       = useState("")
    const [descripcion, setDescripcion] = useState("")
    const [busqueda,    setBusqueda]    = useState("")
    const [error,       setError]       = useState("")
    const [categorias, setCategorias] = useState([
        { id: 1, nombre: "Alquiler",  icono: "🏠", descripcion: "Pago mensual del alquiler" },
        { id: 2, nombre: "Luz",       icono: "💡", descripcion: "Recibo de electricidad"    },
        { id: 3, nombre: "Agua",      icono: "💧", descripcion: "Recibo de agua"            },
        { id: 4, nombre: "Internet",  icono: "📶", descripcion: "Servicio de internet"      },
        { id: 5, nombre: "Comida",    icono: "🍛", descripcion: "Mercado y alimentación"    },
        { id: 6, nombre: "Limpieza",  icono: "🧹", descripcion: "Productos de limpieza"     },
        { id: 7, nombre: "Otros",     icono: "📦", descripcion: "Gastos varios"             },
    ])
    // ── Agregar categoría ────────────────────────────────────
    function agregarCategoria() {
        if (!nombre.trim()) {
            setError("El nombre es obligatorio")
            return
        }
        if (categorias.some(c => c.nombre.toLowerCase() === nombre.toLowerCase())) {
            setError("Esa categoría ya existe")
            return
        }
        const nueva = {
            id:          categorias.length + 1,
            nombre:      nombre.trim(),
            icono:       icono.trim() || "📦",
            descripcion: descripcion.trim()
        }
        setCategorias([...categorias, nueva])
        setNombre("")
        setIcono("")
        setDescripcion("")
        setError("")
    }

    // ── Eliminar categoría ───────────────────────────────────
    function eliminarCategoria(id) {
        setCategorias(categorias.filter(c => c.id !== id))
    }

    // ── Filtrar por búsqueda ─────────────────────────────────
    const categoriasFiltradas = categorias.filter(c =>
        c.nombre.toLowerCase().includes(busqueda.toLowerCase())
    )

    return (
        <div>
            {/* Encabezado */}
            <div className="d-flex justify-content-between align-items-end flex-wrap gap-3 mb-4">
                <div>
                    <h2 className="fw-bold mb-1"
                        style={{ fontFamily: "Playfair Display, serif" }}>
                        Categorías de gasto
                    </h2>
                    <p className="text-muted mb-0">
                        Organiza los tipos de gasto de tu hogar.
                    </p>
                </div>
                <span className="badge rounded-pill"
                    style={{ background: "var(--accent)", fontSize: "0.9rem", padding: "0.5rem 1rem" }}>
                    <FaTags className="me-1" />
                    {categorias.length} categorías
                </span>
            </div>

            <div className="row">

                {/* Formulario */}
                <div className="col-md-4 mb-4">
                    <div className="form-card">
                        <h6 className="form-titulo">🏷️ Nueva Categoría</h6>

                        {error && (
                            <div className="alert alert-danger py-2 px-3 mb-3"
                                style={{ fontSize: "0.84rem", borderRadius: "var(--r-sm)" }}>
                                {error}
                            </div>
                        )}

                        <label className="form-label fw-semibold"
                            style={{ fontSize: "0.82rem" }}>
                            Nombre
                        </label>
                        <input
                            type="text"
                            className="form-control mb-3"
                            placeholder="Ej: Mascotas"
                            value={nombre}
                            onChange={e => setNombre(e.target.value)}
                        />

                        <label className="form-label fw-semibold"
                            style={{ fontSize: "0.82rem" }}>
                            Ícono (emoji)
                        </label>
                        <input
                            type="text"
                            className="form-control mb-3"
                            placeholder="🐾"
                            maxLength={2}
                            value={icono}
                            onChange={e => setIcono(e.target.value)}
                        />

                        <label className="form-label fw-semibold"
                            style={{ fontSize: "0.82rem" }}>
                            Descripción
                        </label>
                        <input
                            type="text"
                            className="form-control mb-3"
                            placeholder="Descripción opcional"
                            value={descripcion}
                            onChange={e => setDescripcion(e.target.value)}
                        />

                        <button
                            className="btn w-100 text-white fw-semibold"
                            style={{ background: "var(--accent)", borderRadius: "var(--r-sm)" }}
                            onClick={agregarCategoria}>
                            + Agregar categoría
                        </button>
                    </div>
                </div>
                {/* Grid de categorías */}
                <div className="col-md-8 mb-4">
                    {/* Buscador */}
                    <input
                        type="text"
                        className="form-control mb-3"
                        placeholder="🔍 Buscar categoría..."
                        value={busqueda}
                        onChange={e => setBusqueda(e.target.value)}
                    />

                    {categoriasFiltradas.length === 0 ? (
                        <div className="text-center text-muted py-5">
                            <FaTags size={40} style={{ opacity: 0.2 }} />
                            <p className="mt-2">No hay categorías registradas.</p>
                        </div>
                    ) : (
                        <div className="row g-3">
                            {categoriasFiltradas.map((c, i) => (
                                <div className="col-6 col-md-4" key={c.id}>
                                    <div className="cat-card position-relative">

                                        {/* Botón eliminar */}
                                        <button
                                            className="btn btn-sm position-absolute"
                                            style={{
                                                top: "0.5rem", right: "0.5rem",
                                                background: "var(--mid)",
                                                borderRadius: "50%",
                                                width: "24px", height: "24px",
                                                fontSize: "0.7rem",
                                                color: "var(--muted)",
                                                padding: 0
                                            }}
                                            onClick={() => eliminarCategoria(c.id)}>
                                            ✕
                                        </button>

                                        <div className="cat-ico">{c.icono}</div>
                                        <div className="fw-semibold" style={{ fontSize: "0.9rem" }}>
                                            {c.nombre}
                                        </div>

                                        {c.descripcion && (
                                            <div className="text-muted mt-1"
                                                style={{ fontSize: "0.76rem" }}>
                                                {c.descripcion}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

            </div>
        </div>
    )
}

export default Categoria