import React, { useState } from "react";
import style from "./MainPart.module.css";

export default function MainPart() {
  const [isActive, setIsActive] = useState(false); // 버튼의 상태를 관리

  const handleClick = () => {
    setIsActive((prev) => !prev); // 상태 토글
  };

  return (
    <div className={style["wrap-container"]}>
      <div className={style["top-area"]}>
        <div className={style["content-title"]}>
          <header>[ 시연 ] 관련 인기 해시태그</header>
          <div>화살표</div>
        </div>
        <div className={style["tag-container"]}>
          <button
            className={style["hashtag-text"]}
            onClick={handleClick}
            style={{
              backgroundColor: isActive ? "#051243" : "#373737",
              cursor: "pointer",
            }}
          >
            #시연시연시연시연시연
          </button>
        </div>
      </div>

      <div className={style["main-area"]}>
        <div className={style["feed-box"]}>
          <div className={style["name-container"]}>
            <div className={style["profile"]}> </div>
            <h2 className={style["name-text"]}>익명 바위게</h2>
            <button className={style["more-see"]}>더보기</button>
          </div>
          <section className={style["text-container"]}>
            <div className={style["tag-text"]}>
              <span className={style["tag"]}>#시연</span>
              <span className={style["tag"]}>#이쁘다</span>
            </div>
            <div className={style["main-text"]}>젠타 나이 질문이요 젠타 98년생 아닌가요??</div>
          </section>

          <footer className={style["like-comment"]}>좋아요 수 댓글 수</footer>
        </div>
      </div>
    </div>
  );
}
