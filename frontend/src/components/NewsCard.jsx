const NewsCard = ({ topic, summary, onClick }) => {
  return (
    <div 
      className="bg-gray-800 text-white p-4 rounded-lg shadow-md border hover:border-blue-300 transition-all cursor-pointer"
      onClick={onClick}
    >
      <h2 className="text-lg font-bold">{topic}</h2>
      <p className="text-gray-400 mt-2 line-clamp-2">{summary}</p>
    </div>
  );
};

export default NewsCard;