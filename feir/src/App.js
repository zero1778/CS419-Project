import logo from './logo.svg';
import './App.css';
import DragAndDrop from './DragAndDrop';
import GalleryResult from './Gallery';
import React from 'react';
import { Routes, Route } from "react-router-dom";
import myNavbar from './myNavbar';
import { Navbar, Nav, Container, NavLink } from 'reactstrap';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';

function App() {

  const reducer = (state, action) => {
    switch (action.type) {
      case 'SET_DROP_DEPTH':
        return { ...state, dropDepth: action.dropDepth }
      case 'SET_IN_DROP_ZONE':
        return { ...state, inDropZone: action.inDropZone };
      case 'ADD_FILE_TO_LIST':
        return { ...state, fileList: (action.files)};
      case 'ADD_RES_TO_LIST':
        return { ...state, resData: (action.resData)};
      default:
        return state;
    }
  };

  const [data, dispatch] = React.useReducer(
    reducer, { dropDepth: 0, inDropZone: false, fileList: [], resData: []}
  )

  
  let navigate = useNavigate();

  useEffect(() => {
    if (data.resData.length > 0) navigate("/result")

  }, [data.resData]);

  
  
  return (
    <div className="App">
        <Routes>
          <Route exact path="/" element={<>
              <p>"Don't come here and start asking to crop, but crop your mind before coming here" - The author</p>
              <h1>FEIR</h1>
              <DragAndDrop data={data} dispatch={dispatch} />
            </> } />
          <Route exact path="/result" element={<GalleryResult displayList={data.resData} />} />          
        </Routes>
    </div>
  );
}

export default App;


// <div className="App">
      //   <GalleryResult />
      //   <h1>FEIR</h1>
      //   <DragAndDrop data={data} dispatch={dispatch} />
      //   {/* <ol className="dropped-files">
      //     {data.fileList.map(f => {
      //       return (
      //         <div>
      //             <img src={URL.createObjectURL(f)} width="300" height="300" />
      //         </div>
      //       )
      //     })}
      //   </ol> */}
      // </div>