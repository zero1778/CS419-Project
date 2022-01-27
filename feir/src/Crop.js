import React, { useRef } from "react";
import Cropper from "react-cropper";
import "cropperjs/dist/cropper.css";
import { useState } from "react/cjs/react.development";
import { Button } from "reactstrap";

const Demo = () => {
  const cropperRef = useRef(null);
  const [src, setSrc] = useState(null)
  const onCrop = () => {
    const imageElement = cropperRef?.current;
    const cropper = imageElement?.cropper;
    var x = cropper.getCroppedCanvas().toDataURL();
    setSrc(x);
  };

  return (
    <>
    <div className="container">
      <div className="row">
        <Cropper
          src="./gallery/cat2.jpg"
          style={{ height: 500, width: "100%" }}
          // Cropper.js options
          initialAspectRatio={16 / 9}
          guides={false}
          crop={onCrop}
          ref={cropperRef}
        />
      </div>
      <div className="row">
        <div className="col-3">
          <Button color="primary">Crop</Button>
        </div>
        <div className="col">
          <img src={src} alt='Croped img' style={{ height: 50, width: "100%" }}/>
        </div>
      </div>
    </div>
    </>  
  );
};

export default Demo