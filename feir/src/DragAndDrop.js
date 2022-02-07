import React, { useRef } from 'react';
import { Button } from 'reactstrap';
import axios from 'axios';
import Cropper from "react-cropper";
import "cropperjs/dist/cropper.css";

const DragAndDrop = props => {

    const { data, dispatch } = props;
    let myScreenW = 0.7*window.screen.width
    let myScreenH = myScreenW*0.6
    

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
      
      }
    };
    

    const handleResponse = (resData) => {
      dispatch({ type: 'ADD_RES_TO_LIST', resData });
    }

    const handleSubmit = e => {
      console.log("Handling submit")
      if (data?.fileList.length === 0) return;
      
      var file = null
   
      if (typeof(data.fileList[0]) === 'string') {
         file = dataURLtoFile(data.fileList[0], data.originName)
      }
      else file = data.fileList[0]

      const formData = new FormData();
      formData.append('image', file);
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
   }


  const cropperRef = useRef(null);
//   const [src, setSrc] = useState(null)
//   const [cropFile, setCropFile] = useState(null)
//   const onCrop = () => {
//     const imageElement = cropperRef?.current;
//     const cropper = imageElement?.cropper;
//     var newImageFile = cropper.getCroppedCanvas().toDataURL();
//     setCropFile(newImageFile)
//     setSrc(newImageFile);
//   };

  const handleCropClick = e => {
      //dispatch({ type: 'ADD_CROP_TO_LIST', cropFile});
      const imageElement = cropperRef?.current;
      const cropper = imageElement?.cropper;
      var cropFile = cropper.getCroppedCanvas().toDataURL();
      dispatch({ type: 'ADD_CROP_TO_LIST', cropFile});
  }

  const dataURLtoFile = (dataUrl, fileName) => {
      var arr = dataUrl.split(','), mime = arr[0].match(/:(.*?);/)[1],
      bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
      while(n--){
      u8arr[n] = bstr.charCodeAt(n);
      }
      return new File([u8arr], fileName, {type:mime});
   }

   const handleClear = (e) => {
      // dispatch({ type: 'CLEAR'});
      window.location.href='/'
   }

    return (
        <>
        <div className='container' style={{width: '100%', maxWidth: 'none'}}>
           <div className='row justify-content-center'>
               <div className='col-auto'>
                  <div className={data.inDropZone ? 'drag-drop-zone inside-drag-area' : 'drag-drop-zone'}
                     onDrop={e => handleDrop(e)}
                     onDragOver={e => handleDragOver(e)}
                     onDragEnter={e => handleDragEnter(e)}
                     onDragLeave={e => handleDragLeave(e)}
                     accept="image/*"
                  >
                     {  
                        (data?.displayList?.length > 0) ? <div style={{maxHeight: 400, maxWidth: 360, marginTop: 'auto', marginBottom:'auto', marginLeft:'auto', marginRight:'auto'}}>
                           <img src={data.displayList[0]} width="80%" height="80%" style={{maxHeight: 400, maxWidth: 360, marginTop: 'auto', marginBottom:'auto', marginLeft:'auto', marginRight:'auto'}} /> 
                        </div>: <></>
                     }
                     <p>(Drag files here to upload or replace)</p>
                  </div>

                  <input type="file" id="input" name='image-upload' accept="image/*" onChange={e => handleChooseFile(e)} />
                  <div className='label'>
                     <label htmlFor="input" className='image-upload'>
                           <p type="button" className="btn btn-primary mt-3">
                              Choose file
                           </p>
                     </label>
                  </div>
                  <Button color="primary" className='mb-3'
                     onClick={e => handleSubmit(e)}
                  >
                     Search
                  </Button>
               </div>
               {/* <div className='col-auto'>
               </div> */}
            <div className='row justify-content-center'>
                  <div className='crop-zone' style={{height: "100%", width: "100%", maxHeight: myScreenH, maxWidth: myScreenW, marginTop: 'auto', marginBottom:'auto', marginLeft:'auto', marginRight:'auto'}}>
                     {  
                        (data?.displayList?.length > 0) ? 
                        <>
                           <Cropper
                              src={data.displayList[0]}
                              style={{ height: "100%", width: "100%", maxHeight: myScreenH, maxWidth: myScreenW, marginTop: 'auto', marginBottom:'auto', marginLeft:'auto', marginRight:'auto' }}
                              // Cropper.js options
                              initialAspectRatio={1/1}
                              guides={true}
                              // crop={onCrop}
                              ref={cropperRef}
                           />
                        {/* <div className="col-6" style={{maxHeight: 400, maxWidth: 350, marginTop: 'auto', marginBottom:'auto', marginLeft:'auto', marginRight:'auto'}}>
                           <img src={src} style={{ height: "80%", width: "80%", maxHeight: 400, maxWidth: 350}}/>
                        </div> */}
                        </>
                        : <></>
                     }
                  </div>
                    <div>
                    <Button color="primary" className='m-3'onClick={e => handleCropClick(e)}>Crop</Button>

                    <Button color="primary" className='m-3'onClick={e => handleClear(e)}>Clear and Reset</Button>
                    </div>
               </div>      
           </div>
        </div>
        
        </>
    );

  
};
export default DragAndDrop;