import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";

import postApi from "../../services/apis/postApi.js";
import mainApi from "../../services/apis/mainApi.js";
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

export default function FeedList() {
  const [params] = useSearchParams();
  const type = params.get("type");

  const target = useRef(null);
  const observerRef = useRef(null);

  let [isFilterClicked, setIsFilterClicked] = useState(false);
  let [isLoading, setIsLoading] = useState(true);

  let [feedData, setFeedData] = useState([]);
  let [nextData, setNextData] = useState(-1);

  let [biasId, setBiasId] = useState();
  let [board, setBoard] = useState("자유게시판");

  const [hashtag, setHashTag] = useState("");

  let header = {
    "request-type": "default",
    "client-version": "v1.0.1",
    "client-ip": "127.0.0.1",
    uid: "1234-abcd-5678",
    endpoint: "/user_system/",
  };

  const brightModeFromUrl = params.get("brightMode");

  const initialMode = brightModeFromUrl || localStorage.getItem("brightMode") || "bright"; // URL에서 가져오고, 없으면 로컬 스토리지에서 가져옴
  const [mode, setMode] = useState(initialMode);

  let { biasList } = useBiasStore();
  useEffect(() => {
    console.log("동작");
  }, []);

  let bids = biasList.map((item, i) => {
    return item.bid;
  });
  useEffect(() => {
    if (bids.length > 0 && !biasId) {
      setBiasId(bids[0]);
    }
  }, [bids]);
  async function fetchBiasCategoryData(bid) {
    await postApi
      .post(`feed_explore/feed_with_community`, {
        header: header,
        body: {
          bid: biasId || bids?.[0] || "",
          board: board || "",
          key: nextData || -1,
        },
      })
      .then((res) => {
        console.log("first bias data", res.data);
        setFeedData((prevData) => [...prevData, ...res.data.body.send_data]);
        setNextData(res.data.body.key);
        setIsLoading(false);
      });
  }

  useEffect(() => {
    setFeedData([]);
    setNextData(-1);
    if (type === "bias") {
      fetchBiasCategoryData();
    }
  }, [biasId, board]);

  let [filterCategory, setFilterCategory] = useState([]);
  let [filterFclass, setFilterFclass] = useState("");
  let [isClickedFetch, setIsClickedFetch] = useState(false);
  const FETCH_URL = "https://nova-platform.kr/feed_explore/";

  function onClickApplyButton1() {
    setNextData(-1);
    console.log(nextData);
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

    // 지역변수로 사용하기로함
    let send_form = {
      header: header,
      body: {
        key: updatedNextData, // 여기에서  사용됨
        category: filterCategory || [""],
        fclass: filterFclass || "",
      },
    };

    if (type === "all" || isClickedFetch) {
      await fetch(`${FETCH_URL}all_feed`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(send_form),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("all feed first feed 3개", data.body);
          setNextData(data.body.key);
          setIsLoading(false);
          setFeedData(data.body.send_data);
          // setFeedData((prevData) => {
          //   const newData = [...prevData, ...data.body.send_data];
          //   return newData;
          // });
        });
    }
  }

  function fetchData() {
    if (type === "today" || type === "weekly") {
      mainApi.get(`feed_explore/${type}_best`).then((res) => {
        console.log(`${type} feed`, res.data.body);
        setFeedData(res.data.body.send_data);
        setNextData(res.data.body.key);
        setIsLoading(false);
      });
    }
  }

  function fetchFeedWithTag(tag) {
    console.log("dasdasda", hashtag);
    mainApi
      .get(`feed_explore/search_feed_with_hashtag?hashtag=${tag}&key=-1&target_time=day`)
      .then((res) => {
        console.log("fff", res.data);
        setFeedData(res.data.body.send_data);
        // setNextData(res.data.body.key);
        setIsLoading(false);
      });
  }
  useEffect(() => {
    setFeedData([]);
  }, []);

  function onClickTag(tag) {
    fetchFeedWithTag(tag);
  }

  function fetchPlusData() {
    if (type === "today" || type === "weekly") {
      mainApi.get(`feed_explore/${type}_best?key=${nextData}`).then((res) => {
        setNextData(res.data.body.key);
        setFeedData((prevData) => {
          const newData = [...prevData, ...res.data.body.send_data];
          return newData;
        });
        setIsLoading(false);
        console.log(`more ${type}`, res.data);
      });
    } else if (type === "all" || isClickedFetch) {
      // 지역 변수 데이터로 활용하기로함
      let send_form = {
        header: header,
        body: {
          key: nextData,
          category: filterCategory || [""],
          fclass: filterFclass || "",
        },
      };

      fetch(`${FETCH_URL}all_feed`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(send_form),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("all feed first feed 3개", data.body);
          setNextData(data.body.key);
          setIsLoading(false);
          setFeedData((prevData) => {
            const newData = [...prevData, ...data.body.send_data];
            return newData;
          });
        });
    }
  }

  useEffect(() => {
    observerRef.current = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        if (isLoading) return;

        // fetchAllFeed();
        fetchPlusData();
        if (type === "bias") {
          fetchBiasCategoryData();
        }
      });
    });

    if (target.current) {
      observerRef.current.observe(target.current);
    }

    return () => {
      if (observerRef.current && target.current) {
        observerRef.current.unobserve(target.current);
        observerRef.current.disconnect();
      }
    };
  }, [isLoading, nextData]);

  useEffect(() => {
    fetchData();
    fetchAllFeed(false);

    return () => {
      setFeedData([]);
    };
  }, []);

  let [isOpendCategory, setIsOpendCategory] = useState(false);

  function onClickCategory() {
    setIsOpendCategory(!isOpendCategory);
  }

  useEffect(() => {
    // mode가 변경될 때만 localStorage에 저장
    localStorage.setItem("brightMode", mode);
  }, [mode]);

  function onClickFilterButton() {
    setIsFilterClicked(!isFilterClicked);
  }

  if (isFilterClicked) {
    document.body.style.overflow = "hidden";
  } else {
    document.body.style.overflow = "auto";
  }

  if (isLoading) {
    return <p>데이터 불러오는 중</p>;
  }

  return (
    <div className={`all-box ${style["all_container"]}`}>
      <div className={`${style["container"]} ${style[getModeClass(mode)]}`}>
        <Header />
        {type === "bias" && (
          <div className={style["bias-section"]}>
            <BiasBoxes setBiasId={setBiasId} fetchBiasCategoryData={fetchBiasCategoryData} />
            <h4>스토리 게시판</h4>
            <div className={style["story_container"]}>
              <div className={style["story_wrapper"]}>
                {feedData.map((feed, i) => {
                  return <StoryFeed key={`story_${feed.feed.fid}`} feedData={feed} />;
                })}
              </div>
            </div>

            <div className={style["category-info"]}>
              <p>모든 게시글</p>
              <p className={style["category_change"]} onClick={onClickCategory}>
                카테고리 변경
              </p>
            </div>

            {isOpendCategory && (
              <CategoryModal
                SetIsOpen={setIsOpendCategory}
                onClickCategory={onClickCategory}
                biasId={biasId}
                board={board}
                setBoard={setBoard}
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
            />
          </div>
        )}

        <div className={feedData.length > 0 ? style["scroll-area"] : style["none_feed_scroll"]}>
          {feedData.length > 0 ? (
            feedData.map((feed, i) => {
              return (
                <Feed
                  key={`feed_${feed.feed.fid}`}
                  className={`${style["feed-box"]} ${style[getModeClass(mode)]}`}
                  feed={feed.feed}
                  setFeedData={setFeedData}
                ></Feed>
              );
            })
          ) : (
            <NoneFeed />
          )}
          <div ref={target} style={{ height: "1px" }}></div>
          {isLoading && <p>Loading...</p>}
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
