import React, { useState } from 'react';
import { Button } from 'reactstrap';
import axios from 'axios';

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

       //const existingFiles = data.fileList.map(f => f.name)
       //files = files.filter(f => !existingFiles.includes(f.name))
       
       dispatch({ type: 'ADD_FILE_TO_LIST', files });
       e.dataTransfer.clearData();
       dispatch({ type: 'SET_DROP_DEPTH', dropDepth: 0 });
       dispatch({ type: 'SET_IN_DROP_ZONE', inDropZone: false });
      
       setDefaultMsg(files[0].name + '\n (Drag files here to replace)')
      }
    };
    
    const handleResponse = (resData) => {
      dispatch({ type: 'ADD_RES_TO_LIST', resData });
    }

    const handleSubmit = e => {
      console.log("Handling submit")
      if (data?.fileList.length === 0) return;
      
      var file = data.fileList[0]
      const formData = new FormData();
      formData.append('image', file, file.name);

      axios.post('http://localhost:8000/search', formData)
      .then(res => {
        console.log('captured data');
        handleResponse(res.data);
      })
      .catch(error => console.log(error))

   //    fetch("http://localhost:8000/search", {
   //      method: "POST",
   //      // headers: { "Content-Type": "application/json" },
   //      body: formData
   //  })
   //  .then(res => console.log(res.json()))
   //  .catch(error => console.log(error))
      
      console.log("Done")
   }
   
   const handleChooseFile = e => {
      if (e.target.files.length === 0) return
      var files = e.target.files
      dispatch({ type: 'ADD_FILE_TO_LIST', files});

      setDefaultMsg(files[0].name + '\n (Drag files here to replace)')
   }

    return (
        <>
        <div className={data.inDropZone ? 'drag-drop-zone inside-drag-area' : 'drag-drop-zone'}
          onDrop={e => handleDrop(e)}
          onDragOver={e => handleDragOver(e)}
          onDragEnter={e => handleDragEnter(e)}
          onDragLeave={e => handleDragLeave(e)}
        >
         {  
            (data?.fileList?.length > 0) ? <img src={URL.createObjectURL(data.fileList[0])} width="400" height="400" /> : <></>
         }
        <p>{defaultMsg}</p>
        </div>

        <input type="file" id="input" name='image-upload' accept="image/*" onChange={e => handleChooseFile(e)} />
        <div className='label'>
           <label htmlFor="input" className='image-upload'>
               <p type="button" className="btn btn-primary mt-3">
                  Choose file
               </p>
           </label>
        </div>
        <Button color="primary"
          onClick={e => handleSubmit(e)}
        >
           Search
        </Button>
        </>
    );

  
};
export default DragAndDrop;