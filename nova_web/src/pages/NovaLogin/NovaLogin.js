import React, { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import backword from "./../../img/back_icon.png";
import See from "./../../img/pwSee.png";
import SeeOff from "./../../img/pwNoneSee.png";
import style from "./NovaLogin.module.css";
import { getModeClass } from "./../../App.js";

import useLoginStore from "../../stores/LoginStore/useLoginStore.js";
import HEADER from "../../constant/header.js";
const NOVALogin = ({ brightmode }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [login, setLogin] = useState("");
  const [detail, setDetail] = useState("");
  let emailRef = useRef(null);

  useEffect(() => {
    emailRef.current.focus();
  }, []);

  const { tryLogin } = useLoginStore();
  const navigate = useNavigate();
  const handleLogin = async () => {
    if (!email || !password) {
      alert("이메일과 비밀번호를 모두 입력해주세요.");
      return; // POST 요청을 보내지 않음
    }

    const send_data = {
      header: HEADER,
      body: {
        email: email,
        password: password,
      },
    };

    fetch("https://nova-platform.kr/user_home/try_login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(send_data),
    })
      .then((response) => response.json())
      .then((result) => {
        //console.log("login", result);
        setLogin(result.body.result);
        setDetail(result.body.detail);
        tryLogin(result.body.result);
        if (result.body.result === "done") {
          navigate("/");
        }
      });
  };

  function onKeyDown(event) {
    if (event.key === "Enter") {
      handleLogin();
    }
  }

  useEffect(() => {
    return () => {
      setLogin("");
      setDetail("");
    };
  }, []);
  const [mode, setMode] = useState(() => {
    // 로컬 스토리지에서 가져온 값이 있으면 그것을, 없으면 'bright'로 초기화
    return localStorage.getItem("brightMode") || "bright";
  });

  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className={`${style["container"]} ${style[getModeClass(mode)]}`}>
      <div className={style.Topbar}>
        <img
          src={backword}
          alt="Arrow"
          className={style.backword}
          onClick={() => {
            navigate("/");
          }}
        />
        <div className={style.title}>로그인</div>
      </div>

      <div className={style.form}>
        {/* <div className={`${styleSignUp.box}`}> */}
        <div className={style["input-box"]}>
          이메일
          <br />
          <label>
            <input
              ref={emailRef}
              type="email"
              placeholder="이메일 주소"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className={style.input}
            />
          </label>
          {login === "email" && <div className={style.errorMessage}>{detail}</div>}
        </div>
        {/* </div> */}

        {/* <div className={`${styleSignUp.box} ${style["box-margin"]}`}> */}
        <div className={style["input-box"]}>
          비밀번호
          <br />
          <label>
            <input
              type={showPassword ? "text" : "password"}
              placeholder="비밀번호"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className={style.input}
              onKeyDown={(e) => {
                onKeyDown(e);
              }}
            />
            <button
              type="button"
              className={style["toggle-btn"]}
              onClick={() => setShowPassword((prev) => !prev)}
            >
              {showPassword ? (
                <img src={SeeOff} alt="비밀번호 숨김" />
              ) : (
                <img src={See} alt="비밀번호 표시" />
              )}
            </button>
          </label>
          {login === "password" && <div className={style.errorMessage}>{detail}</div>}
        </div>
        {/* </div> */}
      </div>

      <div className={style["login-box"]}>
        <button className={style.loginButton} onClick={handleLogin}>
          로그인
        </button>
        <button
          className={`${style.loginButton} ${style["sign-up-btn"]}`}
          onClick={() => {
            navigate("/signup");
          }}
        >
          회원 가입
        </button>
        <div
          className={style["sign-up"]}
          onClick={() => {
            navigate("/find_pw");
          }}
        >
          비밀번호 찾기
        </div>
      </div>
    </div>
  );
};

export default NOVALogin;
