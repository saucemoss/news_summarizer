import React, { useState, useEffect, useCallback } from 'react';
import NewsCard from './components/NewsCard';
import NewsDetails from './components/NewsDetails';
import SkeletonCard from './components/SkeletonCard';
import useInfiniteScroll from './hooks/useInfiniteScroll';

function App() {
  const [articles, setArticles] = useState([]);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(0);
  const [loadingMore, setLoadingMore] = useState(false);

  const fetchArticles = useCallback(async (pageNum = 0) => {
    console.log('Fetching articles for page:', pageNum);
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/articles?skip=${pageNum * 10}&limit=10`);
      if (!response.ok) {
        throw new Error('Failed to fetch articles');
      }
      const data = await response.json();
      
      console.log('Received articles:', {
        count: data.articles.length,
        hasMore: data.has_more,
        total: data.total
      });
      
      if (pageNum === 0) {
        setArticles(data.articles);
      } else {
        setArticles(prev => [...prev, ...data.articles]);
      }
      
      setHasMore(data.has_more);
      setPage(pageNum);
      setLoading(false);
      setLoadingMore(false);
    } catch (err) {
      console.error('Error fetching articles:', err);
      setError(err.message);
      setLoading(false);
      setLoadingMore(false);
    }
  }, []);

  useEffect(() => {
    fetchArticles(0);
  }, [fetchArticles]);

  const loadMore = useCallback(() => {
    console.log('loadMore called', { loadingMore, hasMore, page });
    if (!loadingMore && hasMore) {
      console.log('Starting to load more articles...');
      setLoadingMore(true);
      fetchArticles(page + 1);
    } else {
      console.log('Skipping load more:', { loadingMore, hasMore });
    }
  }, [fetchArticles, loadingMore, hasMore, page]);

  const [triggerRef] = useInfiniteScroll(loadMore, hasMore, articles);

  const handleArticleClick = async (article) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/articles/${article.id}`);
      if (!response.ok) {
        throw new Error('Failed to fetch article details');
      }
      const fullArticle = await response.json();
      setSelectedArticle(fullArticle);
    } catch (err) {
      setError(err.message);
    }
  };

  if (error) {
    return (
      <div className="min-h-screen bg-gray-900 text-white p-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-red-500">Error: {error}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto p-4">
        <h1 className="text-3xl font-bold mb-8">News Summarizer</h1>
        
        <div className="flex gap-4">
          {/* Left side - Article List */}
          <div className="w-1/2 space-y-4">
            {loading ? (
              <SkeletonCard />
            ) : (
              <>
                {articles.map((article) => (
                  <div key={article.id} onClick={() => handleArticleClick(article)}>
                    <NewsCard
                      title={article.title}
                      summary={article.summary}
                      processed_at={article.processed_at}
                    />
                  </div>
                ))}
                {/* Loading indicator */}
                {loadingMore && (
                  <div className="flex justify-center py-4">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
                  </div>
                )}
                {/* Infinite scroll trigger */}
                <div ref={triggerRef} className="h-4" />
              </>
            )}
          </div>

          {/* Right side - Article Details */}
          <div className="w-1/2">
            {selectedArticle ? (
              <NewsDetails article={selectedArticle} />
            ) : (
              <p className="text-gray-400 text-center">
                Select an article to view details
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
