import { useEffect, useState } from "react";
import style from "./MainPart.module.css";
import more_icon from "./../../img/backword.png";
import { useNavigate } from "react-router-dom";
import { getModeClass } from "./../../App.js";
export default function AllPost({ brightMode }) {
  let navigate = useNavigate();
  const [mode, setMode] = useState(brightMode); // 초기 상태는 부모로부터 받은 brightMode 값
  useEffect(() => {
    setMode(brightMode); // brightMode 값이 바뀔 때마다 mode 업데이트
  }, [brightMode]);
  return (
    <div className={style["wrap-container"]}>
      <div className={`${style["top-area"]} ${style[getModeClass(mode)]}`}>
        <div className={style["content-title"]}>
          <header className={style["header-text"]}>전체 글</header>
        </div>
        <div className={`${style["main-area"]} ${style["all-main-area"]} ${style[getModeClass(mode)]}`}>
          <ul className={`${style["all-list"]} ${style[getModeClass(mode)]}`}>
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
          <button onClick={() => navigate("/feed_list?type=all")} className={style["all_see-button"]}>
            전체보기
          </button>
        </div>
      </div>
    </div>
  );
}
