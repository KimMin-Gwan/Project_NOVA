import React, { useState } from "react";
import "./Signup.css";
import back from "../img/back.png";
import { useNavigate } from "react-router-dom";
import Button from "../component/button/button";
import axios from "axios";
import Cookies from "js-cookie"; // 쿠키에 저장하기 위해 js-cookie 패키지를 사용합니다.

export default function Signup() {
  const nav = useNavigate();

  const [email, setEmail] = useState("");
  const [verificationCode, setVerificationCode] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("");
  const [emailError, setEmailError] = useState("");
  const [allChecked, setAllChecked] = useState(false);
  const [termsChecked, setTermsChecked] = useState({
    termsOfService: false,
    privacyPolicy: false,
  });

  const validateEmail = () => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    //^문자열을 나타내고, [^\s@]= 공백이나 @이로 시작하지 않는 문자열을 나타낸다.
    if (!email) {
      setEmailError("이메일을 입력해주세요.");
      return false;
    } else if (!emailRegex.test(email)) {
      setEmailError("유효한 이메일 주소를 입력해주세요.");
      return false;
    } else {
      setEmailError("");
      return true;
    }
  };

  const onClickUpdate = () => {
    if (validateEmail() && password === passwordConfirm) {
      // 서버로 데이터 전송
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
          verification_code: verificationCode,
          password: password,
          age: age,
          gender: gender,
        },
      };

      axios
        .post("https://your-server-endpoint.com/api/auth/signup", send_data)
        .then((response) => {
          if (response.data.success) {
            // 서버가 성공을 반환했을 때
            const token = response.data.token;

            // 토큰을 쿠키에 저장합니다.
            Cookies.set("authToken", token, { expires: 7 }); // 7일 동안 유효한 쿠키로 설정

            console.log("로그인에 성공했습니다.");
            // 필요시 다른 페이지로 이동
            nav("/dashboard");
          } else {
            console.log("인증 실패:", response.data.message);
          }
        })
        .catch((error) => {
          console.error("에러 발생:", error);
          // 에러 처리
        });
    } else if (password !== passwordConfirm) {
      setEmailError("비밀번호가 일치하지 않습니다.");
    }
  };

  const handleAllChecked = () => {
    const newCheckedState = !allChecked;
    setAllChecked(newCheckedState);
    setTermsChecked({
      termsOfService: newCheckedState,
      privacyPolicy: newCheckedState,
    });
  };

  const handleIndividualCheck = (e) => {
    const { name, checked } = e.target;
    //개별 체크박스의 상태를 업데이트
    setTermsChecked((prevState) => ({
      ...prevState,
      [name]: checked,
    }));
    //모든 체크박스가 선택된 경우 '전체 동의'체크박스를 자동으로 체크
    setAllChecked(
      checked &&
        Object.values({ ...termsChecked, [name]: checked }).every(Boolean)
    );
  };

  return (
    <div className="SignupContainer">
      <div className="Header">
        <div className="BackBtn">
          <button onClick={() => nav(-1)}>
            <img src={back} alt="Back"></img>
          </button>
        </div>
        <div className="Top">
          <h3>회원가입</h3>
        </div>
      </div>
      <div className="Info">
        <div className="EmailContainer">
          <span>이메일 주소</span>
          <div className="EmailFunc">
            <input
              placeholder="이메일을 입력해주세요"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <Button onClick={onClickUpdate} text={"인증"} />
          </div>
          {emailError && <span className="error">{emailError}</span>}
        </div>
        <div className="ConfirmContainer">
          <span>인증번호</span>
          <input
            placeholder="인증번호를 입력하세요"
            value={verificationCode}
            onChange={(e) => setVerificationCode(e.target.value)}
          />
        </div>
        <div className="PasswordContainer">
          <span>비밀번호</span>
          <input
            placeholder="비밀번호를 입력하세요"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
          />
        </div>
        <div className="PasswordConfirm">
          <span>비밀번호 확인</span>
          <input
            placeholder="비밀번호 확인"
            value={passwordConfirm}
            onChange={(e) => setPasswordConfirm(e.target.value)}
            type="password"
          />
        </div>
        <div className="AgeContainer">
          <span>나이</span>
          <input
            placeholder="나이를 입력하세요"
            value={age}
            onChange={(e) => setAge(e.target.value)}
          />
        </div>
        <div className="SexContainer">
          <span>성별</span>
          <div className="SexBtn">
            <Button text={"남성"} onClick={() => setGender("male")} />
            <Button text={"여성"} onClick={() => setGender("female")} />
            <Button text={"기타"} onClick={() => setGender("other")} />
            <Button text={"비공개"} onClick={() => setGender("private")} />
          </div>
        </div>
        <div className="ContractContainer">
          <span>약관동의</span>
          <div className="ContractBox">
            <div className="contract1">
              <input
                type="checkbox"
                className="custom-checkbox"
                name="termsOfService"
                checked={termsChecked.termsOfService}
                onChange={handleIndividualCheck}
              />
              <div className="spec">
                <span>(필수) 이용약관 동의</span>
                <a href="#" className="detail-link">
                  상세보기
                </a>
              </div>
            </div>
            <div className="contract2">
              <input
                type="checkbox"
                className="custom-checkbox"
                name="privacyPolicy"
                checked={termsChecked.privacyPolicy}
                onChange={handleIndividualCheck}
              />
              <div className="spec">
                <span>(필수) 개인정보처리 동의</span>
                <a href="#" className="detail-link">
                  상세보기
                </a>
              </div>
            </div>
          </div>

          <div className="AllContractConfirm">
            <input
              type="checkbox"
              className="custom-checkbox"
              checked={allChecked}
              onChange={handleAllChecked}
            />
            <span> 약관 전체 동의</span>
          </div>
        </div>

        <div className="StartBtn">
          <Button text={"노바 시작하기"} onClick={onClickUpdate} />
        </div>
      </div>
    </div>
  );
}
