import Navbar from "../Components/Navbar"
import "./MainPage.css"
import Icon from "../assets/resolution.png"
import { useState, useRef } from "react"

export const MainPage = () => {
    const [file, setFile] = useState("");
    const [fileName, setFileName] = useState("No inserted picture");
    const hiddenFileInput = useRef(null);
    const [toggleState, setToggleState] = useState(false);

    const handleClick = event => {
        hiddenFileInput.current.click();
    }

    const handleSwitch = event => {
        {toggleState? setToggleState(false): setToggleState(true)}
    }

    const handleChange = event => {
        console.log(event.target.files);
        setFile(event.target.files[0]);
        setFileName(event.target.files[0].name);
    };

  return (
    <div className="main-container">
        <div className="navbar">
            <Navbar></Navbar>
        </div>
        <div className="content-container">
            <div className="left">
                <div className="top-button">
                    <div className="insert-button" onClick={handleClick}>
                            Insert an Image
                            <input 
                                type="file" 
                                accept="image/*"
                                onChange={handleChange}
                                ref={hiddenFileInput}
                                style={{display:'none'}}
                            />
                    </div>
                </div>
                <div className="bot-button">
                    <div className="toggle-button" onClick={handleSwitch}>
                        {toggleState? <p className="toggle-tag">Texture</p>:<p className="toggle-tag">Colour</p>}
                    </div>
                    <div className="search-button">
                        Search
                    </div>
                </div>
            </div>
            <div className="right">
            <div className="pic">
                    {file ? <img src={URL.createObjectURL(file)} className="icon" /> : <img src={Icon} className="icon" />}
                </div>
                <p className="picture-tag">{fileName}</p>
            </div>
        </div>
    </div>
  )
}
