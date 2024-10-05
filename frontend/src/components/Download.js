import React from 'react';

const Download = () => {
  const downloadUrl = 'http://127.0.0.1:8000/download-software/'; // Your backend API endpoint for downloading the file

  const handleDownload = () => {
    window.location.href = downloadUrl; // Trigger the file download by setting the window location to the download URL
  };

  return (
    <div className="download-container">
      <h2>Download Clipboard Manager</h2>
      <p>Click the button below to download the Clipboard Manager software:</p>
      <button onClick={handleDownload} className="download-button">
        Download
      </button>
    </div>
  );
};

export default Download;
