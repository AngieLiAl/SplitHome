// Página para gestionar los miembros del hogar
// Puedes agregar, editar y eliminar miembros
import { useState, useEffect } from "react"
import api from "../api/axios"

function Persona() {

    const [nombre,       setNombre]       = useState("")
    const [email,        setEmail]        = useState("")
    const [busqueda,     setBusqueda]     = useState("")
    const [error,        setError]        = useState("")
    const [personas,     setPersonas]     = useState([])
    const [mostrarModal, setMostrarModal] = useState(false)
    const [editandoId,   setEditandoId]   = useState(null)

    useEffect(() => { cargarPersonas() }, [])

    async function cargarPersonas() {
        const r = await api.get("/personas/")
        setPersonas(r.data)
    }

    function abrirModalNuevo() {
        setNombre(""); setEmail(""); setError("")
        setEditandoId(null); setMostrarModal(true)
    }

    function abrirModalEditar(p) {
        setNombre(p.nombre); setEmail(p.email); setError("")
        setEditandoId(p.id_persona); setMostrarModal(true)
    }

    function cerrarModal() {
        setMostrarModal(false); setEditandoId(null)
        setNombre(""); setEmail(""); setError("")
    }

    async function guardarPersona() {
        if (!nombre.trim()) { setError("El nombre es obligatorio"); return }
        if (!email.includes("@")) { setError("Ingresa un email válido"); return }
        try {
            if (editandoId) {
                await api.put(`/personas/${editandoId}`, { nombre, email })
            } else {
                await api.post("/personas/", { nombre, email })
            }
            await cargarPersonas()
            cerrarModal()
        } catch (ex) {
            setError(ex.response?.data?.detail || "Ocurrió un error")
        }
    }

    async function eliminarPersona(id) {
        if (!window.confirm("¿Eliminar este miembro del hogar?")) return
        try {
            await api.delete(`/personas/${id}`)
            await cargarPersonas()
        } catch (ex) {
            alert(ex.response?.data?.detail || "No se pudo eliminar")
        }
    }

    function iniciales(nombre) {
        return nombre.split(" ").map(p => p[0]).slice(0, 2).join("").toUpperCase()
    }

    const personasFiltradas = personas.filter(p =>
        p.nombre.toLowerCase().includes(busqueda.toLowerCase())
    )

    return (
        <div className="container-fluid py-4">

            {/* Encabezado */}
            <div className="d-flex justify-content-between align-items-end flex-wrap gap-3 mb-4">
                <div>
                    <h2 style={{ fontFamily: "Playfair Display, serif", fontSize: "1.7rem" }}>
                        Miembros del hogar
                    </h2>
                    <p className="text-muted mb-0">
                        Gestiona quién forma parte del hogar.
                    </p>
                </div>
                <button className="btn-primario" onClick={abrirModalNuevo}>
                    + Nuevo miembro
                </button>
            </div>

            {/* Buscador */}
            <div className="mb-4">
                <input
                    type="text"
                    className="form-control"
                    style={{ maxWidth: 360, borderColor: "var(--border)" }}
                    placeholder="🔍 Buscar miembro por nombre..."
                    value={busqueda}
                    onChange={e => setBusqueda(e.target.value)}
                />
            </div>

            {/* Tarjetas de miembros */}
            {personasFiltradas.length === 0 ? (
                <div className="text-center text-muted py-5">
                    <div style={{ fontSize: "2.5rem", opacity: 0.3 }}>👥</div>
                    <p className="mt-2">No hay miembros registrados.</p>
                    <button className="btn-primario" onClick={abrirModalNuevo}>
                        Agregar el primero
                    </button>
                </div>
            ) : (
                <div className="row g-3">
                    {personasFiltradas.map((p) => (
                        <div className="col-12 col-sm-6 col-md-4 col-lg-3" key={p.id_persona}>
                            <div className="member-card text-center p-3">

                                {/* Avatar con iniciales */}
                                <div className="member-avatar mx-auto mb-2">
                                    {iniciales(p.nombre)}
                                </div>

                                <div className="fw-semibold mb-1">{p.nombre}</div>
                                <div className="text-muted mb-1"
                                    style={{ fontSize: "0.8rem" }}>
                                    {p.email}
                                </div>
                                <div className="text-muted mb-2"
                                    style={{ fontSize: "0.75rem" }}>
                                    Desde: {p.fecha_registro}
                                </div>

                                <span className="member-tag">Activo</span>

                                {/* Botones */}
                                <div className="d-flex gap-2 justify-content-center mt-3">
                                    <button
                                        className="btn btn-sm"
                                        style={{
                                            background: "var(--mid)",
                                            border: "none",
                                            borderRadius: "var(--r-sm)",
                                            width: 32, height: 32
                                        }}
                                        title="Editar"
                                        onClick={() => abrirModalEditar(p)}>
                                        ✏️
                                    </button>
                                    <button
                                        className="btn btn-sm"
                                        style={{
                                            background: "var(--danger-bg)",
                                            border: "none",
                                            borderRadius: "var(--r-sm)",
                                            width: 32, height: 32
                                        }}
                                        title="Eliminar"
                                        onClick={() => eliminarPersona(p.id_persona)}>
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
                            <h3>{editandoId ? "Editar miembro" : "Nuevo miembro"}</h3>
                            <button className="btn-cerrar" onClick={cerrarModal}>✕</button>
                        </div>

                        {error && (
                            <div className="alert alert-danger py-2 px-3 mb-3"
                                style={{ fontSize: "0.84rem" }}>
                                {error}
                            </div>
                        )}

                        <div className="campo">
                            <label>Nombre completo</label>
                            <input
                                type="text"
                                className="form-control"
                                placeholder="Ej: Ana García"
                                value={nombre}
                                onChange={e => setNombre(e.target.value)}
                            />
                        </div>

                        <div className="campo">
                            <label>Correo electrónico</label>
                            <input
                                type="email"
                                className="form-control"
                                placeholder="Ej: ana@mail.com"
                                value={email}
                                onChange={e => setEmail(e.target.value)}
                            />
                        </div>

                        <div className="d-flex justify-content-end gap-2 mt-3">
                            <button className="btn btn-outline-secondary"
                                onClick={cerrarModal}>
                                Cancelar
                            </button>
                            <button className="btn-primario" onClick={guardarPersona}>
                                {editandoId ? "Guardar cambios" : "Agregar miembro"}
                            </button>
                        </div>

                    </div>
                </div>
            )}

        </div>
    )
}

export default Persona