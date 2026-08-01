import { useState } from "react"
import { FaBalanceScale } from "react-icons/fa"

function Balance() {

    const personas = [
        { id: 1, nombre: "Angie Lizarsaburu",  email: "angie@splithome.pe"  },
        { id: 2, nombre: "Angela Escobedo",     email: "angela@splithome.pe" },
    ]

    const gastos = [
        { id: 1, descripcion: "Alquiler Enero",  monto: 1200.00, idPersona: 1, esCompartido: true  },
        { id: 2, descripcion: "Recibo de Luz",   monto: 85.00,   idPersona: 2, esCompartido: true  },
        { id: 3, descripcion: "Recibo de Agua",  monto: 60.00,   idPersona: 2, esCompartido: true  },
        { id: 4, descripcion: "Internet",        monto: 99.00,   idPersona: 1, esCompartido: true  },
        { id: 5, descripcion: "Mercado semanal", monto: 180.00,  idPersona: 2, esCompartido: false },
    ]

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

            







        </div>
    )
}

export default Balance