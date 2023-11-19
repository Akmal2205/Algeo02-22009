import Navbar from "./Components/Navbar"
import { Routes, Route } from "react-router-dom"
import { MainPage } from "./Pages/MainPage"
import { HowPage } from "./Pages/HowPage"
import { AboutPage } from "./Pages/AboutPage"

function App() {
  return (<div className="Page">
    <Navbar />
      <Routes>
        <Route path="/" element={<MainPage></MainPage>}></Route>
        <Route path="/About" element={<AboutPage/>}></Route>
        <Route path="/How" element={<HowPage/>}></Route>
      </Routes>
    </div>
  )
}

export default App