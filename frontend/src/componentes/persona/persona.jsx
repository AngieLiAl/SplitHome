import { useState } from "react"
import { FaUsers } from "react-icons/fa"

function Persona() {

    const [nombre,   setNombre]   = useState("")
    const [email,    setEmail]    = useState("")
    const [busqueda, setBusqueda] = useState("")

    const [personas, setPersonas] = useState([
        { id: 1, nombre: "Angie Lizarsaburu",  email: "angie@splithome.pe",  fecha: "2025-01-01" },
        { id: 2, nombre: "Angela Escobedo",     email: "angela@splithome.pe", fecha: "2025-01-01" },
    ])

    const [error, setError] = useState("")

    // ── Agregar persona ──────────────────────────────────────
    function agregarPersona() {
        if (!nombre.trim()) {
            setError("El nombre es obligatorio")
            return
        }
        if (!email.includes("@")) {
            setError("Ingresa un email válido")
            return
        }
        if (personas.some(p => p.email === email)) {
            setError("Ese email ya está registrado")
            return
        }

        const nueva = {
            id:     personas.length + 1,
            nombre: nombre.trim(),
            email:  email.trim(),
            fecha:  new Date().toISOString().slice(0, 10)
        }
        setPersonas([...personas, nueva])
        setNombre("")
        setEmail("")
        setError("")
    }

    // ── Eliminar persona ─────────────────────────────────────
    function eliminarPersona(id) {
        setPersonas(personas.filter(p => p.id !== id))
    }

    // ── Iniciales para el avatar ─────────────────────────────
    function iniciales(nombre) {
        return nombre.split(" ").map(p => p[0]).slice(0, 2).join("").toUpperCase()
    }

    // ── Filtrar por búsqueda ─────────────────────────────────
    const personasFiltradas = personas.filter(p =>
        p.nombre.toLowerCase().includes(busqueda.toLowerCase())
    )

    return (
        <div>

            {/* Encabezado */}
            <div className="d-flex justify-content-between align-items-end flex-wrap gap-3 mb-4">
                <div>
                    <h2 className="fw-bold mb-1"
                        style={{ fontFamily: "Playfair Display, serif" }}>
                        Miembros del hogar
                    </h2>
                    <p className="text-muted mb-0">
                        Gestiona quién forma parte del hogar.
                    </p>
                </div>
                <span className="badge rounded-pill"
                    style={{ background: "var(--accent)", fontSize: "0.9rem", padding: "0.5rem 1rem" }}>
                    <FaUsers className="me-1" />
                    {personas.length} miembros
                </span>
            </div>

            <div className="row">

                {/* Formulario */}
                <div className="col-md-4 mb-4">
                    <div className="form-card">
                        <h6 className="form-titulo">👤 Nuevo Miembro</h6>

                        {error && (
                            <div className="alert alert-danger py-2 px-3 mb-3"
                                style={{ fontSize: "0.84rem", borderRadius: "var(--r-sm)" }}>
                                {error}
                            </div>
                        )}

                        <label className="form-label fw-semibold" style={{ fontSize: "0.82rem" }}>
                            Nombre completo
                        </label>
                        <input
                            type="text"
                            className="form-control mb-3"
                            placeholder="Ej: Ana García"
                            value={nombre}
                            onChange={e => setNombre(e.target.value)}
                        />

                        <label className="form-label fw-semibold" style={{ fontSize: "0.82rem" }}>
                            Correo electrónico
                        </label>
                        <input
                            type="email"
                            className="form-control mb-3"
                            placeholder="Ej: ana@mail.com"
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                        />

                        <button
                            className="btn w-100 text-white fw-semibold"
                            style={{ background: "var(--accent)", borderRadius: "var(--r-sm)" }}
                            onClick={agregarPersona}>
                            + Agregar miembro
                        </button>
                    </div>
                </div>

                {/* Lista de miembros */}
                <div className="col-md-8 mb-4">

                    {/* Buscador */}
                    <input
                        type="text"
                        className="form-control mb-3"
                        placeholder="🔍 Buscar miembro por nombre..."
                        value={busqueda}
                        onChange={e => setBusqueda(e.target.value)}
                    />

                    {personasFiltradas.length === 0 ? (
                        <div className="text-center text-muted py-5">
                            <FaUsers size={40} style={{ opacity: 0.2 }} />
                            <p className="mt-2">No hay miembros registrados.</p>
                        </div>
                    ) : (
                        <div className="row g-3">
                            {personasFiltradas.map((p, i) => (
                                <div className="col-md-6" key={p.id}>
                                    <div className="member-card">

                                        {/* Botón eliminar */}
                                        <button
                                            className="btn btn-sm position-absolute"
                                            style={{
                                                top: "0.6rem", right: "0.6rem",
                                                background: "var(--mid)",
                                                borderRadius: "50%",
                                                width: "26px", height: "26px",
                                                fontSize: "0.7rem",
                                                color: "var(--muted)",
                                                padding: 0
                                            }}
                                            onClick={() => eliminarPersona(p.id)}>
                                            ✕
                                        </button>

                                        {/* Avatar */}
                                        <div className="member-avatar">
                                            {iniciales(p.nombre)}
                                        </div>

                                        <div className="fw-semibold mb-1">{p.nombre}</div>
                                        <div className="text-muted mb-2"
                                            style={{ fontSize: "0.8rem" }}>
                                            {p.email}
                                        </div>

                                        <span style={{
                                            fontSize: "0.72rem",
                                            background: "var(--ok-bg)",
                                            color: "var(--accent2)",
                                            padding: "0.2rem 0.6rem",
                                            borderRadius: "99px",
                                            fontWeight: 600
                                        }}>
                                            Activo
                                        </span>

                                        <div className="text-muted mt-2"
                                            style={{ fontSize: "0.74rem" }}>
                                            Desde {p.fecha}
                                        </div>

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

export default Persona