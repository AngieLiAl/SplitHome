import { useState } from "react"
import { FaUsers } from "react-icons/fa"

function Persona() {
    const [nombre,   setNombre]   = useState("")
    const [email,    setEmail]    = useState("")
    const [busqueda, setBusqueda] = useState("")
    const [personas, setPersonas] = useState([
        { id: 1, nombre: "Angie Lizarsaburu",  email: "angie@splithome.pe",  fecha: "2025-01-01" },
        { id: 2, nombre: "Angela Escobedo",     email: "angela@splithome.pe", fecha: "2025-01-01" },
    ])
    const [error, setError] = useState("")

    return (
        <div>

        </div>
    )
}

export default Persona