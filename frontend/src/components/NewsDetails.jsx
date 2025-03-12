import { useState } from "react";
import { FaChevronDown, FaChevronUp } from "react-icons/fa"; // Correct import path


const NewsDetails = ({ topic, insights, full_text, links, onClose }) => {
  const [isTextVisible, setIsTextVisible] = useState(false);

  const toggleTextVisibility = () => {
    setIsTextVisible(!isTextVisible);
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold mt-4 mb-2">{topic}</h3>
      {/* Insights Section */}
      <h3 className="text-lg font-semibold mt-4">Insights:</h3>
      <ul className="list-disc list-inside text-gray-300">
        {insights.length > 0 &&
          Object.values(insights[0]).map((insight, index) => (
            <li key={index}>{insight}</li>
          ))}
      </ul>

      {/* Full Text Section with collapsible functionality */}
      <h3 className="text-lg font-semibold mt-4 mb-2">Full Text:</h3>
      {/* Toggle button for showing/hiding full text */}
      <button
        className="flex items-center text-blue-500 hover:underline"
        onClick={toggleTextVisibility}
      >
        {/* Show appropriate arrow based on visibility */}
        {isTextVisible ? (
          <FaChevronUp className="mr-2" />
        ) : (
          <FaChevronDown className="mr-2" />
        )}
        {isTextVisible ? "Hide Text" : "Show Full Text"}
      </button>

      {/* Conditionally render the full text */}
      {isTextVisible && (
        <ul className="text-gray-400 mt-2">
          <li>{full_text}</li>
        </ul>
      )}

      {/* Articles Section */}
      <h3 className="text-lg font-semibold mt-4">Articles:</h3>
      {links.map((link, index) => (
        <a
          key={index}
          href={link.url}
          target="_blank"
          rel="noopener noreferrer"
          className="block text-blue-400 hover:underline mb-2 break-words"
        >
          {link}
        </a>
      ))}

      {/* Close Button */}
      <button
        onClick={onClose}
        className="mt-4 px-4 py-2 bg-blue-900 text-white rounded-lg"
      >
        Close
      </button>
    </div>
  );
};

export default NewsDetails;
