import React from 'react';
import { Navbar, NavLink } from 'reactstrap';

const myNavbar= () =>{
  return (
    <Navbar className='bg-primary variant-dark'>
          <NavLink className='AppName' href='/'><h1>FEIR</h1></NavLink>
    </Navbar>
  );
}
export default myNavbar;