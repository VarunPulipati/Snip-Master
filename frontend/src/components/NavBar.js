import React from 'react';
import { Link } from 'react-router-dom';
import './NavBar.css'; // Corresponding CSS file for NavBar styling

const NavBar = () => {
  const downloadUrl = 'http://example.com/downloads/my-clipboard-manager-setup.exe';

  return (
    <nav className="navbar">
      <Link to="/" className="nav-brand">SNIPMASTER</Link>
      <div className="nav-links">
      <Link to="/donate" className="nav-item">Donate</Link>
        <Link to="/account" className="nav-item">Account</Link>
        <a href={downloadUrl} className="nav-item" download>
          Download
        </a>
        <Link to="/contact" className="nav-item">Contact</Link>
      </div>
    </nav>
  );
};

export default NavBar;
