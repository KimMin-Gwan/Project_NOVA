import "@toast-ui/editor/dist/toastui-editor-viewer.css";
import { useEffect, useLocation, useMemo, useRef, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import BiasBoxes from "../../component/BiasBoxes.js";
import FilterModal from "../../component/FilterModal/FilterModal.js";
import SearchBox from "../../component/SearchBox.js";
import KeywordBox from "../../component/keyword/KeywordBox.js";
import { getModeClass } from "./../../App.js";
import Feed from "./../../component/feed";
import filter_icon from "./../../img/filter.svg";
import style from "./FeedHashList.module.css";
import CategoryModal from "../../component/CategoryModal/CategoryModal.js";
import NoneFeed from "../../component/NoneFeed/NoneFeed.js";
import useBiasStore from "../../stores/BiasStore/useBiasStore.js";
import NavBar from "../../component/NavBar.js";
import Header from "../../component/Header/Header.js";
import StoryFeed from "../../component/StoryFeed/StoryFeed.js";
import postApi from "../../services/apis/postApi.js";
import mainApi from "../../services/apis/mainApi.js";

export default function FeedList(isUserState) {
  const [params] = useSearchParams();
  const type = params.get("type");

  const target = useRef(null);
  const observerRef = useRef(null);

  let [isFilterClicked, setIsFilterClicked] = useState(false);
  let [isLoading, setIsLoading] = useState(true);

  let [feedData, setFeedData] = useState([]);
  let [feedInteraction, setFeedInteraction] = useState([]);
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
  let navigate = useNavigate();

  let { biasList, fetchBiasList } = useBiasStore();
  useEffect(() => {
    console.log("동작");
    fetchBiasList();
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
    // console.log(bids, board);
  }, [biasId, board]);

  let [filterCategory, setFilterCategory] = useState([]);
  let [filterFclass, setFilterFclass] = useState("");
  let [isClickedFetch, setIsClickedFetch] = useState(false);
  let [allFeed, setAllFeed] = useState([]);
  const FETCH_URL = "https://nova-platform.kr/feed_explore/";

  //let send_form = {
  //header: header,
  //body: {
  //key: nextData,
  //category: filterCategory || [""],
  //fclass: filterFclass || "",
  //},
  //};

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
    if (type === "best") {
      fetch(`${FETCH_URL}today_best`, {
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("first feed 3개", data.body);
          setFeedData(data.body.send_data);
          setNextData(data.body.key);
          setIsLoading(false);
        });
    } else if (type === "weekly_best") {
      fetch(`${FETCH_URL}weekly_best`, {
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("first weekly feed 3개", data);
          setFeedData(data.body.send_data);
          setNextData(data.body.key);
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
    if (type === "best") {
      fetch(`${FETCH_URL}today_best?key=${nextData}`, {
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          setNextData(data.body.key);
          setFeedData((prevData) => {
            const newData = [...prevData, ...data.body.send_data];
            return newData;
          });
          setIsLoading(false);
          console.log("more", data);
        });
    } else if (type === "weekly_best") {
      fetch(`${FETCH_URL}weekly_best?key=${nextData}`, {
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          setNextData(data.body.key);
          setFeedData((prevData) => {
            const newData = [...prevData, ...data.body.send_data];
            return newData;
          });
          setIsLoading(false);
          console.log("mor2", data);
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
          // setFeedData(data.body.send_data);
          // setFeedInteraction(data.body.send_data.map((interaction, i) => interaction));
          setNextData(data.body.key);
          setIsLoading(false);
          // setFeedData(data.body.send_data);
          setFeedData((prevData) => {
            const newData = [...prevData, ...data.body.send_data];
            return newData;
          });
        });
    }
  }

  let [isError, setIsError] = useState();
  async function handleInteraction(event, fid, action) {
    event.preventDefault();
    // setIsLoading(true);
    await fetch(
      `https://nova-platform.kr/feed_explore/interaction_feed?fid=${fid}&action=${action}`,
      {
        credentials: "include",
      }
    )
      .then((response) => {
        if (!response.ok) {
          if (response.status === 401) {
            setIsError(response.status);
            navigate("/novalogin");
          } else {
            throw new Error(`status: ${response.status}`);
          }
        }
        return response.json();
      })
      .then((data) => {
        setFeedData((prevFeeds) => {
          const updatedFeeds = prevFeeds.map((feed) => {
            return feed.feed.fid === fid ? { ...feed, interaction: data.body.interaction } : feed;
          });

          return updatedFeeds;
        });
        setIsLoading(false);
      });
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
                  return <StoryFeed key={feed.feed.fid} feedData={feed} />;
                })}
              </div>
            </div>
            {biasId && (
              <div className={style["category-info"]}>
                <p>모든 게시글</p>
                <p className={style["category_change"]} onClick={onClickCategory}>
                  카테고리 변경
                </p>
              </div>
            )}
            {isOpendCategory && (
              <CategoryModal
                SetIsOpen={setIsOpendCategory}
                onClickCategory={onClickCategory}
                biasId={biasId}
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
        {type === "best" && (
          <div className={style["keyword-section"]}>
            <KeywordBox
              type={"today"}
              title={"인기 급상승"}
              subTitle={"오늘의 키워드"}
              onClickTagButton={onClickTag}
              fetchData={fetchData}
            />
          </div>
        )}
        {type === "weekly_best" && (
          <div className={style["keyword-section"]}>
            <KeywordBox
              type={"weekly"}
              title={"많은 사랑을 받은"}
              subTitle={"이번주 키워드"}
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
                  key={feed.feed.fid}
                  className={`${style["feed-box"]} ${style[getModeClass(mode)]}`}
                  feed={feed.feed}
                  interaction={feed.interaction}
                  feedInteraction={feedInteraction}
                  setFeedData={setFeedData}
                  handleInteraction={handleInteraction}
                ></Feed>
              );
            })
          ) : (
            <NoneFeed />
          )}
          <div ref={target} style={{ height: "1px" }}></div>
          {isLoading && <p>Loading...</p>}
          {isFilterClicked && (
            // <div className={style["filter-modal"]}>
            <FilterModal
              isFilterClicked={isFilterClicked}
              onClickFilterButton={onClickFilterButton}
              setFilterCategory={setFilterCategory}
              setFilterFclass={setFilterFclass}
              fetchAllFeed={fetchAllFeed}
              onClickApplyButton1={onClickApplyButton1}
              setNextData={setNextData}
            />
            // {/* </div> */}
          )}
        </div>
      </div>
      <NavBar />
    </div>
  );
}
