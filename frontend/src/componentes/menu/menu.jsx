import "./Menu.css"

import {
  FaHome,
  FaUsers,
  FaTags,
  FaWallet,
  FaBalanceScale
} from "react-icons/fa"

import { useState, useEffect } from "react"
import { Link } from "react-router-dom"


function Menu() {

  const [fecha, setFecha] = useState(new Date())


  useEffect(() => {

    const intervalo = setInterval(() => {
      setFecha(new Date())
    }, 1000)

    return () => clearInterval(intervalo)

  }, [])


  return (

    <nav 
      className="navbar navbar-expand-lg"
      style={{ background: "#1a1917" }}
    >

      <div className="container-fluid">


        <span
          className="navbar-brand fw-bold text-white"
          style={{
            fontFamily: "Georgia",
            fontSize: "22px"
          }}
        >
          Split
          <span style={{ color:"#d4622a" }}>
            Home
          </span>
        </span>



        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >

          <span className="navbar-toggler-icon"></span>

        </button>



        <div
          className="collapse navbar-collapse"
          id="navbarNav"
        >

          <ul className="navbar-nav">


            <li className="nav-item">

              <Link
                className="nav-link text-white"
                to="/panel"
              >
                <FaHome className="me-2"/>
                Inicio
              </Link>

            </li>



            <li className="nav-item">

              <Link
                className="nav-link text-white"
                to="/persona"
              >
                <FaUsers className="me-2"/>
                Miembros
              </Link>

            </li>



            <li className="nav-item">

              <Link
                className="nav-link text-white"
                to="/categoria"
              >
                <FaTags className="me-2"/>
                Categorías
              </Link>

            </li>



            <li className="nav-item">

              <Link
                className="nav-link text-white"
                to="/gasto"
              >
                <FaWallet className="me-2"/>
                Gastos
              </Link>

            </li>



            <li className="nav-item">

              <Link
                className="nav-link text-white"
                to="/balance"
              >
                <FaBalanceScale className="me-2"/>
                Balance
              </Link>

            </li>


          </ul>

        </div>



        <div className="text-end text-white ms-auto">

          <div className="fw-bold">
            SplitHome
          </div>


          <div style={{fontSize:"13px"}}>

            {fecha.toLocaleTimeString()}
            {" — "}
            {fecha.toLocaleDateString()}

          </div>

        </div>


      </div>

    </nav>

  )

}


export default Menu