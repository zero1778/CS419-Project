import React from 'react';
import Gallery from "react-photo-gallery";
//import cat2 from "./gallery/cat2.jpg"
import { Navbar, Nav, Container, NavLink } from 'reactstrap';

const GalleryResult  = props => {

  const photoList = ['cat1.jpg', 'cat2.jpg', 'dog1.jpg', 'dog2.jpg', 'house1.jpg', 'house2.jpg']
  const getPhoto = () => {
    var temp = []

    for (var i=0; i < photoList.length; ++i) {
      temp.push({
        src: "gallery/"+photoList[i],
        width: 1,
        height: 1,
        alt: photoList[i]
      })
    }
    for (var t=0; t < 10; ++t) {
      for (i=0; i < photoList.length; ++i) {
        temp.push(temp[i])
      }
    }


    return temp;

    // return [{
    //   src: "gallery/cat2.jpg",
    //   width: 1,
    //   height: 1,
    //   alt: 'cat2'
    // }]
  }

  const photos = getPhoto()

  return (
    <>
      <Navbar className='bg-primary variant-dark'>
          <NavLink className='AppName' href='/'><h1>FEIR</h1></NavLink>
      </Navbar>
      <p>"Don't come here and start asking to crop, but crop your mind before coming here" - The author</p>
      {photos.length === 0 ? <h1>No result found !!!</h1> : <Gallery photos={photos} />}
    </>
);

}

export default GalleryResult;