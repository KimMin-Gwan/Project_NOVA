import { useEffect, useMemo, useRef, useState, useLocation } from "react";
import style from "./FeedHashList.module.css";
import logo from "./../../img/NOVA_Platform.png";
import logo2 from "./../../img/logo2.png";
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
import { Viewer } from "@toast-ui/react-editor";
import "@toast-ui/editor/dist/toastui-editor-viewer.css";

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
  let [nextData, setNextData] = useState([]);

  let [biasId, setBiasId] = useState();

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
        board: "",
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
  }, []);

  const FETCH_URL = "https://nova-platform.kr/feed_explore/";
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
    } else if (type === "all") {
      fetch(`${FETCH_URL}all_feed`, {
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
    } else if (type === "all") {
      fetch(`${FETCH_URL}all_feed?key=${nextData}`, {
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          setNextData(data.body.key);
          setFeedData((prevData) => {
            const newData = [...prevData, ...data.body.send_data];
            return newData;
          });
          // setFeedInteraction(data.body.send_data.map((interaction, i) => interaction));
          // setFeedInteraction((prevData) => {
          //   const newData = [
          //     ...prevData,
          //     ...data.body.send_data.map((interaction, i) => interaction),
          //   ];
          //   return newData;
          // });
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
            const newData = [...prevData, ...data.body.send_data];
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
    setIsLoading(true);
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
        console.log(data);
        console.log("클릭 ", feedData.feed); //배열이라 안나오는듯
        console.log("상호작용 전 피드 데이터", feedData); //여기선 다 나옴
        // setFeedData((prevFeeds) => {
        //   return prevFeeds.map((feed, i) =>
        //     feed.interaction.fid === fid
        //       ? {
        //           ...feed.interaction,
        //           attend: data.body.interaction.attend,
        //           result: data.body.interaction.result,
        //         }
        //       : feed.interaction
        //   );
        // });
        // setMyAttend(data.body.feed[0].attend);
        // setFeedInteraction(data.body.interaction);
        setFeedData((prevFeeds) => {
          return prevFeeds.map((feed) => {
            return feed.feed.fid === fid && { ...feed, interaction: data.body.interaction };
          });
        });
        console.log("상호작용 후 피드 데이터", feedData); //변경되지 않음, 왜?
        setIsLoading(false);
      });
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
          <BiasBoxes setBiasId={setBiasId} fetchBiasCategoryData={fetchBiasCategoryData} />
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
          <KeywordBox
            title={"인기 급상승"}
            subTitle={"오늘의 키워드"}
            onClickTagButton={onClickTag}
          />
          // <div className={`${style["title"]} ${style[getModeClass(mode)]}`}>오늘의 베스트 피드</div>
        )}
        {type === "weekly_best" && (
          <KeywordBox
            title={"많은 사랑을 받은"}
            subTitle={"이번주 키워드"}
            onClickTagButton={onClickTag}
          />
          // <div className={`${style["title"]} ${style[getModeClass(mode)]}`}>주간 베스트 피드</div>
        )}
        {keyword && (
          <div className={`${style["title"]} ${style[getModeClass(mode)]}`}>{keyword}</div>
        )}
        <div className={style["scroll-area"]}>
          {feedData &&
            feedData.map((feed, i) => {
              if (!feed.feed) {
                console.log("erororo");
                console.log(feed.feed);
                return null;
              } else if (!feed.feed.fid) {
                console.log("qoqoqoqoqo");
                return null;
              }

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
