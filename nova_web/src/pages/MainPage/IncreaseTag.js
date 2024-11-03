import { useEffect, useState } from "react";
import style from "./MainPart.module.css";

import one from './../../img/1.png'
import two from './../../img/2.png'
import three from './../../img/3.png'
import four from './../../img/4.png'
import five from './../../img/5.png'
import six from './../../img/6.png'
import seven from './../../img/7.png'
import eight from './../../img/8.png'
import nine from './../../img/9.png'
import ten from './../../img/10.png'

let imgList = [one, two, three, four, five, six, seven, eight, nine, ten];
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
                    <div className={style["ranking-img"]}>
                      <img src={imgList[i]} alt="img"></img>
                    </div>
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
