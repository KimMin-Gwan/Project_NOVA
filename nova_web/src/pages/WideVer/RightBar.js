import style from "./WideVer.module.css";
import style_hash from "./../MainPage/MainPart.module.css";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import one from "./../../img/1.png";
import two from "./../../img/2.png";
import three from "./../../img/3.png";
import four from "./../../img/4.png";
import five from "./../../img/5.png";
import six from "./../../img/6.png";
import seven from "./../../img/7.png";
import eight from "./../../img/8.png";
import nine from "./../../img/9.png";
import ten from "./../../img/10.png";
let imgList = [one, two, three, four, five, six, seven, eight, nine, ten];

export default function RightBar({ brightMode }) {
  let [tagList, setTagList] = useState([]);

  function fetchTagData() {
    fetch("https://nova-platform.kr/home/realtime_best_hashtag", {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setTagList(data.body.hashtags);
      });
  }

  useEffect(() => {
    fetchTagData();
  }, []);

  return (
    <div className={style["wrap_container"]}>
      <div className={`${style["hashtag-box"]} ${brightMode === "dark" ? style["dark-mode"] : style["light-mode"]}`}>
        <div className={style["top-bar"]}>
          <header className={style["wide-text"]}>급상승 해시태그</header>
          <span className={style_hash["time-text"]}>13:00 기준</span>
        </div>
        <ol className={style_hash["ranking-container"]}>
          {tagList.map((tag, i) => {
            return (
              <li key={i} className={`${style_hash["ranking-box"]} ${style["ranking-box-w"]}`}>
                <div className={style_hash["ranking-img"]}>
                  <img src={imgList[i]} alt="img"></img>
                </div>
                <div className={style_hash["ranking-name"]}>{tag}</div>
              </li>
            );
          })}
        </ol>
      </div>

      <div className={style["ad-container"]}>광고</div>
    </div>
  );
}
