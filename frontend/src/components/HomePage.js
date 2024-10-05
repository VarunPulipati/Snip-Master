import React from 'react';
import './HomePage.css'; // CSS file for styling

const HomePage = () => {
  return (
    <div className="home">
      <header className="home-header">
        <h1>Welcome to SnipMaster</h1>
        <p>Your ultimate snippet management tool. Create, store, and manage your code snippets efficiently, enhancing your coding workflow and productivity.</p>
      </header>
      
      <section className="home-content">
        <article className="features">
          <h2>Features</h2>
          <ul>
            <li>Easy to use interface</li>
            <li>Search and paste previous copy entries</li>
            <li>Keep multiple computer's clipboards in sync</li>
            <li>Data is encrypted when sent over the network</li>
            <li>Accessed from tray icon or global hot key</li>
            <li>Select entry by double click, enter key, or drag drop</li>
            <li>Display thumbnail of copied images in list</li>
            <li>Full Unicode support (display foreign characters)</li>
            <li>UTF-8 support for language files (create language files in any language)</li>
            <li>Uses SQLite database (<a href="https://www.sqlite.org">www.sqlite.org</a>)</li>
          </ul>
        </article>

        <article className="installation">
          <h2>Installation</h2>
          <ol>
            <li>Download the installer from our website.</li>
            <li>Run the installer and follow the on-screen instructions.</li>
            <li>Once installed, launch SnipMaster from your desktop or start menu.</li>
            <li>Follow the setup wizard to configure your preferences.</li>
            <li>For detailed commands and usage, refer to the documentation.</li>
          </ol>
        </article>

        <article className="commands">
          <h2>Commands</h2>
          <ul>
            <li><b>Ctrl + C + {`{identifier}`}:</b> Copy selected text or item to clipboard</li>
            <li><b>Ctrl + X + {`{identifier}`}:</b> Cut selected text or item to clipboard</li>
            <li><b>Ctrl + V + {`{identifier}`}:</b> Paste content from clipboard</li>
          </ul>
          <p><strong>NOTE:</strong> Customize these commands in your settings.</p>
        </article>
      </section>
    </div>
  );
};

export default HomePage;
