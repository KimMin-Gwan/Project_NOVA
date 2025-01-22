import { useNavigate } from "react-router-dom";
import React, { useState } from "react";
import style from "./Mypage.module.css";
import backword from "./../../img/back_icon.png";
import MyEdit from "./../MyPage/MypageEdit";
function MyPage() {
  let navigate = useNavigate();

  function handleMovePage(e, page) {
    e.preventDefault();
    navigate(page);
  }

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
      <div className={style["user-container"]}>
        <div className={style["user-img"]}>이미지</div>
        <div>
          <section className={style["user-name"]}>
            <h3>사용자 이름</h3>{" "}
            <img
              src={backword}
              alt=""
              onClick={(e) => handleMovePage(e, "/mypage_edit")} // 클릭 시 /yourPage로 이동
              style={{ cursor: "pointer" }}
            />
          </section>
          <section className={style["user-info"]}>
            <ul>
              <li>
                <b>23</b>
                <p>포스트</p>
              </li>
              <li>
                <b>23</b>
                <p>포스트</p>
              </li>
              <li>
                <b>23</b>
                <p>포스트</p>
              </li>
              <li>
                <b>23</b>
                <p>포스트</p>
              </li>
            </ul>
          </section>
          <section className={style["info-list"]}>
            <ul className={style["post-list"]}>
              {["포스트", "모멘트", "좋아요", "댓글"].map((post, index) => (
                <li key={index} className={`${style.post} ${activeIndex === index ? style.active : ""}`} onClick={() => handleClick(index)}>
                  <button>{post}</button>
                </li>
              ))}
            </ul>
          </section>
        </div>
      </div>
    </div>
  );
}

export default MyPage;
