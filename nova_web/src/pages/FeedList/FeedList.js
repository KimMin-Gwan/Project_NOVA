import "@toast-ui/editor/dist/toastui-editor-viewer.css";
import { Viewer } from "@toast-ui/react-editor";
import { useEffect, useLocation, useMemo, useRef, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import BiasBoxes from "../../component/BiasBoxes.js";
import FilterModal from "../../component/FilterModal/FilterModal.js";
import SearchBox from "../../component/SearchBox.js";
import KeywordBox from "../../component/keyword/KeywordBox.js";
import { getModeClass } from "./../../App.js";
import Feed, { Comments } from "./../../component/feed";
import logo from "./../../img/NOVA_Platform.png";
import logo2 from "./../../img/logo2.png";
import menu from "./../../img/menu-burger.png";
import LeftBar from "./../WideVer/LeftBar.js";
import RightBar from "./../WideVer/RightBar.js";
import style from "./FeedHashList.module.css";
import NoticeBox from "../../component/NoticeBox/NoticeBox.js";
import CategoryModal from "../../component/CategoryModal/CategoryModal.js";

export default function FeedList(isUserState) {
  const [params] = useSearchParams();
  const type = params.get("type");
  const keyword = params.get("keyword");

  const target = useRef(null);
  const observerRef = useRef(null);

  let [isFilterClicked, setIsFilterClicked] = useState(false);
  let [contents, setContents] = useState("");
  let [isLoading, setIsLoading] = useState(true);

  let [feedData, setFeedData] = useState([]);
  let [feedInteraction, setFeedInteraction] = useState([]);
  let [nextData, setNextData] = useState(-1);

  let [biasId, setBiasId] = useState();
  let [board, setBoard] = useState("자유게시판");

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

  function fetchBiasCategoryData(bid) {
    let send_data = {
      header: header,
      body: {
        bid: bid || "",
        board: board || "",
        last_fid: "",
      },
    };
    // setIsLoading(true);
    if (type === "bias") {
      fetch(`${FETCH_URL}feed_with_community`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(send_data),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("first bias data", data);
          setFeedData(data.body.send_data);
          setNextData(data.body.last_fid);
          setIsLoading(false);
        });
    }
  }

  useEffect(() => {
    fetchBiasCategoryData();
    console.log(biasId, board);
  }, [board]);

  let [filterCategory, setFilterCategory] = useState([]);
  let [filterFclass, setFilterFclass] = useState("");
  let [isClickedFetch, setIsClickedFetch] = useState(false);
  let [allFeed, setAllFeed] = useState([]);
  const FETCH_URL = "https://nova-platform.kr/feed_explore/";

  let send_form = {
    header: header,
    body: {
      key: nextData,
      category: filterCategory || [""],
      fclass: filterFclass || "",
    },
  };
  async function fetchAllFeed() {
    if (type === "all" || isClickedFetch) {
      if (isClickedFetch) {
        setNextData(-1);
      }
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
          // setFeedData(data.body.send_data);
          // setFeedInteraction(data.body.send_data.map((interaction, i) => interaction));
          setNextData(data.body.key);
          setIsLoading(false);
          setFeedData(data.body.send_data);
          setIsClickedFetch(false);
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
          // setFeedInteraction(data.body.send_data.map((interaction, i) => interaction));
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
          setFeedData(data.body.send_data);
          setNextData(data.body.key);
          setIsLoading(false);
        });
    }

    if (keyword) {
      fetch(`${FETCH_URL}search_feed_with_hashtag?hashtag=${keyword}&key=-1`)
        .then((response) => response.json())
        .then((data) => {
          setFeedData(data.body.send_data);
          setNextData(data.body.key);
          setIsLoading(false);
        });
    }
  }

  function fetchFeedWithTag(tag) {
    fetch(`${FETCH_URL}search_feed_with_hashtag?hashtag=${tag}&key=-1`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("tag", data);
        setFeedData(data.body.send_data);
        // setFeedInteraction(data.body.send_data.map((interaction, i) => interaction));

        setNextData(data.body.key);
        setIsLoading(false);
      });
  }

  function onClickTag(tag) {
    fetchFeedWithTag(tag);
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

    if (keyword) {
      fetch(`${FETCH_URL}search_feed_with_hashtag?hashtag=${keyword}&key=${nextData}`, {
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
          console.log("mor", data);
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
            return feed.feed.fid === fid
              ? { ...feed, interaction: data.body.interaction }
              : feed;
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

        // console.log("???????");

        // fetchAllFeed();
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
    fetchAllFeed();

    return () => {
      setFeedData([]);
    };
  }, [keyword]);

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
    <div className="all-box">
      {/* <section className="contents com1">
        <LeftBar brightMode={mode} />
      </section> */}
      <div className={`${style["container"]} ${style[getModeClass(mode)]}`}>
        <header className={style.header}>
          <div className="logo">
            <img
              src={logo2}
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
        {type == "bias" && (
          <div className={style["bias-section"]}>
            <BiasBoxes
              setBiasId={setBiasId}
              fetchBiasCategoryData={fetchBiasCategoryData}
            />
            <NoticeBox />
            <div className={style["category-info"]}>
              <h4>모든 게시글</h4>
              {biasId && <p onClick={onClickCategory}>카테고리 변경</p>}
            </div>
            {isOpendCategory && (
              <CategoryModal
                onClickCategory={onClickCategory}
                biasId={biasId}
                setBoard={setBoard}
              />
            )}
          </div>
        )}
        {type === "all" && (
          // <BiasBoxes />
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
          // <div className={`${style["title"]} ${style[getModeClass(mode)]}`}>전체 피드</div>
        )}
        {type === "best" && (
          <div className={style["keyword-section"]}>
            <KeywordBox
              title={"인기 급상승"}
              subTitle={"오늘의 키워드"}
              onClickTagButton={onClickTag}
            />
          </div>
          // <div className={`${style["title"]} ${style[getModeClass(mode)]}`}>오늘의 베스트 피드</div>
        )}
        {type === "weekly_best" && (
          <div className={style["keyword-section"]}>
            <KeywordBox
              title={"많은 사랑을 받은"}
              subTitle={"이번주 키워드"}
              onClickTagButton={onClickTag}
            />
          </div>
          // <div className={`${style["title"]} ${style[getModeClass(mode)]}`}>주간 베스트 피드</div>
        )}
        {keyword && (
          <div className={`${style["title"]} ${style[getModeClass(mode)]}`}>
            {keyword}
          </div>
        )}
        <div className={style["scroll-area"]}>
          {feedData &&
            feedData.map((feed, i) => {
              return (
                <Feed
                  key={feed.feed.fid}
                  className={`${style["feed-box"]} ${style[getModeClass(mode)]}`}
                  feed={feed.feed}
                  func={true}
                  feedData={feedData}
                  interaction={feed.interaction}
                  feedInteraction={feedInteraction}
                  setFeedData={setFeedData}
                  isUserState={isUserState}
                  handleInteraction={handleInteraction}
                ></Feed>
              );
            })}
          {isLoading && <p>Loading...</p>}
          {isFilterClicked && (
            // <div className={style["filter-modal"]}>
            <FilterModal
              isFilterClicked={isFilterClicked}
              onClickFilterButton={onClickFilterButton}
              setFilterCategory={setFilterCategory}
              setFilterFclass={setFilterFclass}
              fetchAllFeed={fetchAllFeed}
              setIsClickedFetch={setIsClickedFetch}
              setNextData={setNextData}
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
