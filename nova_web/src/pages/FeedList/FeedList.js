import { useEffect, useMemo, useRef, useState } from "react";
import style from "./FeedHashList.module.css";
import logo from "./../../img/NOVA.png";
import menu from "./../../img/menu-burger.png";
import Feed, { Comments } from "./../../component/feed";
import { useNavigate } from "react-router-dom";
import LeftBar from "./../WideVer/LeftBar.js";
import RightBar from "./../WideVer/RightBar.js";
export default function FeedList(isUserState) {
  const target = useRef(null);
  const observerRef = useRef(null);
  let [isLoading, setIsLoading] = useState(true);

  let [feedData, setFeedData] = useState([]);
  let [nextData, setNextData] = useState([]);
  let navigate = useNavigate();
  function fetchData() {
    // setIsLoading(true);
    fetch("https://nova-platform.kr/home/home_feed", {
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

  function fetchPlusData() {
    // setIsLoading(true);
    fetch(`https://nova-platform.kr/home/home_feed?key=${nextData}`, {
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
        console.log('mor',data)
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
  }, []);

  if (isLoading) {
    return <p>데이터 </p>;
  }

  return (
    <div className="all-box">
      <section className="contents com1">
        <LeftBar />
      </section>
      <div className={style.container}>
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
        <div className={style.title}>최근 인기 피드</div>
        <div className={style["scroll-area"]}>
          {feedData.map((feed, i) => {
            return <Feed key={feed.fid + i} className="" feed={feed} func={true} feedData={feedData} setFeedData={setFeedData} isUserState={isUserState}></Feed>;
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
