import { useEffect, useState, useRef } from "react"
import "./ResultPage.css"
import Result from "./dataset.json"
import Result2 from "./dataset2.json"
import Images from "../Components/Images"
import axios from "axios"


export const ResultPage = (props, props2) => {
  const { toggle } = props;
  const { Res1 } = props2;
  const [files, setFiles] = useState("");
  const [fileLength, setFileLength] = useState("");
  const hiddenFileInput = useRef(null);

  const handleClick = event => {
    hiddenFileInput.current.click();
  }

  const handleChange = event => {
    console.log(event.target.files);
    setFiles(event.target.files);
    setFileLength(Result);
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
    <>
    <div>
    {Result ? (
        toggle ? (
          <p className="result-tag">Result : {Object.keys(Result).length} results in 0 seconds.</p>
        ) : (
          <p className="result-tag">Result : {Object.keys(Result2).length} results in 0 seconds.</p>
        )
      ) : (
        <p>Result :</p>
      )}
    </div>
      <div className="result-container">
        {Result ? (
        toggle ? (
          <Images data = {Result}></Images>
        ) : (
          <Images data = {Result2}></Images>
        )
      ) : (
        <p>No Images</p>
      )}
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
    </>
  )
}