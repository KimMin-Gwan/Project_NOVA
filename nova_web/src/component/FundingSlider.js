import "./slider.css";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import s_style from "./FundingSlider.module.css";
import style from "./../pages/NovaFunding/NovaFunding.module.css";
import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";

import { getModeClass } from "./../App.js";
import ProgressBar from "./ProgressBar.js";
const FundingSlider = ({ biasProjects, brightMode }) => {
  const showMaxCnt = 1;

  const settings = {
    className: "slider-items",
    dots: true,
    infinite: biasProjects.length > showMaxCnt,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    centerMode: true,
    centerPadding: "0px",
    arrows: false,
  };
  // style안붙은 것은 slider.css에서 수정
  let navigate = useNavigate();

  function onClickMore(fid) {
    navigate(`/feed_page?fid=${fid}`);
  }

  const [mode, setMode] = useState(brightMode); // 초기 상태는 부모로부터 받은 brightMode 값
  useEffect(() => {
    setMode(brightMode); // brightMode 값이 바뀔 때마다 mode 업데이트
  }, [brightMode]);

  return (
    <div
      className={`${s_style["slider-container"]} ${
        brightMode === "dark" ? "dark-mode" : "bright-mode"
      }`}
    >
      <Slider {...settings}>
        {biasProjects.map((project, i) => {
          return (
            <div key={project.pid + i} className={style["funding-main"]}>
              {/*  
              {style["album-area"]}*/}
              <div className={` ${style["album-area"]}`}>
                <div className={style["album-img"]}>
                  <img src={`${project.head_image[0]}`} />
                </div>
                <p>{project.pname}</p>
              </div>
              <div className={style["more-container"]}>
                <p>별별 티켓 | {project.goal_progress}개</p>
                <p>펀딩 가능 기간 | {project.expire_date} 까지</p>
                <p>{project.now_progress}개 투자됨</p>
                <div className={style["progress-bar"]}>
                  <ProgressBar point={project.int_progress} />
                  {/* <progress value="70" max="100"></progress> */}
                  <p>{project.int_progress}%</p>
                </div>
                <button className={style["moresee-btn"]}>자세히보기</button>
              </div>
            </div>
          );
        })}
      </Slider>
    </div>
  );
};

export default FundingSlider;
