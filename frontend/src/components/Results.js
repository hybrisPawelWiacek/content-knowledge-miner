// src/components/Results.js

import React from 'react';

function Results({ data }) {
  if (!data) return null;

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-2">Summary:</h2>
      <p className="mb-4">{data.summary.summary_text}</p>

      <h2 className="text-xl font-bold mb-2">Metadata:</h2>
      <ul className="list-disc list-inside mb-4">
        <li><strong>Title:</strong> {data.metadata.title}</li>
        <li><strong>Description:</strong> {data.metadata.description}</li>
        <li><strong>Published At:</strong> {data.metadata.published_at}</li>
        <li><strong>Duration:</strong> {data.metadata.duration}</li>
        <li><strong>View Count:</strong> {data.metadata.view_count}</li>
        <li><strong>Like Count:</strong> {data.metadata.like_count}</li>
        <li><strong>Comment Count:</strong> {data.metadata.comment_count}</li>
      </ul>

      {data.summary.key_topics && data.summary.key_topics.length > 0 && (
        <>
          <h2 className="text-xl font-bold mb-2">Key Topics:</h2>
          <ul className="list-disc list-inside mb-4">
            {data.summary.key_topics.map((topic, index) => (
              <li key={index}>{topic}</li>
            ))}
          </ul>
        </>
      )}
      <a
        href={`https://www.youtube.com/watch?v=${data.video_id}`}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-600 underline"
      >
        View Original Video
      </a>
    </div>
  );
}

export default Results;
