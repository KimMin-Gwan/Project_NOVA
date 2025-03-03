// import { useEffect, useRef } from "react";

// export default function useInfiniteScroll() {
//   const target = useRef(null);
//   const observerRef = useRef(null);

//   useEffect(() => {
//     observerRef.current = new IntersectionObserver((entries) => {
//       entries.forEach((entry) => {
//         if (!entry.isIntersecting) return;
//         if (isLoading) return;

//         // fetchAllFeed();
//         fetchPlusData();
//         if (type === "bias") {
//           fetchBiasCategoryData();
//         }
//       });
//     });

//     if (target.current) {
//       observerRef.current.observe(target.current);
//     }

//     return () => {
//       if (observerRef.current && target.current) {
//         observerRef.current.unobserve(target.current);
//         observerRef.current.disconnect();
//       }
//     };
//   }, [isLoading, nextData]);
// }
