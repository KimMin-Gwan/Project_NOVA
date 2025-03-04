import React, { useEffect, useState } from "react";
import style from "./FindPw.module.css";
import backword from "./../../img/back_icon.png";
import { useNavigate } from "react-router-dom";

function FindPwChange() {
  let navigate = useNavigate();

  // 상태 관리
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [result, setResult] = useState(null);
  const [passwordError, setPasswordError] = useState(false);
  const [passwordMessage, setPasswordMessage] = useState("");
  const handlePage = (url) => {
    navigate(url);
  };

  // 비밀번호 확인 함수
  const handleSubmit = (e) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      setErrorMessage("비밀번호가 같지 않습니다.");
      return;
    } else {
      setErrorMessage("");
      handleChangePW();
    }
  };
  // 비밀번호 정규식 검증 함수
  const validatePassword = (password) => {
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{10,}$/;
    const isValid = passwordRegex.test(password);
    setPasswordError(!isValid);
    setPasswordMessage(isValid ? "" : "대소문자, 숫자, 특수문자를 포함해 10자리 이상이어야 합니다.");
    return isValid;
  };

  const handleCheckPassword = (e) => {
    const confirmPwd = e.target.value;
    setConfirmPassword(confirmPwd);

    if (confirmPwd && newPassword !== confirmPwd) {
      setErrorMessage("비밀번호가 같지 않습니다.");
    } else {
      setErrorMessage("");
    }
  };

  const header = {
    "request-type": "default",
    "client-version": "v1.0.1",
    "client-ip": "127.0.0.1",
    uid: "1234-abcd-5678",
    endpoint: "/user_system/",
  };

  const handleChangePW = () => {
    const send_data = {
      header: header,
      body: {
        password: 1234,
        new_password: newPassword,
      },
    };

    fetch("https://nova-platform.kr/user_home/try_find_password", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(send_data),
    })
      .then((response) => response.json())
      .then((data) => {
        //console.log(data);
        setResult(data.body.result);

        if (data.body.result === true) {
          alert("변경이 완료되었습니다.");
          handlePage("/");
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
      <form className={style.form} onSubmit={handleSubmit}>
        <p className={style.input_text}>새로운 비밀번호</p>
        <section className={style.section}>
          <input
            type="password"
            name="newPassword"
            className={style.input}
            value={newPassword}
            placeholder="새로운 비밀번호를 입력해주세요"
            onChange={(e) => {
              setNewPassword(e.target.value);
              validatePassword(e.target.value);
            }}
          />
          {passwordError && <p style={{ color: "red" }}>{passwordMessage}</p>}
        </section>
        <p className={style.input_text}>비밀번호 확인</p>
        <section className={style.section}>
          <input type="password" name="confirmPassword" className={style.input} value={confirmPassword} placeholder="새로운 비밀번호를 입력해주세요" onChange={handleCheckPassword} />
          {errorMessage && <p className={style.error}>{errorMessage}</p>} {/* Show error only if it exists */}
          <button type="submit" className={style.button} onClick={handleChangePW}>
            비밀번호 변경
          </button>
        </section>
      </form>
    </div>
  );
}

export default FindPwChange;
