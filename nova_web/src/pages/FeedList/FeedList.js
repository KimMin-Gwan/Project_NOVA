import { useEffect, useMemo, useRef, useState, useLocation } from "react";
import style from "./FeedHashList.module.css";
import logo from "./../../img/NOVA.png";
import menu from "./../../img/menu-burger.png";
import Feed, { Comments } from "./../../component/feed";
import { useNavigate, useSearchParams } from "react-router-dom";
import LeftBar from "./../WideVer/LeftBar.js";
import RightBar from "./../WideVer/RightBar.js";
import { getModeClass } from "./../../App.js";
export default function FeedList(isUserState) {
  const [params] = useSearchParams();
  const type = params.get("type");

  const target = useRef(null);
  const observerRef = useRef(null);
  let [isLoading, setIsLoading] = useState(true);

  let [feedData, setFeedData] = useState([]);
  let [nextData, setNextData] = useState([]);

  const brightModeFromUrl = params.get("brightMode");

  const initialMode = brightModeFromUrl || localStorage.getItem("brightMode") || "bright"; // URL에서 가져오고, 없으면 로컬 스토리지에서 가져옴
  const [mode, setMode] = useState(initialMode);
  let navigate = useNavigate();
  function fetchData() {
    // setIsLoading(true);
    if (type === "best") {
      fetch("https://nova-platform.kr/feed_explore/today_best", {
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          // console.log('first feed 3개', data.body);
          setFeedData(data.body.feed);
          setNextData(data.body.key);
          setIsLoading(false);
        });
    } else if (type === "all") {
      fetch("https://nova-platform.kr/feed_explore/all_feed", {
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          // console.log('first feed 3개', data.body);
          setFeedData(data.body.feed);
          setNextData(data.body.key);
          setIsLoading(false);
        });
    }
  }

  function fetchPlusData() {
    // setIsLoading(true);
    if (type === "best") {
      fetch(`https://nova-platform.kr/feed_explore/today_best?key=${nextData}`, {
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
    } else if (type === "all") {
      fetch(`https://nova-platform.kr/feed_explore/all_feed?key=${nextData}`, {
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
  }, []);
  useEffect(() => {
    // mode가 변경될 때만 localStorage에 저장
    localStorage.setItem("brightMode", mode);
  }, [mode]);
  if (isLoading) {
    return <p>데이터 불러오는 중</p>;
  }

  return (
    <div className="all-box">
      <section className="contents com1">
        <LeftBar />
      </section>
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
        {type === "all" && <div className={`${style["title"]} ${style[getModeClass(mode)]}`}>전체 피드</div>}
        {type === "best" && <div className={`${style["title"]} ${style[getModeClass(mode)]}`}>최근 인기 피드</div>}
        <div className={style["scroll-area"]}>
          {feedData.map((feed, i) => {
            return <Feed key={feed.fid + i} className={`${style[getModeClass(mode)]}`} feed={feed} func={true} feedData={feedData} setFeedData={setFeedData} isUserState={isUserState}></Feed>;
          })}
          {isLoading && <p>Loading...</p>}
          <div ref={target} style={{ height: "1px", backgroundColor: "blue" }}></div>
        </div>
      </div>
      <section className="contents com1">
        <RightBar />
      </section>
    </div>
  );
}
