// Este archivo crea la conexión con el backend (FastAPI)
// Todos los componentes usan este archivo para pedir
// o enviar datos al servidor, sin tener que escribir
// la dirección completa cada vez
import axios from "axios"

const api = axios.create({
    // Dirección donde está corriendo el backend
    baseURL: "http://localhost:8000",
})

export default api