import "./NavbarStyle.css"
import Search from "../assets/search.png"

const Navbar = () => {
  return (
    <nav className="navbar-items">
      <a href="/" className="navbar-title">
      <img src={Search} className="logo" />Reverse Search Image</a>
      <div className="links">
        <a href="/About" className="navbar-link">About Us</a>
        <a href="/How" className="navbar-link">How to Use</a>
      </div>
    </nav>
  )
}

export default Navbar