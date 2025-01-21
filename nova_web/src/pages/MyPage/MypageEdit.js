import { useNavigate } from "react-router-dom";
import React, { useState } from "react";
import style from "./Mypage.module.css";

function MyPage() {
  let navigate = useNavigate();

  const handleLogout = (e) => {
    e.preventDefault();
    fetch("https://nova-platform.kr/user_home/try_logout", {
      credentials: "include",
    })
      .then((response) => {
        if (!response.ok) {
          return response.text().then((text) => {
            throw new Error(`Error: ${response.status}, ${text}`);
          });
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
        navigate("/");
      })
      .catch((error) => {
        console.error("Logout error:", error);
      });
  };

  const [activeIndex, setActiveIndex] = useState(null);

  const handleClick = (index) => {
    setActiveIndex(index);
  };
  return (
    <div className={style.container}>
      <div className={style.top_area}>
        <p
          className={style.backword}
          onClick={() => {
            navigate(-1);
          }}
        >
          뒤로
        </p>
      </div>
      <div className={style["user-img-edit"]}>이미지</div>
      <button>프로필 사진 변경</button>

      <section>
        <h3>프로필 정보</h3>
        <p>닉네임</p>
        <input type="text" placeholder="사용자 이름" />
        <button>변경</button>

        <p>비밀번호 변경</p>
        <div>
          <input type="text" placeholder="기존 비밀번호" />
          <input type="text" placeholder="새로운 비밀번호" />
          <input type="text" placeholder="비밀번호 확인" />
        </div>
        <button>변경</button>
      </section>

      <section>
        <h3>개인정보</h3>
        <p>uid</p>
        <input type="text" placeholder="1234-1234-1234" />
        <p>email</p>
        <input type="text" placeholder="asd@naver.com" />
        <p>나이</p>
        <input type="text" placeholder="24살" />
        <p>성별별</p>
        <input type="text" placeholder="남성" />
      </section>
      <div className={`${style["logout_box"]}`} onClick={handleLogout} style={{ cursor: "pointer" }}>
        로그아웃
      </div>
    </div>
  );
}

export default MyPage;
