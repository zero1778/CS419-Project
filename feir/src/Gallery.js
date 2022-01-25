import React from 'react';
import Gallery from "react-photo-gallery";
import { Navbar, Nav, Container, NavLink, Modal } from 'reactstrap';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';

const GalleryResult  = props => {
  const { displayList } = props;

  const formatPhoto = (photoList) => {
    var temp = []

    for (var i=0; i < photoList.length; ++i) {
      temp.push({
        src: "http://localhost:8000/data/oxbuild_images/"+photoList[i],
        width: 1,
        height: 1,
        alt: photoList[i]
      })
    }

    return temp;
  }

  const [photos, setPhotos] = useState(formatPhoto(displayList));

  useEffect(() => {
    setPhotos(formatPhoto(displayList))
  }, [displayList]);
  
  let navigate = useNavigate();

  const handleReturn = (e) => {
      e.preventDefault();
      e.stopPropagation();

      navigate('/');
  }

  const handleClickView = e => {
    console.log(e.target.src)
    setViewDetail(e.target.src)
    setModal(true)
  }

  const handleCloseView = e => {
    setViewDetail(null)
  }
  // var dummies = formatPhoto()

  const [viewDetail, setViewDetail] = useState(null)
  const [modal, setModal] = useState(false)
  const toggle = e => {
    setModal(!modal)
  }
  return (
    <>
      <Navbar className='bg-primary variant-dark'>
          <NavLink className='AppName' href='#' onClick={e => handleReturn(e)}><h1>FEIR</h1></NavLink>
      </Navbar>
      <p>"Don't come here and start asking to crop, but crop your mind before coming here" - The author</p>
      {photos.length === 0 ? <h1>No result found !!!</h1> : <Gallery photos={photos} onClick={e => handleClickView(e)}/>}
      <Modal isOpen={modal} toggle={e => toggle(e)} centered onClosed={e => handleCloseView(e)}>
        <img src={viewDetail} width="100%" height="100%" /> 
      </Modal>
    </>
);

}

export default GalleryResult;