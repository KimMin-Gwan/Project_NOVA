import style from "./MoreSee.module.css";
import backword from "./../../img/back_icon.png";
import x_icon from "./../../img/x_color.png";
import discord_icon from "./../../img/discord_color.png";
import insta_icon from "./../../img/insta_color.png";
import youtube_icon from "./../../img/youtube_color.png";
import set_icon from "./../../img/setting_icon.png";
import fav_icon from "./../../img/favset_icon.png";
import noti_icon from "./../../img/noti_icon.png";
import login_icon from "./../../img/login_icon.png";
import mypage_icon from "./../../img/mypage_icon.png";
import terms_icon from "./../../img/terms_icon.png";
import business_logo from "./../../img/business_logo.png";
import more_icon from "./../../img/Icon.png";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import popular_icon from "./../../img/popular.png";
import month_funding from "./../../img/month-funding.png";
import fav_like from "./../../img/fav-like.png";
import duck_funding from "./../../img/duck-funding.png";
import new_feed from "./../../img/new-feed.png";
import guide_icon from "./../../img/guide.png";
import short_feed from "./../../img/short-feed.png";
import up_hashtag from "./../../img/up-hashtag.png";
function MoreSee() {
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

  return (
    <div className={style.font}>
      <div className={style.container}>
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
            <img src={isLogin ? mypage_icon : login_icon} alt="Arrow" className={style.vector_login} />
            <p className={style.bodyText_login}>{isLogin ? "마이페이지" : "로그인"}</p>
          </div>

          <div className={style["list-bar"]}>노바 플랫폼</div>
          <hr></hr>
          <ul className={style.listContainer}>
            <li className={style.mainComponent} onClick={() => handlePage("/feed_list")}>
              <img src={fav_icon} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>전체 피드</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
            <li className={style.mainComponent} onClick={() => handlePage("/feed_page")}>
              <img src={short_feed} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>숏피드</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
            <li className={style.mainComponent} onClick={() => handlePage("/feed_list")}>
              <img src={popular_icon} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>최근 인기 피드</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
            <li className={style.mainComponent}>
              <img src={up_hashtag} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>급상승 해시태그</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
            <li className={style.mainComponent} onClick={() => handlePage("/write_feed")}>
              <img src={new_feed} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>새로운 피드 작성</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
          </ul>
          <br></br>
          <div className={style["list-bar"]}>노바 펀딩</div>
          <hr></hr>
          <ul className={style.listContainer}>
            <li className={style.mainComponent}>
              <img src={fav_like} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>최애 펀딩</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
            <li className={style.mainComponent}>
              <img src={duck_funding} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>덕질 펀딩</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
            <li className={style.mainComponent}>
              <img src={month_funding} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>이달의 펀딩 목록</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
            <li className={style.mainComponent}>
              <img src={guide_icon} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>펀딩 가이드</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
          </ul>
          <br></br>
          <div className={style["list-bar"]}>정보</div>
          <hr></hr>
          <ul className={style.listContainer}>
            <li className={style.mainComponent} onClick={() => handleRequestURL(requestURL.naverform)}>
              <img src={fav_icon} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>최애 신청하기(네이버 폼)</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
            <li className={style.mainComponent} onClick={() => handlePage("/notice_list")}>
              <img src={noti_icon} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>공지사항</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
            <li className={style.mainComponent} onClick={() => handlePage("/terms_page")}>
              <img src={terms_icon} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>이용약관</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
            <li className={style.mainComponent}>
              <img src={set_icon} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>페이지 설정</p>
              <img src={more_icon} alt="Arrow" className={style.more_vector} />
            </li>
          </ul>
        </div>

        <div className={style.inquiry}>
          <div className={style.iconBox} onClick={() => handleRequestURL(requestURL.x)}>
            <img src={x_icon} alt="x_Icon" className={style.icon_img} />
            <p className={style.icon_name}> X </p>
          </div>
          <div className={style.iconBox} onClick={() => handleRequestURL(requestURL.discord)}>
            <img src={discord_icon} alt="discord_Icon" className={style.icon_img} />
            <p className={style.icon_name}> Discord </p>
          </div>
          <div className={style.iconBox} onClick={() => handleRequestURL(requestURL.instagram)}>
            <img src={insta_icon} alt="insta_Icon" className={style.icon_img} />
            <p className={style.icon_name}> Instagram </p>
          </div>
          <div className={style.iconBox} onClick={() => handleRequestURL(requestURL.youtube)}>
            <img src={youtube_icon} alt="youtube_Icon" className={style.icon_img} />
            <p className={style.icon_name}> Youtube </p>
          </div>
        </div>

        <footer className={style.footer}>
          <div>
            <img src={business_logo} alt="logo_Icon" className={style.logo_img} />
          </div>
          <p className={style.nova_info}>경북 경산시 압량읍 압독2로1길 21, 1층 184</p>
          <p className={style.nova_info}>대표: 김민관 | 사업자등록번호: 380-08-03011</p>
          {/* <p className="nova-info">통신판매업신고번호: 0000-0000-000000</p> */}
          <p className={style.nova_info}>전화번호: 010-9875-2508 | 이메일:youths0828@nova-platform.kr</p>
          <p className={style.nova_info}>사업자 정보</p>
        </footer>
      </div>
    </div>
  );
}

export default MoreSee;
