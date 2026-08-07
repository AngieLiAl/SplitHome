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

    // ── Calcular cuánto pagó cada persona ────────────────────
    function calcularPagado(idPersona) {
        return gastos
            .filter(g => g.idPersona === idPersona)
            .reduce((acc, g) => acc + g.monto, 0)
    }

    // ── Total general ────────────────────────────────────────
    const totalGeneral = gastos.reduce((acc, g) => acc + g.monto, 0)

    // ── Promedio que debería pagar cada uno ──────────────────
    const promedio = totalGeneral / personas.length

    // ── Iniciales para el avatar ─────────────────────────────
    function iniciales(nombre) {
        return nombre.split(" ").map(p => p[0]).slice(0, 2).join("").toUpperCase()
    }

    // ── Calcular deudas ──────────────────────────────────────
    // diff positivo = le deben dinero
    // diff negativo = debe dinero
    function calcularDiff(idPersona) {
        return calcularPagado(idPersona) - promedio
    }

    return (
        <div>

            {/* Encabezado */}
            <div className="d-flex justify-content-between align-items-end flex-wrap gap-3 mb-4">
                <div>
                    <h2 className="fw-bold mb-1"
                        style={{ fontFamily: "Playfair Display, serif" }}>
                        Balance entre miembros
                    </h2>
                    <p className="text-muted mb-0">
                        Así está repartida la cuenta del hogar hoy.
                    </p>
                </div>
                <span className="badge rounded-pill"
                    style={{ background: "var(--accent)", fontSize: "0.9rem", padding: "0.5rem 1rem" }}>
                    <FaBalanceScale className="me-1" />
                    Total: S/. {totalGeneral.toFixed(2)}
                </span>
            </div>

            {/* Tarjetas de balance por persona */}
            <div className="row mb-4">
                {personas.map((p) => {
                    const pagado = calcularPagado(p.id)
                    const diff   = calcularDiff(p.id)

                    return (
                        <div className="col-md-6 mb-3" key={p.id}>
                            <div className="balance-card">

                                {/* Avatar */}
                                <div className="balance-avatar">
                                    {iniciales(p.nombre)}
                                </div>

                                {/* Info */}
                                <div className="flex-grow-1">
                                    <div className="fw-semibold">{p.nombre}</div>
                                    <div className="text-muted" style={{ fontSize: "0.78rem" }}>
                                        {p.email}
                                    </div>
                                    <div className="mt-1" style={{ fontSize: "0.82rem" }}>
                                        Pagó: <strong>S/. {pagado.toFixed(2)}</strong>
                                    </div>
                                    <div style={{ fontSize: "0.8rem" }}>
                                        Le corresponde: <strong>S/. {promedio.toFixed(2)}</strong>
                                    </div>
                                    <div className="mt-1">
                                        {diff > 0 ? (
                                            <span className="text-recibe fw-semibold">
                                                ✅ Le deben S/. {diff.toFixed(2)}
                                            </span>
                                        ) : diff < 0 ? (
                                            <span className="text-debe fw-semibold">
                                                ⚠️ Debe S/. {Math.abs(diff).toFixed(2)}
                                            </span>
                                        ) : (
                                            <span className="text-muted fw-semibold">
                                                ✓ Al día
                                            </span>
                                        )}
                                    </div>
                                </div>

                                {/* Monto destacado */}
                                <div style={{
                                    fontFamily: "Playfair Display, serif",
                                    fontSize: "1.3rem",
                                    color: diff >= 0 ? "var(--accent2)" : "var(--danger)"
                                }}>
                                    S/. {Math.abs(diff).toFixed(2)}
                                </div>

                            </div>
                        </div>
                    )
                })}
            </div>

            {/* Resumen general */}
            <div className="row mb-4">
                <div className="col-md-4 mb-3">
                    <div className="kpi-card card p-3">
                        <span className="kpi-label">Total gastado</span>
                        <span className="kpi-value">S/. {totalGeneral.toFixed(2)}</span>
                        <span style={{ fontSize: "0.78rem", color: "var(--muted)" }}>
                            entre {personas.length} miembros
                        </span>
                    </div>
                </div>
                <div className="col-md-4 mb-3">
                    <div className="kpi-card card p-3">
                        <span className="kpi-label">Le corresponde a cada uno</span>
                        <span className="kpi-value">S/. {promedio.toFixed(2)}</span>
                        <span style={{ fontSize: "0.78rem", color: "var(--muted)" }}>
                            división igualitaria
                        </span>
                    </div>
                </div>
                <div className="col-md-4 mb-3">
                    <div className="kpi-card card p-3">
                        <span className="kpi-label">Gastos registrados</span>
                        <span className="kpi-value">{gastos.length}</span>
                        <span style={{ fontSize: "0.78rem", color: "var(--muted)" }}>
                            en total
                        </span>
                    </div>
                </div>
            </div>

            {/* ¿Quién le debe a quién? */}
            <div className="panel-card">
                <h6 className="panel-titulo">¿Quién le debe a quién?</h6>

                {personas.map((p) => {
                    const diff = calcularDiff(p.id)

                    if (diff >= 0) return null

                    const acreedor = personas.find(a => calcularDiff(a.id) > 0)

                    return (
                        <div className="d-flex align-items-center gap-3 py-2"
                            key={p.id}
                            style={{ borderBottom: "1px solid var(--mid)" }}>
                            <div style={{ fontSize: "1.5rem" }}>💸</div>
                            <div className="flex-grow-1">
                                <div className="fw-semibold" style={{ fontSize: "0.9rem" }}>
                                    {p.nombre} le debe a {acreedor ? acreedor.nombre : "—"}
                                </div>
                                <div className="text-muted" style={{ fontSize: "0.78rem" }}>
                                    Para equilibrar el balance del hogar
                                </div>
                            </div>
                            <span className="badge-monto">
                                S/. {Math.abs(diff).toFixed(2)}
                            </span>
                        </div>
                    )
                })}

                {personas.every(p => calcularDiff(p.id) === 0) && (
                    <p className="text-muted text-center py-3 mb-0">
                        🎉 Todo está equilibrado entre los miembros
                    </p>
                )}
            </div>

        </div>
    )
}

export default Balance