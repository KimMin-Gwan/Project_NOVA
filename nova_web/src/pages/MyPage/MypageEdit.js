import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";
import style from "./Mypage.module.css";
import axios from "axios";
import user_icon from "./../../img/user_profile.svg";
import useLoginStore from "../../stores/LoginStore/useLoginStore";
import useBiasStore from "../../stores/BiasStore/useBiasStore";

function MyPage() {
  const { tryLogin, tryLogout } = useLoginStore();
  const { fetchBiasList } = useBiasStore();
  let navigate = useNavigate();
  let [isLoading, setIsLoading] = useState(true);
  let [nickname, setNickname] = useState("");
  let [password, setPassword] = useState("");
  let [newPassword, setNewPassword] = useState("");
  let [myProfile, setMyProfile] = useState();

  let [newNickname, setNewNickname] = useState("");
  let header = {
    "request-type": "default",
    "client-version": "v1.0.1",
    "client-ip": "127.0.0.1",
    uid: "1234-abcd-5678",
    endpoint: "/core_system/",
  };

  async function fetchChangeNickname() {
    await axios
      .post(
        `https://nova-platform.kr/user_home/try_change_nickname`,
        {
          header: header,
          body: {
            uname: nickname,
          },
        },
        {
          withCredentials: true,
          headers: {
            "Content-Type": "application/json",
          },
        }
      )
      .then((res) => {
        console.log(res.data);
        if (res.data.body.result) {
          setNewNickname(res.data.body.uname);
        }
      });
  }

  async function fetchPasswordChange() {
    await axios
      .post(
        "https://nova-platform.kr/user_home/try_change_password",
        {
          header: header,
          body: {
            password: password,
            new_password: newPassword,
          },
        },
        {
          withCredentials: true,
          headers: {
            "Content-Type": "application/json",
          },
        }
      )
      .then((res) => {
        console.log(res.data);
        if (!res.data.body.result) {
          alert(res.data.body.detail);
        }
      });
  }

  function onChangeNickname(e) {
    setNickname(e.target.value);
  }

  function onChangePassword(e) {
    setPassword(e.target.value);
  }
  function onChangeNewPassword(e) {
    setNewPassword(e.target.value);
  }

  const handleLogout = (e) => {
    tryLogin("");

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
        console.log("lgogio", data);
        navigate("/");
        fetchBiasList();
      })
      .catch((error) => {
        console.error("Logout error:", error);
      });
  };

  async function fetchEditProfile() {
    await fetch("https://nova-platform.kr/user_home/get_my_profile_data", {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => {
        setMyProfile(data.body);
        setIsLoading(false);
        console.log(data);
      });
  }

  useEffect(() => {
    fetchEditProfile();
  }, []);

  if (isLoading) {
    return <div>loading...</div>;
  }

  const profile = `https://kr.object.ncloudstorage.com/nova-user-profile/${myProfile.uid}.png`;

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
          <img src={profile} alt="profile" onError={(e) => (e.target.src = user_icon)} />
        </div>
        <button>프로필 사진 변경</button>
      </section>

      <section className={style["profile-info"]}>
        <h3>프로필 정보</h3>
        <p className={style["input-name"]}>닉네임</p>
        <div className={style["user-name-input"]}>
          <input
            className={style["input-st"]}
            type="text"
            value={nickname}
            onChange={(e) => {
              onChangeNickname(e);
            }}
            placeholder={myProfile.uname}
          />
          <button
            className={style["change-button"]}
            onClick={(e) => {
              fetchChangeNickname();
            }}
          >
            변경
          </button>
        </div>

        <p className={style["input-name"]}> 비밀번호 변경</p>
        <div className={style["pw-change"]}>
          <input
            className={style["input-st"]}
            type="text"
            value={password}
            onChange={(e) => {
              onChangePassword(e);
            }}
            placeholder="기존 비밀번호"
          />
          <input
            className={style["input-st"]}
            value={newPassword}
            onChange={(e) => {
              onChangeNewPassword(e);
            }}
            type="text"
            placeholder="새로운 비밀번호"
          />
          <input className={style["input-st"]} type="text" placeholder="비밀번호 확인" />
          <button className={style["change-button"]} onClick={fetchPasswordChange}>
            변경
          </button>
        </div>
      </section>

      <section className={style["user-info"]}>
        <h3>개인정보</h3>
        <p className={style["input-name"]}>uid</p>
        <input className={style["input-st"]} type="text" placeholder={myProfile.uid} readOnly />
        <p className={style["input-name"]}>email</p>
        <input className={style["input-st"]} type="text" placeholder={myProfile.email} readOnly />
        <p className={style["input-name"]}>나이</p>
        <input
          className={style["input-st"]}
          type="text"
          placeholder={`${myProfile.age}살`}
          readOnly
        />
        <p className={style["input-name"]}>성별</p>
        <input
          className={style["input-st"]}
          type="text"
          placeholder={myProfile.gender === "f" ? "여성" : "남성"}
          readOnly
        />
      </section>
      <button className={`${style["logout_box"]}`} onClick={handleLogout}>
        로그아웃
      </button>
    </div>
  );
}

export default MyPage;
