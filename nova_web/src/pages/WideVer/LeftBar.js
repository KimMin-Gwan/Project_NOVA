import style from "./WideVer.module.css";
import style_hash from "./../MainPage/MainPart.module.css";
import galaxy from "./../../img/galaxy.png";
import { useNavigate } from "react-router-dom";
import popular_feed from "./../FeedList/FeedList";
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
          <li>
            <a href="/" className={style["direct-link"]}>
              플랫폼 홈
            </a>
          </li>
          <li>
            <a href="/" className={style["direct-link"]}>
              전체 피드
            </a>
          </li>
          <li>
            <a href="/" className={style["direct-link"]}>
              숏피드
            </a>
          </li>
          <li>
            <a href="/" className={style["direct-link"]}>
              피드 작성
            </a>
          </li>
          <li>
            <a href="/" className={style["direct-link"]}>
              인기 피드
            </a>
          </li>
        </ul>
      </div>
      <a href="./../" className={style["go-nova"]}>
        노바펀딩 바로가기
      </a>

      <div className={style["search-box"]}>
        <h4 className={style["wide-text"]}>검색</h4>
        <div className={style["search-bar"]}>
          <input></input>
          <div>돋보기</div>
        </div>
        <span className={style["search-memo"]}>
          <p>검색기록</p>
          <p>엑스</p>
        </span>
      </div>
    </div>
  );
}
