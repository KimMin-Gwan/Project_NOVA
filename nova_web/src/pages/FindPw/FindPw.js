import React from "react";
import style from "./FindPw.module.css";
import { useNavigate } from "react-router-dom";
import backword from "./../../img/back_icon.png";

function FindPw() {
  let navigate = useNavigate();

  const handlePage = (url) => {
    navigate(url);
  };

  const handleVerifyCode = () => {
    handlePage("/find_pw_change");
  };

  const header = {
    "request-type": "default",
    "client-version": "v1.0.1",
    "client-ip": "127.0.0.1",
    uid: "1234-abcd-5678",
    endpoint: "/user_system/",
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
          <input type="email" name="email" className={style.input} />
          <button type="button" className={style.button}>
            보안코드 전송
          </button>
        </section>

        <p className={style.input_text}>보안코드</p>
        <section>
          <input type="text" name="code" className={style.input} />
          <button type="button" className={style.button} onClick={handleVerifyCode}>
            보안코드 확인
          </button>
        </section>
      </form>
    </div>
  );
}

export default FindPw;
