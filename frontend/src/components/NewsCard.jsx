const NewsCard = ({ title, summary, processed_at }) => {
  // Format the date
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="bg-gray-800 p-4 rounded-lg shadow-md cursor-pointer hover:bg-gray-700 transition-colors">
      <h3 className="text-lg font-semibold text-white mb-2">{title}</h3>
      <p className="text-gray-300 text-sm mb-2">{summary}</p>
      <p className="text-gray-400 text-xs">{formatDate(processed_at)}</p>
    </div>
  );
};

export default NewsCard;