import { useEffect, useState, useRef } from "react"
import "./ResultPage.css"
import Result from "./dataset.json"
import Images from "../Components/Images"
import axios from "axios"


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

  // handle upload dataset api
  const handleUpload = async () => {
    try {
      const formData = new FormData();
      for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
      }

      const response = await axios.post('http://localhost:8000/api/upload_folder/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Files uploaded successfully:', response.data);
      // Handle response if needed
    } catch (error) {
      console.error('Error uploading files:', error);
      // Handle errors if needed
    }
  };
  

  return (
    <div className="result-container">
        {Result? <Images data = {Result}></Images>: <p>No Images</p>}
      <div className="result-button-section">
        <div className="data-button" onClick={handleClick}>
          <input hidden 
            multiple
            type="file" 
            id = "ctrl"
            webkitdirectory = ""
            directory=""
            accept="image/*"
            onChange={handleChange}
            ref={hiddenFileInput}/>
          <p className="data-button">Insert Dataset</p>
        </div>
        <div className="data-button" onClick={handleUpload}>
          <p className="data-button">Upload Dataset</p>
        </div>
      </div>
    </div>
  )
}