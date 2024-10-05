import React, { useState } from 'react';
import './Account.css'; // Shared CSS for all authentication components
import { Navigate } from "react-router-dom";


const Register = () => {
  const [user, setUser] = useState({
    username: '',
    email: '',
    password: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUser({ ...user, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        const response = await fetch('http://127.0.0.1:8000/api/signup/', {  // Correct URL for backend signup
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(user),
        });

        if (response.ok) {
            console.log('User registered successfully');
            Navigate('/login');  // Optionally redirect to the login page after successful registration
        } else {
            console.error('Failed to register:', response.statusText);
        }
    } catch (error) {
        console.error('Error during registration:', error);
    }
};


  return (
    <div className="auth-container">
      <div className="auth-form">
        <h2>Register</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="username"
            value={user.username}
            onChange={handleChange}
            placeholder="Username"
            className="auth-input"
            required
          />
          <input
            type="email"
            name="email"
            value={user.email}
            onChange={handleChange}
            placeholder="Email"
            className="auth-input"
            required
          />
          <input
            type="password"
            name="password"
            value={user.password}
            onChange={handleChange}
            placeholder="Password"
            className="auth-input"
            required
          />
          <button type="submit" className="auth-button">Register</button>
        </form>
        <p>
          Already have an account? <a href="/login" className="auth-link">Login here</a>
        </p>
      </div>
    </div>
  );
};

export default Register;
