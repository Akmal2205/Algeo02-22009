import { useEffect, useState, useRef } from "react"
import "./ResultPage.css"
import Result from "./dataset.json"
import Images from "../Components/Images"
import { useDropzone } from 'react-dropzone'


export const ResultPage = () => {
  const [files, setFiles] = useState("");
  const hiddenFileInput = useRef(null);

  const handleClick = event => {
    hiddenFileInput.current.click();
  }

  const handleChange = event => {
    console.log(event.target.files);
    setFiles(event.target.files);
};

  return (
    <div className="result-container">
        {Result? <Images data = {Result}></Images>: <p>No Images</p>}
      <div className="result-button-section">
        <div className="data-button" onClick={handleClick}>
        <input hidden 
          multiple
          type="file" 
          accept="image/*"
          onChange={handleChange}
          ref={hiddenFileInput}/>
        <p className="upload-button">Upload Dataset</p>
        </div>
      </div>
    </div>
  )
}