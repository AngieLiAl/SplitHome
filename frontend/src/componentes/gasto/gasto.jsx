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

    

    return (
        <div className="container-fluid py-4">

            {/* Encabezado */}
            <div className="d-flex justify-content-between align-items-end flex-wrap gap-3 mb-4">
                <div>
                    <h2 style={{ fontFamily: "Playfair Display, serif", fontSize: "1.7rem" }}>
                        Gastos del hogar
                    </h2>
                    <p className="text-muted mb-0">
                        Registra, edita o elimina los gastos compartidos.
                    </p>
                </div>
                <div className="d-flex align-items-center gap-3">
                    {/* Total acumulado */}
                    <span style={{
                        background: "var(--dark)",
                        color: "#fff",
                        padding: "0.5rem 1rem",
                        borderRadius: "99px",
                        fontSize: "0.88rem",
                        fontWeight: 600
                    }}>
                        Total: S/. {totalGastado.toFixed(2)}
                    </span>
                    <button className="btn-primario" onClick={abrirModalNuevo}>
                        + Nuevo gasto
                    </button>
                </div>
            </div>

            {/* Filtros */}
            <div className="row g-2 mb-3">
                <div className="col-12 col-md-5">
                    <input
                        type="text"
                        className="form-control"
                        style={{ borderColor: "var(--border)" }}
                        placeholder="🔍 Buscar gasto..."
                        value={busqueda}
                        onChange={e => setBusqueda(e.target.value)}
                    />
                </div>
                <div className="col-6 col-md-3">
                    <select
                        className="form-select"
                        style={{ borderColor: "var(--border)" }}
                        value={filtroCat}
                        onChange={e => setFiltroCat(e.target.value)}>
                        <option value="">Todas las categorías</option>
                        {categorias.map(c => (
                            <option key={c.id_categoria} value={c.id_categoria}>
                                {c.icono} {c.nombre}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="col-6 col-md-4">
                    <select
                        className="form-select"
                        style={{ borderColor: "var(--border)" }}
                        value={filtroPersona}
                        onChange={e => setFiltroPersona(e.target.value)}>
                        <option value="">Todos los miembros</option>
                        {personas.map(p => (
                            <option key={p.id_persona} value={p.id_persona}>
                                {p.nombre}
                            </option>
                        ))}
                    </select>
                </div>
            </div>

            {/* Tabla de gastos */}
            {gastosFiltrados.length === 0 ? (
                <div className="text-center text-muted py-5">
                    <div style={{ fontSize: "2.5rem", opacity: 0.3 }}>🧾</div>
                    <p className="mt-2">No hay gastos registrados.</p>
                    <button className="btn-primario" onClick={abrirModalNuevo}>
                        Registrar el primero
                    </button>
                </div>
            ) : (
                <div className="table-responsive"
                    style={{
                        background: "#fff",
                        border: "1px solid var(--border)",
                        borderRadius: "var(--r)",
                        overflow: "hidden"
                    }}>
                    <table className="table table-hover mb-0">
                        <thead style={{ background: "var(--cream)" }}>
                            <tr>
                                <th style={{ fontSize: "0.74rem", textTransform: "uppercase",
                                    letterSpacing: "0.04em", color: "var(--muted)",
                                    padding: "0.9rem 1.2rem", borderBottom: "1px solid var(--border)" }}>
                                    Descripción
                                </th>
                                <th style={{ fontSize: "0.74rem", textTransform: "uppercase",
                                    letterSpacing: "0.04em", color: "var(--muted)",
                                    padding: "0.9rem 1.2rem", borderBottom: "1px solid var(--border)" }}>
                                    Categoría
                                </th>
                                <th style={{ fontSize: "0.74rem", textTransform: "uppercase",
                                    letterSpacing: "0.04em", color: "var(--muted)",
                                    padding: "0.9rem 1.2rem", borderBottom: "1px solid var(--border)" }}>
                                    Pagó
                                </th>
                                <th style={{ fontSize: "0.74rem", textTransform: "uppercase",
                                    letterSpacing: "0.04em", color: "var(--muted)",
                                    padding: "0.9rem 1.2rem", borderBottom: "1px solid var(--border)" }}>
                                    Fecha
                                </th>
                                <th style={{ fontSize: "0.74rem", textTransform: "uppercase",
                                    letterSpacing: "0.04em", color: "var(--muted)",
                                    padding: "0.9rem 1.2rem", borderBottom: "1px solid var(--border)" }}>
                                    Monto
                                </th>
                                <th style={{ fontSize: "0.74rem", textTransform: "uppercase",
                                    letterSpacing: "0.04em", color: "var(--muted)",
                                    padding: "0.9rem 1.2rem", borderBottom: "1px solid var(--border)" }}>
                                    Compartido
                                </th>
                                <th style={{ borderBottom: "1px solid var(--border)" }}></th>
                            </tr>
                        </thead>
                        <tbody>
                            {gastosFiltrados.map((g) => (
                                <tr key={g.id_gasto}>
                                    <td style={{ padding: "0.85rem 1.2rem", fontSize: "0.88rem" }}>
                                        {g.descripcion}
                                    </td>
                                    <td style={{ padding: "0.85rem 1.2rem", fontSize: "0.88rem" }}>
                                        <span style={{
                                            background: "var(--mid)",
                                            padding: "0.2rem 0.6rem",
                                            borderRadius: "99px",
                                            fontSize: "0.78rem"
                                        }}>
                                            {getNombreCategoria(g.id_categoria)}
                                        </span>
                                    </td>
                                    <td style={{ padding: "0.85rem 1.2rem", fontSize: "0.88rem" }}>
                                        {getNombrePersona(g.id_persona)}
                                    </td>
                                    <td style={{ padding: "0.85rem 1.2rem", fontSize: "0.88rem" }}>
                                        {g.fecha}
                                    </td>
                                    <td style={{ padding: "0.85rem 1.2rem" }}>
                                        <span className="badge-monto">
                                            S/. {Number(g.monto).toFixed(2)}
                                        </span>
                                    </td>
                                    <td style={{ padding: "0.85rem 1.2rem" }}>
                                        <span style={{
                                            background: g.es_compartido ? "var(--ok-bg)" : "var(--mid)",
                                            color: g.es_compartido ? "var(--accent2)" : "var(--muted)",
                                            padding: "0.2rem 0.6rem",
                                            borderRadius: "99px",
                                            fontSize: "0.76rem",
                                            fontWeight: 600
                                        }}>
                                            {g.es_compartido ? "Sí" : "No"}
                                        </span>
                                    </td>
                                    <td style={{ padding: "0.85rem 1.2rem" }}>
                                        <div className="d-flex gap-1 justify-content-end">
                                            <button
                                                className="btn btn-sm"
                                                style={{
                                                    background: "var(--mid)",
                                                    border: "none",
                                                    borderRadius: "var(--r-sm)",
                                                    width: 30, height: 30
                                                }}
                                                title="Editar"
                                                onClick={() => abrirModalEditar(g)}>
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
                                                onClick={() => eliminarGasto(g.id_gasto)}>
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
    )
}

export default Gasto