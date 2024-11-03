import { useEffect, useState } from "react";
import style from "./MainPart.module.css";

export default function IncreaseTag() {
  let [tagList, setTagList] = useState([]);

  function fetchTagData() {
    fetch('https://nova-platform.kr/home/realtime_best_hashtag', {
      credentials: "include",
    })
      .then(response => response.json())
      .then(data => {
        setTagList(data.body.hashtags)
      })
  }

  useEffect(() => {
    fetchTagData();
  }, [])
  
  return (
    <div className={style["wrap-container"]}>
      <div className={style["top-area"]}>
        <div className={style["content-title"]}>
          <header>급상승 해시태그</header>
          {/* <div>화살표</div> */}
        </div>
      </div>

      <div className={style["main-area"]}>
        <div className={style["hashtag-box"]}>
          <span className={style["time-text"]}>13:00 기준</span>
          <ol className={style["ranking-container"]}>
            {
              tagList.map((tag, i) => {
                return (
                  <li key={i} className={style["ranking-box"]}>
                    <div className={style["ranking"]}>{i+1}위</div>
                    <div className={style["ranking-name"]}>{tag}</div>
                  </li>
                )
              })
            }
          </ol>
        </div>
      </div>
    </div>
  );
}
