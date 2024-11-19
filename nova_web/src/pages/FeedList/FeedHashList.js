import { useEffect, useMemo, useRef, useState } from "react";
import style from "./FeedHashList.module.css";
import logo from "./../../img/NOVA.png";
import menu from "./../../img/menu-burger.png";
import Feed, { Comments } from "./../../component/feed";
import LeftBar from "./../WideVer/LeftBar.js";
import RightBar from "./../WideVer/RightBar.js";
import { useNavigate, useSearchParams } from "react-router-dom";
import { getModeClass } from "./../../App.js";
export default function FeedHashList(isUserState) {
  const target = useRef(null);
  const observerRef = useRef(null);
  let [isLoading, setIsLoading] = useState(true);
  let navigate = useNavigate();
  let [feedData, setFeedData] = useState([]);
  let [nextData, setNextData] = useState([]);
  const [isActive, setIsActive] = useState(false);
  let [hashTags, setHashTags] = useState([]);
  let [tag, setTag] = useState("");
  let [isClickedTag, setIsClickedTag] = useState(null);
  let [clickIndex, setClickIndex] = useState(0);
  let [biasData, setBiasData] = useState(null);
  const [params] = useSearchParams();
  const brightModeFromUrl = params.get("brightMode");

  const initialMode = brightModeFromUrl || localStorage.getItem("brightMode") || "bright"; // URL에서 가져오고, 없으면 로컬 스토리지에서 가져옴
  const [mode, setMode] = useState(initialMode);

  function fetchHashTagData() {
    // setIsLoading(true);
    fetch("https://nova-platform.kr/home/hot_hashtag", {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("first feed 3개", data);
        setHashTags(data.body.hashtags);
        // setFeedData(data.body.feed);
        // setNextData(data.body.key);
        setBiasData(data.body);
        setIsLoading(false);
        setIsClickedTag(data.body.hashtags[0]);
      });
  }

  // let fetchUrl = `https://nova-platform.kr/feed_explore/search_feed_with_hashtag?hashtag=${tag}&key=${}`

  function fetchPlusData(tag) {
    // setIsLoading(true);
    fetch(`https://nova-platform.kr/feed_explore/search_feed_with_hashtag?hashtag=${tag}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setFeedData(data.body.feed);

        // setNextData(data.body.key);
        // setFeedData((prevData) => {
        //   const newData = [...prevData, ...data.body.feed];
        //   return newData;
        // });
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
    fetchHashTagData();
  }, []);

  useEffect(() => {
    fetchPlusData(isClickedTag);
  }, [isClickedTag]);

  // function handleClickTag(index, tag) {
  //   // fetchPlusData();
  //   // setClickIndex(index);
  //   setIsClickedTag(tag);
  // }
  let scrollRef = useRef(null);
  let [isDrag, setIsDrag] = useState(false);
  let [dragStart, setDragStart] = useState("");
  let [hasDragged, setHasDragged] = useState(false);

  function onMouseDown(e) {
    e.preventDefault();
    setIsDrag(true);
    setDragStart(e.pageX + scrollRef.current.scrollLeft);
    setHasDragged(false);
  }

  function onMouseUp(e) {
    setIsDrag(false);
  }

  function onMouseMove(e) {
    if (isDrag) {
      scrollRef.current.scrollLeft = dragStart - e.pageX;
      setHasDragged(true);
    }
  }

  function handleTagClick(index, tag) {
    if (!hasDragged) {
      // handleClickTag(index);
      // setTag(tag);
      setIsClickedTag(tag);
    }
  }
  useEffect(() => {
    // mode가 변경될 때만 localStorage에 저장
    localStorage.setItem("brightMode", mode);
  }, [mode]);
  if (isLoading) {
    return <p>데이터 </p>;
  }

  return (
    <div className="all-box">
      <section className="contents com1">
        <LeftBar brightMode={mode} />
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
        <div className={`${style["title"]} ${style[getModeClass(mode)]}`}>
          {biasData.title ? biasData.title : "인기 해시태그"}
        </div>
        <div
          ref={scrollRef}
          onMouseDown={onMouseDown}
          onMouseMove={onMouseMove}
          onMouseUp={onMouseUp}
          className={`${style["tag-container"]} ${style[getModeClass(mode)]}`}
        >
          {hashTags.map((tag, i) => {
            return (
              <button
                key={i}
                style={{ background: isClickedTag === tag ? "purple" : "black" }}
                onClick={() => handleTagClick(i, tag)}
                className={style["hashtag-text"]}
              >
                #{tag}
              </button>
            );
          })}
        </div>
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
          <div ref={target} style={{ height: "1px" }}></div>
        </div>
      </div>
      <section className="contents com1">
        <RightBar brightMode={mode} />
      </section>
    </div>
  );
}
