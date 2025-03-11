const NewsDetails = ({ name, summary, insights, articles, onClose }) => {
  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold">{name}</h2>
      <p className="text-gray-400 mt-2">{summary}</p>

      <h3 className="text-lg font-semibold mt-4">Insights:</h3>
      <ul className="list-disc list-inside text-gray-400">
        {insights.map((insight, index) => (
          <li key={index}>{insight}</li>
        ))}
      </ul>

      <h3 className="text-lg font-semibold mt-4">Articles:</h3>
      {articles.map((article, index) => (
        <a key={index} href={article.url} target="_blank" rel="noopener noreferrer" className="block text-blue-400 hover:underline">
          {article.url}
        </a>
      ))}

      <button onClick={onClose} className="mt-4 px-4 py-2 bg-blue-900 text-white rounded-lg">
        Close
      </button>
    </div>
  );
};

export default NewsDetails;
