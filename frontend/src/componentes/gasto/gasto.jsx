// Página para gestionar los gastos del hogar
// Puedes agregar, editar y eliminar gastos
// También puedes filtrar por categoría o persona
import { useState, useEffect } from "react"
import api from "../api/axios"

function Gasto() {
    // Datos del formulario
    const [descripcion,   setDescripcion]   = useState("")
    const [monto,         setMonto]         = useState("")
    const [fecha,         setFecha]         = useState("")
    const [idCategoria,   setIdCategoria]   = useState("")
    const [idPersona,     setIdPersona]     = useState("")
    const [esCompartido,  setEsCompartido]  = useState(false)
    const [error, setError] = useState("")
    
    // Listas que vienen del backend
    const [gastos,     setGastos]     = useState([])
    const [categorias, setCategorias] = useState([])
    const [personas,   setPersonas]   = useState([])

    // Control del modal
    const [mostrarModal, setMostrarModal] = useState(false)
    const [editandoId,   setEditandoId]   = useState(null)

    // Filtros de la tabla
    const [busqueda,       setBusqueda]       = useState("")
    const [filtroCat,      setFiltroCat]      = useState("")
    const [filtroPersona, setFiltroPersona] = useState("")
    
    // Al entrar a la página traemos todos los datos del backend
    useEffect(() => {
        cargarTodo()
    }, [])

    async function cargarTodo() {
        const [rGastos, rCat, rPer] = await Promise.all([
            api.get("/gastos/"),
            api.get("/categorias/"),
            api.get("/personas/"),
        ])
        setGastos(rGastos.data)
        setCategorias(rCat.data)
        setPersonas(rPer.data)
    }

    // Abre el modal vacío para agregar un gasto nuevo
    function abrirModalNuevo() {
        setDescripcion(""); setMonto(""); setFecha("")
        setIdCategoria(""); setIdPersona("")
        setEsCompartido(false); setError("")
        setEditandoId(null); setMostrarModal(true)
    }

    // Abre el modal con los datos del gasto para editarlo
    function abrirModalEditar(g) {
        setDescripcion(g.descripcion)
        setMonto(String(g.monto))
        setFecha(g.fecha)
        setIdCategoria(String(g.id_categoria))
        setIdPersona(String(g.id_persona))
        setEsCompartido(g.es_compartido)
        setError(""); setEditandoId(g.id_gasto); setMostrarModal(true)
    }

    // Cierra el modal y limpia todo
    function cerrarModal() {
        setMostrarModal(false); setEditandoId(null)
        setDescripcion(""); setMonto(""); setFecha("")
        setIdCategoria(""); setIdPersona("")
        setEsCompartido(false); setError("")
    }

    // Guarda el gasto nuevo o actualiza el existente
    async function guardarGasto() {
        // Validaciones antes de enviar al backend
        if (!descripcion.trim()) {
            setError("La descripción es obligatoria"); return
        }
        if (!monto || Number(monto) <= 0) {
            setError("El monto debe ser mayor a 0"); return
        }
        if (!fecha) {
            setError("La fecha es obligatoria"); return
        }
        if (!idCategoria) {
            setError("Selecciona una categoría"); return
        }
        if (!idPersona) {
            setError("Selecciona quién pagó"); return
        }

        try {
            if (editandoId) {
                // Actualizamos el gasto existente
                await api.put(`/gastos/${editandoId}`, {
                    descripcion,
                    monto:        Number(monto),
                    fecha,
                    id_categoria: Number(idCategoria),
                })
            } else {
                // Creamos un gasto nuevo
                await api.post("/gastos/", {
                    descripcion,
                    monto:        Number(monto),
                    fecha,
                    id_categoria: Number(idCategoria),
                    id_persona:   Number(idPersona),
                    es_compartido: esCompartido,
                })
            }
            await cargarTodo()
            cerrarModal()
        } catch (ex) {
            setError(ex.response?.data?.detail || "Ocurrió un error")
        }
    }

    // Elimina un gasto del backend
    async function eliminarGasto(id) {
        if (!window.confirm("¿Eliminar este gasto?")) return
        try {
            await api.delete(`/gastos/${id}`)
            await cargarTodo()
        } catch (ex) {
            alert(ex.response?.data?.detail || "No se pudo eliminar")
        }
    }

    // Busca el nombre de la categoría por su id
    function getNombreCategoria(id) {
        const c = categorias.find(c => c.id_categoria === id)
        return c ? c.icono + " " + c.nombre : "—"
    }

    // Busca el nombre de la persona por su id
    function getNombrePersona(id) {
        const p = personas.find(p => p.id_persona === id)
        return p ? p.nombre : "—"
    }

    // Aplica los filtros de búsqueda, categoría y persona
    const gastosFiltrados = gastos.filter(g => {
        const coincideTexto    = g.descripcion.toLowerCase().includes(busqueda.toLowerCase())
        const coincideCategoria = filtroCat     ? g.id_categoria === Number(filtroCat)    : true
        const coincidePersona   = filtroPersona ? g.id_persona   === Number(filtroPersona) : true
        return coincideTexto && coincideCategoria && coincidePersona
    })

    // Total de todos los gastos
    const totalGastado = gastos.reduce((acc, g) => acc + Number(g.monto), 0)


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