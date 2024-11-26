import style from "./DuckFunding.module.css";
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
        <div className={style.title}>덕질펀딩</div>
        <div className={style.EmptyBox} />
      </header>
     
      <section className={style["success-funding"]}>
       <div className={style["content-title"]}>
          <header className={style["header-text"]}>이미 목표 달성에 성공한 프로젝트</header>
        
        </div>

        <div className={style["best-container"]}>
          <div className={style["best-box"]}>
            <div className={style["best-img"]}>이미지</div>
            <p className={style["best-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지 (1일 남음)</p>
            <p>72% 달성</p>
          </div>
          <div className={style["best-box"]}>
            <div className={style["best-img"]}>이미지</div>
            <p className={style["best-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지 (1일 남음)</p>
            <p>72% 달성</p>
          </div>
          <div className={style["best-box"]}>
            <div className={style["best-img"]}>이미지</div>
            <p className={style["best-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지 (1일 남음)</p>
            <p>72% 달성</p>
          </div>
          <div className={style["best-box"]}>
            <div className={style["best-img"]}>이미지</div>
            <p className={style["best-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지 (1일 남음)</p>
            <p>72% 달성</p>
          </div>
          <div className={style["best-box"]}>
            <div className={style["best-img"]}>이미지</div>
            <p className={style["best-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지 (1일 남음)</p>
            <p>72% 달성</p>
          </div>
          <div className={style["best-box"]}>
            <div className={style["best-img"]}>이미지</div>
            <p className={style["best-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지 (1일 남음)</p>
            <p>72% 달성</p>
          </div>
          <div className={style["best-box"]}>
            <div className={style["best-img"]}>이미지</div>
            <p className={style["best-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지 (1일 남음)</p>
            <p>72% 달성</p>
          </div>
          <div className={style["best-box"]}>
            <div className={style["best-img"]}>이미지</div>
            <p className={style["best-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지 (1일 남음)</p>
            <p>72% 달성</p>
          </div>
          <div className={style["best-box"]}>
            <div className={style["best-img"]}>이미지</div>
            <p className={style["best-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지 (1일 남음)</p>
            <p>72% 달성</p>
          </div>
          <div className={style["best-box"]}>
            <div className={style["best-img"]}>이미지</div>
            <p className={style["best-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지 (1일 남음)</p>
            <p>72% 달성</p>
          </div>
         
        </div>

        <button className={style["more-button"]}>더보기</button>
      </section>  

      
    </div>
  );
}
