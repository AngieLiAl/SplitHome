// Página de inicio del sistema
// Muestra un resumen general: cuánto se ha gastado,
// cuántos gastos hay y los últimos registrados
import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { FaUsers, FaTags, FaWallet, FaBalanceScale } from "react-icons/fa"
import api from "../api/axios"

function Panel() {

    // Aquí guardamos los datos que vienen del backend
    const [personas,   setPersonas]   = useState([])
    const [categorias, setCategorias] = useState([])
    const [gastos,     setGastos]     = useState([])

    // Al entrar a la página cargamos todos los datos del backend
    useEffect(() => {
        api.get("/personas/").then(r   => setPersonas(r.data))
        api.get("/categorias/").then(r => setCategorias(r.data))
        api.get("/gastos/").then(r     => setGastos(r.data))
    }, [])

    // Calculamos el total sumando todos los montos
    const totalGastado = gastos.reduce((acc, g) => acc + Number(g.monto), 0)

    // Solo mostramos los 4 gastos más recientes en el panel
    const gastosRecientes = gastos.slice(0, 4)

    // Buscamos el nombre de la categoría por su id
    function getNombreCategoria(id) {
        const cat = categorias.find(c => c.id_categoria === id)
        return cat ? cat.icono + " " + cat.nombre : "—"
    }

    // Buscamos el nombre de la persona por su id
    function getNombrePersona(id) {
        const p = personas.find(p => p.id_persona === id)
        return p ? p.nombre : "—"
    }

    // Calculamos cuánto gastó cada persona para las barras
    function getMontoCategoria(id) {
        return gastos
            .filter(g => g.id_categoria === id)
            .reduce((acc, g) => acc + Number(g.monto), 0)
    }

    const maxMonto = Math.max(1, ...categorias.map(c => getMontoCategoria(c.id_categoria)))

    return (
        <div>

            {/* Saludo y botón rápido */}
            <div className="greet-row">
                <div>
                    <h2 className="greet-title">Hola, Angie 👋</h2>
                    <p className="greet-sub">
                        Esto es lo que está pasando en tu hogar este mes.
                    </p>
                </div>
                <Link to="/gasto" className="btn-primario">
                    + Nuevo gasto
                </Link>
            </div>

            {/* Tarjetas de resumen */}
            <div className="kpi-row">
                <div className="kpi-card">
                    <span className="kpi-label">Gastado este mes</span>
                    <span className="kpi-value">
                        S/. {totalGastado.toFixed(2)}
                    </span>
                    <span className="kpi-trend up">este mes</span>
                </div>

                <div className="kpi-card">
                    <span className="kpi-label">Gastos registrados</span>
                    <span className="kpi-value">{gastos.length}</span>
                    <span className="kpi-trend">en total</span>
                </div>

                <div className="kpi-card accent">
                    <span className="kpi-label">Miembros del hogar</span>
                    <span className="kpi-value">{personas.length}</span>
                    <span className="kpi-trend">activos</span>
                </div>
            </div>

            {/* Gastos recientes y barras por categoría */}
            <div className="content-grid">

                {/* Gastos recientes */}
                <div className="panel-card">
                    <div className="d-flex justify-content-between align-items-center mb-3">
                        <h6 className="panel-titulo mb-0">Gastos recientes</h6>
                        <Link
                            to="/gasto"
                            style={{ color: "var(--accent)", fontSize: "0.84rem", fontWeight: 600 }}>
                            Ver todos →
                        </Link>
                    </div>

                    {gastosRecientes.length === 0 ? (
                        <div className="empty-state">
                            <span className="empty-ico">🧾</span>
                            <p>Aún no hay gastos registrados.</p>
                        </div>
                    ) : (
                        <div className="mini-list">
                            {gastosRecientes.map((g) => (
                                <div className="mini-row" key={g.id_gasto}>
                                    <div className="mini-ico">
                                        {categorias.find(c => c.id_categoria === g.id_categoria)?.icono || "📦"}
                                    </div>
                                    <div className="mini-info">
                                        <div className="mini-title">{g.descripcion}</div>
                                        <div className="mini-sub">
                                            {getNombrePersona(g.id_persona)} · {g.fecha}
                                        </div>
                                    </div>
                                    <div className="mini-amount">
                                        S/. {Number(g.monto).toFixed(2)}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Barras por categoría */}
                <div className="panel-card">
                    <h6 className="panel-titulo">Por categoría</h6>

                    {categorias.length === 0 ? (
                        <p style={{ color: "var(--muted)", fontSize: "0.88rem" }}>
                            Sin datos todavía.
                        </p>
                    ) : (
                        <div className="cat-bars">
                            {categorias.map((c) => {
                                const monto = getMontoCategoria(c.id_categoria)
                                const pct   = (monto / maxMonto) * 100
                                return (
                                    <div key={c.id_categoria}>
                                        <div className="d-flex justify-content-between mb-1"
                                            style={{ fontSize: "0.84rem" }}>
                                            <span>{c.icono} {c.nombre}</span>
                                            <strong>S/. {monto.toFixed(2)}</strong>
                                        </div>
                                        <div style={{
                                            height: "8px",
                                            background: "var(--mid)",
                                            borderRadius: "99px",
                                            overflow: "hidden"
                                        }}>
                                            <div style={{
                                                width: `${pct}%`,
                                                height: "100%",
                                                background: "var(--accent)",
                                                borderRadius: "99px",
                                                transition: "width 0.6s ease"
                                            }} />
                                        </div>
                                    </div>
                                )
                            })}
                        </div>
                    )}
                </div>

            </div>
        </div>
    )
}

export default Panel