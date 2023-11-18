import Navbar from "../Components/Navbar"
import "./MainPage.css"
import Icon from "../assets/resolution.png"
import { useState, useRef } from "react"
import axios from 'axios'
import { ResultPage } from "./ResultPage"
import Result from "./dataset.json"
import Result2 from "./dataset2.json"
import Images from "../Components/Images"


export const MainPage = () => {
    const [colorResult, setColorResult] = useState([]);
    const [textureResult, setTextureResult] = useState([]);
    const [search, setSearch] = useState(false);
    const [file, setFile] = useState("");
    const [files, setFiles] = useState("");
    const [fileName, setFileName] = useState("No inserted picture");
    const hiddenFileInput = useRef(null);
    const hiddenFileInput2 = useRef(null);
    const [toggleState, setToggleState] = useState(false);

    const handleClick = event => {
        hiddenFileInput.current.click();
    }

    const handleClick2 = event => {
      hiddenFileInput2.current.click();
    }

    const handleSwitch = event => {
        {toggleState? setToggleState(false): setToggleState(true)}
    }

    const handleUpload = async () => {
        try {
          const formData = new FormData();
          formData.append('image', file);
    
          const response = await axios.post('http://127.0.0.1:8000/api/upload_image/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
    
          console.log('Image uploaded successfully:', response.data);
          // Handle response if needed
        } catch (error) {
          console.error('Error uploading image:', error);
          // Handle errors if needed
        }
    };

    const handleUpload2 = async () => {
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

    const handleChange = event => {
        console.log(event.target.files);
        setFile(event.target.files[0]);
        setFileName(event.target.files[0].name);
    };

    const handleChange2 = event => {
      console.log(event.target.files);
      setFiles(event.target.files);
  };
  

  const fetchDataColor = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/color/');
      setColorResult(response.data);
    } catch (error) {
      console.error('Error fetching color data:', error);
    }
  };

  // const fetchDataTexture = async () => {
  //   try {
  //     const response = await axios.get('http://127.0.0.1:8000/api/texture/');
  //     setTextureResult(response.data);
  //   } catch (error) {
  //     console.error('Error fetching texture data:', error);
  //   }
  // };

  const handleSearch = async () => {
    await fetchDataColor();
    // await fetchDataTexture();
    setSearch(true);
    // You can perform any other logic here after fetching data
  };


  return (
    <>
    <div className="main-container">{/* Bagian Main/Search */}
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
                    <div className="upload-button" onClick={handleUpload}>
                        Upload
                    </div>
                </div>
                <div className="bot-button">
                <div className="search-button" onClick={handleSearch}>
                        Search
                    </div>
                    <div className="toggle-button" onClick={handleSwitch}>
                        {toggleState? <p className="toggle-tag">Texture</p>:<p className="toggle-tag">Colour</p>}
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
    <div>{/* Bagian Results */}
    { search ? (
        toggleState ? (
          <p className="result-tag">Result : {Result2.length} results in 0 seconds.</p>
        ) : (
          <p className="result-tag">Result : {colorResult.length} results in 0 seconds.</p>
        )
      ) : (
        <p className="result-tag">Result :</p>
      )}
    </div>
      <div className="result-container">
        {search ? (
        toggleState ? (
          <Images data = {Result2}></Images>
        ) : (
          <Images data = {colorResult}></Images>
        )
      ) : (
        <p>No Images</p>
      )}
      <div className="result-button-section">
        <div className="data-button" onClick={handleClick2}>
          <input hidden 
            multiple
            type="file" 
            id = "ctrl"
            webkitdirectory = ""
            directory=""
            accept="image/*"
            onChange={handleChange2}
            ref={hiddenFileInput2}/>
          <p className="data-button">Insert Dataset</p>
        </div>
        <div className="data-button" onClick={handleUpload2}>
          <p className="data-button">Upload Dataset</p>
        </div>
      </div>
    </div>
    </>
  )
}
