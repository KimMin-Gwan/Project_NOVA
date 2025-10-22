import React, { useState } from "react";
import style from "./FindPw.module.css";
import { useNavigate } from "react-router-dom";
import backword from "./../../img/back_icon.png";

function FindPw() {
  const [email, setEmail] = useState("");
  const [result, setResult] = useState(null);
  const [detail, setDetail] = useState("");
  const [code, setCode] = useState("");
  const [feedbackMessage, setFeedbackMessage] = useState(""); // ✅ 피드백 상태

  const navigate = useNavigate();
  const handlePage = (url) => navigate(url);

  const header = {
    "request-type": "default",
    "client-version": "v1.0.1",
    "client-ip": "127.0.0.1",
    uid: "1234-abcd-5678",
    endpoint: "/user_system/",
  };

  const clickVerifyCode = () => {
    if (!email) {
      setFeedbackMessage("이메일을 입력해주세요.");
      return;
    }

    const send_data = {
      header: header,
      body: { email },
    };

    fetch("https://supernova.io.kr/user_home/try_find_password_send_email", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(send_data),
    })
      .then((response) => response.json())
      .then((data) => {
        setResult(data.body.result);
        setDetail(data.body.detail);

        if (data.body.result === true) {
          setFeedbackMessage("보안코드가 이메일로 전송되었습니다.");
        } else {
          setFeedbackMessage(`❌ ${data.body.detail || "보안코드 전송에 실패했습니다. 운영자에게 문의하세요."}`);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        setFeedbackMessage("보안코드가 일치하지 않습니다. 다시 시도해주세요.");
      });
  };

  const handleSecurityCode = () => {
    const send_data = {
      header: header,
      body: { email, verification_code: code },
    };

    fetch("https://supernova.io.kr/user_home/try_login_temp_user", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(send_data),
    })
      .then((response) => response.json())
      .then((data) => {
        setResult(data.body.result);

        if (data.body.result === "done") {
          navigate("/find_pw_change");
        } else {
          setFeedbackMessage("❌ 보안코드가 잘못되었습니다. 다시 시도해주세요.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        setFeedbackMessage("⚠️ 요청 중 오류가 발생했습니다.");
      });
  };

  const handleCode = (e) => {
    const value = e.target.value;

    // 숫자만 남기기
    const onlyNums = value.replace(/[^0-9]/g, '');

    // 4자리까지만 허용
    const limited = onlyNums.slice(0, 4);

    setCode(limited);
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
        <section className={style.section}>
          <input
            type="email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className={style.input}
            placeholder="이메일을 입력해주세요"
          />
          {feedbackMessage && <p className={style.feedback}>{feedbackMessage}</p>} {/* ✅ 피드백 표시 */}
          <button type="button" className={style.button} onClick={clickVerifyCode}>
            보안코드 전송
          </button>
        </section>

        <p className={style.input_text}>보안코드</p>
        <section className={style.section}>
          <input
            type="text"
            name="code"
            value={code}
            onChange={(e) => handleCode(e)}
            className={style.input}
            placeholder="보안코드를 입력해주세요"
          />
          <button type="button" className={style.button} onClick={handleSecurityCode}>
            보안코드 확인
          </button>
        </section>
      </form>
    </div>
  );
}

export default FindPw;
