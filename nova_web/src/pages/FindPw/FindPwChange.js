import React, { useState } from "react";
import style from "./FindPw.module.css";
import backword from "./../../img/back_icon.png";
import { useNavigate } from "react-router-dom";

function FindPwChange() {
  const navigate = useNavigate();

  // 상태 관리
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [feedbackMessage, setFeedbackMessage] = useState(""); // 성공/실패 피드백
  const [loading, setLoading] = useState(false);

  const handlePage = (url) => navigate(url);

  // ✅ 비밀번호 정규식: 영어 대소문자 + 숫자 조합, 8자리 이상 (공백/특수문자 불허)
  const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$/;

  // 비밀번호 검증 함수
  const validatePassword = (password) => {
    if (!passwordRegex.test(password)) {
      setPasswordError("비밀번호는 영어 대소문자와 숫자를 포함해 8자리 이상이어야 합니다.");
      return false;
    } else {
      setPasswordError("");
      return true;
    }
  };

  // 비밀번호 입력 변경
  const handlePasswordChange = (e) => {
    const value = e.target.value;
    setNewPassword(value);
    validatePassword(value);
  };

  // 비밀번호 확인 입력
  const handleConfirmPasswordChange = (e) => {
    const value = e.target.value;
    setConfirmPassword(value);

    if (value && value !== newPassword) {
      setPasswordError("비밀번호가 일치하지 않습니다.");
    } else {
      setPasswordError("");
    }
  };

  // 비밀번호 변경 요청
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validatePassword(newPassword)) return;

    if (newPassword !== confirmPassword) {
      setPasswordError("비밀번호가 일치하지 않습니다.");
      return;
    }

    setPasswordError("");
    setFeedbackMessage("");
    setLoading(true);

    const send_data = {
      header: {
        "request-type": "default",
        "client-version": "v1.0.1",
        "client-ip": "127.0.0.1",
        uid: "1234-abcd-5678",
        endpoint: "/user_system/",
      },
      body: {
        password: "1234", // ✅ 실제 기존 비밀번호 입력이 필요하면 수정
        new_password: newPassword,
      },
    };

    try {
      const response = await fetch("https://supernova.io.kr/user_home/try_find_password", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(send_data),
      });

      const data = await response.json();

      if (data?.body?.result === true) {
        setFeedbackMessage("비밀번호가 성공적으로 변경되었습니다.");
        setTimeout(() => navigate("/"), 1500);
      } else {
        setFeedbackMessage("❌ 비밀번호 변경에 실패했습니다. 다시 시도해주세요.");
      }
    } catch (error) {
      console.error("Error:", error);
      setFeedbackMessage("⚠️ 요청 중 오류가 발생했습니다. 네트워크를 확인해주세요.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={style.container}>
      <div className={style.Topbar}>
        <img src={backword} alt="Arrow" className={style.backword} onClick={() => handlePage(-1)} />
        <div className={style.title}>비밀번호 변경</div>
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
            onChange={handlePasswordChange}
            enterKeyHint="done"
          />
        </section>

        <p className={style.input_text}>비밀번호 확인</p>
        <section className={style.section}>
          <input
            type="password"
            name="confirmPassword"
            className={style.input}
            value={confirmPassword}
            placeholder="비밀번호를 다시 입력해주세요"
            onChange={handleConfirmPasswordChange}
            enterKeyHint="done"
          />
        </section>

        {passwordError && <p className={style.error}>{passwordError}</p>}

        <button type="submit" className={style.button} disabled={loading}>
          {loading ? "변경 중..." : "비밀번호 변경"}
        </button>

        {feedbackMessage && <p className={style.feedback}>{feedbackMessage}</p>}
      </form>
    </div>
  );
}

export default FindPwChange;
