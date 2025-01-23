import Slider from "react-slick";
import style from "./KeywordBox.module.css";
import { useEffect, useRef, useState } from "react";
import axios from "axios";

export default function KeywordBox({ type, title, subTitle, onClickTagButton }) {
  let [bestTags, setBestTags] = useState([]);
  let [isLoading, setIsLoading] = useState(true);
  console.log(type);

  // function fetchBestTag() {
  //   fetch(`https://nova-platform.kr/home/realtime_best_hashtag`, { credentials: "include" })
  //     .then((response) => response.json())
  //     .then((data) => {
  //       setBestTags(data.body.hashtags);
  //     });
  // }

  // useEffect(() => {
  //   fetchBestTag();
  // }, []);

  async function fetchTodayBest() {
    await fetch("https://nova-platform.kr/home/today_spiked_hot_hashtag", {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => {
        setBestTags(data.body.hashtags);
        setIsLoading(false);
        console.log("today", data);
      });
  }

  useEffect(() => {
    if (type === "today") {
      fetchTodayBest();
    } else if (type === "weekly") {
      fetchWeeklyBest();
    }
  }, []);

  async function fetchWeeklyBest() {
    await axios
      .get("https://nova-platform.kr/home/weekly_spiked_hot_hashtag", {
        withCredentials: true,
      })
      .then((res) => {
        setBestTags(res.data.body.hashtags);
        setIsLoading(false);
        console.log("ddd", res.data);
      });
  }

  // useEffect(() => {

  // }, []);

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
