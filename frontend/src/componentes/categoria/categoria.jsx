import { useState } from "react"
import { FaTags } from "react-icons/fa"

function Categoria() {
    const [nombre,      setNombre]      = useState("")
    const [icono,       setIcono]       = useState("")
    const [descripcion, setDescripcion] = useState("")
    const [busqueda,    setBusqueda]    = useState("")
    const [error,       setError]       = useState("")
    const [categorias, setCategorias] = useState([
        { id: 1, nombre: "Alquiler",  icono: "🏠", descripcion: "Pago mensual del alquiler" },
        { id: 2, nombre: "Luz",       icono: "💡", descripcion: "Recibo de electricidad"    },
        { id: 3, nombre: "Agua",      icono: "💧", descripcion: "Recibo de agua"            },
        { id: 4, nombre: "Internet",  icono: "📶", descripcion: "Servicio de internet"      },
        { id: 5, nombre: "Comida",    icono: "🍛", descripcion: "Mercado y alimentación"    },
        { id: 6, nombre: "Limpieza",  icono: "🧹", descripcion: "Productos de limpieza"     },
        { id: 7, nombre: "Otros",     icono: "📦", descripcion: "Gastos varios"             },
    ])

    return (
        <div>

        </div>
    )
}

export default Categoria