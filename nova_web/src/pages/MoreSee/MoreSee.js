import style from "./MoreSee.module.css";
import backword from "./../../img/backword.png";
import vector from "./../../img/Vector.png";
import x_icon from "./../../img/x_color.png";
import discord_icon from "./../../img/discord_color.png";
import insta_icon from "./../../img/insta_color.png";
import youtube_icon from "./../../img/youtube_color.png";
import set_icon from "./../../img/setting_icon.png";
import fav_icon from "./../../img/favset_icon.png";
import noti_icon from "./../../img/noti_icon.png";
import login_icon from "./../../img/login_icon.png";
import terms_icon from "./../../img/terms_icon.png";

import { useNavigate } from "react-router-dom";

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

  let navigate = useNavigate();
  let tokenCheck = localStorage.getItem("jwtToken");

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
        </div>

        <div className={style.content}>
          <div
            className={style.fullWidthComponent}
            onClick={() => {
              if (tokenCheck) {
                navigate("/mypage");
              } else {
                navigate("/novalogin");
              }
            }}
          >
            <img src={login_icon} alt="Arrow" className={style.vector} />
            <p className={style.bodyText}>{tokenCheck ? "마이페이지" : "로그인"}</p>
          </div>

          <div className={style.row}>
            <div className={style.mainComponent} onClick={() => handleRequestURL(requestURL.naverform)}>
              <img src={fav_icon} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>최애 신청하기(네이버 폼)</p>
            </div>
            <div
              className={style.mainComponent}
              onClick={() => {
                navigate("/notice_list");
              }}
            >
              <img src={noti_icon} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>공지사항</p>
            </div>
          </div>

          <div className={style.row}>
            <div className={style.mainComponent}>
              <img src={terms_icon} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>사업자 정보 및 사용약관</p>
            </div>
            <div className={style.mainComponent}>
              <img src={set_icon} alt="Arrow" className={style.vector} />
              <p className={style.bodyText}>페이지 설정</p>
            </div>
          </div>
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

        <footer className="footer">
          <div className={style.footer}>
            <p>NOVA</p>
            <br />
            <p className="nova-info">경북 경산시 압량읍 압독2로1길 21, 1층 184</p>
            <p className="nova-info">대표: 김민관 | 사업자등록번호: 380-08-03011</p>
            <p className="nova-info">통신판매업신고번호: 0000-0000-000000</p>
            <p className="nova-info">전화번호: 010-9875-2508 | 이메일:youths0828@nova-platform.kr</p>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default MoreSee;
