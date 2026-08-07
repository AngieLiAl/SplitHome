// Página de balance entre los miembros del hogar
// Muestra cuánto pagó cada uno, cuánto le corresponde
// y quién le debe a quién para equilibrar los gastos
import { useState, useEffect } from "react"
import api from "../api/axios"

function Balance() {

    const [personas, setPersonas] = useState([])
    const [gastos,   setGastos]   = useState([])

    // Al entrar a la página traemos los datos del backend
    useEffect(() => {
        cargarTodo()
    }, [])

    async function cargarTodo() {
        const [rPer, rGas] = await Promise.all([
            api.get("/personas/"),
            api.get("/gastos/"),
        ])
        setPersonas(rPer.data)
        setGastos(rGas.data)
    }

    // Suma todo lo que pagó una persona
    function cuantoPago(idPersona) {
        return gastos
            .filter(g => g.id_persona === idPersona)
            .reduce((acc, g) => acc + Number(g.monto), 0)
    }

    // Total general de todos los gastos
    const totalGeneral = gastos.reduce((acc, g) => acc + Number(g.monto), 0)

    // Lo que le tocaría pagar a cada uno si se divide igual
    const promedio = personas.length > 0 ? totalGeneral / personas.length : 0

    // Diferencia entre lo que pagó y lo que le toca
    // positivo = le deben dinero
    // negativo = debe dinero
    function calcularDiff(idPersona) {
        return cuantoPago(idPersona) - promedio
    }

    // Saca las iniciales del nombre para el avatar
    function iniciales(nombre) {
        return nombre.split(" ").map(p => p[0]).slice(0, 2).join("").toUpperCase()
    }

    return (
        <div className="container-fluid py-4">

            {/* Encabezado */}
            <div className="d-flex justify-content-between align-items-end flex-wrap gap-3 mb-4">
                <div>
                    <h2 style={{ fontFamily: "Playfair Display, serif", fontSize: "1.7rem" }}>
                        Balance entre miembros
                    </h2>
                    <p className="text-muted mb-0">
                        Así está repartida la cuenta del hogar hoy.
                    </p>
                </div>
                {/* Total general destacado */}
                <span style={{
                    background: "var(--dark)",
                    color: "#fff",
                    padding: "0.5rem 1rem",
                    borderRadius: "99px",
                    fontSize: "0.88rem",
                    fontWeight: 600
                }}>
                    Total: S/. {totalGeneral.toFixed(2)}
                </span>
            </div>

            {/* Tarjetas de balance por persona */}
            <div className="row g-3 mb-4">
                {personas.map((p) => {
                    const pagado = cuantoPago(p.id_persona)
                    const diff   = calcularDiff(p.id_persona)

                    return (
                        <div className="col-12 col-md-6" key={p.id_persona}>
                            <div className="balance-card">

                                {/* Avatar con iniciales */}
                                <div className="balance-avatar">
                                    {iniciales(p.nombre)}
                                </div>

                                {/* Info de la persona */}
                                <div className="flex-grow-1">
                                    <div className="fw-semibold mb-1">{p.nombre}</div>
                                    <div className="text-muted mb-1"
                                        style={{ fontSize: "0.8rem" }}>
                                        {p.email}
                                    </div>
                                    <div style={{ fontSize: "0.84rem" }}>
                                        Pagó: <strong>S/. {pagado.toFixed(2)}</strong>
                                    </div>
                                    <div style={{ fontSize: "0.82rem" }}>
                                        Le toca: <strong>S/. {promedio.toFixed(2)}</strong>
                                    </div>
                                    {/* Estado del balance */}
                                    <div className="mt-1">
                                        {diff > 0.01 ? (
                                            <span style={{
                                                color: "var(--accent2)",
                                                fontSize: "0.82rem",
                                                fontWeight: 600
                                            }}>
                                                ✅ Le deben S/. {diff.toFixed(2)}
                                            </span>
                                        ) : diff < -0.01 ? (
                                            <span style={{
                                                color: "var(--danger)",
                                                fontSize: "0.82rem",
                                                fontWeight: 600
                                            }}>
                                                ⚠️ Debe S/. {Math.abs(diff).toFixed(2)}
                                            </span>
                                        ) : (
                                            <span style={{
                                                color: "var(--muted)",
                                                fontSize: "0.82rem",
                                                fontWeight: 600
                                            }}>
                                                ✓ Al día
                                            </span>
                                        )}
                                    </div>
                                </div>

                                {/* Monto destacado a la derecha */}
                                <div style={{
                                    fontFamily: "Playfair Display, serif",
                                    fontSize: "1.3rem",
                                    color: diff >= 0 ? "var(--accent2)" : "var(--danger)",
                                    whiteSpace: "nowrap"
                                }}>
                                    S/. {Math.abs(diff).toFixed(2)}
                                </div>

                            </div>
                        </div>
                    )
                })}
            </div>

            {/* Resumen general en 3 tarjetas KPI */}
            <div className="row g-3 mb-4">
                <div className="col-12 col-md-4">
                    <div className="kpi-card">
                        <span className="kpi-label">Total gastado</span>
                        <span className="kpi-value">
                            S/. {totalGeneral.toFixed(2)}
                        </span>
                        <span style={{ fontSize: "0.78rem", color: "var(--muted)" }}>
                            entre {personas.length} miembros
                        </span>
                    </div>
                </div>
                <div className="col-12 col-md-4">
                    <div className="kpi-card">
                        <span className="kpi-label">Le toca a cada uno</span>
                        <span className="kpi-value">
                            S/. {promedio.toFixed(2)}
                        </span>
                        <span style={{ fontSize: "0.78rem", color: "var(--muted)" }}>
                            división igualitaria
                        </span>
                    </div>
                </div>
                <div className="col-12 col-md-4">
                    <div className="kpi-card oscuro">
                        <span className="kpi-label">Gastos registrados</span>
                        <span className="kpi-value">{gastos.length}</span>
                        <span style={{ fontSize: "0.78rem", color: "var(--accent)" }}>
                            en total
                        </span>
                    </div>
                </div>
            </div>

            {/* ¿Quién le debe a quién? */}
            <div className="panel-card">
                <h6 className="panel-titulo">¿Quién le debe a quién?</h6>

                {personas.every(p => Math.abs(calcularDiff(p.id_persona)) <= 0.01) ? (
                    <div className="text-center text-muted py-3">
                        🎉 Todo está equilibrado entre los miembros
                    </div>
                ) : (
                    <div className="d-flex flex-column gap-2">
                        {personas.map((p) => {
                            const diff = calcularDiff(p.id_persona)
                            // Solo mostramos los que deben dinero
                            if (diff >= -0.01) return null

                            // Buscamos quién recibe el dinero
                            const acreedor = personas.find(
                                a => calcularDiff(a.id_persona) > 0.01
                            )

                            return (
                                <div key={p.id_persona}
                                    className="d-flex align-items-center gap-3 py-2"
                                    style={{ borderBottom: "1px solid var(--mid)" }}>

                                    <div style={{ fontSize: "1.4rem" }}>💸</div>

                                    <div className="flex-grow-1">
                                        <div className="fw-semibold"
                                            style={{ fontSize: "0.9rem" }}>
                                            {p.nombre} le debe a{" "}
                                            {acreedor ? acreedor.nombre : "—"}
                                        </div>
                                        <div className="text-muted"
                                            style={{ fontSize: "0.78rem" }}>
                                            Para equilibrar el balance del hogar
                                        </div>
                                    </div>

                                    <span className="badge-monto">
                                        S/. {Math.abs(diff).toFixed(2)}
                                    </span>
                                </div>
                            )
                        })}
                    </div>
                )}
            </div>

        </div>
    )
}

export default Balance