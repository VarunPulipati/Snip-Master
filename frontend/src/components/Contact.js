import React, { useState } from 'react';
import './Auth.css'; // Shared CSS for styling

const Contact = () => {
  const [contactName, setContactName] = useState('');
  const [contactEmail, setContactEmail] = useState('');
  const [contactMessage, setContactMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:8000/api/contact/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: contactName,
          email: contactEmail,
          message: contactMessage,
        }),
      });

      if (response.ok) {
        alert('Message sent successfully');
        setContactName('');
        setContactEmail('');
        setContactMessage('');
      } else {
        console.error('Failed to send message');
      }
    } catch (error) {
      console.error('Error submitting contact form:', error);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-form">
        <h2>Contact Us</h2>

        {/* Contact Information */}
        <div className="contact-info">
          <p><strong>Email:</strong> support@snipmaster.com</p>
          <p><strong>Phone:</strong> +1 234 567 890</p>
          <p><strong>Address:</strong> 123 SnipMaster St., Tech City, TX 75001</p>
        </div>

        {/* Contact Form */}
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Your Name"
            className="auth-input"
            value={contactName}
            onChange={(e) => setContactName(e.target.value)}
            required
          />
          <input
            type="email"
            placeholder="Your Email"
            className="auth-input"
            value={contactEmail}
            onChange={(e) => setContactEmail(e.target.value)}
            required
          />
          <textarea
            placeholder="Your Message"
            className="auth-input"
            rows="4"
            value={contactMessage}
            onChange={(e) => setContactMessage(e.target.value)}
            required
          ></textarea>
          <button type="submit" className="auth-button">Send Message</button>
        </form>
      </div>
    </div>
  );
};

export default Contact;
