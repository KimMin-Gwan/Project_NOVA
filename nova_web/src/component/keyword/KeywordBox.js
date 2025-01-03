import Slider from "react-slick";
import style from "./KeywordBox.module.css";
import { useEffect, useState } from "react";

export default function KeywordBox({ title, subTitle }) {
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

  return (
    <div className={style["keyword-container"]}>
      <div className={style["title-container"]}>
        {title} <span className={style["sub-title"]}>{subTitle}</span>
      </div>

      <div className={style["tags-container"]}>
        <div className={style["tags-wrapper"]}>
          {bestTags.map((tag, i) => {
            return (
              <div key={i} className={style["tags"]}>
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
