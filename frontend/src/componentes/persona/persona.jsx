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

    // ── Agregar persona ──────────────────────────────────────
    function agregarPersona() {
        if (!nombre.trim()) {
            setError("El nombre es obligatorio")
            return
        }
        if (!email.includes("@")) {
            setError("Ingresa un email válido")
            return
        }
        if (personas.some(p => p.email === email)) {
            setError("Ese email ya está registrado")
            return
        }
        const nueva = {
            id:     personas.length + 1,
            nombre: nombre.trim(),
            email:  email.trim(),
            fecha:  new Date().toISOString().slice(0, 10)
        }
        setPersonas([...personas, nueva])
        setNombre("")
        setEmail("")
        setError("")
    }

    // ── Eliminar persona ─────────────────────────────────────
    function eliminarPersona(id) {
        setPersonas(personas.filter(p => p.id !== id))
    }

    // ── Iniciales para el avatar ─────────────────────────────
    function iniciales(nombre) {
        return nombre.split(" ").map(p => p[0]).slice(0, 2).join("").toUpperCase()
    }

    // ── Filtrar por búsqueda ─────────────────────────────────
    const personasFiltradas = personas.filter(p =>
        p.nombre.toLowerCase().includes(busqueda.toLowerCase())
    )

    return (
        <div>
            
        </div>
    )
}

export default Persona