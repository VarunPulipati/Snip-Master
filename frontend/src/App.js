import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Account from './components/Account'; // Import Account component
import Contact from './components/Contact'; // Import Contact component
import Donate from './components/Donate';   // Import Donate component
import NavBar from './components/NavBar';   // Import NavBar if needed
import HomePage from './components/HomePage';
import Download from './components/Download';

function App() {
  return (
    <Router>
      <NavBar /> {/* Ensure NavBar is added for consistent navigation */}
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/account" element={<Account />} />
        <Route path="/download" element={<Download />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/donate" element={<Donate />} />
        {/* Add other routes as necessary */}
      </Routes>
    </Router>
  );
}

export default App;

