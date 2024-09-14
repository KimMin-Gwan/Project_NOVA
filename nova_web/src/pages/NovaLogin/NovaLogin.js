import React, { useEffect, useState } from "react";
import axios from "axios";
import style from "./NovaLogin.module.css";
import back from "../../img/back.png";
import { useNavigate } from 'react-router-dom';


const NOVALogin = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
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
      "uid": "1234-abcd-5678",
      "endpoint": "/user_system/",
    };

    const send_data = {
      header: header,
      body: {
        email: email,
        password: password,
      },
    };

    // "http://nova-platform.kr/user_home/try_login",

    fetch("http://127.0.0.1:4000/user_home/try_login",
      {
        method: 'post',
        headers: {
          "Content-Type": 'application/json',
        },
        body: JSON.stringify(send_data),
      }
    )
      .then(response => response.json())
      .then(result => {
        console.log(result.body);
        // setCheckSupport(result.body.result);
        // setMyCtb(result.body.my_contribution);
      })


    // .catch(error) {
    // console.error("로그인 요청 중 오류가 발생했습니다:", error);
    // console.error('Error:', error.response ? error.response.data : error.message);
    // alert("로그인 중 오류가 발생했습니다.");

    // try {
    //   const response = await axios.post(
    //     "http://127.0.0.1:4000/user_home/try_login",
    //     send_data,
    //     {
    //       headers: {
    //         "Content-Type": 'application/json',
    //       },
    //       withCredentials: true
    //     }
    //   );

    // const result = response.data.body;

    // console.log(result.resust)

    // if (result.resust) {
    //   // 로그인 성공 시 JWT 토큰 저장 (예: 로컬 스토리지)
    //   localStorage.setItem("jwtToken", result.token);
    //   navigate('/')
    // } else {
    //   alert("로그인 실패: " + result.detail);
    // }
    // } catch (error) {
    //   console.error("로그인 요청 중 오류가 발생했습니다:", error);
    //   console.error('Error:', error.response ? error.response.data : error.message);
    //   alert("로그인 중 오류가 발생했습니다.");
    // }
  };

  return (
    <div className={style.container}>
      <div className={style.Header}>
        <div className={style.BackBtn}>
          <button className="tool-button">
            <img src={back} alt="Back" className="backword" onClick={() => {
              alert("뒤로가기")
              navigate(-1)
            }}></img>
          </button>
        </div>
        <div className={style.Top}>
          <h3>로그인</h3>
        </div>
      </div>
      <div className={style.form}>
        <label className={style.label}>아이디</label>
        <input
          type="email"
          placeholder="이메일 주소"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className={style.input}
        />
        <label className='label'>비밀번호</label>
        <input
          type="password"
          placeholder="비밀번호"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className={style.input}
        />
        <button className={style.loginButton} onClick={handleLogin}>
          로그인
        </button>
        <div className={style['sign-up']}>회원가입</div>
      </div>
    </div>
  );
};


export default NOVALogin;
