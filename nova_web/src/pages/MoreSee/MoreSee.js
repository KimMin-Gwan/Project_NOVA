import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import backword from "./../../img/back_icon.png";
import fav_icon from "./../../img/favset_icon.svg";
import bug_icon from "./../../img/bug_icon.svg";
import user_icon from "./../../img/user_profile.svg";
import login_icon from "./../../img/login_icon.png";
import terms_icon from "./../../img/agree.svg";
import more_icon from "./../../img/Icon.png";
import new_moment from "./../../img/new_moment.svg";
import today_up from "./../../img/today_up.svg";
import week_up from "./../../img/week_up.svg";
import all_post from "./../../img/all_post.svg";
import new_post from "./../../img/new_post.svg";
import calendar from "./../../img/calendar.svg";
import calendar_plus from "./../../img/calendar_plus.svg";
import calendar_check from "./../../img/calendar_check.svg";
import fav_follow from "./../../img/fav_follow.svg";
import fav_sub from "./../../img/fav_sub.svg";
import notice from "./../../img/notice_more.svg";
import NavBar from "../../component/NavBar/NavBar.js";
import Footer from "../../component/Footer/Footer.js";
import { getModeClass } from "./../../App.js";
import style from "./MoreSee.module.css";

const boardList = [
  {
    id: 0,
    title: "최애 주제 게시판",
    src: fav_icon,
    end_point: "/feed_list?type=bias",
  },
  {
    id: 1,
    title: "오늘의 급상승 게시글",
    src: today_up,
    end_point: "/feed_list?type=today",
  },
  {
    id: 2,
    title: "주간 급상승 게시글",
    src: week_up,
    end_point: "/feed_list?type=weekly",
  },
  {
    id: 3,
    title: "전체 게시글",
    src: all_post,
    end_point: "/feed_list?type=all",
  },
  {
    id: 4,
    title: "일정 대시보드",
    src: calendar,
    end_point: "/schedule",
  },
  {
    id: 5,
    title: "일정 탐색",
    src: calendar_plus,
    end_point: "/explore/schedule",
  },
  {
    id: 6,
    title: "일정 관리",
    src: calendar_check,
    end_point: "/schedule/my_schedule",
  },
  {
    id: 7,
    title: "일정 등록",
    src: all_post,
    end_point: "/feed_list?type=all",
  },
  {
    id: 8,
    title: "공지사항",
    src: notice,
    end_point: "/notice",
  },
  {
    id: 9,
    title: "버그 리포트",
    src: bug_icon,
    end_point: "/report",
  },
  {
    id: 10,
    title: "이용약관",
    src: terms_icon,
    end_point: "/terms_page",
  },
];

function MoreSee({ onModeChange }) {
  const serviceList = [
    //{
      //id: 0,
      //title: "새로운 모멘트 작성",
      //src: new_moment,
      //alt: "새로운 모멘트 작성",
      //end_point: "/write_feed/short",
      //onClick: (endPoint) => handlePage(endPoint),
    //},
    {
      id: 1,
      title: "새로운 게시글 작성",
      src: new_moment,
      alt: "새로운 게시글 작성",
      end_point: "/write_feed",
      onClick: (endPoint) => handlePage(endPoint),
    },
    {
      id: 2,
      title: "최애 주제 팔로우",
      src: fav_follow,
      alt: "최애 주제 팔로우",
      end_point: "/follow_page",
      onClick: (endPoint) => handlePage(endPoint),
    },
    {
      id: 3,
      title: "최애 주제 신청",
      src: fav_sub,
      alt: "최애 주제 신청",
      requestURL: "https://naver.me/xGImCJSN",
      onClick: (requestURL) => handleRequestURL(requestURL),
    },
  ];

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
  let [user, setUser] = useState("")

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
          //console.log(data);
          setIsLogin(data.body.result);
          setUser(data.body.user);
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


  const profile = `https://kr.object.ncloudstorage.com/nova-profile-bucket/${user}.png`;

  const firstBoardList = boardList.slice(0, 4);
  const secondBoardList = boardList.slice(4, 7);
  const otherFunctionList = boardList.slice(8);
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
          <div
            className={style.fullWidthComponent}
            onClick={() => {
              if (isLogin) {
                navigate("/mypage");
              } else {
                navigate("/novalogin");
              }
            }}
          >
            <img
              src={isLogin ? profile : login_icon}
              alt="Arrow"
              className={style.vector_login}
              onError={(e) => (e.target.src = user_icon)} 
            />
            <p className={style.bodyText_login}>{isLogin ? "마이페이지" : "로그인"}</p>
          </div>

          {/* 게시판 목록 */}
          <div className={style["list-bar"]}>게시판 목록</div>
          <hr></hr>
          <ul className={style.listContainer}>
            {firstBoardList.map((board, i) => {
              return (
                <li
                  key={board.id}
                  className={style.mainComponent}
                  onClick={() => handlePage(board.end_point)}
                >
                  <img src={board.src} alt="Arrow" className={style.vector} />
                  <p className={style.bodyText}>{board.title}</p>
                  <img src={more_icon} alt="Arrow" className={style.more_vector} />
                </li>
              );
            })}
          </ul>
          <br></br>

          {/* 서비스 목록 */}
          <div className={style["service-container"]}>
            <h3>서비스</h3>
            <section className={style["button-container"]}>
              {serviceList.map((service, i) => {
                return (
                  <button
                    key={service.id}
                    onClick={() => service.onClick(service.end_point || service.requestURL)}
                  >
                    <img src={service.src} alt={service.alt} />
                    {service.title}
                  </button>
                );
              })}
            </section>
          </div>

          <br></br>
          {/* 다른 기능 목록 */}
          <div className={style["list-bar"]}>일정</div>
          <hr></hr>
          <ul className={style.listContainer}>
            {secondBoardList.map((board, i) => {
              return (
                <li
                  key={board.id}
                  className={style.mainComponent}
                  onClick={() => handlePage(board.end_point)}
                >
                  <img src={board.src} alt="Arrow" className={style.vector} />
                  <p className={style.bodyText}>{board.title}</p>
                  <img src={more_icon} alt="Arrow" className={style.more_vector} />
                </li>
              );
            })}
          </ul>

          <br></br>
          {/* 다른 기능 목록 */}
          <div className={style["list-bar"]}>다른 기능</div>
          <hr></hr>
          <ul className={style.listContainer}>
            {otherFunctionList.map((board, i) => {
              return (
                <li
                  key={board.id}
                  className={style.mainComponent}
                  onClick={() => handlePage(board.end_point)}
                >
                  <img src={board.src} alt="Arrow" className={style.vector} />
                  <p className={style.bodyText}>{board.title}</p>
                  <img src={more_icon} alt="Arrow" className={style.more_vector} />
                </li>
              );
            })}

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

        <Footer />

        <NavBar />
      </div>
    </div>
  );
}

export default MoreSee;
