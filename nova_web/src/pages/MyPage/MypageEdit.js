import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";
import style from "./Mypage.module.css";
import axios from "axios";

function MyPage() {
  let navigate = useNavigate();
  let [isLoading, setIsLoading] = useState(true);

  const handleLogout = (e) => {
    e.preventDefault();
    fetch("https://nova-platform.kr/user_home/try_logout", {
      credentials: "include",
    })
      .then((response) => {
        if (!response.ok) {
          return response.text().then((text) => {
            throw new Error(`Error: ${response.status}, ${text}`);
          });
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
        navigate("/");
      })
      .catch((error) => {
        console.error("Logout error:", error);
      });
  };

  let [myProfile, setMyProfile] = useState();

  // async function fetchEditProfile() {
  //   await axios
  //     .get("https://nova-platform.kr/user_home/get_my_profile_data", {
  //       withCredentials: true,
  //     })
  //     .then((res) => {
  //       console.log("profile", res.data);
  //       setMyProfile(res.data.body);
  //       setIsLoading(false);
  //     });
  // }

  async function fetchEditProfile() {
    await fetch("https://nova-platform.kr/user_home/get_my_profile_data", {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => {
        setMyProfile(data.body);
        setIsLoading(false);
      });
  }

  useEffect(() => {
    fetchEditProfile();
  }, []);
  // let profile_img = `https://kr.object.ncloudstorage.com/nova-user-profile/${myProfile.uid}.png`;

  if (isLoading) {
    return <div>loading...</div>;
  }

  return (
    <div className={`${style["container"]} ${style["edit-container"]}`}>
      <div className={style.top_area}>
        <p
          className={style.backword}
          onClick={() => {
            navigate(-1);
          }}
        >
          뒤로
        </p>
      </div>
      <section className={style["profile-section"]}>
        <div className={style["user-img-edit"]}>
          <img src={`https://kr.object.ncloudstorage.com/nova-user-profile/${myProfile.uid}.png`} alt="profile" />
        </div>
        <button>프로필 사진 변경</button>
      </section>

      <section className={style["profile-info"]}>
        <h3>프로필 정보</h3>
        <p className={style["input-name"]}>닉네임</p>
        <div className={style["user-name-input"]}>
          <input className={style["input-st"]} type="text" placeholder={myProfile.uname} />
          <button className={style["change-button"]}>변경</button>
        </div>

        <p className={style["input-name"]}> 비밀번호 변경</p>
        <div className={style["pw-change"]}>
          <input className={style["input-st"]} type="text" placeholder="기존 비밀번호" />
          <input className={style["input-st"]} type="text" placeholder="새로운 비밀번호" />
          <input className={style["input-st"]} type="text" placeholder="비밀번호 확인" />
          <button className={style["change-button"]}>변경</button>
        </div>
      </section>

      <section className={style["user-info"]}>
        <h3>개인정보</h3>
        <p className={style["input-name"]}>uid</p>
        <input className={style["input-st"]} type="text" placeholder="1234-1234-1234" readOnly />
        <p className={style["input-name"]}>email</p>
        <input className={style["input-st"]} type="text" placeholder="asd@naver.com" readOnly />
        <p className={style["input-name"]}>나이</p>
        <input className={style["input-st"]} type="text" placeholder="24살" readOnly />
        <p className={style["input-name"]}>성별</p>
        <input className={style["input-st"]} type="text" placeholder="남성" readOnly />
      </section>
      <button className={`${style["logout_box"]}`} onClick={handleLogout} style={{ cursor: "pointer" }}>
        로그아웃
      </button>
    </div>
  );
}

export default MyPage;
