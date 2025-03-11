import React, { useEffect, useState } from "react";
import NewsCard from "./components/NewsCard";
import NewsDetails from "./components/NewsDetails";
import SkeletonCard from "./components/SkeletonCard";
import ThemeToggle from "./components/ThemeToggle";

function App() {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTopic, setSelectedTopic] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/news")
      .then(response => response.json())
      .then(data => {
        setTopics(data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching news:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-black text-white p-6 flex justify-center">
  <div className="w-[90%] max-w-7xl flex gap-6">
    {/* LEFT: News List */}
    <div className="w-2/5 bg-gray-900 p-6 rounded-xl shadow-lg">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">News Summarizer</h1>
      </div>

      <div className="grid gap-4">
        {loading
          ? [...Array(4)].map((_, index) => <SkeletonCard key={index} />)
          : topics.map((topic) => (
              <NewsCard
                key={topic.name}
                topic={topic.name}
                summary={topic.summary}
                onClick={() => setSelectedTopic(topic)}
              />
            ))}
      </div>
    </div>

    {/* RIGHT: News Details */}
    <div className="w-3/5 bg-gray-900 p-6 rounded-xl shadow-lg">
      {selectedTopic ? (
        <NewsDetails {...selectedTopic} onClose={() => setSelectedTopic(null)} />
      ) : (
        <p className="text-gray-400 text-center">Select a news topic to see details here.</p>
      )}
    </div>
  </div>
</div>
  );
}

export default App;
