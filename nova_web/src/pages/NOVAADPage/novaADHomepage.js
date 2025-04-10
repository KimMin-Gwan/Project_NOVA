import React, { useEffect, useState, useRef } from "react";
import styleFunding from "./../NovaFunding/BiasFunding/BiasFunding.module.css";

import shadow from "./../../img/shadow_funding.png";
import { useNavigate } from "react-router-dom";
import Slider from "react-slick";

import "./novaADHomepage.css";

export default function NovaADHomepage() {
  const settings = {
    variableWidth: true,
    dots: false,
    infinite: false,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 1,
    arrows: false,
    focusOnSelect: true,
  };

  let [newProjects, setNewProjects] = useState([]);
  let [isLoading, setIsLoading] = useState(true);
  const numberOfBoxes = 4;
  let totalBoxes = Math.max(numberOfBoxes, newProjects.length - 1);
  const boxes = [];

  let navigate = useNavigate();
  function handleLinkClick(url) {
    navigate(url);
  }

  async function fetchNewProject() {
    await fetch(`https://nova-platform.kr/nova_fund_system/bias_project/new_bias_project`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        //console.log("www", data);
        setNewProjects(data.body.project);
        setIsLoading(false);
      });
  }

  for (let i = 1; i <= totalBoxes; i++) {
    const projects = newProjects[i];
    boxes.push(
      <div className="inner-slick-slide-component" key={i}>
        <div className="new-img">
          {projects && <img src={projects.head_image[0]} alt="img" />}
        </div>

        <div className="new-title">
          <p> 타이틀</p>
          <p className="banner-p-tag">최대 5PT</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container"> 
      <div
        className={styleFunding.Topbar}
        style={{
          backgroundImage: `url(${newProjects.length > 0 && newProjects[0].head_image[0]})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <img src={shadow} alt="Shadow Overlay" className={styleFunding.ShadowOverlay} />

        <section className={styleFunding["new-box"]}>
          {newProjects.length > 0 && (
            <>
              <h3>{newProjects[0].pname}</h3>
              <p>{newProjects[0].introduce}</p>
            </>
          )}
          <button onClick={() => handleLinkClick("/details")}>상세 정보</button>
        </section>
        <p className={styleFunding["new-fav"]}>무료 리워드 광고</p>
      </div>
      <div className="banner-slider">
          <Slider {...settings}>{boxes}</Slider>
      </div>

      <div className="section-separator"> </div>
      <section>
        <div>
          <span className="section-title">
              기여도 포인트 현황
          </span>
          <div className="contribute-point-background">
            <div className="contribute-point-box">
                <div className="bias-detail-section">
                    <div className="bias-profile-image">
                        이미지
                    </div>
                    <div className="bias-name-n-point-box">
                        <div className="bias-name">이름 여기 공개</div>
                        <div className="bias-point">1200 / 20000 PT</div>
                    </div>
                </div>
                <div className="my-point-section">
                    <div className="sum-of-point-box">
                        <p className="title"> 이번달 포인트 총합</p>
                        <p> 1200 PT</p>
                        <button> 포인트 사용</button>
                    </div>
                    <div className="my-point-box">

                    </div>
                </div>
            </div>
          </div>
        </div>
      </section>

      <div className="section-separator"> </div>
      <section>
        <div>
          <div>
            <span className="section-title">
                <span className="highlight"> 무료</span>&nbsp; 리워드 받기
            </span>
          </div>
          <div className="sponser-section">
            


          </div>
        </div>
      </section>

    </div>

  );
}


