const NewsCard = ({ topic, summary, onClick, selected }) => {
  return (
    <div
      className={`bg-gray-800 text-gray-300 p-4 rounded-lg shadow-md border transition-all cursor-pointer
        hover:border-blue-300
        ${selected ? "border-blue-200 ring-1 ring-blue-300" : "border-gray-700"}`}
      onClick={onClick}
    >
      <h2 className="text-lg font-bold">{topic}</h2>
      <p className="text-gray-400 mt-2 line-clamp-2">{summary}</p>
    </div>
  );
};

export default NewsCard;