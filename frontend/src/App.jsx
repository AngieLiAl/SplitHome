import { Routes, Route, NavLink, useLocation } from "react-router-dom"
import { FaHome, FaUsers, FaTags, FaWallet, FaBalanceScale } from "react-icons/fa"
import Panel from "./componentes/panel/Panel"
import Persona from "./componentes/persona/Persona"
import Categoria from "./componentes/categoria/Categoria"
import Gasto from "./componentes/gasto/Gasto"
import Balance from "./componentes/balance/Balance"
import "./App.css"

const titulos = {
  "/panel":     "Inicio",
  "/":          "Inicio",
  "/persona":   "Miembros",
  "/categoria": "Categorías",
  "/gasto":     "Gastos",
  "/balance":   "Balance",
}

function App() {
  const location = useLocation()
  const titulo = titulos[location.pathname] || "SplitHome"

  return (
    <div className="app-shell">

      {/* ── SIDEBAR ── */}
      <aside className="sidebar">
        <div className="sidebar-logo mb-1">
          Split<em>Home</em>
        </div>

        <div className="hogar-pill mb-4">
          <span className="hogar-dot"></span>
          <span>Depa 304</span>
        </div>

        <nav className="side-nav">
          <NavLink to="/panel" className={({isActive}) => "nav-btn" + (isActive ? " activo" : "")}>
            <FaHome /> Inicio
          </NavLink>
          <NavLink to="/persona" className={({isActive}) => "nav-btn" + (isActive ? " activo" : "")}>
            <FaUsers /> Miembros
          </NavLink>
          <NavLink to="/categoria" className={({isActive}) => "nav-btn" + (isActive ? " activo" : "")}>
            <FaTags /> Categorías
          </NavLink>
          <NavLink to="/gasto" className={({isActive}) => "nav-btn" + (isActive ? " activo" : "")}>
            <FaWallet /> Gastos
          </NavLink>
          <NavLink to="/balance" className={({isActive}) => "nav-btn" + (isActive ? " activo" : "")}>
            <FaBalanceScale /> Balance
          </NavLink>
        </nav>

        <div className="side-bottom">
          <button className="nav-btn" onClick={() => alert("Cerrando sesión...")}>
            ↩ Cerrar sesión
          </button>
        </div>
      </aside>

      {/* ── CONTENIDO PRINCIPAL ── */}
      <div className="app-main">

        {/* Topbar */}
        <header className="topbar">
          <span className="topbar-title">{titulo}</span>
          <div className="d-flex align-items-center gap-2">
            <div className="avatar">AL</div>
            <span style={{fontSize:"0.88rem", fontWeight:500}}>Angie</span>
          </div>
        </header>

        {/* Rutas */}
        <div className="p-4">
          <Routes>
            <Route path="/"          element={<Panel />} />
            <Route path="/panel"     element={<Panel />} />
            <Route path="/persona"   element={<Persona />} />
            <Route path="/categoria" element={<Categoria />} />
            <Route path="/gasto"     element={<Gasto />} />
            <Route path="/balance"   element={<Balance />} />
          </Routes>
        </div>

      </div>
    </div>
  )
}

export default App