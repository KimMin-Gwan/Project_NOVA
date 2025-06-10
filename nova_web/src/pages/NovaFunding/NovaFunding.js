import style from "./NovaFunding.module.css";
import logo from "./../../img/NOVA_Funding_logo.png";
import menu from "./../../img/menu-burger.png";
import more_icon from "./../../img/back.png";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import FundingSlider from "../../component/FundingSlider";
import LeftBar from "./WideFunding/LeftBarF.js";
import RightBar from "./WideFunding/RightBarF.js";
import LeftBarF from "./WideFunding/LeftBarF.js";
export default function NovaFunding({ brightmode }) {
  let navigate = useNavigate();

  let [hashTags, setHashTags] = useState([]);
  let [fundProjects, setFundProjects] = useState([]);
  let [biasProjects, setBiasProjects] = useState([]);
  let [bestProjects, setBestProjects] = useState([]);
  let [numProjects, setNumProjects] = useState(0);
  let [fanProjects, setFanProjects] = useState([]);
  let [fundingInfo, setFundingInfo] = useState({});

  function handleLinkClick(url) {
    navigate(url);
  }

  function fetchTag() {
    fetch(`https://supernova.io.kr/nova_fund_system/home/get_recommend_tag`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setHashTags(data.body.tag);
      });
  }

  useEffect(() => {
    fetchTag();
  }, []);

  function fetchTagData(tag) {
    fetch(`https://supernova.io.kr/nova_fund_system/home/get_project_as_tag?tag=${tag}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setFundProjects(data.body.project);
      });
  }

  useEffect(() => {
    fetchTagData();
  }, []);

  function onClickTag(tag, i) {
    fetchTagData(tag);
  }

  function fetchBiasProj() {
    fetch(`https://supernova.io.kr/nova_fund_system/home/get_bias_project`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setBiasProjects(data.body.project);
      });
  }

  useEffect(() => {
    fetchBiasProj();
  }, []);

  function fetchBestProject() {
    fetch(`https://supernova.io.kr/nova_fund_system/home/best_funding_section`)
      .then((response) => response.json())
      .then((data) => {
        // setBestProjects(data.body.project);
        setNumProjects(data.body.num_project);
      });
  }

  useEffect(() => {
    fetchBestProject();
  }, []);

  function fetchFanProj() {
    fetch(`https://supernova.io.kr/nova_fund_system/home/get_fan_funding`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setFanProjects(data.body.project);
      });
  }

  useEffect(() => {
    fetchFanProj();
  }, []);

  function fetchFundingInfo() {
    fetch(`https://supernova.io.kr/nova_fund_system/home/get_nova_funding_info`)
      .then((response) => response.json())
      .then((data) => {
        setFundingInfo(data.body);
      });
  }

  useEffect(() => {
    fetchFundingInfo();
  }, []);

  let [newProjects, setNewProjects] = useState([]);

  function fetchNewProject() {
    fetch(`https://supernova.io.kr/nova_fund_system/bias_project/new_bias_project`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        //console.log(data);
        setNewProjects(data.body.project);
      });
  }

  useEffect(() => {
    fetchNewProject();
  }, []);

  return (
    <div className={style["widever-style"]}>
      <div className={style["empty-box"]}></div>
      {/* <section className="contents com1">
        <LeftBarF />
      </section> */}
      <div className={style.container}>
        <header className={style.header}>
          <div className="logo">
            <img src={logo} alt="logo"></img>
          </div>
          <div className="buttons">
            <button className="tool-button">
              <img
                src={menu}
                alt="menu"
                onClick={() => {
                  handleLinkClick("/more_see");
                }}
              ></img>
            </button>
          </div>
        </header>
        <div className={style["img-box"]}>
          이미지박스
          <div className={style["arrow-icon"]}>화살표</div>
        </div>
        <section className={style["recommend-box"]}>
          <div className={style["title-box"]}>
            <h2 className={style["title-text"]}>이런 펀딩 프로젝트는 어때요?</h2>
            <img src={more_icon} className={style["more-icon"]}></img>
          </div>
          <p className={style["more-text"]}>해시 태그로 찾아보는 펀딩 프로젝트</p>
          <div className={style["tag-container"]}>
            {hashTags.map((tag, i) => {
              return (
                <button
                  key={i}
                  className={style["hashtag-text"]}
                  onClick={() => {
                    onClickTag(tag, i);
                  }}
                >
                  #{tag}
                </button>
              );
            })}
          </div>
          <div className={style["ad-container"]}>
            {fundProjects.map((project, i) => {
              return (
                <div key={project.pid} className={style["ad-box"]}>
                  <div className={style["img"]}>
                    <img src={`${project.head_image[0]}`} />
                  </div>
                  <p className={style["ad-title"]}>{project.pname}</p>
                  <p>{project.expire_date} 일까지</p>
                  <p>{project.int_progress}% 달성했어요</p>
                </div>
              );
            })}
          </div>
        </section>

        <section className={style["best-funding"]}>
          <div className={style["best-title"]}>
            <div className={style["top-title"]}>
              <h4>진행 중인 최애펀딩</h4>
              {/* <a onClick={() => handleLinkClick("/like_funding")}>더보기</a> */}
              <a onClick={() => handleLinkClick("/bias_funding")}>더보기</a>
            </div>
            <p>최애가 직접 만드는 펀딩 프로젝트</p>
          </div>
          {/* {biasProjects.map((project, i) => {
            return (
              <div key={project.pid + i} className={style["funding-main"]}>
                <div className={style["album-area"]}>
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
                    <progress value="70" max="100"></progress>
                    <p>{project.int_progress}%</p>
                  </div>
                  <button>자세히보기</button>
                </div>
              </div>
            );
          })} */}
          <FundingSlider biasProjects={biasProjects} />
        </section>

        <section className={`${style["recommend-box"]} ${style["dis"]}`}>
          <div className={style["title-box"]}>
            <h2 className={style["title-text"]}>베스트 프로젝트 모두 보기</h2>
          </div>
          <p className={style["more-text"]}>지금까지 펀딩된 프로젝트와 투자자들을 알아봐요!</p>

          <div className={style["ad-container"]}>
            <div className={style["ad-box"]}>
              <div className={style["img"]}>이미지</div>
              <p className={style["ad-title"]}>프로젝트 펀딩 순위</p>

              <p>72% 달성했어요</p>
            </div>
            <div className={style["ad-box"]}>
              <div className={style["img"]}>이미지</div>
              <p className={style["ad-title"]}>프로젝트 펀딩 순위</p>

              <p>72% 달성했어요</p>
            </div>
            <div className={style["ad-box"]}>
              <div className={style["img"]}>이미지</div>
              <p className={style["ad-title"]}>프로젝트 펀딩 순위</p>

              <p>총 {numProjects}개의 프로젝트가 있어요.</p>
            </div>
          </div>
        </section>

        <section className={style["open-funding"]}>
          <div className={style["best-title"]}>
            <div className={style["top-title"]}>
              <h4>진행 중인 덕질 펀딩</h4>
              <a onClick={() => handleLinkClick("/duck_funding")}>더보기</a>
            </div>
            <p>누구나 팬 활동을 다같이 하고 싶다면!</p>
            <ul className={style["open-container"]}>
              {fanProjects.map((project, i) => {
                return (
                  <li key={project.pid * i} className={style["open-box"]}>
                    <div className={style["open-img"]}>
                      <img src={`${project.head_image[0]}`} />
                    </div>
                    <div className={style["text-area"]}>
                      <div className={style["who-text"]}>
                        <h4>{project.pname}</h4>
                        <p>{project.uname}</p>
                      </div>
                      <footer className={style["footer-line"]}>
                        <time>{project.expire_date}까지</time>
                        <button>자세히 보기</button>
                      </footer>
                    </div>
                  </li>
                );
              })}
            </ul>
          </div>
        </section>

        <section className={`${style["notice-nova"]} ${style["dis"]}`}>
          <div className={style["title-box"]}>
            <h2 className={style["title-text"]}>노바 펀딩 알아보기</h2>
            <img src={more_icon} className={style["more-icon"]}></img>
          </div>
          <p className={style["more-text"]}>30초만에 알아보는 노바 펀딩</p>

          <div className={style["ad-container"]}>
            <div className={style["ad-box"]}>
              <div className={style["img"]}>이미지</div>
              <p className={style["ad-title"]}>프로젝트 펀딩 순위</p>

              <p>{fundingInfo.bias_funding_view}명이 읽었어요!</p>
            </div>
            <div className={style["ad-box"]}>
              <div className={style["img"]}>이미지</div>
              <p className={style["ad-title"]}>프로젝트 펀딩 순위</p>

              <p>{fundingInfo.fan_funding_view}명이 읽었어요!</p>
            </div>
            <div className={style["ad-box"]}>
              <div className={style["img"]}>이미지</div>
              <p className={style["ad-title"]}>프로젝트 펀딩 순위</p>

              <p>{fundingInfo.good_funding_view}명이 읽었어요!</p>
            </div>
          </div>

          <div className={style["footer-area"]}>
            <div className={style["area-box"]}>참여한 펀딩</div>
            <div className={style["area-box"]}>
              펀딩 신청<br></br>
            </div>
          </div>

          <div className={style["last-project"]}>지난 펀딩 프로젝트</div>
        </section>
      </div>
      {/* <section className="contents com1">
        <RightBar />
      </section> */}
    </div>
  );
}
