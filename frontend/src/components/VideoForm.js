// src/components/VideoForm.js

import React, { useState } from 'react';

function isValidYouTubeUrl(url) {
  const regex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[\w\-]{11}$/;
  return regex.test(url);
}

function VideoForm({ onSubmit }) {
  const [videoUrl, setVideoUrl] = useState('');
  const [modelChoice, setModelChoice] = useState('openai-gpt-3.5-turbo');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submissionMessage, setSubmissionMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!isValidYouTubeUrl(videoUrl)) {
      alert('Please enter a valid YouTube video URL.');
      return;
    }

    setIsSubmitting(true);
    setSubmissionMessage(`Model selected: ${modelChoice}`);
    onSubmit(videoUrl, modelChoice);
    setIsSubmitting(false);
  };

  return (
    <form onSubmit={handleSubmit} className="p-4">
      <label className="block mb-2 text-lg font-medium">
        Enter YouTube Video URL:
      </label>
      <input
        type="text"
        value={videoUrl}
        onChange={(e) => setVideoUrl(e.target.value)}
        className="border rounded w-full p-2 mb-4"
        placeholder="https://www.youtube.com/watch?v=..."
        required
      />
      <label className="block mb-2 text-lg font-medium">
        Select Language Model:
      </label>
      <select
        value={modelChoice}
        onChange={(e) => setModelChoice(e.target.value)}
        className="border rounded w-full p-2 mb-4"
      >
        <option value="gpt-4o">OpenAI GPT-4 Optimized</option>
        <option value="gpt-4o-mini">OpenAI GPT-4 Mini</option>
        <option value="gpt-3.5-turbo-0125">OpenAI GPT-3.5 Turbo 0125</option>
        <option value="gpt-3.5-turbo">OpenAI GPT-3.5 Turbo</option>
        <option value="claude-3-5-sonnet-20240620">Anthropic Claude 3.5 Sonnet</option>
        <option value="claude-3-opus-20240229">Anthropic Claude 3 Opus</option>
        <option value="claude-3-sonnet-20240229">Anthropic Claude 3 Sonnet</option>
        <option value="claude-3-haiku-20240307">Anthropic Claude 3 Haiku</option>
      </select>
      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded"
        disabled={isSubmitting}
      >
        {isSubmitting ? 'Processing...' : 'Process Video'}
      </button>
      {submissionMessage && (
        <p className="mt-4 text-green-600">{submissionMessage}</p>
      )}
    </form>
  );
}

export default VideoForm;
