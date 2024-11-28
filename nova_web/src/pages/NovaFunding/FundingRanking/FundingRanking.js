import style from "./../FundingRanking/FundingRanking.module.css";
import main_style from "./../NovaFunding.module.css";
import backword from "./../../../img/back_icon.png";
import { useNavigate } from "react-router-dom";
import React, { useState } from "react";
export default function DuckFunding() {
  let navigate = useNavigate();

  function handleLinkClick(url) {
    navigate(url);
  }

  return (
    <div className={style.container}>
      <header className={style.Topbar}>
        <img src={backword} alt="Arrow" className={style.backword} onClick={() => handleLinkClick(-1)} />
        <div className={style.title}>펀딩 랭킹</div>
        <div className={style.EmptyBox} />
      </header>

      <div className={style["top-menu"]}>
        <button className={style["top-button"]}>가격 순위</button>
        <button className={style["top-button"]}>최단기간 성공</button>
        <button className={style["top-button"]}>최다인원 참여</button>
      </div>

      <section className={main_style["best-funding"]}>
        <div className={`${main_style["funding-main"]} ${style["funding-main"]}`}>
          <h4>1위</h4>
          <div className={main_style["album-area"]}>
            <div className={main_style["album-img"]}></div>
            <p>앨범 이름</p>
          </div>
          <div className={main_style["more-container"]}>
            <p>별별 티켓 | 180,000개</p>
            <p>펀딩 가능 기간 | 24/05/16 까지</p>
            <p>87,500개 투자됨</p>
            <div className={main_style["progress-bar"]}>
              <progress value="70" max="100"></progress>
              <p>70%</p>
            </div>
            <button>자세히보기</button>
          </div>
        </div>
        <div className={`${main_style["funding-main"]} ${style["funding-main"]}`}>
          <h4>2위</h4>
          <div className={main_style["album-area"]}>
            <div className={main_style["album-img"]}></div>
            <p>앨범 이름</p>
          </div>
          <div className={main_style["more-container"]}>
            <p>별별 티켓 | 180,000개</p>
            <p>펀딩 가능 기간 | 24/05/16 까지</p>
            <p>87,500개 투자됨</p>
            <div className={main_style["progress-bar"]}>
              <progress value="70" max="100"></progress>
              <p>70%</p>
            </div>
            <button>자세히보기</button>
          </div>
        </div>
      </section>
    </div>
  );
}
