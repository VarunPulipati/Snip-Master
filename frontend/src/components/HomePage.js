import React from 'react';
import './HomePage.css'; // Make sure to create a corresponding CSS file for styling

const HomePage = () => {
  return (
    <div className="home">
      <header className="home-header">
        <h1>Welcome to My Clipboard Manager</h1>
        <p>Manage your clipboard efficiently and securely.</p>
      </header>
      <section className="home-content">
        <article>
          <h2>Features</h2>
          <p>Store your clipboard history, organize your clips into slots, and sync across devices.</p>
        </article>
        <article>
          <h2>Security</h2>
          <p>All your clipboard data is encrypted and stored securely.</p>
        </article>
        <article>
          <h2>Get Started</h2>
          <p>Register for an account today and streamline your workflow.</p>
        </article>
      </section>
    </div>
  );
};

export default HomePage;
