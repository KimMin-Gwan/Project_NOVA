import style from "./WideVer.module.css";
import style_hash from "./../MainPage/MainPart.module.css";
import popular_icon from "./../../img/polular_feed.png";
import feed_write from "./../../img/feed_write.png";
import home_icon from "./../../img/home_icon.png";
import all_icon from "./../../img/all_icon.png";
import short_icon from "./../../img/short_icon.png";
import search_icon from "./../../img/search_icon.png";
import direct_icon from "./../../img/direct_icon.png";
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
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
// import popular_feed from "./../FeedList/FeedList";
// import NovaFunding from "./../NovaFunding/NovaFunding.js";
let imgList = [one, two, three, four, five, six, seven, eight, nine, ten];
export default function LeftBar({ brightMode }) {
  let navigate = useNavigate();

  let [tagList, setTagList] = useState([]);

  function fetchTagData() {
    fetch("https://supernova.io.kr/home/realtime_best_hashtag", {
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

  function handleNavigate(page) {
    navigate(page);
  }

  return (
    <div
      className={`${style["wrap_container"]} ${
        brightMode === "dark" ? style["dark-mode"] : style["light-mode"]
      }`}
    >
      <div
        className={`${style["direct-box"]} ${
          brightMode === "dark" ? style["dark-mode"] : style["light-mode"]
        }`}
      >
        {/* <h4 className={style["wide-text"]}>바로가기</h4> */}
        <ul className={style["direct-list"]}>
          <li
            className={style["list-item"]}
            onClick={() => {
              handleNavigate("/");
            }}
          >
            <img src={home_icon} alt="home" className={style["icon-text"]}></img>
            <div
              className={`${style["direct-link"]} ${
                brightMode === "dark" ? style["dark-mode"] : style["light-mode"]
              }`}
            >
              플랫폼 홈
            </div>
          </li>
          <li
            className={style["list-item"]}
            onClick={() => {
              handleNavigate("/feed_list?type=all");
            }}
          >
            <img src={all_icon} alt="전체 피드" className={style["icon-text"]}></img>
            <div
              className={`${style["direct-link"]} ${
                brightMode === "dark" ? style["dark-mode"] : style["light-mode"]
              }`}
            >
              전체 피드
            </div>
          </li>
          <li
            className={style["list-item"]}
            onClick={() => {
              handleNavigate("/feed_page");
            }}
          >
            <img src={short_icon} alt="short_feed" className={style["icon-text"]}></img>
            <div
              className={`${style["direct-link"]} ${
                brightMode === "dark" ? style["dark-mode"] : style["light-mode"]
              }`}
            >
              숏피드
            </div>
          </li>
          <li
            className={style["list-item"]}
            onClick={() => {
              handleNavigate("/write_feed");
            }}
          >
            <img src={feed_write} alt="write" className={style["icon-text"]}></img>
            <div
              className={`${style["direct-link"]} ${
                brightMode === "dark" ? style["dark-mode"] : style["light-mode"]
              }`}
            >
              피드 작성
            </div>
          </li>
          <li
            className={style["list-item"]}
            onClick={() => {
              handleNavigate("/feed_list?type=weekly_best");
            }}
          >
            <img src={popular_icon} alt="popular" className={style["icon-text"]}></img>
            <div
              className={`${style["direct-link"]} ${
                brightMode === "dark" ? style["dark-mode"] : style["light-mode"]
              }`}
            >
              주간 TOP 100
            </div>
          </li>
        </ul>
      </div>

      <div
        className={`${style["hashtag-box"]} ${
          brightMode === "dark" ? style["dark-mode"] : style["light-mode"]
        }`}
      >
        <div className={style["top-bar"]}>
          <header className={style["wide-text"]}>급상승 해시태그</header>
          {/* <span className={style_hash["time-text"]}>13:00 기준</span> */}
        </div>
        <ol className={style_hash["ranking-container"]}>
          {tagList.map((tag, i) => {
            return (
              <li key={i} className={`${style_hash["ranking-box"]} ${style["ranking-box-w"]}`}>
                <div className={style_hash["ranking-img"]}>
                  <img src={imgList[i]} alt="img"></img>
                </div>
                <div
                  className={style_hash["ranking-name"]}
                  onClick={() => handleNavigate(`/feed_list?keyword=${tag}`)}
                >
                  {tag}
                </div>
              </li>
            );
          })}
        </ol>
      </div>
    </div>
  );
}
