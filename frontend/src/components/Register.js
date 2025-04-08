import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom'; // Uncomment if navigation is needed after registration

const Register = () => {
  const [user, setUser] = useState({
    username: '',
    email: '',
    password: '',
  });
  // const navigate = useNavigate(); // Uncomment if navigation is needed

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUser({ ...user, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Here you would make a POST request to your backend endpoint to register the user
    // On success, you might want to navigate to the login page or dashboard
    // navigate('/login');
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" name="username" value={user.username} onChange={handleChange} placeholder="Username" required />
        <input type="email" name="email" value={user.email} onChange={handleChange} placeholder="Email" required />
        <input type="password" name="password" value={user.password} onChange={handleChange} placeholder="Password" required />
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;
