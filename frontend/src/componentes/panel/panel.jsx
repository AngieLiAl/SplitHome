import { FaUsers, FaTags, FaWallet, FaBalanceScale } from "react-icons/fa"
import { Link } from "react-router-dom"
import { useState } from "react"

function Panel() {

    const [totalPersonas] = useState(2)
    const [totalCategorias] = useState(7)
    const [totalGastos] = useState(5)
    const [totalMonto] = useState(1624.00)

    const gastosRecientes = [
        { descripcion: "Alquiler Enero", monto: 1200.00, persona: "Angie", categoria: "🏠 Alquiler" },
        { descripcion: "Recibo de Luz", monto: 85.00, persona: "Angela", categoria: "💡 Luz" },
        { descripcion: "Recibo de Agua", monto: 60.00, persona: "Angela", categoria: "💧 Agua" },
        { descripcion: "Internet", monto: 99.00, persona: "Angie", categoria: "📶 Internet" },
        { descripcion: "Mercado semanal", monto: 180.00, persona: "Angela", categoria: "🍛 Comida" },
    ]
    
    const porCategoria = [
        { nombre: "🏠 Alquiler", monto: 1200, porcentaje: 100 },
        { nombre: "🍛 Comida", monto: 180, porcentaje: 15 },
        { nombre: "📶 Internet", monto: 99, porcentaje: 8 },
        { nombre: "💡 Luz", monto: 85, porcentaje: 7 },
        { nombre: "💧 Agua", monto: 60, porcentaje: 5 },
    ]

    return (
        <div>
            {/* Saludo */}
            <div className="d-flex justify-content-between align-items-end flex-wrap gap-3 mb-4">
                <div>
                    <h2 className="fw-bold mb-1" style={{ fontFamily: "Playfair Display, serif" }}>
                        Hola, Angie 👋
                    </h2>
                    <p className="text-muted mb-0">
                        Esto es lo que está pasando en tu hogar este mes.
                    </p>
                </div>
                <Link to="/gasto" className="btn text-white fw-semibold"
                    style={{ background: "var(--accent)", borderRadius: "var(--r-sm)" }}>
                    + Nuevo gasto
                </Link>
            </div>

            {/* KPIs */}
            <div className="row mb-4">

                <div className="col-md-4 mb-3">
                    <div className="kpi-card card p-3">
                        <span className="kpi-label">Gastado este mes</span>
                        <span className="kpi-value">S/. {totalMonto.toFixed(2)}</span>
                        <span style={{ fontSize: "0.78rem", color: "var(--accent2)" }}>
                            ↑ este mes
                        </span>
                    </div>
                </div>

                <div className="col-md-4 mb-3">
                    <div className="kpi-card card p-3">
                        <span className="kpi-label">Gastos registrados</span>
                        <span className="kpi-value">{totalGastos}</span>
                        <span style={{ fontSize: "0.78rem", color: "var(--muted)" }}>
                            este mes
                        </span>
                    </div>
                </div>

                <div className="col-md-4 mb-3">
                    <div className="kpi-card oscuro card p-3">
                        <span className="kpi-label">Tu balance</span>
                        <span className="kpi-value text-white">S/. 0.00</span>
                        <span style={{ fontSize: "0.78rem", color: "var(--accent)" }}>
                            al día
                        </span>
                    </div>
                </div>

            </div>

            {/* Gastos recientes + barras categoría */}
            <div className="row">

                {/* Gastos recientes */}
                <div className="col-md-8 mb-4">
                    <div className="panel-card">
                        <div className="d-flex justify-content-between align-items-center mb-3">
                            <h6 className="panel-titulo mb-0">Gastos recientes</h6>
                            <Link to="/gasto"
                                style={{ color: "var(--accent)", fontSize: "0.84rem", fontWeight: 600 }}>
                                Ver todos →
                            </Link>
                        </div>

                        <table className="table tabla-sh table-hover mb-0">
                            <thead>
                                <tr>
                                    <th>Descripción</th>
                                    <th>Categoría</th>
                                    <th>Pagó</th>
                                    <th>Monto</th>
                                </tr>
                            </thead>
                            <tbody>
                                {gastosRecientes.map((g, i) => (
                                    <tr key={i}>
                                        <td>{g.descripcion}</td>
                                        <td>{g.categoria}</td>
                                        <td>{g.persona}</td>
                                        <td>
                                            <span className="badge-monto">
                                                S/. {g.monto.toFixed(2)}
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

        </div>
    )
}