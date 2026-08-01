import { useState } from "react"
import { FaWallet } from "react-icons/fa"

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


    

}
export default Gasto