import { useEffect, useState } from "react";
import style from "./SignUp.module.css";
import { useLocation, useNavigate } from "react-router-dom";
import backword from "./../../img/back_icon.png";
export default function SignUp() {
  let [inputEmail, setInputEmail] = useState("");
  let [authen, setAuthen] = useState(false);
  let [code, setCode] = useState("");
  let [pwd, setPwd] = useState("");
  let [checkPwd, setCheckPwd] = useState("");
  let [birthYear, setBirthYear] = useState("2000");
  let [gender, setGender] = useState("none");
  const location = useLocation();
  let navigate = useNavigate();
  const [agree1, setAgree1] = useState(false);
  const [agree2, setAgree2] = useState(false);
  const [allAgree, setAllAgree] = useState(false);
  let [emailError, setEmailError] = useState(false);
  let [passwordError, setPasswordError] = useState(false);
  let [passwordMessage, setPasswordMessage] = useState("");
  let [isCheckPwdFocused, setIsCheckPwdFocused] = useState(false);
  let [showPassword, setShowPassword] = useState(false);
  let [showCheckPassword, setShowCheckPassword] = useState(false);

  let [errorMessage, setErrorMessage] = useState("이메일 형식으로 아이디를 입력해주세요.");

  let header = {
    "request-type": "default",
    "client-version": "v1.0.1",
    "client-ip": "127.0.0.1",
    uid: "1234-abcd-5678",
    endpoint: "/user_system/",
  };

  let send_data = {
    header: header,
    body: {
      email: inputEmail,
    },
  };

  let signUp_data = {
    header: header,
    body: {
      email: inputEmail,
      password: pwd,
      verification_code: code,
      birth_year: birthYear,
      gender: gender,
    },
  };

  function handleInputEmail(e) {
    const email = e.target.value;
    setInputEmail(email);
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    setEmailError(!emailRegex.test(email));
  }
  function handlePassWord(e) {
    const password = e.target.value;
    setPwd(password);

    const passwordRegex = /^(?=.*[a-z])(?=.*\d)(?=.*[@$#!%*?&])[a-z\d@$#!%*?&]{8,}$/;

    const isValid = passwordRegex.test(password);

    setPasswordError(!isValid);
    setPasswordMessage(isValid ? "" : "영문, 숫자, 특수문자를 포함해 8자리 이상이어야 합니다.");
  }

  function handleCheckPassWord(e) {
    const confirmPwd = e.target.value;
    setCheckPwd(confirmPwd);

    if (isCheckPwdFocused) {
      setPasswordError(confirmPwd !== pwd);
    }
  }
  function handleBirthYear(e) {
    const value = e.target.value;
    if (/^\d*$/.test(value)) {
      setBirthYear(value); // 입력은 그대로 반영
    }
  }

  function handleBirthYearBlur() {
    if (birthYear === "") return; // 빈값이면 패스

    let num = parseInt(birthYear, 10);

    if (num < 1900) num = 1900;
    if (num > 2020) num = 2020;

    setBirthYear(num.toString());
  }

  function handleKeyDown(e) {
    if (!/[0-9]/.test(e.key) && e.key !== "Backspace" && e.key !== "Delete" && e.key !== "Tab") {
      e.preventDefault();
    }
  }

  function handleGender(gender) {
    console.log(gender);
    setGender(gender);
  }

  function handleCode(e) {
    let value = e.target.value;

    // 숫자만 허용
    value = value.replace(/\D/g, "");

    // 최대 4자리 제한
    if (value.length > 4) {
      value = value.slice(0, 4);
    }

    setCode(value);
  }

  useEffect(() => {
    return setInputEmail("");
  }, []);

  function fetchAuthenEmail() {
    fetch(`https://supernova.io.kr/user_home/try_send_email`, {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify(send_data),
    })
      .then((response) => response.json())
      .then((data) => {
        const newAuthen = data.body.result;
        setAuthen(newAuthen);

        setEmailError(!emailError);
        setErrorMessage(data.body.detail);
      });
    if (authen) {
      alert("인증코드가 전송되었습니다");
    }
  }

  function fetchSignUp() {
    fetch(`https://supernova.io.kr/user_home/try_sign_up`, {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify(signUp_data),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.body.result) {
          alert("회원가입이 완료되었습니다.");
          navigate("/novalogin");
        } else {
          alert(data.body.detail);
        }
      });
  }

  function handleSubmit(e) {
    e.preventDefault();

    if (pwd !== checkPwd) {
      alert("비밀번호가 같지 않습니다.");
      return;
    }
    fetchSignUp();
  }

  const handleAllAgreeChange = (e) => {
    const isChecked = e.target.checked;
    setAllAgree(isChecked);
    setAgree1(isChecked);
    setAgree2(isChecked);
  };

  const handleIndividualChange = (e) => {
    const { name, checked } = e.target;
    if (name === "agree1") {
      setAgree1(checked);
      setAllAgree(checked && agree2);
    } else if (name === "agree2") {
      setAgree2(checked);
      setAllAgree(checked && agree1);
    }
  };

  return (
    <div className={style.container}>
      <div className={style.Topbar}>
        <img
          src={backword}
          alt="Arrow"
          className={style.backword}
          onClick={() => {
            navigate('/');
          }}
        />
        <div className={style.title}>회원가입</div>
        <div className={style.EmptyBox} />
      </div>
      <div>
        <form onSubmit={(e) => handleSubmit(e)}>
          <div className={style.box}>
            <div className={style.test}>
              이메일 주소
              <br />
              <label>
                <input type="email" name="email" value={inputEmail} placeholder="사용할 이메일 주소를 입력하세요" onChange={(e) => handleInputEmail(e)} required className={emailError ? style.error : ""} />
                <button
                  className={style.authen}
                  disabled={!inputEmail}
                  style={{
                    background: inputEmail ? "#107BF4" : "",
                    color: inputEmail ? "white" : "",
                    pointerEvents: inputEmail ? "auto" : "none",
                  }}
                  onClick={() => {
                    fetchAuthenEmail();
                  }}
                >
                  인증
                </button>
                {emailError && <p className={style.errorMessage}>{errorMessage}</p>}
              </label>
            </div>
          </div>

          <div className={style.box}>
            <div className={style.test}>
              인증번호
              <br />
              <label>
                <input
                  name="password"
                  placeholder="이메일 확인 후 4자리 코드를 입력해주세요"
                  required
                  maxLength={4}
                  onChange={(e) => {
                    handleCode(e);
                  }}
                ></input>
              </label>
            </div>
          </div>

          <div className={style.box}>
            <div className={style.test}>
              비밀번호
              <br />
              <label className={style.inputContainer}>
                <input type={showPassword ? "text" : "password"} name="password" required onChange={(e) => handlePassWord(e)} placeholder="영문 + 숫자 조합, 8자 이상이어야 합니다" className={passwordError && passwordMessage ? style.error : ""} />
                <button type="button" onClick={() => setShowPassword(!showPassword)} className={style.toggleButton}>
                  {showPassword ? "숨기기" : "보기"}
                </button>
                {passwordMessage && <p className={style.errorMessage}>{passwordMessage}</p>}
              </label>
            </div>
          </div>

          <div className={style.box}>
            <div className={style.test}>
              비밀번호 확인
              <br />
              <label className={style.inputContainer}>
                <input type={showCheckPassword ? "text" : "password"} name="check_pwd" required onChange={(e) => handleCheckPassWord(e)} placeholder="비밀번호 확인을 위해 다시 입력해주세요" onFocus={() => setIsCheckPwdFocused(true)} className={passwordError && pwd && isCheckPwdFocused ? style.error : ""} />
                <button type="button" onClick={() => setShowCheckPassword(!showCheckPassword)} className={style.toggleButton}>
                  {showCheckPassword ? "숨기기" : "보기"}
                </button>
                {passwordError && pwd && isCheckPwdFocused && <p className={style.errorMessage}>비밀번호가 일치하지 않습니다.</p>}
              </label>
            </div>
          </div>

          <div className={style.box}>
            <div className={style.test}>
              태어난 해
              <br />
              <label>
                <input type="number" name="age" 
                 value={birthYear} min="1900" max="2020"
                 required onChange={handleBirthYear}
                 onKeyDown={handleKeyDown}
                 onBlur={handleBirthYearBlur}
                 placeholder="2000" />
              </label>
            </div>
          </div>

          <div className={style.box}>
            <div className={style.test}>
              성별
            <div className={style.genderButtonWrapper}>
              <br />
              <div
                className={style.genderButton}
                style={gender === "male" ? { backgroundColor: "#107BF4", color: "white" } : {}}
                onClick={() => handleGender("male")}
              >
                남자
              </div>

              <div className={style.genderButton}
                style={gender === "female" ? { backgroundColor: "#107BF4", color: "white" } : {}}
                onClick={() => handleGender("female")}
              >
                여성
              </div>
              <div className={style.genderButton}
                style={gender === "none" ? { backgroundColor: "#107BF4", color: "white" } : {}}
                onClick={() => handleGender("none")}
              >
                비공개
              </div>
            </div>
            </div>
          </div>

          <div className={style.box}>
            <div className={style.agree_box}>
              <label>
                <input type="checkbox" name="agree1" checked={agree1} onChange={handleIndividualChange} required />
                <span className={style.termsDetail}>
                  (필수) 이용약관 동의
                </span>
                <p onClick={() => window.open('https://supernova.io.kr/service_terms_and_conditions.pdf', '_blank')}>상세보기</p>
              </label>
              <label>
                <input type="checkbox" name="agree2" checked={agree2} onChange={handleIndividualChange} required />
                <span className={style.termsDetail}>
                  (필수) 개인정보처리 동의
                </span>
                <p onClick={() => window.open('https://supernova.io.kr/personal_information_processing_agreement.pdf', '_blank')}>상세보기</p>
              </label>
            </div>
          </div>
          <div className={style.all_check}>
            <input type="checkbox" name="all-agree" checked={allAgree} onChange={handleAllAgreeChange} />
            약관 전체 동의
          </div>
          <div className={style["submit_area"]}>
            <button type="submit" className={style["submit_btn"]}>
              노바 시작하기
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
