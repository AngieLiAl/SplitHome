// Página para gestionar las categorías de gasto del hogar
// Puedes agregar, editar y eliminar categorías
import { useState, useEffect } from "react"
import api from "../api/axios"

function Categoria() {

    const [nombre,       setNombre]       = useState("")
    const [icono,        setIcono]        = useState("")
    const [descripcion,  setDescripcion]  = useState("")
    const [busqueda,     setBusqueda]     = useState("")
    const [error,        setError]        = useState("")
    const [categorias,   setCategorias]   = useState([])
    const [mostrarModal, setMostrarModal] = useState(false)
    const [editandoId,   setEditandoId]   = useState(null)

    useEffect(() => { cargarCategorias() }, [])

    async function cargarCategorias() {
        const r = await api.get("/categorias/")
        setCategorias(r.data)
    }

    function abrirModalNuevo() {
        setNombre(""); setIcono(""); setDescripcion("")
        setError(""); setEditandoId(null); setMostrarModal(true)
    }

    function abrirModalEditar(c) {
        setNombre(c.nombre)
        setIcono(c.icono || "")
        setDescripcion(c.descripcion || "")
        setError(""); setEditandoId(c.id_categoria); setMostrarModal(true)
    }

    function cerrarModal() {
        setMostrarModal(false); setEditandoId(null)
        setNombre(""); setIcono(""); setDescripcion(""); setError("")
    }

    async function guardarCategoria() {
        if (!nombre.trim()) { setError("El nombre es obligatorio"); return }
        try {
            if (editandoId) {
                await api.put(`/categorias/${editandoId}`, {
                    nombre,
                    icono:       icono       || "📦",
                    descripcion: descripcion || ""
                })
            } else {
                await api.post("/categorias/", {
                    nombre,
                    icono:       icono       || "📦",
                    descripcion: descripcion || ""
                })
            }
            await cargarCategorias()
            cerrarModal()
        } catch (ex) {
            setError(ex.response?.data?.detail || "Ocurrió un error")
        }
    }

    async function eliminarCategoria(id) {
        if (!window.confirm("¿Eliminar esta categoría?")) return
        try {
            await api.delete(`/categorias/${id}`)
            await cargarCategorias()
        } catch (ex) {
            alert(ex.response?.data?.detail || "No se pudo eliminar, puede tener gastos asociados")
        }
    }

    const categoriasFiltradas = categorias.filter(c =>
        c.nombre.toLowerCase().includes(busqueda.toLowerCase())
    )

    return (
        <div className="container-fluid py-4">

            {/* Encabezado */}
            <div className="d-flex justify-content-between align-items-end flex-wrap gap-3 mb-4">
                <div>
                    <h2 style={{ fontFamily: "Playfair Display, serif", fontSize: "1.7rem" }}>
                        Categorías de gasto
                    </h2>
                    <p className="text-muted mb-0">
                        Organiza los tipos de gasto de tu hogar.
                    </p>
                </div>
                <button className="btn-primario" onClick={abrirModalNuevo}>
                    + Nueva categoría
                </button>
            </div>

            {/* Buscador */}
            <div className="mb-4">
                <input
                    type="text"
                    className="form-control"
                    style={{ maxWidth: 360, borderColor: "var(--border)" }}
                    placeholder="🔍 Buscar categoría..."
                    value={busqueda}
                    onChange={e => setBusqueda(e.target.value)}
                />
            </div>

            {/* Grid de categorías */}
            {categoriasFiltradas.length === 0 ? (
                <div className="text-center text-muted py-5">
                    <div style={{ fontSize: "2.5rem", opacity: 0.3 }}>🏷️</div>
                    <p className="mt-2">No hay categorías registradas.</p>
                    <button className="btn-primario" onClick={abrirModalNuevo}>
                        Crear la primera
                    </button>
                </div>
            ) : (
                <div className="row g-3">
                    {categoriasFiltradas.map((c) => (
                        <div className="col-6 col-sm-4 col-md-3 col-lg-2"
                            key={c.id_categoria}>
                            <div className="cat-card h-100">

                                {/* Ícono */}
                                <div className="cat-ico">{c.icono || "📦"}</div>

                                <div className="fw-semibold mb-1"
                                    style={{ fontSize: "0.9rem" }}>
                                    {c.nombre}
                                </div>

                                {c.descripcion && (
                                    <div className="text-muted"
                                        style={{ fontSize: "0.76rem" }}>
                                        {c.descripcion}
                                    </div>
                                )}

                                {/* Botones */}
                                <div className="d-flex gap-2 justify-content-center mt-3">
                                    <button
                                        className="btn btn-sm"
                                        style={{
                                            background: "var(--mid)",
                                            border: "none",
                                            borderRadius: "var(--r-sm)",
                                            width: 30, height: 30
                                        }}
                                        title="Editar"
                                        onClick={() => abrirModalEditar(c)}>
                                        ✏️
                                    </button>
                                    <button
                                        className="btn btn-sm"
                                        style={{
                                            background: "var(--danger-bg)",
                                            border: "none",
                                            borderRadius: "var(--r-sm)",
                                            width: 30, height: 30
                                        }}
                                        title="Eliminar"
                                        onClick={() => eliminarCategoria(c.id_categoria)}>
                                        🗑️
                                    </button>
                                </div>

                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Modal centrado */}
            {mostrarModal && (
                <div className="modal-overlay" onClick={cerrarModal}>
                    <div className="modal-card" onClick={e => e.stopPropagation()}>

                        <div className="modal-head">
                            <h3>{editandoId ? "Editar categoría" : "Nueva categoría"}</h3>
                            <button className="btn-cerrar" onClick={cerrarModal}>✕</button>
                        </div>

                        {error && (
                            <div className="alert alert-danger py-2 px-3 mb-3"
                                style={{ fontSize: "0.84rem" }}>
                                {error}
                            </div>
                        )}

                        <div className="campo">
                            <label>Nombre</label>
                            <input
                                type="text"
                                className="form-control"
                                placeholder="Ej: Mascotas"
                                value={nombre}
                                onChange={e => setNombre(e.target.value)}
                            />
                        </div>

                        {/* Ícono y descripción en dos columnas */}
                        <div className="row g-2">
                            <div className="col-4">
                                <div className="campo">
                                    <label>Ícono</label>
                                    <input
                                        type="text"
                                        className="form-control text-center"
                                        placeholder="🐾"
                                        maxLength={2}
                                        value={icono}
                                        onChange={e => setIcono(e.target.value)}
                                    />
                                </div>
                            </div>
                            <div className="col-8">
                                <div className="campo">
                                    <label>Descripción (opcional)</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        placeholder="Descripción breve"
                                        value={descripcion}
                                        onChange={e => setDescripcion(e.target.value)}
                                    />
                                </div>
                            </div>
                        </div>

                        <div className="d-flex justify-content-end gap-2 mt-3">
                            <button className="btn btn-outline-secondary"
                                onClick={cerrarModal}>
                                Cancelar
                            </button>
                            <button className="btn-primario" onClick={guardarCategoria}>
                                {editandoId ? "Guardar cambios" : "Crear categoría"}
                            </button>
                        </div>

                    </div>
                </div>
            )}

        </div>
    )
}

export default Categoria