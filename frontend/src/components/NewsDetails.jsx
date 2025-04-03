import { useState } from "react";

const NewsDetails = ({ article }) => {
  if (!article) return null;

  // Parse insights JSON if it's a string
  const parsedInsights = typeof article.insights === 'string' 
    ? JSON.parse(article.insights)
    : article.insights;

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg sticky top-6 max-h-[calc(100vh-3rem)] overflow-y-auto">
      {article.image_url && (
        <div className="mb-6">
          <img 
            src={article.image_url} 
            alt={article.title}
            className="w-full h-64 object-cover rounded-lg shadow-md"
          />
        </div>
      )}
      <h2 className="text-2xl font-bold text-white mb-4">{article.title}</h2>
      <p className="text-gray-300 mb-4">{article.summary}</p>
      <div className="text-gray-300 mb-4">
        {Array.isArray(parsedInsights) && parsedInsights.map((insight, index) => (
          <div key={index} className="mb-2">
            {typeof insight === 'object' ? (
              Object.entries(insight).map(([key, value]) => (
                <p key={key} className="ml-4">• {value}</p>
              ))
            ) : (
              <p>• {insight}</p>
            )}
          </div>
        ))}
      </div>
      <a 
        href={article.url} 
        target="_blank" 
        rel="noopener noreferrer"
        className="text-blue-400 hover:text-blue-300"
      >
        Read full article →
      </a>
    </div>
  );
};

export default NewsDetails;
