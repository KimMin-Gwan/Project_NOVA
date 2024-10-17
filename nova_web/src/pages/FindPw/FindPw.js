import React, { useEffect, useState } from "react";
import style from "./FindPw.module.css";
import { useNavigate } from "react-router-dom";
import backword from "./../../img/back_icon.png";

function FindPw() {
  const [email, setEmail] = useState("");
  const [result, setResult] = useState(null);
  const [detail, setDetail] = useState("");
  const [coderesult, setcodeResult] = useState("");
  const [code, setCode] = useState("");
  let navigate = useNavigate();
  const handlePage = (url) => {
    navigate(url);
  };

  const header = {
    "request-type": "default",
    "client-version": "v1.0.1",
    "client-ip": "127.0.0.1",
    uid: "1234-abcd-5678",
    endpoint: "/user_system/",
  };

  const clickVerifyCode = () => {
    const send_data = {
      header: header,
      body: {
        email: email,
      },
    };

    fetch("https://nova-platform.kr/user_home/try_find_password_send_email", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(send_data),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setResult(data.body.result);
        setDetail(data.body.detail);
      });
  };

  const handleSecurityCode = () => {
    const send_data = {
      header: header,
      body: {
        email: email,
        verification_code: code,
      },
    };

    fetch("https://nova-platform.kr/user_home/try_login_temp_user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(send_data),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setResult(data.body.result);

        if (data.body.result === "done") {
          handlePage("/find_pw_change");
        } else {
          alert("보안코드가 잘못되었습니다. 다시 시도해 주세요.");
        }
      })

      .catch((error) => {
        console.error("Error:", error);
        alert("요청 중 오류가 발생했습니다.");
      });
  };

  return (
    <div className={style.container}>
      <div className={style.Topbar}>
        <img src={backword} alt="Arrow" className={style.backword} onClick={() => handlePage(-1)} />
        <div className={style.title}>비밀번호 찾기</div>
        <div className={style.EmptyBox} />
      </div>

      <form className={style.form}>
        <p className={style.input_text}>이메일 주소</p>
        <section>
          <input type="email" name="email" value={email} onChange={(e) => setEmail(e.target.value)} className={style.input} />
          {!result && <div className={style.error}>{detail}</div>}
          <button type="button" className={style.button} onClick={clickVerifyCode}>
            보안코드 전송
          </button>
        </section>

        <p className={style.input_text}>보안코드</p>
        <section>
          <input type="text" name="code" value={code} onChange={(e) => setCode(e.target.value)} className={style.input} />
          <button type="button" className={style.button} onClick={handleSecurityCode}>
            보안코드 확인
          </button>
        </section>
      </form>
    </div>
  );
}

export default FindPw;
