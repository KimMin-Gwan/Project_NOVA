import search_icon from "./../../img/search_icon.png";
import arrow from "./../../img/home_arrow.svg";
import style from "./ScheduleSearch.module.css";
import React, { useState } from "react";
import TopicModal from "../TopicModal/TopicModal";
import { useNavigate } from "react-router-dom";

export default function ScheduleSearch({
  title,
  searchKeyword,
  setSearchKeyword,
  clickButton,
  fetchSearchData,
}) {
  // const [searchKeyword, setKeyword] = useState("");
  const [isClicked, setIsClicked] = useState(false);
  const navigate = useNavigate();

  const onChangeSearchKeyWord = (e) => {
    setSearchKeyword(e.target.value);
  };

  const handleClickBtn = () => {
    setIsClicked(true);
  };

  // async function fetchData() {
  //   await fetchSearchData();
  // }

  const keyword = {
    word: ["인터넷방송", "유튜버", "버튜버"],
  };

  const titleKind = [
    {
      titleName: "주제 탐색",
      button: "탐색",
    },
    {
      titleName: "일정 탐색",
      button: "등록",
    },
    {
      titleName: "이벤트 상세",
      button: "",
    },
  ];

  return (
    <div className={style["SearchSection"]}>
      <div className={style["sectionTop"]}>
        <h3>{titleKind[title].titleName}</h3>
        {titleKind[title].button !== "" && (
          <button
            onClick={() => {
              // clickButton();
              handleClickBtn();
            }}
          >
            일정 {titleKind[title].button}
          </button>
        )}
        {isClicked && <TopicModal />}
      </div>
      <div className={style["searchFac"]}>
        <div className={style["searchBox"]}>
          <input
            type="text"
            value={searchKeyword}
            onChange={onChangeSearchKeyWord}
            placeholder="키워드 또는 일정 코드를 입력해 보세요!"
          />
          <img
            src={search_icon}
            onClick={() => {
              fetchSearchData();
              navigate(`/search/topic?keyword=${searchKeyword}`);
            }}
            alt="검색바"
          />
        </div>
      </div>
      <section className={style["wordSection"]}>
        <img src={arrow} alt="화살표" />
        {keyword.word.map((item, index) => {
          return <button key={index}>{item}</button>;
        })}
      </section>
    </div>
  );
}
