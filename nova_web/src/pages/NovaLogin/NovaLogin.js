import React, { useEffect, useState } from "react";
import axios from "axios";
import style from "./NovaLogin.module.css";
import styleSignUp from "./../SignUp/SignUp.module.css";
// import back from "../../img/back.png";
import backword from "./../../img/back_icon.png";

import { useNavigate } from "react-router-dom";

const NOVALogin = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [login, setLogin] = useState("");
  const [detail, setDetail] = useState("");

  const navigate = useNavigate();
  const handleLogin = async () => {
    if (!email || !password) {
      alert("이메일과 비밀번호를 모두 입력해주세요.");
      return; // POST 요청을 보내지 않음
    }

    const header = {
      "request-type": "default",
      "client-version": "v1.0.1",
      "client-ip": "127.0.0.1",
      uid: "1234-abcd-5678",
      endpoint: "/user_system/",
    };

    const send_data = {
      header: header,
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
        // console.log('login', result.body);
        setLogin(result.body.result);
        setDetail(result.body.detail);
        if (result.body.result === "done") {
          navigate("/");
        }
      });
  };

  useEffect(() => {
    return () => {
      setLogin("");
      setDetail("");
    };
  }, []);

  return (
    <div className={style.container}>
      <div className={style.Topbar}>
        <img
          src={backword}
          alt="Arrow"
          className={style.backword}
          onClick={() => {
            navigate(-1);
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
              <input type="email" placeholder="이메일 주소" value={email} onChange={(e) => setEmail(e.target.value)} className={style.input} />
            </label>
            {login === "email" && <div className={style.errorMessage}>{detail}</div>}
          </div>
        {/* </div> */}

        {/* <div className={`${styleSignUp.box} ${style["box-margin"]}`}> */}
          <div className={style["input-box"]}>
            비밀번호
            <br />
            <label>
              <input type="password" placeholder="비밀번호" value={password} onChange={(e) => setPassword(e.target.value)} className={style.input} />
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
        <div className={style["sign-up"]} onClick={()=>{navigate('/find_pw')}}>비밀번호 찾기</div>
      </div>
    </div>
  );
};

export default NOVALogin;
