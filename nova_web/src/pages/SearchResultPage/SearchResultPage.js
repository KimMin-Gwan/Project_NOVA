import { useNavigate } from "react-router-dom";
import SearchBox from "../../component/SearchBox";
import { useState } from "react";
import back from "./../../img/backword.png";
import logo2 from "../../img/logo2.png";

import style from "./../MyPage/Mypage.module.css";
import "./../SearchPage/index.css";

export default function SearchResultPage() {
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
    <div className="container">
      <header className="header">
        <div
          className="logo"
          onClick={() => {
            navigate("/");
          }}
        >
          <img src={logo2} alt="logo" className={`logo-st`}></img>
        </div>
      </header>
      <div className="top-bar">
        <div className="back">
          <img src={back} />
        </div>
        <SearchBox type="search" />
        <section className={style["info-list"]}>
          <ul className={style["post-list"]}>
            {["포스트", "모멘트", "좋아요", "댓글"].map((post, index) => (
              <li
                key={index}
                className={`${style.post} ${activeIndex === index ? style.active : ""}`}
                onClick={() => handleClick(index)}
              >
                <p>{post}</p>
              </li>
            ))}
          </ul>
        </section>
      </div>
    </div>
  );
}
