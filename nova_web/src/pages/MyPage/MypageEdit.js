import { useNavigate } from "react-router-dom";
import React, { useState } from "react";
import style from "./Mypage.module.css";

function MyPage() {
  let navigate = useNavigate();

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
        <div className={style["user-img-edit"]}>이미지</div>
        <button>프로필 사진 변경</button>
      </section>

      <section className={style["profile-info"]}>
        <h3>프로필 정보</h3>
        <p className={style["input-name"]}>닉네임</p>
        <div class={style["user-name-input"]}>
          <input className={style["input-st"]} type="text" placeholder="사용자 이름" />
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
        <input className={style["input-st"]} type="text" placeholder="1234-1234-1234" />
        <p className={style["input-name"]}>email</p>
        <input className={style["input-st"]} type="text" placeholder="asd@naver.com" />
        <p className={style["input-name"]}>나이</p>
        <input className={style["input-st"]} type="text" placeholder="24살" />
        <p className={style["input-name"]}>성별</p>
        <input className={style["input-st"]} type="text" placeholder="남성" />
      </section>
      <button className={`${style["logout_box"]}`} onClick={handleLogout} style={{ cursor: "pointer" }}>
        로그아웃
      </button>
    </div>
  );
}

export default MyPage;
