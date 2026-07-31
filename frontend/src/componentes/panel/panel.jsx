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
        </div>
    )
}