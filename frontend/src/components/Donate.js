import React, { useState } from 'react';
import './Auth.css'; // Using the same CSS for consistency

const Donate = () => {
  // State to store form input values
  const [donorName, setDonorName] = useState('');
  const [donorEmail, setDonorEmail] = useState('');
  const [donationAmount, setDonationAmount] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:8000/api/donate/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: donorName,
          email: donorEmail,
          amount: donationAmount,
        }),
      });

      if (response.ok) {
        alert('Donation successful! Thank you for your support.');
        setDonorName('');
        setDonorEmail('');
        setDonationAmount('');
      } else {
        console.error('Failed to process donation');
      }
    } catch (error) {
      console.error('Error processing donation:', error);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-form">
        <h2>Donate</h2>
        <p>We appreciate your support! Please fill in the form below to donate.</p>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Your Name"
            className="auth-input"
            value={donorName}
            onChange={(e) => setDonorName(e.target.value)}
            required
          />
          <input
            type="email"
            placeholder="Your Email"
            className="auth-input"
            value={donorEmail}
            onChange={(e) => setDonorEmail(e.target.value)}
            required
          />
          <input
            type="number"
            placeholder="Donation Amount"
            className="auth-input"
            value={donationAmount}
            onChange={(e) => setDonationAmount(e.target.value)}
            required
          />
          <button type="submit" className="auth-button">Donate</button>
        </form>
      </div>
    </div>
  );
};

export default Donate;
