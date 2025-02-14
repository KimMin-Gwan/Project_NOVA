import style from "./MoreSee.module.css";
import backword from "./../../img/back_icon.png";
import fav_icon from "./../../img/favset_icon.svg";
import bug_icon from "./../../img/bug_icon.svg";
import user_icon from "./../../img/user_profile.svg";
import login_icon from "./../../img/login_icon.png";
import mypage_icon from "./../../img/mypage_icon.png";
import terms_icon from "./../../img/terms_icon.svg";
import business_logo from "./../../img/business_logo.png";
import more_icon from "./../../img/Icon.png";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import new_moment from "./../../img/new_moment.svg";
import today_up from "./../../img/today_up.svg";
import week_up from "./../../img/week_up.svg";
import all_post from "./../../img/all_post.svg";
import new_post from "./../../img/new_post.svg";
import fav_follow from "./../../img/fav_follow.svg";
import fav_sub from "./../../img/fav_sub.svg";
import notice from "./../../img/notice_more.svg";
import { getModeClass } from "./../../App.js";
import NavBar from "../../component/NavBar.js";

function MoreSee({ onModeChange }) {
  const requestURL = {
    x: "https://x.com/sebacheong",
    discord: "https://discord.com",
    instagram: "https://www.instagram.com/yth4chg_/profilecard/?igsh=MTRhcDd1NWRpZWo3dw==",
    youtube: "https://www.youtube.com/channel/UCyvmJ49lux5R1NVlBTJZt2Q",
    naverform: "https://naver.me/xGImCJSN",
  };

  function handleRequestURL(url) {
    window.open(url, "_blank", "noopener, noreferrer");
  }

  function handlePage(url) {
    navigate(url);
  }
  let navigate = useNavigate();

  let [isLogin, setIsLogin] = useState();
  let [isError, setIsError] = useState();

  function handleFetch() {
    fetch("https://nova-platform.kr/home/is_valid", {
      credentials: "include", // 쿠키를 함께 포함한다는 것
    })
      .then((response) => {
        if (!response.ok) {
          if (response.status === 401) {
            setIsError(response.status);
            setIsLogin(false);
            return null;
          } else {
            throw new Error(`status: ${response.status}`);
          }
        }
        return response.json();
      })
      .then((data) => {
        if (data) {
          console.log(data);
          setIsLogin(data.body.result);
        }
      })
      .catch((error) => {
        console.error("Fetch error:", error);
        setIsError(error.message);
      });
  }

  useEffect(() => {
    handleFetch();
  }, []);
  const [brightMode, setBrightMode] = useState(() => {
    return localStorage.getItem("brightMode") || "bright"; // 기본값은 'bright'
  });

  const handleChangeMode = () => {
    const newMode = brightMode === "dark" ? "bright" : "dark";
    setBrightMode(newMode);
    localStorage.setItem("brightMode", newMode); // 상태를 localStorage에 저장
    onModeChange(newMode); // 부모 컴포넌트에 변경된 상태 전달
  };

  useEffect(() => {
    document.body.className = brightMode === "dark" ? "dark-mode" : "bright-mode";
  }, [brightMode]);
  return (
    <div className={style.font}>
      <div className={`${style["container"]} ${style[getModeClass(brightMode)]}`}>
        <div className={style.TopBar}>
          <img
            src={backword}
            alt="Arrow"
            className={style.backword}
            onClick={() => {
              navigate(-1);
            }}
          />
          <div className={style.TitleBox}>
            <p className={style.titleName}> 더보기 </p>
          </div>
          <div className={style.EmptyBox} />
        </div>

        <div className={style.content}>
          <div className={style.fullWidthComponent}>
            <img
              src={isLogin ? user_icon : login_icon}
              alt="Arrow"
              className={style.vector_login}
            />
            <p
              className={style.bodyText_login}
              onClick={() => {
                if (isLogin) {
                  navigate("/mypage");
                } else {
                  navigate("/novalogin");
                }
              }}
            >
              {isLogin ? "마이페이지" : "로그인"}
            </p>
          </div>

          <div className={style["list-bar"]}>게시판 목록</div>
          <hr></hr>
          <ul className={style.listContainer}>
            <li className={style.mainComponent} onClick={() => handlePage("/feed_list?type=bias")}>
              <img src={fav_icon} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>최애 주제 게시판</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
            <li className={style.mainComponent} onClick={() => handlePage("/feed_list?type=best")}>
              <img src={today_up} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>오늘의 급상승 게시글</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
            <li
              className={style.mainComponent}
              onClick={() => handlePage("/feed_list?type=weekly_best")}
            >
              <img src={week_up} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>주간 급상승 게시글</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
            <li className={style.mainComponent} onClick={() => handlePage("/feed_list?type=all")}>
              <img src={all_post} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>전체 게시글</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
          </ul>
          <br></br>
          <div className={style["service-container"]}>
            <h3>서비스</h3>
            <section className={style["button-container"]}>
              <button onClick={() => handlePage("/write_feed/short")}>
                <img src={new_moment} alt="새로운 모멘트 작성" />
                새로운 모멘트 작성
              </button>
              <button onClick={() => handlePage("/write_feed/long")}>
                <img src={new_post} alt="새로운 포스트 작성" />
                새로운 포스트 작성
              </button>
              <button onClick={() => handlePage("/follow_page")}>
                <img src={fav_follow} alt="최애 주제 팔로우" />
                최애 주제 팔로우
              </button>
              <button onClick={() => handleRequestURL(requestURL.naverform)}>
                <img src={fav_sub} alt="최애 주제 신청" />
                최애 주제 신청
              </button>
            </section>
          </div>
          <br></br>
          <div className={style["list-bar"]}>다른 기능</div>
          <hr></hr>
          <ul className={style.listContainer}>
            <li className={style.mainComponent} onClick={() => handlePage("/notice")}>
              <img src={notice} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>공지사항</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
            <li className={style.mainComponent}>
              <img src={bug_icon} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>버그 리포트</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
            <li className={style.mainComponent} onClick={() => handlePage("/terms_page")}>
              <img src={terms_icon} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>이용약관</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
            {/* <li className={style.mainComponent} onClick={handleChangeMode}>
              <img src={set_icon} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>
                {brightMode === "dark" ? "☀️ Light Mode" : "🌑 Dark Mode"}
              </p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li> */}
          </ul>
        </div>
        <div className={style.inquiry}></div>

        <footer className={style.footer}>
          <div>
            <img src={business_logo} alt="logo_Icon" className={style.logo_img} />
          </div>
          <h4>세상을 바꾸는 청년들</h4>
          <p className={style.nova_info}>경북 경산시 압량읍 압독2로1길 21, 1층 184</p>
          <p className={style.nova_info}>대표: 김민관 | 사업자등록번호: 380-08-03011</p>
          <p className={style.nova_info}>통신판매업신고번호: 0000-0000-000000</p>
          <p className={style.nova_info}>
            전화번호: 010-9875-2508 | 이메일:youths0828@nova-platform.kr
          </p>
        </footer>

        <NavBar />
      </div>
    </div>
  );
}

export default MoreSee;
