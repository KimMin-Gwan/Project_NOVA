import style from "./WideVer.module.css";
import popular_icon from "./../../img/polular_feed.png";
import feed_write from "./../../img/feed_write.png";
import home_icon from "./../../img/home_icon.png";
import all_icon from "./../../img/all_icon.png";
import short_icon from "./../../img/short_icon.png";
import search_icon from "./../../img/search_icon.png";
import direct_icon from "./../../img/direct_icon.png";
import { useNavigate } from "react-router-dom";
// import popular_feed from "./../FeedList/FeedList";
// import NovaFunding from "./../NovaFunding/NovaFunding.js";
import { Link } from "react-router-dom";
export default function LeftBar({ brightMode }) {
  let navigate = useNavigate();

  function handleNavigate(page) {
    navigate(page); // "/about" 페이지로 이동
  }

  return (
    <div className={`${style["wrap_container"]} ${brightMode === "dark" ? style["dark-mode"] : style["light-mode"]}`}>
      <div className={`${style["direct-box"]} ${brightMode === "dark" ? style["dark-mode"] : style["light-mode"]}`}>
        <h4 className={style["wide-text"]}>바로가기</h4>
        <ul className={style["direct-list"]}>
          <li className={style["list-item"]}>
            <img src={home_icon} alt="home" className={style["icon-text"]}></img>
            <div
              className={`${style["direct-link"]} ${brightMode === "dark" ? style["dark-mode"] : style["light-mode"]}`}
              onClick={() => {
                handleNavigate("/");
              }}
            >
              플랫폼 홈
            </div>
          </li>
          <li className={style["list-item"]}>
            <img src={all_icon} alt="전체 피드" className={style["icon-text"]}></img>
            <div
              className={`${style["direct-link"]} ${brightMode === "dark" ? style["dark-mode"] : style["light-mode"]}`}
              onClick={() => {
                handleNavigate("/");
              }}
            >
              전체 피드
            </div>
          </li>
          <li className={style["list-item"]}>
            <img src={short_icon} alt="short_feed" className={style["icon-text"]}></img>
            <div
              className={`${style["direct-link"]} ${brightMode === "dark" ? style["dark-mode"] : style["light-mode"]}`}
              onClick={() => {
                handleNavigate("/feed_page");
              }}
            >
              숏피드
            </div>
          </li>
          <li className={style["list-item"]}>
            <img src={feed_write} alt="write" className={style["icon-text"]}></img>
            <div
              className={`${style["direct-link"]} ${brightMode === "dark" ? style["dark-mode"] : style["light-mode"]}`}
              onClick={() => {
                handleNavigate("/write_feed");
              }}
            >
              피드 작성
            </div>
          </li>
          <li className={style["list-item"]}>
            <img src={popular_icon} alt="popular" className={style["icon-text"]}></img>
            <div
              className={`${style["direct-link"]} ${brightMode === "dark" ? style["dark-mode"] : style["light-mode"]}`}
              onClick={() => {
                handleNavigate("/feed_list");
              }}
            >
              인기 피드
            </div>
          </li>
        </ul>
      </div>

      <div className={style["nova_direct-box"]}>
        <img src={direct_icon} alt="노바펀딩 바로가기" className={style["icon-text"]}></img>
        <Link to="/nova_funding" className={style["go-nova"]}>
          노바펀딩 바로가기
        </Link>
      </div>

      <div className={`${style["search-box"]} ${brightMode === "dark" ? style["dark-mode"] : style["light-mode"]}`}>
        <h4 className={style["wide-text"]}>검색</h4>
        <div className={style["search-bar"]}>
          <input></input>
          <button>
            <img src={search_icon} className={style["icon-text"]}></img>
          </button>
        </div>
        <span className={style["search-memo"]}>
          <p>검색기록</p>
          <p>X</p>
        </span>
      </div>
    </div>
  );
}
