import React, { useCallback, useEffect, useRef, useState } from "react";
import style from "./MainPart.module.css";
import SimpleSlider from "../../component/SimpleSlider";
import more_icon from "./../../img/backword.png";
import { useNavigate } from "react-router-dom";
import { getModeClass } from "./../../App.js";
export default function MainPart({ brightMode }) {
  let [bias, setBias] = useState("");
  let [biasTag, setBiasTag] = useState([]);
  let [tagFeed, setTagFeed] = useState([]);
  let [hashTag, setHashTag] = useState(null);
  let [clickIndex, setClickIndex] = useState(0);

  const navigate = useNavigate();
  // const handleClick = (index) => {
  //   // fetchTagFeed();
  //   setClickIndex(index);
  // };

  function fetchHashTag() {
    fetch("https://nova-platform.kr/home/hot_hashtag", {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setBias(data.body);
        setBiasTag(data.body.hashtags);
        setHashTag(data.body.hashtags[0]);
      });
  }

  // const fetchUrl = `https://nova-platform.kr/home/search_feed_with_hashtag?hashtag=${hashTag}`;

  const fetchTagFeed = (tag) => {
    fetch(`https://nova-platform.kr/home/search_feed_with_hashtag?hashtag=${tag}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setTagFeed(data.body.feed);
        // console.log("data", data);
      });
  };

  useEffect(() => {
    fetchHashTag();
  }, []);

  useEffect(() => {
    if (hashTag) {
      fetchTagFeed(hashTag);
    }
  }, [hashTag]);

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
      // handleClick(index);
      setHashTag(tag);
      // fetchTagFeed(tag);
    }
  }

  const [mode, setMode] = useState(brightMode); // 초기 상태는 부모로부터 받은 brightMode 값
  useEffect(() => {
    setMode(brightMode); // brightMode 값이 바뀔 때마다 mode 업데이트
  }, [brightMode]);

  return (
    <div className={`${style["wrap-container"]} ${style[getModeClass(mode)]}`}>
      <div className={`${style["top-area"]} ${style[getModeClass(mode)]}`}>
        <div className={style["content-title"]}>
          {/* bid : ''이면 인기 해시태그
  -1이 아니면 [title] 관련 인기 해시트=ㅐ그 */}
          {bias.bid === "" ? (
            <header className={style["header-text"]}>인기 해시태그</header>
          ) : (
            <header className={style["header-text"]}>[ {bias.title} ] 관련 인기 해시태그</header>
          )}
          <img
            src={more_icon}
            alt="menu"
            onClick={() => navigate("/feed_hash_list")}
            className={`${style["more-icon"]} ${style[getModeClass(mode)]}`}
          ></img>
        </div>

        <div
          className={style["tag-container"]}
          ref={scrollRef}
          onMouseDown={onMouseDown}
          onMouseMove={onMouseMove}
          onMouseUp={onMouseUp}
        >
          {biasTag.map((tag, i) => {
            return (
              <button
                key={i}
                className={style["hashtag-text"]}
                onClick={() => {
                  handleTagClick(i, tag);
                }}
                style={{
                  backgroundColor:
                    hashTag === tag
                      ? getModeClass(mode) === "bright-mode"
                        ? "#98A0FF"
                        : "#051243"
                      : getModeClass(mode) === "bright-mode"
                      ? "#CCCFFF"
                      : "#373737",

                  cursor: "pointer",
                }}
              >
                #{tag}
              </button>
            );
          })}
        </div>
      </div>

      <div className={`${style["main-area"]} ${style[getModeClass(mode)]}`}>
        {/* <div className={style["feed-box"]}> */}
        {/*<div className={style["name-container"]}>
            <div className={style["profile"]}> </div>
            <h2 className={style["name-text"]}>익명 바위게</h2>
            <button className={style["more-see"]}>더보기</button>
          </div>
          <section className={style["text-container"]}>
            <div className={style["tag-text"]}>
              <span className={style["tag"]}>#시연</span>
              <span className={style["tag"]}>#이쁘다</span>
            </div>
            <div className={style["main-text"]}>젠타 나이 질문이요 젠타 98년생 아닌가요??</div>
          </section>

          <footer className={style["like-comment"]}>좋아요 수 댓글 수</footer>*/}
        <SimpleSlider tagFeed={tagFeed} brightMode={brightMode} />
      </div>
      {/* </div> */}
    </div>
  );
}
