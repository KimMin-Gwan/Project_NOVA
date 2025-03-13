import TestRef from "../../component/TestRef";

export default function TestPage() {
  return <TestRef />;
}

// import { useEffect, useState } from "react";
// import { useSearchParams } from "react-router-dom";

// import useBiasStore from "../../stores/BiasStore/useBiasStore.js";

// import { getModeClass } from "./../../App.js";

// import filter_icon from "./../../img/filter.svg";

// // 컴포넌트
// import Feed from "./../../component/feed";
// import BiasBoxes from "../../component/BiasBoxes.js";
// import FilterModal from "../../component/FilterModal/FilterModal.js";
// import SearchBox from "../../component/SearchBox.js";
// import KeywordBox from "../../component/keyword/KeywordBox.js";
// import CategoryModal from "../../component/CategoryModal/CategoryModal.js";
// import NoneFeed from "../../component/NoneFeed/NoneFeed.js";
// import NavBar from "../../component/NavBar/NavBar.js";
// import Header from "../../component/Header/Header.js";
// import StoryFeed from "../../component/StoryFeed/StoryFeed.js";
// import LoadingPage from "../LoadingPage/LoadingPage.js";

// // 스타일
// import "@toast-ui/editor/dist/toastui-editor-viewer.css";
// import style from "./../FeedList/FeedHashList.module.css";

// // 커스텀 훅
// import useDragScroll from "../../hooks/useDragScroll.js";
// import useIntersectionObserver from "../../hooks/useIntersectionObserver.js";
// import useFetchFeedList from "../../hooks/useFetchFeedList.js";

// export default function TestPage() {
//   // url 파라미터 가져오기
//   const [params] = useSearchParams();
//   const type = params.get("type");
//   const brightModeFromUrl = params.get("brightMode");

//   // 상태 관리
//   let { biasList } = useBiasStore();
//   const [isSameTag, setIsSameTag] = useState(true);
//   let [biasId, setBiasId] = useState("");
//   let [board, setBoard] = useState("자유게시판");
//   let [isClickedFetch, setIsClickedFetch] = useState(false);

//   // 필터 모달 및 카테고리 모달
//   let [isFilterClicked, setIsFilterClicked] = useState(false);
//   let [isOpendCategory, setIsOpendCategory] = useState(false);

//   const initialMode = brightModeFromUrl || localStorage.getItem("brightMode") || "bright"; // URL에서 가져오고, 없으면 로컬 스토리지에서 가져옴

//   const [mode, setMode] = useState(initialMode);
//   // 필터 카테고리 , 게시글 종류 초기 설정
//   let [filterCategory, setFilterCategory] = useState(
//     JSON.parse(localStorage.getItem("board")) || [""]
//   );
//   let [filterFclass, setFilterFclass] = useState(JSON.parse(localStorage.getItem("content")) || "");

//   // 드래그 기능
//   const { scrollRef, hasDragged, dragHandlers } = useDragScroll();
//   // 피드 관련 요청 커스텀 훅
//   const { feedData, isLoading, hasMore, fetchFeedList, fetchPlusFeedList, fetchFeedWithTag } =
//     useFetchFeedList(type, biasId, isClickedFetch, filterCategory, filterFclass);

//   // 데이터 로드
//   useEffect(() => {
//     fetchFeedList();
//   }, [type]);

//   // 모드 체인지
//   useEffect(() => {
//     localStorage.setItem("brightMode", mode);
//   }, [mode]);

//   let bids = biasList.map((item) => {
//     return item.bid;
//   });

//   useEffect(() => {
//     if (bids.length > 0 && !biasId) {
//       setBiasId(bids[0]);
//     }
//   }, [bids]);

//   const loadMoreCallBack = () => {
//     if (!isLoading && hasMore) {
//       fetchPlusFeedList();
//     }
//   };

//   // 무한 스크롤
//   const targetRef = useIntersectionObserver(loadMoreCallBack, { threshold: 0.5 }, hasMore);

//   // useEffect(() => {
//   //   if (isSameTag) {
//   //     setHasMore(true);
//   //   } else {
//   //     setHasMore(false);
//   //   }
//   // }, [isSameTag]);

//   // 이벤트 핸들러
//   function onClickTag(tag) {
//     fetchFeedWithTag(tag);
//   }

//   function onClickCategory() {
//     setIsOpendCategory(!isOpendCategory);
//   }

//   function onClickFilterButton() {
//     setIsFilterClicked(!isFilterClicked);
//   }

//   if (isFilterClicked) {
//     document.body.style.overflow = "hidden";
//   } else {
//     document.body.style.overflow = "auto";
//   }

//   //   // if (isLoading) {
//   //   //   return <LoadingPage />;
//   //   // }

//   return (
//     <div className={`all-box ${style["all_container"]}`}>
//       <div className={`${style["container"]} ${style[getModeClass(mode)]}`}>
//         <Header />
//         {type === "bias" && (
//           <div className={style["bias-section"]}>
//             <BiasBoxes setBiasId={setBiasId} fetchBiasCategoryData={fetchFeedList} />
//             <h4>스토리 게시판</h4>
//             <div
//               ref={scrollRef}
//               className={style["story_container"]}
//               onMouseDown={dragHandlers.onMouseDown}
//               onMouseUp={dragHandlers.onMouseUp}
//               onMouseMove={dragHandlers.onMouseMove}
//             >
//               <div className={style["story_wrapper"]}>
//                 {feedData.map((feed, i) => {
//                   return (
//                     <StoryFeed
//                       key={`story_${feed.feed.fid}`}
//                       feedData={feed}
//                       hasDragged={hasDragged}
//                     />
//                   );
//                 })}
//               </div>
//             </div>

//             <div className={style["category-info"]}>
//               <p>모든 게시글</p>
//               <p className={style["category_change"]} onClick={onClickCategory}>
//                 카테고리 변경
//               </p>
//             </div>

//             {isOpendCategory && (
//               <CategoryModal
//                 SetIsOpen={setIsOpendCategory}
//                 onClickCategory={onClickCategory}
//                 biasId={biasId}
//                 board={board}
//                 setBoard={setBoard}
//               />
//             )}
//           </div>
//         )}
//         {type === "all" && (
//           <div className={style["search-section"]}>
//             <SearchBox />
//             <div className={style["search-filter"]}>
//               <button onClick={onClickFilterButton}>
//                 필터
//                 <span className={style["filter-icon"]}>
//                   <img src={filter_icon} alt="filter" />
//                 </span>
//               </button>
//             </div>
//           </div>
//         )}

//         {(type === "today" || type === "weekly") && (
//           <div className={style["keyword-section"]}>
//             <KeywordBox
//               type={type}
//               title={type === "today" ? "인기 급상승" : "많은 사랑을 받은"}
//               subTitle={type === "today" ? "오늘의 키워드" : "이번주 키워드"}
//               onClickTagButton={onClickTag}
//               fetchData={fetchFeedList}
//               setIsSameTag={setIsSameTag}
//             />
//           </div>
//         )}

//         <div className={feedData.length > 0 ? style["scroll-area"] : style["none_feed_scroll"]}>
//           {feedData.length > 0 ? (
//             feedData.map((feed, i) => {
//               return (
//                 <Feed
//                   key={`feed_${feed.feed.fid}`}
//                   className={`${style["feed-box"]} ${style[getModeClass(mode)]}`}
//                   feed={feed.feed}
//                   //   setFeedData={setFeedData}
//                 ></Feed>
//               );
//             })
//           ) : (
//             <NoneFeed />
//           )}
//           <div ref={targetRef} style={{ height: "1px" }}></div>
//           {isLoading && <p>loading...</p>}
//           {isFilterClicked && (
//             <FilterModal
//               onClickFilterButton={onClickFilterButton}
//               setFilterCategory={setFilterCategory}
//               setFilterFclass={setFilterFclass}
//               fetchAllFeed={fetchFeedList}
//               // onClickApplyButton1={onClickApplyButton1}
//             />
//           )}
//         </div>
//       </div>
//       <NavBar />
//     </div>
//   );
// }
