import { FaUsers, FaTags, FaWallet, FaBalanceScale } from "react-icons/fa"
import { Link } from "react-router-dom"
import { useState } from "react"

function Panel() {

    const [totalPersonas]   = useState(2)
    const [totalCategorias] = useState(7)
    const [totalGastos]     = useState(5)
    const [totalMonto] = useState(1624.00)

    
