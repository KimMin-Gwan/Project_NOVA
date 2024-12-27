import style_sub from "./../DuckFunding/DuckFunding.module.css";
import style from "./BiasFunding.module.css";
import backword from "./../../../img/back_icon.png";
import test from "./../../../img/galaxyleague.png";
import shadow from "./../../../img/shadow_funding.png";
import { useNavigate } from "react-router-dom";
import Slider from "react-slick";
import { useEffect, useState } from "react";

export default function BiasFunding() {
  const settings = {
    dots: false,
    infinite: true,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 1,
    arrows: false,
    focusOnSelect: true,
  };
  let [isLoading, setIsLoading] = useState(true);
  let [newProjects, setNewProjects] = useState([]);
  const numberOfBoxes = 6;
  let totalBoxes = Math.max(numberOfBoxes, newProjects.length);
  const boxes = [];

  async function fetchNewProject() {
    await fetch(`https://nova-platform.kr/nova_fund_system/bias_project/new_bias_project`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("www", data);
        setNewProjects(data.body.project);
        setIsLoading(false);
      });
  }

  useEffect(() => {
    fetchNewProject();
  }, []);

  let [recommendProjects, setRecommendProjects] = useState([]);

  function fetchRecommendProject() {
    fetch(`https://nova-platform.kr/nova_fund_system/bias_project/recommend_project`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setRecommendProjects(data.body.project);
      });
  }

  useEffect(() => {
    fetchRecommendProject();
  }, []);

  let [allProjects, setAllProjects] = useState([]);

  function fetchAllProject() {
    fetch(`https://nova-platform.kr/nova_fund_system/bias_project/all_project`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setAllProjects(data.body.project);
      });
  }

  useEffect(() => {
    fetchAllProject();
  }, []);

  // for (let i = 1; i <= numberOfBoxes; i++) {
  //   boxes.push(
  //     <div className={style["new-list"]} key={i}>
  //       <div className={style["new-img"]}>
  //         <img src={newProjects[i].head_image[0]} />
  //       </div>

  //       <div className={style["new-title"]}>
  //         <span>{newProjects[i].pname}</span>
  //         <p>후원형</p>
  //       </div>
  //     </div>
  //   );
  // }

  let navigate = useNavigate();

  function handleLinkClick(url) {
    navigate(url);
  }

  return (
    <div className={`${style_sub.container} ${style["container"]}`}>
      <div
        className={style.Topbar}
        style={{
          backgroundImage: `url(${newProjects.length > 0 && newProjects[0].head_image[0]})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <img src={shadow} alt="Shadow Overlay" className={style.ShadowOverlay} />

        <img
          src={backword}
          alt="Arrow"
          className={`${style_sub.backword} ${style["backword"]}`}
          onClick={() => handleLinkClick(-1)}
        />
        <section className={style["new-box"]}>
          {newProjects.length > 0 && (
            <>
              <h3>{newProjects[0].pname}</h3>
              <p>{newProjects[0].introduce}</p>
            </>
          )}
          <button onClick={() => handleLinkClick("/details")}>상세 정보</button>
        </section>
        <p className={style["new-fav"]}>신규 최애 펀딩 프로젝트</p>
      </div>
      <div className={style.SliderContainer}>
        <div className={style["new-list"]}>
          <div className={style["new-img"]}>
            <img src={newProjects[1].head_image[0]} />
          </div>

          <div className={style["new-title"]}>
            <span>{newProjects[1].pname}</span>
            <p>후원형</p>
          </div>
        </div>
      </div>
      {/* <Slider {...settings}>
            {Array.from({ length: totalBoxes }).map((_, i) => {
              <div className={style["new-list"]} key={i}>
                <div className={style["new-img"]}>
                  {/* <img src={newProjects[i].head_image[0]} /> */}
      {/* </div> */}
      {/* // <div className={style["new-title"]}> */}
      {/* <span>{newProjects[i].pname}</span> */}
      {/* <p>후원형</p> */}
      {/* </div> */}
      {/* // </div>; */}
      {/* // })} */}
      {/* </Slider> */} */}
      <section className={`${style_sub["success-funding"]} ${style["success-funding"]}`}>
        <div className={`${style_sub["content-title"]} ${style["content-title"]}`}>
          <header className={style_sub["header-text"]}>추천하는 프로젝트</header>
          <div onClick={() => handleLinkClick("/bias_funding/recommend")}>전체보기</div>
        </div>
        <hr className={style["hr-style"]} />
        <ul>
          {recommendProjects.map((project, i) => {
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
      </section>
      <section className={`${style_sub["success-funding"]} ${style["success-funding"]}`}>
        <div className={`${style_sub["content-title"]} ${style["content-title"]}`}>
          <header className={style_sub["header-text"]}>진행중인 프로젝트</header>
          <div onClick={() => handleLinkClick("/bias_funding/progress")}>전체보기</div>
        </div>
        <hr className={style["hr-style"]} />
        <ul>
          {allProjects.map((project, i) => {
            return (
              <li key={project.pid + i}>
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
      </section>
    </div>
  );
}
