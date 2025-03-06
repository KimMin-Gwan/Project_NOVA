import { useEffect, useRef } from "react";

export default function useIntersectionObserver(callback, options = {}, hasMore) {
  const targetRef = useRef(null);

  useEffect(() => {
    if (!hasMore) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          callback();
        }
      });
    }, options);

    // observerRef.current = new IntersectionObserver((entries) => {
    //   entries.forEach((entry) => {
    //     if (!entry.isIntersecting) return;
    //     if (isLoading) return;

    //     // fetchAllFeed();
    //     fetchPlusData();
    //     if (type === "bias") {
    //       fetchBiasCategoryData();
    //     }
    //   });
    // });

    if (targetRef.current) {
      observer.observe(targetRef.current);
    }

    return () => {
      if (targetRef.current) {
        observer.unobserve(targetRef.current);
        observer.disconnect();
      }
    };
  }, [callback, options, hasMore]);

  return targetRef;
}
