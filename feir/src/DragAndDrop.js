import React, { useState } from 'react';
import { Button } from 'reactstrap';
import { Link } from 'react-router-dom';
import { useNavigate as navigate } from 'react-router-dom';

const DragAndDrop = props => {

    const { data, dispatch } = props;

    const [defaultMsg, setDefaultMsg] = useState("Drag files here to upload");


    const handleDragEnter = e => {
       e.preventDefault();
       e.stopPropagation();

       dispatch({ type: 'SET_DROP_DEPTH', dropDepth: data.dropDepth + 1 });
    };

    const handleDragLeave = e => {
       e.preventDefault();
       e.stopPropagation();

       dispatch({ type: 'SET_DROP_DEPTH', dropDepth: data.dropDepth - 1 });
       if (data.dropDepth > 0) return dispatch({ type: 'SET_IN_DROP_ZONE', inDropZone: false })
    };

    const handleDragOver = e => {
       e.preventDefault();
       e.stopPropagation();

       e.dataTransfer.dropEffect = 'copy';
       dispatch({ type: 'SET_IN_DROP_ZONE', inDropZone: true });
    };
    
    const handleDrop = e => {
       e.preventDefault();
       e.stopPropagation();

       let files = [...e.dataTransfer.files];
  
       if (files && files.length > 0) {
       const existingFiles = data.fileList.map(f => f.name)
       //files = files.filter(f => !existingFiles.includes(f.name))
    
       dispatch({ type: 'ADD_FILE_TO_LIST', files });
       e.dataTransfer.clearData();
       dispatch({ type: 'SET_DROP_DEPTH', dropDepth: 0 });
       dispatch({ type: 'SET_IN_DROP_ZONE', inDropZone: false });
      
       if (files.length > 0) setDefaultMsg(files[0].name + '\n (Drag files here to replace)')
       else setDefaultMsg('Drag files here to upload')
  }
    };
    
    const handleSubmit = e => {
      console.log("Handling submit")
   
      /*
      TODO: send request and recieve list of image name
      */
      
      console.log("Done")

      //navigate("//result")
      window.location.href='/result'
   }

    return (
        <>
        <div className={data.inDropZone ? 'drag-drop-zone inside-drag-area' : 'drag-drop-zone'}
          onDrop={e => handleDrop(e)}
          onDragOver={e => handleDragOver(e)}
          onDragEnter={e => handleDragEnter(e)}
          onDragLeave={e => handleDragLeave(e)}
        >
         {/* {data?.files?.length > 0 ? msg = data.files[0].name : msg = defaultMsg} */}
         {
            (data?.fileList?.length > 0) ? <img src={URL.createObjectURL(data.fileList[0])} width="400" height="400" /> : <></>
         }
        <p>{defaultMsg}</p>
        </div>
         {/* {
            (data?.fileList?.length > 0) ? <img src={URL.createObjectURL(data.fileList[0])} width="300" height="300" /> : <></>
         } */}
        
        <Button className='mt-3' color="primary"
          onClick={e => handleSubmit(e)}
        >
           Search
        </Button>
        </>
    );

  
};
export default DragAndDrop;