import { useEffect, useMemo, useRef, useState } from "react";
import style from "./FeedHashList.module.css";
import logo from "./../../img/NOVA.png";
import menu from "./../../img/menu-burger.png";
import Feed, { Comments } from "./../../component/feed";
import LeftBar from "./../WideVer/LeftBar.js";
import RightBar from "./../WideVer/RightBar.js";
import { useNavigate } from "react-router-dom";
export default function FeedHashList(isUserState) {
  const target = useRef(null);
  const observerRef = useRef(null);
  let [isLoading, setIsLoading] = useState(true);
  let navigate = useNavigate();
  let [feedData, setFeedData] = useState([]);
  let [nextData, setNextData] = useState([]);
  const [isActive, setIsActive] = useState(false);
  let [hashTags, setHashTags] = useState([]);
  let [tag, setTag] = useState('');
  let [clickIndex, setClickIndex] = useState(0);

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
        // setIsLoading(false);
      });
  }

  // let fetchUrl = `https://nova-platform.kr/feed_explore/search_feed_with_hashtag?hashtag=${}&key=${}`

  function fetchPlusData() {
    // setIsLoading(true);
    fetch(`https://nova-platform.kr/feed_explore/search_feed_with_hashtag?hashtag=임시`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('1241', data)
        setFeedData(data.body.feed);
        // setNextData(data.body.key);
        // setFeedData((prevData) => {
        //   const newData = [...prevData, ...data.body.feed];
        //   return newData;
        // });
        setIsLoading(false);
      });
  }
  // useEffect(() => {
  //   fetchPlusData()
  // }, [])

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
    // return () => {
    //   setFeedData([]);
    // };
  }, []);

  function handleClickTag(index) {
    fetchPlusData()
    setClickIndex(index);
  };
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
      handleClickTag(index);
      setTag(tag);
    }
  }


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
        <div className={style.title}>시연</div>
        <div ref={scrollRef}
          onMouseDown={onMouseDown}
          onMouseMove={onMouseMove}
          onMouseUp={onMouseUp}
          className={style["tag-container"]}>
          {
            hashTags.map((tag, i) => {
              return (
                <button key={i}
                  style={{ background: clickIndex === i ? 'purple' : 'black' }}
                  onClick={() => handleTagClick(i, tag)}
                  className={style["hashtag-text"]}>#{tag}</button>
              )
            })
          }
        </div>
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
