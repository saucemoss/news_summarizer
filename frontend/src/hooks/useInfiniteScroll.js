import { useEffect, useRef, useState } from 'react';

const useInfiniteScroll = (callback, hasMore, articles) => {
  const observer = useRef();
  const [isIntersecting, setIsIntersecting] = useState(false);
  const triggerRef = useRef(null);

  useEffect(() => {
    const options = {
      root: null,
      rootMargin: '20px',
      threshold: 0.1
    };

    observer.current = new IntersectionObserver(([entry]) => {
      console.log('Intersection observed:', entry.isIntersecting);
      console.log('Has more items:', hasMore);
      setIsIntersecting(entry.isIntersecting);
      if (entry.isIntersecting && hasMore) {
        console.log('Triggering load more...');
        callback();
      }
    }, options);

    return () => {
      if (observer.current) {
        observer.current.disconnect();
      }
    };
  }, [callback, hasMore]);

  // Separate effect to handle observation
  useEffect(() => {
    if (observer.current && triggerRef.current) {
      console.log('Starting to observe trigger element');
      observer.current.observe(triggerRef.current);
    } else {
      console.log('Waiting for trigger element or observer to be ready');
    }
  }, [articles]); // Re-run when articles change

  return [triggerRef, isIntersecting];
};

export default useInfiniteScroll; 