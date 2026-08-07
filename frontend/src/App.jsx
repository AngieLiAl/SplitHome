// Archivo principal que organiza el sidebar y el contenido
import { Routes, Route, NavLink, useLocation } from "react-router-dom"
import { FaHome, FaUsers, FaTags, FaWallet, FaBalanceScale } from "react-icons/fa"

import Panel     from "./componentes/panel/Panel"
import Persona   from "./componentes/persona/Persona"
import Categoria from "./componentes/categoria/Categoria"
import Gasto     from "./componentes/gasto/Gasto"
import Balance   from "./componentes/balance/Balance"

import "./App.css"

// Títulos que se muestran en la barra superior según la página
const titulos = {
  "/":          "Inicio",
  "/panel":     "Inicio",
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
      {/* En móvil se oculta con d-none d-md-flex de Bootstrap */}
      <aside className="sidebar d-none d-md-flex">

        <div className="sidebar-logo mb-1">
          Split<em>Home</em>
        </div>

        <div className="hogar-pill mb-4">
          <span className="hogar-dot"></span>
          <span>Depa 304</span>
        </div>

        <nav className="side-nav">
          <NavLink
            to="/panel"
            className={({ isActive }) => "nav-btn" + (isActive ? " activo" : "")}
          >
            <FaHome /> Inicio
          </NavLink>

          <NavLink
            to="/persona"
            className={({ isActive }) => "nav-btn" + (isActive ? " activo" : "")}
          >
            <FaUsers /> Miembros
          </NavLink>

          <NavLink
            to="/categoria"
            className={({ isActive }) => "nav-btn" + (isActive ? " activo" : "")}
          >
            <FaTags /> Categorías
          </NavLink>

          <NavLink
            to="/gasto"
            className={({ isActive }) => "nav-btn" + (isActive ? " activo" : "")}
          >
            <FaWallet /> Gastos
          </NavLink>

          <NavLink
            to="/balance"
            className={({ isActive }) => "nav-btn" + (isActive ? " activo" : "")}
          >
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

        {/* Barra superior */}
        <header className="topbar">
          <span className="topbar-title">{titulo}</span>
          <div className="d-flex align-items-center gap-2">
            <div className="avatar">AL</div>
            <span style={{ fontSize: "0.88rem", fontWeight: 500 }}>
              Angie
            </span>
          </div>
        </header>

        {/* En móvil mostramos un navbar horizontal simple de Bootstrap */}
        <nav className="d-flex d-md-none gap-2 p-2"
          style={{ background: "#1a1917", overflowX: "auto" }}>
          <NavLink to="/panel"     className="nav-btn" style={{ whiteSpace: "nowrap" }}><FaHome />     Inicio</NavLink>
          <NavLink to="/persona"   className="nav-btn" style={{ whiteSpace: "nowrap" }}><FaUsers />    Miembros</NavLink>
          <NavLink to="/categoria" className="nav-btn" style={{ whiteSpace: "nowrap" }}><FaTags />     Categorías</NavLink>
          <NavLink to="/gasto"     className="nav-btn" style={{ whiteSpace: "nowrap" }}><FaWallet />   Gastos</NavLink>
          <NavLink to="/balance"   className="nav-btn" style={{ whiteSpace: "nowrap" }}><FaBalanceScale /> Balance</NavLink>
        </nav>

        <div className="page-content p-4">
          <Routes>
            <Route path="/"          element={<Panel />}     />
            <Route path="/panel"     element={<Panel />}     />
            <Route path="/persona"   element={<Persona />}   />
            <Route path="/categoria" element={<Categoria />} />
            <Route path="/gasto"     element={<Gasto />}     />
            <Route path="/balance"   element={<Balance />}   />
          </Routes>
        </div>

      </div>
    </div>
  )
}

export default App