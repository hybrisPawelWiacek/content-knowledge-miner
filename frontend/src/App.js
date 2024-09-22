// src/App.js

import React, { useState } from 'react';
import Header from './components/Header';
import VideoForm from './components/VideoForm';
import Results from './components/Results';
import { ClipLoader } from 'react-spinners';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [testMessage, setTestMessage] = useState('');

  const handleSubmit = async (videoUrl, modelChoice) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch('/process_video', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ video_url: videoUrl, model: modelChoice }),
      });

      if (!response.ok) {
        throw new Error('Failed to process video');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleTestConnection = () => {
    setTestMessage('');
    fetch('/test', {
      method: 'GET',
    })
      .then((response) => response.json())
      .then((data) => {
        setTestMessage(data.message);
      })
      .catch((err) => {
        setTestMessage('Connection test failed: ' + err.message);
      });
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      <div className="container mx-auto">
        <VideoForm onSubmit={handleSubmit} />
        <button
          onClick={handleTestConnection}
          className="mt-4 bg-green-500 text-white px-4 py-2 rounded"
        >
          Test Connection
        </button>
        {testMessage && (
          <div className="mt-2 p-2 bg-blue-100 text-blue-700 rounded">
            {testMessage}
          </div>
        )}
        {loading && (
          <div className="p-4 flex items-center">
            <ClipLoader size={35} color={"#123abc"} loading={loading} />
            <p className="ml-2">Processing...</p>
          </div>
        )}
        {error && (
          <div className="p-4 text-red-600">
            <p><strong>Error:</strong> {error}</p>
          </div>
        )}
        {results && <Results data={results} />}
      </div>
    </div>
  );
}

export default App;
