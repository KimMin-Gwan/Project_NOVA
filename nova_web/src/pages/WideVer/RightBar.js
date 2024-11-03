import style from "./WideVer.module.css";
import style_hash from "./../MainPage/MainPart.module.css";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
export default function RightBar() {

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
  }, []);

  return (
    <div className={style["wrap_container"]}>
      <div className={style["hashtag-box"]}>
        <div className={style["top-bar"]}>
          <header className={style["wide-text"]}>급상승 해시태그</header>
          <span className={style_hash["time-text"]}>13:00 기준</span>
        </div>
        <ol className={style_hash["ranking-container"]}>
          {
            tagList.map((tag, i) => {
              return (
                <li key={i} className={style_hash["ranking-box"]}>
                  <div className={style_hash["ranking"]}>{i+1}위</div>
                  <div className={style_hash["ranking-name"]}>{tag}</div>
                </li>
              )
            })
          }

          
        </ol>
      </div>

      <div className={style["ad-container"]}>광고</div>
    </div>
  );
}
