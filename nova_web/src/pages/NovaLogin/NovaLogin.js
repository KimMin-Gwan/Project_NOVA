import React, { useEffect, useState, useRef } from "react";
import ReCAPTCHA from "react-google-recaptcha";
import { useNavigate } from "react-router-dom";
import backword from "./../../img/back_icon.png";
import See from "./../../img/pwSee.png";
import SeeOff from "./../../img/pwNoneSee.png";
import style from "./NovaLogin.module.css";
import { getModeClass } from "./../../App.js";
import mainApi from "../../services/apis/mainApi.js";

import useLoginStore from "../../stores/LoginStore/useLoginStore.js";
import HEADER from "../../constant/header.js";
const NOVALogin = ({ brightmode }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [login, setLogin] = useState("");
  const [detail, setDetail] = useState("");
  const [loginCount, setLoginCount] = useState(0);
  const [captcha, setCaptcha] = useState("");

  const handleCaptcha = (value) => {
    setCaptcha(value);
  };

  let emailRef = useRef(null);

  const isThisClientRobot = async () => {
    await mainApi.get("/user_home/is_this_client_robot").then((res)=>{
      if (res.status == 200){
        setLoginCount(res.data.count) 
      }else{
        alert("서버에 문제가 있습니다. 관리자에게 문의하세요")
        navigate("/");
      }
    })
  }
  console.log(loginCount);

  useEffect(() => {
    emailRef.current.focus();
    isThisClientRobot()
  }, []);

  const { tryLogin } = useLoginStore();
  const navigate = useNavigate();
  const handleLogin = async () => {
    if (!email || !password) {
      alert("이메일과 비밀번호를 모두 입력해주세요.");
      return; // POST 요청을 보내지 않음
    }

    if (loginCount > 5){
      if (!captcha){
        alert("보안을 위해 캡차 인증이 필요합니다.");
        return; // POST 요청을 보내지 않음
      }
    }


    const send_data = {
      header: HEADER,
      body: {
        email: email,
        password: password,
        captcha_response: captcha
      },
    };

    fetch("https://supernova.io.kr/user_home/try_login", {
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
        setLoginCount(result.body.count)
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
      
      {
        loginCount > 5 && 
        <div style ={{
          marginBottom: "10px"
        }}>
          <ReCAPTCHA
            sitekey="6LePWrErAAAAAHE58_Rrc2Cxe9j01Ioxu8hZaysO"
            onChange={handleCaptcha}
          />
          <p style={{ display:"flex", justifyContent:"center", marginBottom: "8px", color: "#ff7676ff" }}>
            보안을 위해 캡차 인증을 완료해 주세요.
          </p>
        </div>
      }


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
