import style from "./WideVer.module.css";
import style_hash from "./../MainPage/MainPart.module.css";
import galaxy from "./../../img/galaxy.png";
import popular_icon from "./../../img/polular_feed.png";
import feed_write from "./../../img/feed_write.png";
import home_icon from "./../../img/home_icon.png";
import all_icon from "./../../img/all_icon.png";
import short_icon from "./../../img/short_icon.png";
import search_icon from "./../../img/search_icon.png";
import { useNavigate } from "react-router-dom";
import popular_feed from "./../FeedList/FeedList";
import NovaFunding from "./../NovaFunding/NovaFunding.js";
import { Link } from "react-router-dom";
export default function LeftBar() {
  let navigate = useNavigate();

  let handleClick = (page) => {
    navigate("/about"); // "/about" 페이지로 이동
  };

  return (
    <div className={style["wrap_container"]}>
      <div className={style["direct-box"]}>
        <h4 className={style["wide-text"]}>바로가기</h4>
        <ul className={style["direct-list"]}>
          <li className={style["list-item"]}>
            <img src={home_icon} className={style["icon-text"]}></img>
            <a href="/" className={style["direct-link"]}>
              플랫폼 홈
            </a>
          </li>
          <li className={style["list-item"]}>
            <img src={all_icon} className={style["icon-text"]}></img>
            <a href="/" className={style["direct-link"]}>
              전체 피드
            </a>
          </li>
          <li className={style["list-item"]}>
            <img src={short_icon} className={style["icon-text"]}></img>
            <a href="/" className={style["direct-link"]}>
              숏피드
            </a>
          </li>
          <li className={style["list-item"]}>
            <img src={feed_write} className={style["icon-text"]}></img>
            <a href="/" className={style["direct-link"]}>
              피드 작성
            </a>
          </li>
          <li className={style["list-item"]}>
            <img src={popular_icon} className={style["icon-text"]}></img>
            <a href="/" className={style["direct-link"]}>
              인기 피드
            </a>
          </li>
        </ul>
      </div>

      <Link to="/nova_funding" className={style["go-nova"]}>
        노바펀딩 바로가기
      </Link>

      <div className={style["search-box"]}>
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