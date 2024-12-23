import style_sub from "./../../WideVer/WideVer.module.css";
import style from "./WideFunding.module.css";
import popular_icon from "./../../../img/polular_feed.png";
import feed_write from "./../../../img/feed_write.png";
import home_icon from "./../../../img/home_icon.png";
import all_icon from "./../../../img/all_icon.png";
import short_icon from "./../../../img/short_icon.png";
import direct_icon from "./../../../img/direct_icon.png";
import search_icon from "./../../../img/search_icon.png";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

export default function LeftBarF({ brightMode }) {
  let navigate = useNavigate();

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

  function handleNavigate(page) {
    navigate(page);
  }

  return (
    <div className={`${style_sub["wrap_container"]} `}>
      <div className={`${style_sub["direct-box"]} `}>
        <h4 className={style_sub["wide-text"]}>바로가기</h4>
        <ul className={style_sub["direct-list"]}>
          <li
            className={style_sub["list-item"]}
            onClick={() => {
              handleNavigate("/");
            }}
          >
            <img src={home_icon} alt="home" className={style_sub["icon-text"]}></img>
            <div className={`${style_sub["direct-link"]} `}>플랫폼 홈</div>
          </li>
          <li
            className={style_sub["list-item"]}
            onClick={() => {
              handleNavigate("/feed_list?type=all");
            }}
          >
            <img src={all_icon} alt="전체 피드" className={style_sub["icon-text"]}></img>
            <div className={`${style_sub["direct-link"]} `}>전체 피드</div>
          </li>
          <li
            className={style_sub["list-item"]}
            onClick={() => {
              handleNavigate("/feed_page");
            }}
          >
            <img src={short_icon} alt="short_feed" className={style_sub["icon-text"]}></img>
            <div className={`${style_sub["direct-link"]} `}>숏피드</div>
          </li>
          <li
            className={style_sub["list-item"]}
            onClick={() => {
              handleNavigate("/write_feed");
            }}
          >
            <img src={feed_write} alt="write" className={style_sub["icon-text"]}></img>
            <div className={`${style_sub["direct-link"]} `}>피드 작성</div>
          </li>
          <li
            className={style_sub["list-item"]}
            onClick={() => {
              handleNavigate("/feed_list?type=weekly_best");
            }}
          >
            <img src={popular_icon} alt="popular" className={style_sub["icon-text"]}></img>
            <div className={`${style_sub["direct-link"]} `}>주간 TOP 100</div>
          </li>
        </ul>
      </div>

      <div className={style_sub["nova_direct-box"]}>
        <img src={direct_icon} alt="노바펀딩 바로가기" className={style_sub["icon-text"]}></img>
        <Link to="/" className={style_sub["go-nova"]}>
          노바 플랫폼 바로가기
        </Link>
      </div>

      <div
        className={`${style["search-box"]} ${
          brightMode === "dark" ? style["dark-mode"] : style["light-mode"]
        }`}
      >
        <h4 className={style["wide-text"]}>검색</h4>
        <div className={style["search-bar"]}>
          <input type="text"></input>
          <button onClick={handleNavigate}>
            <img src={search_icon} className={style["icon-text"]}></img>
          </button>
        </div>
        <span className={style["search-memo"]}>
          <p>검색기록</p>
        </span>
      </div>
    </div>
  );
}
