import "./About.css"
import Syarafi from "../assets/syarafi.jpg"
import Fabian from "../assets/fabian.jpg"
import Cupi from "../assets/cupi.jpg"


export const AboutPage = () => {
  return (
    <div className="about-container">
        <div className="bio-container">
            <div className="bio">
               <div className="profile-pic">
                    <img src={Syarafi} className="pp" />
                </div> 
                <div className="desc">
                    Frontend Contributor
                    <a href="https://instagram.com/syarafi_akmal?igshid=MTNiYzNiMzkwZA==" className="nama" target="_blank">Muhammad Syarafi Akmal</a>
                    <br />
                </div>
            </div>
            <div className="bio">
                <div className="profile-pic">
                    <img src={Cupi} className="pp" />
                </div>
                <div className="desc">
                    Backend Contributor
                    <a href="https://instagram.com/rafiyusuf_?igshid=MmVlMjlkMTBhMg==" className="nama" target="_blank">Muhammad Yusuf Rafi</a>
                    <p>CBIR Color</p>
                </div>
            </div>
            <div className="bio">
                <div className="profile-pic">
                    <img src={Fabian} className="pp" />
                </div>
                <div className="desc">
                    Backend Contributor
                    <a href="https://instagram.com/fabianradenta?igshid=YTQwZjQ0NmI0OA%3D%3D&utm_source=qr" className="nama" target="_blank">Fabian Radenta Bangun</a>
                    <p>CBIR Texture</p>
                </div>
            </div>
        </div>
    </div>
  )
}
