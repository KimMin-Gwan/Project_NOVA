import search_icon from "./../../img/search_icon.png";
import arrow from "./../../img/home_arrow.svg";
import style from "./ScheduleSearch.module.css";
import React, {useState, useEffect} from "react";

import Input from "../Input/Input";
import { TITLE_TYPES } from "../../constant/type_data";
import { useNavigate, useSearchParams } from "react-router-dom";

import back from "./Vector.svg";
import mainApi from "../../services/apis/mainApi";

//const KEYWORD = ["인터넷방송", "유튜버", "버튜버"];

const TITLES = {
  [TITLE_TYPES.BIAS]: { titleName: "주제 탐색", button: "탐색" },
  [TITLE_TYPES.SCHEDULE]: { titleName: "일정 탐색", button: "등록" },
  [TITLE_TYPES.EVENT]: { titleName: "이벤트 상세", button: "" },
};

export default function ScheduleSearch({
  title,
  makeSchedule,
  searchKeyword,
  setSearchKeyword,
  fetchSearchData,
}) {
  const titles = TITLES[title];
  const onChangeSearchKeyWord = (e) => {
    setSearchKeyword(e.target.value);
  };

  let navigate = useNavigate();
  const [keywords, setKeywords] = useState([]);

  // 주간 날짜 받기
  function fetchRecommendKeyword() {
    mainApi.get("time_table_server/try_get_recommend_keyword").then((res) => {
      setKeywords(res.data.body.recommend_keywords)
    });
  }
  useEffect(()=>{
    fetchRecommendKeyword()
  }, [])


  return (
    <div className={style["SearchSection"]}>
      <div className={style["top-container"]}>
        <div
          className={style["back-button"]}
          onClick={() => {
            navigate(-1);
          }}
        >
          <img src={back} alt="back" />
          <span> 뒤로</span>
        </div>
      </div>
      <div className={style["sectionTop"]}>
        <h3>{titles.titleName}</h3>
        {titles.button !== "" && <button
            onClick={() => {
              makeSchedule();
            }}
        >일정 {titles.button}</button>}
      </div>
      <div className={style["searchFac"]}>
        <div className={style["searchBox"]}>
          <Input
            type="text"
            value={searchKeyword}
            onChange={onChangeSearchKeyWord}
            placeholder="키워드 또는 일정 코드를 입력해 보세요!"
          />
          <img
            src={search_icon}
            onClick={() => {
              fetchSearchData();
            }}
            alt="검색바"
          />
        </div>
      </div>
      <section className={style["wordSection"]}>
        <img src={arrow} alt="화살표" />
        {keywords.map((item, index) => {
          return <button key={index}>{item}</button>;
        })}
      </section>
    </div>
  );
}
