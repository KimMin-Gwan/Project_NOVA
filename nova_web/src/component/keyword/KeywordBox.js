import Slider from "react-slick";
import style from "./KeywordBox.module.css";
import { useEffect, useRef, useState } from "react";
import axios from "axios";

export default function KeywordBox({ type, title, subTitle, onClickTagButton }) {
  let [bestTags, setBestTags] = useState([]);
  let [isLoading, setIsLoading] = useState(true);

  async function fetchHashTags() {
    if (type === "today") {
      await fetch("https://nova-platform.kr/home/today_spiked_hot_hashtag", {
        credentials: "include",
      })
        .then((res) => res.json())
        .then((data) => {
          setBestTags(data.body.hashtags);
          setIsLoading(false);
          console.log("today", data);
        });
    } else if (type === "weekly") {
      await axios
        .get("https://nova-platform.kr/home/weekly_spiked_hot_hashtag", {
          withCredentials: true,
        })
        .then((res) => {
          setBestTags(res.data.body.hashtags);
          setIsLoading(false);
          console.log("weekly", res.data);
        });
    }
  }

  useEffect(() => {
    fetchHashTags();
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
    </div>
  );
}
