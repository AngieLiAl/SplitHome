import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import api from "../api/axios"

function Panel() {

    const [personas,   setPersonas]   = useState([])
    const [categorias, setCategorias] = useState([])
    const [gastos,     setGastos]     = useState([])

    useEffect(() => {
        api.get("/personas/").then(r   => setPersonas(r.data))
        api.get("/categorias/").then(r => setCategorias(r.data))
        api.get("/gastos/").then(r     => setGastos(r.data))
    }, [])

    const totalGastado = gastos.reduce((acc, g) => acc + Number(g.monto), 0)
    const gastosRecientes = gastos.slice(0, 4)

    function getNombrePersona(id) {
        const p = personas.find(p => p.id_persona === id)
        return p ? p.nombre : "—"
    }

    function getIconoCategoria(id) {
        const c = categorias.find(c => c.id_categoria === id)
        return c ? c.icono : "📦"
    }

    function getMontoCategoria(id) {
        return gastos
            .filter(g => g.id_categoria === id)
            .reduce((acc, g) => acc + Number(g.monto), 0)
    }

    const maxMonto = Math.max(1, ...categorias.map(c => getMontoCategoria(c.id_categoria)))

    return (
        <div className="container-fluid py-4">

            {/* Saludo */}
            <div className="d-flex justify-content-between align-items-end flex-wrap gap-3 mb-4">
                <div>
                    <h2 style={{ fontFamily: "Playfair Display, serif", fontSize: "1.7rem" }}>
                        Hola, Angie 👋
                    </h2>
                    <p className="text-muted mb-0">
                        Esto es lo que está pasando en tu hogar este mes.
                    </p>
                </div>
                <Link to="/gasto" className="btn-primario">
                    + Nuevo gasto
                </Link>
            </div>

            {/* KPIs — 3 tarjetas en fila */}
            <div className="row g-3 mb-4">
                <div className="col-12 col-md-4">
                    <div className="kpi-card">
                        <span className="kpi-label">Gastado este mes</span>
                        <span className="kpi-value">
                            S/. {totalGastado.toFixed(2)}
                        </span>
                        <span style={{ fontSize: "0.78rem", color: "var(--accent2)" }}>
                            este mes
                        </span>
                    </div>
                </div>
                <div className="col-12 col-md-4">
                    <div className="kpi-card">
                        <span className="kpi-label">Gastos registrados</span>
                        <span className="kpi-value">{gastos.length}</span>
                        <span style={{ fontSize: "0.78rem", color: "var(--muted)" }}>
                            en total
                        </span>
                    </div>
                </div>
                <div className="col-12 col-md-4">
                    <div className="kpi-card oscuro">
                        <span className="kpi-label">Miembros del hogar</span>
                        <span className="kpi-value">{personas.length}</span>
                        <span style={{ fontSize: "0.78rem", color: "var(--accent)" }}>
                            activos
                        </span>
                    </div>
                </div>
            </div>

            {/* Gastos recientes + barras por categoría */}
            <div className="row g-3">

                {/* Gastos recientes */}
                <div className="col-12 col-md-8">
                    <div className="panel-card h-100">
                        <div className="d-flex justify-content-between align-items-center mb-3">
                            <h6 className="panel-titulo mb-0">Gastos recientes</h6>
                            <Link to="/gasto"
                                style={{ color: "var(--accent)", fontSize: "0.84rem", fontWeight: 600 }}>
                                Ver todos →
                            </Link>
                        </div>

                        {gastosRecientes.length === 0 ? (
                            <div className="text-center text-muted py-4">
                                <div style={{ fontSize: "2rem", opacity: 0.3 }}>🧾</div>
                                <p className="mt-2 mb-0">Aún no hay gastos registrados.</p>
                            </div>
                        ) : (
                            <div className="d-flex flex-column gap-2">
                                {gastosRecientes.map((g) => (
                                    <div key={g.id_gasto}
                                        className="d-flex align-items-center gap-3 py-2"
                                        style={{ borderBottom: "1px solid var(--mid)" }}>

                                        {/* Ícono de categoría */}
                                        <div style={{
                                            width: 38, height: 38,
                                            borderRadius: 10,
                                            background: "var(--mid)",
                                            display: "flex",
                                            alignItems: "center",
                                            justifyContent: "center",
                                            fontSize: "1rem",
                                            flexShrink: 0
                                        }}>
                                            {getIconoCategoria(g.id_categoria)}
                                        </div>

                                        {/* Info */}
                                        <div className="flex-grow-1 min-w-0">
                                            <div style={{ fontWeight: 500, fontSize: "0.9rem" }}>
                                                {g.descripcion}
                                            </div>
                                            <div className="text-muted"
                                                style={{ fontSize: "0.78rem" }}>
                                                {getNombrePersona(g.id_persona)} · {g.fecha}
                                            </div>
                                        </div>

                                        {/* Monto */}
                                        <div style={{ fontWeight: 600, fontSize: "0.92rem", whiteSpace: "nowrap" }}>
                                            S/. {Number(g.monto).toFixed(2)}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>

                {/* Barras por categoría */}
                <div className="col-12 col-md-4">
                    <div className="panel-card h-100">
                        <h6 className="panel-titulo">Por categoría</h6>

                        {categorias.length === 0 ? (
                            <p className="text-muted" style={{ fontSize: "0.88rem" }}>
                                Sin datos todavía.
                            </p>
                        ) : (
                            <div className="d-flex flex-column gap-3">
                                {categorias.map((c) => {
                                    const monto = getMontoCategoria(c.id_categoria)
                                    const pct   = (monto / maxMonto) * 100
                                    return (
                                        <div key={c.id_categoria}>
                                            <div className="d-flex justify-content-between mb-1"
                                                style={{ fontSize: "0.82rem" }}>
                                                <span>{c.icono} {c.nombre}</span>
                                                <strong>S/. {monto.toFixed(2)}</strong>
                                            </div>
                                            {/* Barra de progreso con Bootstrap */}
                                            <div className="progress" style={{ height: "8px", borderRadius: "99px" }}>
                                                <div
                                                    className="progress-bar"
                                                    style={{
                                                        width: `${pct}%`,
                                                        background: "var(--accent)",
                                                        borderRadius: "99px"
                                                    }}>
                                                </div>
                                            </div>
                                        </div>
                                    )
                                })}
                            </div>
                        )}
                    </div>
                </div>

            </div>
        </div>
    )
}

export default Panel