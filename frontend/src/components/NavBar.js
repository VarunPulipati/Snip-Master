import React from 'react';
import { Link } from 'react-router-dom';
import './NavBar.css'; // Make sure to create a corresponding CSS file

const NavBar = () => {
  const downloadUrl = 'http://example.com/downloads/my-clipboard-manager-setup.exe';

  return (
    <nav className="navbar">
      <Link to="/" className="nav-brand">My Clipboard Manager</Link>
      <div className="nav-links">
      <a href={downloadUrl} className="nav-item" download>
        Download
      </a>
        <Link to="/login" className="nav-item">Login</Link>
        <Link to="/register" className="nav-item">Register</Link>
        {/* Add more navigation links as needed */}
      </div>
    </nav>
  );
};

export default NavBar;
