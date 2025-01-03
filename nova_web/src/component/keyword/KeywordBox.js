import Slider from "react-slick";
import style from "./KeywordBox.module.css";
import { useEffect, useRef, useState } from "react";

export default function KeywordBox({ title, subTitle, onClickTagButton }) {
  let [bestTags, setBestTags] = useState([]);

  function fetchBestTag() {
    fetch(`https://nova-platform.kr/home/realtime_best_hashtag`, { credentials: "include" })
      .then((response) => response.json())
      .then((data) => {
        setBestTags(data.body.hashtags);
      });
  }

  useEffect(() => {
    fetchBestTag();
  }, []);

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

  let [currentTag, setCurrentTag] = useState();

  function onClickTags(index) {
    if (currentTag === index) {
      setCurrentTag();
    } else {
      setCurrentTag(index);
      onClickTagButton(index);
    }
  }

  // function fetchFeedWithTag() {
  //   fetch(
  //     `https://nova-platform.kr/feed_explore/search_feed_with_hashtag?hashtag=${keyword}&key=-1`,
  //     {
  //       credentials: "include",
  //     }
  //   )
  //     .then((response) => response.json())
  //     .then((data) => {
  //       setFeedData(data.body.send_data);
  //       setNextData(data.body.key);
  //       setIsLoading(false);
  //     });
  // }

  return (
    <div className={style["keyword-container"]}>
      <div className={style["title-container"]}>
        {title} <span className={style["sub-title"]}>{subTitle}</span>
      </div>

      <div
        className={style["tags-container"]}
        ref={scrollRef}
        onMouseDown={onMouseDown}
        onMouseMove={onMouseMove}
        onMouseUp={onMouseUp}
      >
        <div className={style["tags-wrapper"]}>
          {bestTags.map((tag, i) => {
            return (
              <div
                key={i}
                onClick={() => onClickTags(i)}
                className={`${style["tags"]} ${currentTag === i ? style["click-tag"] : ""}`}
              >
                #{tag}
              </div>
            );
          })}
        </div>
      </div>
      {/* <div className={style["tags-container"]}>
        <div className={style["tags-wrapper"]}>
          <div className={style["tags"]}>tags</div>
          <div className={style["tags"]}>tags</div>
          <div className={style["tags"]}>tagddddds</div>
          <div className={style["tags"]}>tagddddds</div>
          <div className={style["tags"]}>tagddddddddddddddddssssss</div>
        </div>
      </div> */}
    </div>
  );
}
