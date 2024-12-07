import style_sub from "./../../WideVer/WideVer.module.css";
import style_sub2 from "./../NovaFunding.module.css"
import style from "./WideFunding.module.css";
import more_icon from "./../../../img/back.png";


import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

export default function RightBarF() {
  let navigate = useNavigate();

  let [tagList, setTagList] = useState([]);

  function fetchTagData() {
    fetch("https://nova-platform.kr/home/realtime_best_hashtag", {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setTagList(data.body.hashtags);
      });
  }

  useEffect(() => {
    fetchTagData();
  }, []);

  function handleNavigate(page) {
    navigate(page);
  }

  return (
    <div className={`${style_sub["wrap_container"]} ${style["wrap_container"]}`}>

      <section className={`${style_sub2["recommend-box"]} ${style["recommend-box"]}`}>
          <div className={style_sub2["title-box"]}>
            <h2 className={style_sub2["title-text"]}>베스트 프로젝트 모두 보기</h2>
          </div>
          <p className={style_sub2["more-text"]}>지금까지 펀딩된 프로젝트와 투자자들을 알아봐요!</p>

          <div className={`${style_sub2["ad-container"]} ${style["ad-container"]}`}>
            <div className={style_sub2["ad-box"]}>
              <div className={style_sub2["img"]}>이미지</div>
              <p className={style_sub2["ad-title"]}>프로젝트 펀딩 순위</p>

              <p>72% 달성했어요</p>
            </div>
            <div className={style_sub2["ad-box"]}>
              <div className={style_sub2["img"]}>이미지</div>
              <p className={style_sub2["ad-title"]}>프로젝트 펀딩 순위</p>

              <p>72% 달성했어요</p>
            </div>
            <div className={style_sub2["ad-box"]}>
              <div className={style_sub2["img"]}>이미지</div>
              <p className={style_sub2["ad-title"]}>프로젝트 펀딩 순위</p>

              <p>총 10개의 프로젝트가 있어요.</p>
            </div>
          </div>
        </section>


        <section className={`${style_sub2["notice-nova"]} ${style["notice-nova"]}`}>
          
            <div className={style_sub2["title-box"]}>
              <h2 className={style_sub2["title-text"]}>노바 펀딩 알아보기</h2>
              <img src={more_icon} className={style_sub2["more-icon"]}></img>
            </div>
            <p className={style_sub2["more-text"]}>30초만에 알아보는 노바 펀딩</p>
  
            <div className={`${style_sub2["ad-container"]} ${style["ad-container"]}`}>
              <div className={style_sub2["ad-box"]}>
                <div className={style_sub2["img"]}>이미지</div>
                <p className={style_sub2["ad-title"]}>프로젝트 펀딩 순위</p>
  
                <p>10명이 읽었어요!</p>
              </div>
              <div className={style_sub2["ad-box"]}>
                <div className={style_sub2["img"]}>이미지</div>
                <p className={style_sub2["ad-title"]}>프로젝트 펀딩 순위</p>
  
                <p>1명이 읽었어요!</p>
              </div>
              <div className={style_sub2["ad-box"]}>
                <div className={style_sub2["img"]}>이미지</div>
                <p className={style_sub2["ad-title"]}>프로젝트 펀딩 순위</p>
  
                <p>1명이 읽었어요!</p>
              </div>
            </div>
            </section>

            <section className={`${style_sub2["notice-nova"]} ${style["notice-nova"]} ${style["my-funding"]}`}>
            <div className={style_sub2["footer-area"]}>
              <div className={style_sub2["area-box"]}>참여한 펀딩</div>
              <div className={style_sub2["area-box"]}>
                펀딩 신청<br></br>
              </div>
            </div>
  
            <div className={style_sub2["last-project"]}>지난 펀딩 프로젝트</div>
         
        </section>
    </div>
  );
}
