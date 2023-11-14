import "./NavbarStyle.css"
import Search from "../assets/search.png"

const Navbar = () => {
  return (
    <nav className="navbar-items">
      <a href="/" className="navbar-title">
      <img src={Search} className="logo" />Reverse Search Image</a>
    </nav>
  )
}

export default Navbar