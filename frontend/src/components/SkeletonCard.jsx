const SkeletonCard = () => {
  return (
    <div className="bg-gray-800 p-4 rounded-xl shadow-lg animate-pulse border border-gray-500">
      <div className="h-6 w-3/4 bg-gray-600 rounded"></div>
      <div className="h-4 w-full bg-gray-600 rounded mt-2"></div>
      <div className="h-4 w-2/3 bg-gray-600 rounded mt-2"></div>
    </div>
  );
};

export default SkeletonCard;