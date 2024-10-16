import React, { useState } from "react";
import style from "./FindPw.module.css";
import backword from "./../../img/back_icon.png";
import { useNavigate } from "react-router-dom";

function FindPwChange() {
  let navigate = useNavigate();

  // 상태 관리
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handlePage = (url) => {
    navigate(url);
  };

  // 비밀번호 확인 함수
  const handleSubmit = (e) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      setErrorMessage("비밀번호가 같지 않습니다.");
    } else {
      setErrorMessage("");
    }
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

  return (
    <div className={style.container}>
      <div className={style.Topbar}>
        <img src={backword} alt="Arrow" className={style.backword} onClick={() => handlePage(-1)} />
        <div className={style.title}>비밀번호 찾기</div>
        <div className={style.EmptyBox} />
      </div>
      <form className={style.form} onSubmit={handleSubmit}>
        <p className={style.input_text}>새로운 비밀번호</p>
        <section className="section">
          <input type="password" name="newPassword" className={style.input} value={newPassword} onChange={(e) => setNewPassword(e.target.value)} />
        </section>
        <p className={style.input_text}>비밀번호 확인</p>
        <section>
          <input type="password" name="confirmPassword" className={style.input} value={confirmPassword} onChange={handleCheckPassword} />
          {errorMessage && <p className={style.error}>{errorMessage}</p>} {/* Show error only if it exists */}
          <button type="submit" className={style.button}>
            비밀번호 변경
          </button>
        </section>
      </form>
    </div>
  );
}

export default FindPwChange;
