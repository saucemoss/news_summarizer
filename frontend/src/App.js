import React, { useEffect, useState } from "react";
import NewsCard from "./components/NewsCard";
import NewsDetails from "./components/NewsDetails";
import SkeletonCard from "./components/SkeletonCard";
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [detailsLoading, setDetailsLoading] = useState(false); // For details loading
  const [selectedTopicTitle, setSelectedTopicTitle] = useState(null); // Track selected topic title


// Define fetchTopics function
const fetchTopics = async () => {
setLoading(true);
try {
  const response = await axios.get(`${API_BASE_URL}/topic_list`);
  setTopics(response.data);
} catch (error) {
  console.error("Error fetching topics:", error);
}
setLoading(false);
};

useEffect(() => {
  const storedTopics = sessionStorage.getItem("topics");
  if (storedTopics) {
    setTopics(JSON.parse(storedTopics));
    setLoading(false);
  } else {
    fetchTopics();
  }
}, []);

useEffect(() => {
  if (topics.length > 0) {
    sessionStorage.setItem("topics", JSON.stringify(topics));
  }
}, [topics]);


// Function to fetch details when a topic is clicked
const handleTopicClick = async (urls, title) => {
  setSelectedTopicTitle(title); // Store selected topic title
  setDetailsLoading(true);

  try {
    const response = await axios.post(`${API_BASE_URL}/summary`, { urls });
    setSelectedTopic(response.data);
  } catch (error) {
    console.error("Error fetching topic details:", error);
  }

  setDetailsLoading(false);
};

return (
    <div className="min-h-screen bg-black text-white p-6 flex justify-center">
    <div className="w-[90%] max-w-7xl flex gap-6">
    {/* LEFT: News List */}
    <div className="w-2/5 bg-gray-900 p-6 rounded-xl shadow-lg">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold text-center">News</h1>
      </div>

      <div className="grid gap-4">
        {loading
          ? [...Array(1)].map((_, index) => <SkeletonCard key={index} />)
          : topics.map((topic) => (
              <NewsCard
                topic={topic.title}
                summary={topic.summary}
                onClick={() => handleTopicClick(topic.links, topic.title)}
                selected={selectedTopicTitle === topic.title} // Compare with stored title
              />
            ))}
      </div>
    </div>
{/* RIGHT: News Details */}
<div className="w-3/5 bg-gray-900 p-6 rounded-xl shadow-lg">
  <h1 className="text-2xl font-bold text-center">Summarizer</h1>
  <br />

  {detailsLoading ? ( // Show Skeleton while details are loading
    <SkeletonCard />
  ) : selectedTopic ? (
    <NewsDetails {...selectedTopic} onClose={() => setSelectedTopic(null)} />
  ) : (
    <p className="text-gray-400 text-center">
      Select a news topic to see details here.
    </p>
  )}
</div>
  </div>
</div>
  );
}

export default App;
