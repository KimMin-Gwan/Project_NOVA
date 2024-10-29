import style from "./WideVer.module.css";
import style_hash from "./../MainPage/MainPart.module.css";
import galaxy from "./../../img/galaxy.png";
export default function LeftBar() {
  return (
    <div className={style["wrap_container"]}>
      <div className={style["direct-box"]}>
        바로가기
        <ul className={style["direct-list"]}>
          <li className={style["direct-text"]}>플랫폼 홈</li>
          <li className={style["direct-text"]}>전체 피드</li>
          <li className={style["direct-text"]}>숏피드</li>
          <li className={style["direct-text"]}>피드 작성</li>
          <li className={style["direct-text"]}>인기 피드</li>
        </ul>
      </div>
      <a href="./../" className={style["go-nova"]}>
        노바펀딩 바로가기
      </a>

      <div className={style["search-box"]}>
        검색
        <div className={style["search-bar"]}>
          <input></input>
          <div>돋보기</div>
        </div>
        <span>검색기록</span>
      </div>
    </div>
  );
}
