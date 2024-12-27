import style_sub from "./../DuckFunding/DuckFunding.module.css";
import style from "./BiasFunding.module.css";
import backword from "./../../../img/back_icon.png";
import { useNavigate, useParams } from "react-router-dom";
import React, { useEffect, useState } from "react";

export default function MoreProjects() {
  let navigate = useNavigate();
  function handleLinkClick(url) {
    navigate(url);
  }

  let { type } = useParams();

  let [projects, setProjects] = useState([]);

  function fetchProjects() {
    fetch("https://nova-platform.kr/nova_fund_system/bias_project_list/recommend_project", {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setProjects(data.body.project);
      });
  }

  useEffect(() => {
    fetchProjects();
  }, []);

  return (
    <div className={`${style_sub.container} ${style["container"]}`}>
      <header className={style_sub.Topbar}>
        <img
          src={backword}
          alt="Arrow"
          className={style_sub.backword}
          onClick={() => handleLinkClick(-1)}
        />
        <div className={style_sub.title}>최애 펀딩</div>
        <div className={style_sub.EmptyBox} />
      </header>

      <section className={`${style_sub["success-funding"]} ${style["success-funding"]}`}>
        <div className={`${style_sub["content-title"]} ${style["content-title"]}`}>
          <header className={style_sub["header-text"]}>
            {type === "recommend" ? "추천하는 프로젝트" : "진행중인 프로젝트"}
          </header>
        </div>
        <hr className={style["hr-style"]} />
        <ul>
          {projects.map((project, i) => {
            return (
              <li key={project.pid}>
                <div className={style["project-list"]}>
                  <div className={style["pj-img"]}>
                    <img src={project.head_image[0]} />
                  </div>
                  <div className={style["pj-des"]}>
                    <p>{project.ftype === "attend" ? "참여형" : "후원형"}</p>
                    <h4>{project.pname}</h4>
                    <p>{project.uname}</p>
                    <p>{project.expire_date}</p>
                    <p>80% 달성</p>
                    <button>상세정보</button>
                  </div>
                </div>
              </li>
            );
          })}
          <hr className={style["hr-style"]} />
        </ul>
        <button className={style["moresee_button"]}>더보기</button>
      </section>
    </div>
  );
}
