import style_sub from "./../DuckFunding/DuckFunding.module.css";
import style from "./MoreSeeFunding.module.css";
import backword from "./../../../img/back_icon.png";
import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";

export default function RecommendAll() {
  let navigate = useNavigate();
  function handleLinkClick(url) {
    navigate(url);
  }
  return (
    <div className={style_sub.container}>
      <header className={style_sub.Topbar}>
        <img src={backword} alt="Arrow" className={style_sub.backword} onClick={() => handleLinkClick(-1)} />
        <div className={style_sub.title}>최애펀딩</div>
        <div className={style_sub.EmptyBox} />
      </header>

      <section className={`${style_sub["success-funding"]} ${style["success-funding"]}`}>
        <div className={`${style_sub["content-title"]} ${style["content-title"]}`}>
          <header className={style_sub["header-text"]}>추천하는 프로젝트</header>
        </div>
        <hr className={style["hr-style"]} />
        <ul>
          <li>
            <div className={style["project-list"]}>
              <div className={style["pj-img"]}>이미지</div>
              <div className={style["pj-des"]}>
                <p>참여형</p>
                <h4>하꼬 버트버 키링 굿즈 제작 프로젝트</h4>
                <p>천유정</p>
                <p>12월 30일까지</p>
                <p>80% 달성</p>
                <button>상세정보</button>
              </div>
            </div>
          </li>
          <hr className={style["hr-style"]} />
          <li>
            <div className={style["project-list"]}>
              <div className={style["pj-img"]}>이미지</div>
              <div className={style["pj-des"]}>
                <p>참여형</p>
                <h4>하꼬 버트버 키링 굿즈 제작 프로젝트</h4>
                <p>천유정</p>
                <p>12월 30일까지</p>
                <p>80% 달성</p>
                <button>상세정보</button>
              </div>
            </div>
          </li>
          <hr className={style["hr-style"]} />
          <li>
            <div className={style["project-list"]}>
              <div className={style["pj-img"]}>이미지</div>
              <div className={style["pj-des"]}>
                <p>참여형</p>
                <h4>하꼬 버트버 키링 굿즈 제작 프로젝트</h4>
                <p>천유정</p>
                <p>12월 30일까지</p>
                <p>80% 달성</p>
                <button>상세정보</button>
              </div>
            </div>
          </li>
          <hr className={style["hr-style"]} />
          <li>
            <div className={style["project-list"]}>
              <div className={style["pj-img"]}>이미지</div>
              <div className={style["pj-des"]}>
                <p>참여형</p>
                <h4>하꼬 버트버 키링 굿즈 제작 프로젝트</h4>
                <p>천유정</p>
                <p>12월 30일까지</p>
                <p>80% 달성</p>
                <button>상세정보</button>
              </div>
            </div>
          </li>
          <hr className={style["hr-style"]} />
          <li>
            <div className={style["project-list"]}>
              <div className={style["pj-img"]}>이미지</div>
              <div className={style["pj-des"]}>
                <p>참여형</p>
                <h4>하꼬 버트버 키링 굿즈 제작 프로젝트</h4>
                <p>천유정</p>
                <p>12월 30일까지</p>
                <p>80% 달성</p>
                <button>상세정보</button>
              </div>
            </div>
          </li>
          <hr className={style["hr-style"]} />
          <li>
            <div className={style["project-list"]}>
              <div className={style["pj-img"]}>이미지</div>
              <div className={style["pj-des"]}>
                <p>참여형</p>
                <h4>하꼬 버트버 키링 굿즈 제작 프로젝트</h4>
                <p>천유정</p>
                <p>12월 30일까지</p>
                <p>80% 달성</p>
                <button>상세정보</button>
              </div>
            </div>
          </li>
          <hr className={style["hr-style"]} />
        </ul>
        <button className={style["moresee_button"]}>더보기</button>
      </section>
    </div>
  );
}
