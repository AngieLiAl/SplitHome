// Página para gestionar los gastos del hogar
// Puedes agregar, editar y eliminar gastos
// También puedes filtrar por categoría o persona
import { useState, useEffect } from "react"
import api from "../api/axios"

function Gasto() {

    const [descripcion,   setDescripcion]   = useState("")
    const [monto,         setMonto]         = useState("")
    const [fecha,         setFecha]         = useState("")
    const [idCategoria,   setIdCategoria]   = useState("")
    const [idPersona,     setIdPersona]     = useState("")
    const [esCompartido,  setEsCompartido]  = useState(false)
    const [busqueda,      setBusqueda]      = useState("")
    const [error,         setError]         = useState("")
    const [editandoId,    setEditandoId]    = useState(null)

    const categorias = [
        { id: 1, nombre: "Alquiler",  icono: "🏠" },
        { id: 2, nombre: "Luz",       icono: "💡" },
        { id: 3, nombre: "Agua",      icono: "💧" },
        { id: 4, nombre: "Internet",  icono: "📶" },
        { id: 5, nombre: "Comida",    icono: "🍛" },
        { id: 6, nombre: "Limpieza",  icono: "🧹" },
        { id: 7, nombre: "Otros",     icono: "📦" },
    ]

    const personas = [
        { id: 1, nombre: "Angie Lizarsaburu"  },
        { id: 2, nombre: "Angela Escobedo"    },
    ]

    const [gastos, setGastos] = useState([
        { id: 1, descripcion: "Alquiler Enero",  monto: 1200.00, fecha: "2025-01-01", idCategoria: 1, idPersona: 1, esCompartido: true  },
        { id: 2, descripcion: "Recibo de Luz",   monto: 85.00,   fecha: "2025-01-10", idCategoria: 2, idPersona: 2, esCompartido: true  },
        { id: 3, descripcion: "Recibo de Agua",  monto: 60.00,   fecha: "2025-01-12", idCategoria: 3, idPersona: 2, esCompartido: true  },
        { id: 4, descripcion: "Internet",        monto: 99.00,   fecha: "2025-01-15", idCategoria: 4, idPersona: 1, esCompartido: true  },
        { id: 5, descripcion: "Mercado semanal", monto: 180.00,  fecha: "2025-01-05", idCategoria: 5, idPersona: 2, esCompartido: false },
    ])

// ── Helpers ──────────────────────────────────────────────
function getNombreCategoria(id) {
    const c = categorias.find(c => c.id === id)
    return c ? c.icono + " " + c.nombre : "—"
}

function getNombrePersona(id) {
    const p = personas.find(p => p.id === id)
    return p ? p.nombre : "—"
}

function limpiarFormulario() {
    setDescripcion("")
    setMonto("")
    setFecha("")
    setIdCategoria("")
    setIdPersona("")
    setEsCompartido(false)
    setError("")
    setEditandoId(null)
}

    // ── Validar y guardar ────────────────────────────────────
function guardarGasto() {
    if (!descripcion.trim()) {
        setError("La descripción es obligatoria")
        return
    }
    if (!monto || Number(monto) <= 0) {
        setError("El monto debe ser mayor a 0")
        return
    }
    if (!fecha) {
        setError("La fecha es obligatoria")
        return
    }
    if (!idCategoria) {
        setError("Selecciona una categoría")
        return
    }
    if (!idPersona) {
        setError("Selecciona quién pagó")
        return
    }

    if (editandoId !== null) {
        // Actualizar gasto existente
        setGastos(gastos.map(g =>
            g.id === editandoId
                ? { ...g, descripcion, monto: Number(monto), fecha,
                    idCategoria: Number(idCategoria),
                    idPersona: Number(idPersona), esCompartido }
                : g
        ))
    } else {
         // Crear nuevo gasto
        const nuevo = {
            id:           gastos.length + 1,
            descripcion:  descripcion.trim(),
            monto:        Number(monto),
            fecha,
            idCategoria:  Number(idCategoria),
            idPersona:    Number(idPersona),
            esCompartido
        }
        setGastos([...gastos, nuevo])
    }
    limpiarFormulario()
}

// ── Editar gasto ─────────────────────────────────────────
function editarGasto(g) {
    setEditandoId(g.id)
    setDescripcion(g.descripcion)
    setMonto(String(g.monto))
    setFecha(g.fecha)
    setIdCategoria(String(g.idCategoria))
    setIdPersona(String(g.idPersona))
    setEsCompartido(g.esCompartido)
    setError("")
}

// ── Eliminar gasto ───────────────────────────────────────
function eliminarGasto(id) {
    setGastos(gastos.filter(g => g.id !== id))
}

// ── Filtrar ──────────────────────────────────────────────
    const gastosFiltrados = gastos.filter(g =>
        g.descripcion.toLowerCase().includes(busqueda.toLowerCase())
    )

    const totalMonto = gastos.reduce((acc, g) => acc + g.monto, 0)

    return (
        <div>

            {/* Encabezado */}
            <div className="d-flex justify-content-between align-items-end flex-wrap gap-3 mb-4">
                <div>
                    <h2 className="fw-bold mb-1"
                        style={{ fontFamily: "Playfair Display, serif" }}>
                        Gastos del hogar
                    </h2>
                    <p className="text-muted mb-0">
                        Registra, edita o elimina los gastos compartidos.
                    </p>
                </div>
                <span className="badge rounded-pill"
                    style={{ background: "var(--accent)", fontSize: "0.9rem", padding: "0.5rem 1rem" }}>
                    <FaWallet className="me-1" />
                    Total: S/. {totalMonto.toFixed(2)}
                </span>
            </div>

            <div className="row">
                {/* Formulario */}
                <div className="col-md-4 mb-4">
                    <div className="form-card">
                        <h6 className="form-titulo">
                            {editandoId ? "✏️ Editar Gasto" : "🧾 Nuevo Gasto"}
                        </h6>

                        {error && (
                            <div className="alert alert-danger py-2 px-3 mb-3"
                                style={{ fontSize: "0.84rem", borderRadius: "var(--r-sm)" }}>
                                {error}
                            </div>
                        )}

                        <label className="form-label fw-semibold"
                            style={{ fontSize: "0.82rem" }}>
                            Descripción
                        </label>
                        <input
                            type="text"
                            className="form-control mb-3"
                            placeholder="Ej: Recibo de luz"
                            value={descripcion}
                            onChange={e => setDescripcion(e.target.value)}
                        />

                        <label className="form-label fw-semibold"
                            style={{ fontSize: "0.82rem" }}>
                            Monto (S/.)
                        </label>
                        <input
                            type="number"
                            className="form-control mb-3"
                            placeholder="0.00"
                            min="0"
                            step="0.01"
                            value={monto}
                            onChange={e => setMonto(e.target.value)}
                        />

                        <label className="form-label fw-semibold"
                            style={{ fontSize: "0.82rem" }}>
                            Fecha
                        </label>
                        <input
                            type="date"
                            className="form-control mb-3"
                            value={fecha}
                            onChange={e => setFecha(e.target.value)}
                        />

                        <label className="form-label fw-semibold"
                            style={{ fontSize: "0.82rem" }}>
                            Categoría
                        </label>
                        <select
                            className="form-select mb-3"
                            value={idCategoria}
                            onChange={e => setIdCategoria(e.target.value)}>
                            <option value="">Selecciona una categoría</option>
                            {categorias.map(c => (
                                <option key={c.id} value={c.id}>
                                    {c.icono} {c.nombre}
                                </option>
                            ))}
                        </select>

                        <label className="form-label fw-semibold"
                            style={{ fontSize: "0.82rem" }}>
                            ¿Quién pagó?
                        </label>
                        <select
                            className="form-select mb-3"
                            value={idPersona}
                            onChange={e => setIdPersona(e.target.value)}>
                            <option value="">Selecciona un miembro</option>
                            {personas.map(p => (
                                <option key={p.id} value={p.id}>
                                    {p.nombre}
                                </option>
                            ))}
                        </select>

                        <div className="form-check mb-3">
                            <input
                                type="checkbox"
                                className="form-check-input"
                                id="esCompartido"
                                checked={esCompartido}
                                onChange={e => setEsCompartido(e.target.checked)}
                            />
                            <label className="form-check-label"
                                style={{ fontSize: "0.84rem" }}
                                htmlFor="esCompartido">
                                Dividir entre los miembros del hogar
                            </label>
                        </div>

                        <div className="d-flex gap-2">
                            {editandoId && (
                                <button
                                    className="btn btn-outline-secondary w-50 fw-semibold"
                                    style={{ borderRadius: "var(--r-sm)" }}
                                    onClick={limpiarFormulario}>
                                    Cancelar
                                </button>
                            )}
                            <button
                                className="btn text-white fw-semibold"
                                style={{
                                    background: "var(--accent)",
                                    borderRadius: "var(--r-sm)",
                                    width: editandoId ? "50%" : "100%"
                                }}
                                onClick={guardarGasto}>
                                {editandoId ? "Guardar cambios" : "+ Agregar gasto"}
                            </button>
                        </div>
                    </div>
                </div>

                {/* Tabla de gastos */}
                <div className="col-md-8 mb-4">

                    {/* Buscador */}
                    <input
                        type="text"
                        className="form-control mb-3"
                        placeholder="🔍 Buscar gasto..."
                        value={busqueda}
                        onChange={e => setBusqueda(e.target.value)}
                    />

                    {gastosFiltrados.length === 0 ? (
                        <div className="text-center text-muted py-5">
                            <FaWallet size={40} style={{ opacity: 0.2 }} />
                            <p className="mt-2">No hay gastos registrados.</p>
                        </div>
                    ) : (
                        <div className="panel-card p-0" style={{ overflow: "hidden" }}>
                            <table className="table tabla-sh table-hover mb-0">
                                <thead>
                                    <tr>
                                        <th className="ps-3">Descripción</th>
                                        <th>Categoría</th>
                                        <th>Pagó</th>
                                        <th>Fecha</th>
                                        <th>Monto</th>
                                        <th>Compartido</th>
                                        <th></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {gastosFiltrados.map((g) => (
                                        <tr key={g.id}>
                                            <td className="ps-3">{g.descripcion}</td>
                                            <td>{getNombreCategoria(g.idCategoria)}</td>
                                            <td>{getNombrePersona(g.idPersona)}</td>
                                            <td>{g.fecha}</td>
                                            <td>
                                                <span className="badge-monto">
                                                    S/. {g.monto.toFixed(2)}
                                                </span>
                                            </td>
                                            <td>
                                                <span className="badge rounded-pill"
                                                    style={{
                                                        background: g.esCompartido ? "var(--ok-bg)" : "var(--mid)",
                                                        color: g.esCompartido ? "var(--accent2)" : "var(--muted)",
                                                        fontSize: "0.76rem"
                                                    }}>
                                                    {g.esCompartido ? "Sí" : "No"}
                                                </span>
                                            </td>
                                            <td>
                                                <div className="d-flex gap-1 justify-content-end pe-2">
                                                    <button
                                                        className="btn btn-sm"
                                                        style={{
                                                            background: "var(--mid)",
                                                            borderRadius: "var(--r-sm)",
                                                            width: "30px", height: "30px",
                                                            padding: 0
                                                        }}
                                                        onClick={() => editarGasto(g)}>
                                                        ✏️
                                                    </button>
                                                    <button
                                                        className="btn btn-sm"
                                                        style={{
                                                            background: "var(--danger-bg)",
                                                            borderRadius: "var(--r-sm)",
                                                            width: "30px", height: "30px",
                                                            padding: 0
                                                        }}
                                                        onClick={() => eliminarGasto(g.id)}>
                                                        🗑️
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default Gasto