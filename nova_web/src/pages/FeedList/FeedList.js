import { useEffect, useMemo, useRef, useState, useLocation } from "react";
import style from "./FeedHashList.module.css";
import logo from "./../../img/NOVA_Platform.png";
import menu from "./../../img/menu-burger.png";
import Feed, { Comments } from "./../../component/feed";
import { useNavigate, useSearchParams } from "react-router-dom";
import LeftBar from "./../WideVer/LeftBar.js";
import RightBar from "./../WideVer/RightBar.js";
import { getModeClass } from "./../../App.js";
import BiasBoxes from "../../component/BiasBoxes.js";
import SearchBox from "../../component/SearchBox.js";
import KeywordBox from "../../component/keyword/KeywordBox.js";
import FilterModal from "../../component/FilterModal/FilterModal.js";
export default function FeedList(isUserState) {
  const [params] = useSearchParams();
  const type = params.get("type");
  const keyword = params.get("keyword");

  const target = useRef(null);
  const observerRef = useRef(null);

  let [isFilterClicked, setIsFilterClicked] = useState(false);

  let [isLoading, setIsLoading] = useState(true);

  let [feedData, setFeedData] = useState([]);
  let [nextData, setNextData] = useState([]);

  const brightModeFromUrl = params.get("brightMode");

  const initialMode = brightModeFromUrl || localStorage.getItem("brightMode") || "bright"; // URL에서 가져오고, 없으면 로컬 스토리지에서 가져옴
  const [mode, setMode] = useState(initialMode);
  let navigate = useNavigate();

  const FETCH_URL = "https://nova-platform.kr/feed_explore/";
  // fetch(`https://nova-platform.kr/feed_explore/search_feed_with_hashtag?hashtag=${tag}`, {
  function fetchData() {
    // setIsLoading(true);
    if (type === "best") {
      fetch(`${FETCH_URL}today_best`, {
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("first feed 3개", data.body);
          setFeedData(data.body.feed);
          setNextData(data.body.key);
          setIsLoading(false);
        });
    } else if (type === "all") {
      fetch(`${FETCH_URL}all_feed`, {
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("first feed 3개", data.body);
          setFeedData(data.body.feed);
          setNextData(data.body.key);
          setIsLoading(false);
        });
    } else if (type === "weekly_best") {
      fetch(`${FETCH_URL}weekly_best`, {
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          // console.log("first feed 3개", data);
          setFeedData(data.body.feed);
          setNextData(data.body.key);
          setIsLoading(false);
        });
    }

    if (keyword) {
      fetch(`${FETCH_URL}search_feed_with_hashtag?hashtag=${keyword}&key=-1`)
        .then((response) => response.json())
        .then((data) => {
          setFeedData(data.body.feed);
          setNextData(data.body.key);
          setIsLoading(false);
        });
    }
  }

  function fetchPlusData() {
    // setIsLoading(true);
    if (type === "best") {
      fetch(`${FETCH_URL}today_best?key=${nextData}`, {
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          setNextData(data.body.key);
          setFeedData((prevData) => {
            const newData = [...prevData, ...data.body.feed];
            return newData;
          });
          setIsLoading(false);
          console.log("more", data);
        });
    } else if (type === "all") {
      fetch(`${FETCH_URL}all_feed?key=${nextData}`, {
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          setNextData(data.body.key);
          setFeedData((prevData) => {
            const newData = [...prevData, ...data.body.feed];
            return newData;
          });
          setIsLoading(false);
          console.log("mor1", data);
        });
    } else if (type === "weekly_best") {
      fetch(`${FETCH_URL}weekly_best?key=${nextData}`, {
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          setNextData(data.body.key);
          setFeedData((prevData) => {
            const newData = [...prevData, ...data.body.feed];
            return newData;
          });
          setIsLoading(false);
          console.log("mor2", data);
        });
    }

    if (keyword) {
      fetch(`${FETCH_URL}search_feed_with_hashtag?hashtag=${keyword}&key=${nextData}`, {
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          setNextData(data.body.key);
          setFeedData((prevData) => {
            const newData = [...prevData, ...data.body.feed];
            return newData;
          });
          setIsLoading(false);
          console.log("mor", data);
        });
    }
  }

  useEffect(() => {
    observerRef.current = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        if (isLoading) return;

        fetchPlusData();
      });
    });

    if (target.current) {
      observerRef.current.observe(target.current);
    }

    return () => {
      if (observerRef.current && target.current) {
        observerRef.current.unobserve(target.current);
      }
    };
  }, [isLoading, nextData]);

  useEffect(() => {
    fetchData();
    return () => {
      setFeedData([]);
    };
  }, [keyword]);

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
    <div className="all-box">
      {/* <section className="contents com1">
        <LeftBar brightMode={mode} />
      </section> */}
      <div className={`${style["container"]} ${style[getModeClass(mode)]}`}>
        <header className={style.header}>
          <div className="logo">
            <img
              src={logo}
              alt="logo"
              onClick={() => {
                navigate("/");
              }}
            ></img>
          </div>
          <div className="buttons">
            <button className="tool-button">
              <img
                src={menu}
                alt="menu"
                onClick={() => {
                  navigate("/more_see");
                }}
              ></img>
            </button>
          </div>
        </header>
        {type === "all" && (
          <BiasBoxes />
          // <div className={`${style["title"]} ${style[getModeClass(mode)]}`}>전체 피드</div>
        )}
        {type === "best" && (
          <div className={style["search-section"]}>
            <SearchBox />
            <div className={style["search-filter"]}>
              <button onClick={onClickFilterButton}>필터순</button>
              <div className={style["sort-btn-container"]}>
                <button>최신순</button>
                <button>랜덤순</button>
              </div>
            </div>
          </div>
          // <div className={`${style["title"]} ${style[getModeClass(mode)]}`}>오늘의 베스트 피드</div>
        )}
        {type === "weekly_best" && (
          <KeywordBox title={"인기 급상승"} subTitle={"오늘의 키워드"} />
          // <div className={`${style["title"]} ${style[getModeClass(mode)]}`}>주간 베스트 피드</div>
        )}
        {keyword && (
          <div className={`${style["title"]} ${style[getModeClass(mode)]}`}>{keyword}</div>
        )}
        <div className={style["scroll-area"]}>
          {feedData.map((feed, i) => {
            return (
              <Feed
                key={feed.fid + i}
                className={`${style["feed-box"]} ${style[getModeClass(mode)]}`}
                feed={feed}
                func={true}
                feedData={feedData}
                setFeedData={setFeedData}
                isUserState={isUserState}
              ></Feed>
            );
          })}
          {isLoading && <p>Loading...</p>}
          {isFilterClicked && (
            // <div className={style["filter-modal"]}>
            <FilterModal
              isFilterClicked={isFilterClicked}
              onClickFilterButton={onClickFilterButton}
            />
            // {/* </div> */}
          )}
          <div ref={target} style={{ height: "1px" }}></div>
        </div>
      </div>
      {/* <section className="contents com1">
        <RightBar brightMode={mode} />
      </section> */}
    </div>
  );
}
