import { useEffect, useState } from "react";
import style from "./MainPart.module.css";
import more_icon from "./../../img/backword.png";
import { useNavigate } from "react-router-dom";
export default function AllPost() {
  let navigate = useNavigate();

  return (
    <div className={style["wrap-container"]}>
      <div className={style["top-area"]}>
        <div className={style["content-title"]}>
          <header className={style["header-text"]}>전체 글</header>
          <img src={more_icon} alt="more_icon" className={style["more-icon"]} onClick={() => navigate("/feed_list?type=all")} />
        </div>
        <div className={`${style["main-area"]} ${style["all-main-area"]}`}>
          <ul className={style["all-list"]}>
            <li>
              <div className={style["all-img"]}>이미지</div>
              <div className={style["all-text"]}>
                <span># 해시태그</span>
                <p>충주맨이 말하는 공무원 과장님 모시는 방법</p>
                <footer className={style["like-comment"]}>좋아요 250개 | 댓글 20개</footer>
              </div>
            </li>
            <li>
              <div className={style["all-img"]}>이미지</div>
              <div className={style["all-text"]}>
                <span># 해시태그</span>
                <p>충주맨이 말하는 공무원 과장님 모시는 방법</p>
                <footer className={style["like-comment"]}>좋아요 250개 | 댓글 20개</footer>
              </div>
            </li>
            <li>
              <div className={style["all-img"]}>이미지</div>
              <div className={style["all-text"]}>
                <span># 해시태그</span>
                <p>충주맨이 말하는 공무원 과장님 모시는 방법</p>
                <footer className={style["like-comment"]}>좋아요 250개 | 댓글 20개</footer>
              </div>
            </li>
            <li>
              <div className={style["all-img"]}>이미지</div>
              <div className={style["all-text"]}>
                <span># 해시태그</span>
                <p>충주맨이 말하는 공무원 과장님 모시는 방법</p>
                <footer className={style["like-comment"]}>좋아요 250개 | 댓글 20개</footer>
              </div>
            </li>
            <li>
              <div className={style["all-img"]}>이미지</div>
              <div className={style["all-text"]}>
                <span># 해시태그</span>
                <p>충주맨이 말하는 공무원 과장님 모시는 방법</p>
                <footer className={style["like-comment"]}>좋아요 250개 | 댓글 20개</footer>
              </div>
            </li>
          </ul>
          <button className={style["all_see-button"]}>전체보기</button>
        </div>
      </div>
    </div>
  );
}
