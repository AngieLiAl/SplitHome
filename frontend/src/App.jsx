import { Routes, Route } from "react-router-dom"
import Menu from "./componentes/menu/Menu"
import Panel from "./componentes/panel/Panel"
import Persona from "./componentes/persona/Persona"
import Categoria from "./componentes/categoria/Categoria"
import Gasto from "./componentes/gasto/Gasto"
import Balance from "./componentes/balance/Balance"

function App() {
  return (
    <>
      <Menu />

      <Routes>
        <Route path="/"          element={<Panel />} />
        <Route path="/panel"     element={<Panel />} />
        <Route path="/persona"   element={<Persona />} />
        <Route path="/categoria" element={<Categoria />} />
        <Route path="/gasto"     element={<Gasto />} />
        <Route path="/balance"   element={<Balance />} />
      </Routes>
    </>
  )
}

export default App