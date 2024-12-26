import style from "./DuckFunding.module.css";
import backword from "./../../../img/back_icon.png";
import { useNavigate, useParams } from "react-router-dom";
import React, { useEffect, useState } from "react";
export default function DuckFunding() {
  let navigate = useNavigate();
  const URL = `https://nova-platform.kr/nova_fund_system/fan_project_list/`;

  let project = [
    {
      id: 1,
      title: "목표 달성 성공 프로젝트",
      type: "achieve_project",
      url: "achieve_the_goal",
    },
    {
      id: 2,
      title: "마감 임박 프로젝트",
      type: "soon_expire_project",
      url: "soon_expire",
    },
    {
      id: 3,
      title: "관심있어 할 만한 프로젝트",
      type: "recommend_project",
      url: "recommend_project",
    },
    {
      id: 4,
      title: "참여형 프로젝트",
      type: "funding_project",
      url: "funding_project",
    },
    {
      id: 5,
      title: "모금형 프로젝트",
      type: "donation_project",
      url: "donation_project",
    },
  ];

  const { type } = useParams();
  const currentProject = project.find((project) => project.type === type);
  console.log(type);

  let [currentProjects, setCurrentProjects] = useState([]);

  function handleLinkClick(url) {
    navigate(url);
  }

  function fetchCurrentProj() {
    fetch(`${URL}${currentProject.url}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setCurrentProjects(data.body.project);
      });
  }

  useEffect(() => {
    fetchCurrentProj();
  }, []);

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
          <header className={style["header-text"]}>{currentProject.title}</header>
        </div>

        <div className={style["best-container"]}>
          {currentProjects.map((project, i) => {
            return (
              <div key={project.pid} className={style["best-box"]}>
                <div className={style["best-img"]}>
                  <img src={project.head_image[0]} />
                </div>
                <p className={style["best-title"]}>{project.pname}</p>
                <p>{project.expire_date}일 까지 (1일 남음)</p>
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
