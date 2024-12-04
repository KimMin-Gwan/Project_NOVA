import style from "./DuckFunding.module.css";
import backword from "./../../../img/back_icon.png";
import more_icon from "./../../../img/backword.png";

import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";
export default function DuckFunding() {
  let navigate = useNavigate();
  const [activeButton, setActiveButton] = useState(0);
  const buttonLabels = [
    {
      id: 1,
      type: "recommend_project",
      label: "프로젝트 추천",
    },
    {
      id: 2,
      type: "funding_project",
      label: "참여 프로젝트",
    },
    {
      id: 3,
      type: "donation_project",
      label: "모금 프로젝트",
    },
  ];
  const URL = `https://nova-platform.kr/nova_fund_system/fan_project/`;

  let [achieveProj, setAchieveProj] = useState([]);
  let [soonExpireProj, setSoonExpireProj] = useState([]);
  let [clickProject, setClickProject] = useState([]);

  function handleLinkClick(url) {
    navigate(url);
  }

  function fetchAchieveProj() {
    fetch(`${URL}achieve_the_goal`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setAchieveProj(data.body.project);
      });
  }

  useEffect(() => {
    fetchAchieveProj();
  }, []);

  function fetchSoonExpireProj() {
    fetch(`${URL}soon_expire`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setSoonExpireProj(data.body.project);
      });
  }

  useEffect(() => {
    fetchSoonExpireProj();
  }, []);

  function fetchClickButton(type) {
    const endPoint = type ? `${URL}${type}` : `${URL}recommend_project`;
    fetch(endPoint, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setClickProject(data.body.project);
      });
  }

  useEffect(() => {
    fetchClickButton();
  }, []);

  const handleButtonClick = (index, label) => {
    setActiveButton(index);
    fetchClickButton(label.type);
  };

  return (
    <div className={style.container}>
      <header className={style.Topbar}>
        <img
          src={backword}
          alt="Arrow"
          className={style.backword}
          onClick={() => handleLinkClick(-1)}
        />
        <div className={style.title}>덕질펀딩</div>
        <div className={style.EmptyBox} />
      </header>

      <section className={style["success-funding"]}>
        <div className={style["content-title"]}>
          <header className={style["header-text"]}>이미 목표 달성에 성공한 프로젝트</header>
          <div onClick={() => handleLinkClick("/funding_project/achieve_project")}>전체보기</div>
        </div>

        <div className={style["best-container"]}>
          {achieveProj.map((project, i) => {
            return (
              <div key={project.pid} className={style["best-box"]}>
                <div className={style["best-img"]}>
                  <img src={project.head_image[0]}></img>
                </div>
                <p className={style["best-title"]}>{project.pname}</p>
                <p>{project.expire_date}일 까지 (1일 남음)</p>
                <p>{project.int_progress}% 달성</p>
              </div>
            );
          })}
        </div>
      </section>

      <section className={style["success-funding"]}>
        <div className={style["content-title"]}>
          <header className={style["header-text"]}>마감임박 프로젝트</header>
          <div onClick={() => handleLinkClick("/funding_project/soon_expire_project")}>
            전체보기
          </div>
        </div>

        <div className={style["ad-container"]}>
          {soonExpireProj.map((project, i) => {
            return (
              <div key={project.pid} className={style["ad-box"]}>
                <div className={style["soon-img"]}>
                  <img src={project.head_image[0]}></img>
                </div>
                <p className={style["ad-title"]}>{project.pname}</p>
                <p>{project.expire_date}일 까지</p>
                <p>{project.int_progress}% 달성</p>
              </div>
            );
          })}
        </div>
      </section>

      <section className={style["success-funding"]}>
        <div className={style["content-title"]}>
          {/* <header className={style["header-text"]}>덕질 펀딩 프로젝트</header> */}
        </div>
        <div className={style["recommend-project"]}>
          {buttonLabels.map((label, index) => (
            <button
              key={label.id}
              className={`${style["recommend-button"]} ${
                activeButton === index ? style.active : ""
              }`}
              onClick={() => handleButtonClick(index, label)}
            >
              {label.label}
            </button>
          ))}
        </div>
      </section>

      <section className={`${style["success-funding"]} ${style["interest-funding"]}`}>
        <div className={style["content-title"]}>
          {activeButton === 0 && (
            <header className={style["header-text"]}>관심있어 할 프로젝트</header>
          )}
          {activeButton === 1 && <header className={style["header-text"]}>참여한 프로젝트</header>}
          {activeButton === 2 && <header className={style["header-text"]}>모금 프로젝트</header>}
          <div
            onClick={() => handleLinkClick(`/funding_project/${buttonLabels[activeButton].type}`)}
          >
            전체보기
          </div>
        </div>
        <div className={style["ad-container"]}>
          {clickProject.map((project, i) => {
            return (
              <div key={project.pid} className={style["ad-box"]}>
                <div className={style["soon-img"]}>
                  <img src={project.head_image[0]} />
                </div>
                <p className={style["ad-title"]}>{project.pname}</p>
                <p>{project.expire_date}일 까지</p>
                <p>{project.int_progress}% 달성</p>
              </div>
            );
          })}
        </div>

        <button className={style["more-button"]}>더보기</button>
      </section>
    </div>
  );
}
