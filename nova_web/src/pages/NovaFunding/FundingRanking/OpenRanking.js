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
        <button className={style["top-button"]}>최고 금액 랭킹</button>
        <button className={style["top-button"]}>분야 랭킹</button>
      </div>

      <section className={main_style["best-funding"]}>
        <div className={`${main_style["funding-main"]} ${style["funding-area"]}`}>
          <h4>1위</h4>
          <div className={style["album-area"]}>
            <div className={style["album-img"]}>이미지</div>

            <div className={style["more-container"]}>
              <p>신입 남자 아이돌 [언네임] 1집 앨범 펀딩</p>
              <p>뭐시기 MCU</p>
              <p>24/12/31 ~ 24/12/31</p>
              <p>23,300명 참여</p>
            </div>
          </div>
          <div className={style["funding-count"]}>
            <p>총 3,580,000개 펀딩됨</p>
            <p>(12508%)</p>
          </div>
          <button>자세히보기</button>
        </div>
      </section>
    </div>
  );
}
