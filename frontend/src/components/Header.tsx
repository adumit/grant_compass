import React from 'react';
import './css/Header.css';

const Header = () => {
  return (
    <header className="header">
      <h1 className="header-title">Grant Compass</h1>
      <nav className="header-nav">
        <a href="#what-is-grant-compass">What is Grant Compass?</a>
        <a href="#about-us">About Us</a>
        <a href="#contact">Contact</a>
      </nav>
    </header>
  );
};

export default Header;
