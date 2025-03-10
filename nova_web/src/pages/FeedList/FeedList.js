import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import postApi from "../../services/apis/postApi.js";
import {
  fetchAllFeedList,
  fetchDateFeedList,
  fetchFeedListWithTag,
  fetchBiasFeedList,
} from "../../services/getFeedApi.js";
import useBiasStore from "../../stores/BiasStore/useBiasStore.js";

import { getModeClass } from "./../../App.js";

import filter_icon from "./../../img/filter.svg";

import Feed from "./../../component/feed";
import BiasBoxes from "../../component/BiasBoxes.js";
import FilterModal from "../../component/FilterModal/FilterModal.js";
import SearchBox from "../../component/SearchBox.js";
import KeywordBox from "../../component/keyword/KeywordBox.js";
import CategoryModal from "../../component/CategoryModal/CategoryModal.js";
import NoneFeed from "../../component/NoneFeed/NoneFeed.js";
import NavBar from "../../component/NavBar/NavBar.js";
import Header from "../../component/Header/Header.js";
import StoryFeed from "../../component/StoryFeed/StoryFeed.js";

import "@toast-ui/editor/dist/toastui-editor-viewer.css";
import style from "./FeedHashList.module.css";
import useDragScroll from "../../hooks/useDragScroll.js";
import LoadingPage from "../LoadingPage/LoadingPage.js";
import HEADER from "../../constant/header.js";
import useIntersectionObserver from "../../hooks/useIntersectionObserver.js";
import useFetchFeedList from "../../hooks/useFetchFeedList.js";

export default function FeedList() {
  // url 파라미터 가져오기
  const [params] = useSearchParams();
  const type = params.get("type");
  const brightModeFromUrl = params.get("brightMode");

  // 전역 상태 관리
  let { biasList } = useBiasStore();
  // const { feedDatas, isLoadings, nextKey } = useFetchFeedList(type);

  // 드래그 기능
  const { scrollRef, hasDragged, dragHandlers } = useDragScroll();

  let [isFilterClicked, setIsFilterClicked] = useState(false);
  let [isOpendCategory, setIsOpendCategory] = useState(false);

  let [isLoading, setIsLoading] = useState(true);
  let [feedData, setFeedData] = useState([]);
  let [nextData, setNextData] = useState(-1);

  const [isSameTag, setIsSameTag] = useState(true);
  let [biasId, setBiasId] = useState();
  let [board, setBoard] = useState("자유게시판");

  const initialMode =
    brightModeFromUrl || localStorage.getItem("brightMode") || "bright"; // URL에서 가져오고, 없으면 로컬 스토리지에서 가져옴
  const [mode, setMode] = useState(initialMode);

  const [hasMore, setHasMore] = useState(true);

  let [filterCategory, setFilterCategory] = useState(
    JSON.parse(localStorage.getItem("board")) || [""]
  );
  let [filterFclass, setFilterFclass] = useState(
    JSON.parse(localStorage.getItem("content")) || ""
  );
  let [isClickedFetch, setIsClickedFetch] = useState(false);

  // 모드 체인지
  useEffect(() => {
    localStorage.setItem("brightMode", mode);
  }, [mode]);

  let bids = biasList.map((item) => {
    return item.bid;
  });

  useEffect(() => {
    if (bids.length > 0 && !biasId) {
      setBiasId(bids[0]);
    }
  }, [bids]);

  const loadMoreCallBack = () => {
    if (!isLoading && hasMore) {
      if (type === "bias") {
        fetchBiasPlusCategoryData();
      } else {
        fetchPlusData();
      }
    }
  };

  // 주제별 피드 리스트
  async function fetchBiasCategoryData(bid) {
    setIsLoading(true);

    const data = await fetchBiasFeedList(bid, bids, board, (nextData = -1));
    console.log("first bias data", data);
    setFeedData(data.body.send_data);
    setNextData(data.body.key);
    setHasMore(data.body.send_data.length > 0);
    setIsLoading(false);
  }

  async function fetchBiasPlusCategoryData() {
    setIsLoading(true);
    const data = await fetchBiasFeedList(biasId, bids, board, nextData);
    console.log("first111 bias data", data);
    setFeedData((prevData) => [...prevData, ...data.body.send_data]);
    setNextData(data.body.key);
    setHasMore(data.body.send_data.length > 0);
    setIsLoading(false);
  }

  useEffect(() => {
    if (type === "bias") {
      fetchBiasCategoryData();
    }
  }, []);

  useEffect(() => {
    setFeedData([]);
    setNextData(-1);
  }, [biasId, board, type]);

  function onClickApplyButton1() {
    setNextData(-1);
  }

  async function fetchAllFeed(clickedFetch) {
    let updatedNextData = -1;

    //  만약 적용 버튼을 누르면 -1로 세팅
    if (clickedFetch) {
      updatedNextData = -1;
      setNextData(-1);
    }
    // 그게 아닌 상황에서는 기존의 nextData 를 사용
    else {
      updatedNextData = nextData;
    }

    if (type === "all" || isClickedFetch) {
      const data = await fetchAllFeedList(
        updatedNextData,
        filterCategory,
        filterFclass
      );
      console.log("ffff", data);
      setFeedData(data.body.send_data);
      setNextData(data.body.key);
      setIsLoading(false);
    }
  }

  // 오늘, 주간 피드 받기
  async function fetchData() {
    if (type === "today" || type === "weekly") {
      const data = await fetchDateFeedList(type);
      setFeedData(data.body.send_data);
      setNextData(data.body.key);
      setIsLoading(false);
    } else if (type === "all") {
      fetchAllFeed(false);
    }
  }

  // 태그 클릭 시 데이터 받기
  async function fetchFeedWithTag(tag) {
    let time;
    if (type === "today") {
      time = "day";
    } else if (type === "weekly") {
      time = "weekly";
    }
    const data = await fetchFeedListWithTag(tag, time);
    setFeedData(data.body.send_data);
    setIsLoading(false);
  }

  useEffect(() => {
    if (isSameTag) {
      setHasMore(true);
    } else {
      setHasMore(false);
    }
  }, [isSameTag]);

  function onClickTag(tag) {
    fetchFeedWithTag(tag);
  }

  // 데이터 더 받기
  async function fetchFeedListType(
    fetchFunction,
    type,
    nextData,
    filterCategory,
    filterFclass
  ) {
    const data = await fetchFunction(
      type,
      nextData,
      filterCategory,
      filterFclass
    );

    setFeedData((prevData) => {
      const newData = [...prevData, ...data.body.send_data];
      return newData;
    });
    setNextData(data.body.key);
    setIsLoading(false);
    setHasMore(data.body.send_data.length > 0);
  }

  // 데이터 더 받기
  async function fetchPlusData() {
    if (type === "today" || type === "weekly") {
      await fetchFeedListType(fetchDateFeedList, type, nextData);
    } else if (type === "all" || isClickedFetch) {
      await fetchFeedListType(
        fetchAllFeedList,
        nextData,
        filterCategory,
        filterFclass
      );
    }
  }
  // 무한 스크롤
  const targetRef = useIntersectionObserver(
    loadMoreCallBack,
    { threshold: 0.5 },
    hasMore
  );

  useEffect(() => {
    fetchData();

    return () => {
      setFeedData([]);
    };
  }, []);

  function onClickCategory() {
    setIsOpendCategory(!isOpendCategory);
  }

  function onClickFilterButton() {
    setIsFilterClicked(!isFilterClicked);
  }

  if (isFilterClicked) {
    document.body.style.overflow = "hidden";
  } else {
    document.body.style.overflow = "auto";
  }

  // if (isLoading) {
  //   return <LoadingPage />;
  // }

  return (
    <div className={`all-box ${style["all_container"]}`}>
      <div className={`${style["container"]} ${style[getModeClass(mode)]}`}>
        <Header />
        {type === "bias" && (
          <div className={style["bias-section"]}>
            <BiasBoxes
              setBiasId={setBiasId}
              fetchBiasCategoryData={fetchBiasCategoryData}
            />
            <h4>스토리 게시판</h4>
            <div
              ref={scrollRef}
              className={style["story_container"]}
              onMouseDown={dragHandlers.onMouseDown}
              onMouseUp={dragHandlers.onMouseUp}
              onMouseMove={dragHandlers.onMouseMove}
            >
              <div className={style["story_wrapper"]}>
                {feedData.map((feed, i) => {
                  return (
                    <StoryFeed
                      key={`story_${feed.feed.fid}`}
                      feedData={feed}
                      hasDragged={hasDragged}
                    />
                  );
                })}
              </div>
            </div>

            <div className={style["category-info"]}>
              <p>모든 게시글</p>
              <p className={style["category_change"]} onClick={onClickCategory}>
                카테고리 변경
              </p>
            </div>

            {biasId && (
              <CategoryModal
                SetIsOpen={setIsOpendCategory}
                onClickCategory={onClickCategory}
                biasId={biasId}
                board={board}
                setBoard={setBoard}
                isOpend={isOpendCategory}
              />
            )}
          </div>
        )}
        {type === "all" && (
          <div className={style["search-section"]}>
            <SearchBox />
            <div className={style["search-filter"]}>
              <button onClick={onClickFilterButton}>
                필터
                <span className={style["filter-icon"]}>
                  <img src={filter_icon} alt="filter" />
                </span>
              </button>
            </div>
          </div>
        )}

        {(type === "today" || type === "weekly") && (
          <div className={style["keyword-section"]}>
            <KeywordBox
              type={type}
              title={type === "today" ? "인기 급상승" : "많은 사랑을 받은"}
              subTitle={type === "today" ? "오늘의 키워드" : "이번주 키워드"}
              onClickTagButton={onClickTag}
              fetchData={fetchData}
              setHasMore={setHasMore}
              setIsSameTag={setIsSameTag}
            />
          </div>
        )}

        <div
          className={
            feedData.length > 0
              ? style["scroll-area"]
              : style["none_feed_scroll"]
          }
        >
          {feedData.length > 0 ? (
            feedData.map((feed, i) => {
              return (
                <Feed
                  key={`feed_${feed.feed.fid}`}
                  className={`${style["feed-box"]} ${
                    style[getModeClass(mode)]
                  }`}
                  feed={feed.feed}
                  setFeedData={setFeedData}
                ></Feed>
              );
            })
          ) : (
            <NoneFeed />
          )}
          <div ref={targetRef} style={{ height: "1px" }}></div>
          {isLoading && <p>loading...</p>}
          {isFilterClicked && (
            <FilterModal
              onClickFilterButton={onClickFilterButton}
              setFilterCategory={setFilterCategory}
              setFilterFclass={setFilterFclass}
              fetchAllFeed={fetchAllFeed}
              onClickApplyButton1={onClickApplyButton1}
            />
          )}
        </div>
      </div>
      <NavBar />
    </div>
  );
}
