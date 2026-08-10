// La URL del backend se lee desde el archivo .env
// para no tenerla hardcodeada en el código
import axios from "axios"

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
})

export default api