import style from "./WideVer.module.css";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

import direct_icon from "./../../img/direct_icon.png";
import search_icon from "./../../img/search_icon.png";
import { Link } from "react-router-dom";

export default function RightBar({ brightMode }) {
  let navigate = useNavigate();
  let [searchWord, setSearchWord] = useState("");
  let [searchHistory, setSearchHistory] = useState(storeSearchHistory);

  function storeSearchHistory() {
    const searchHistory = localStorage.getItem("history");
    return searchHistory ? JSON.parse(searchHistory) : [];
  }

  function handleNavigate() {
    if (!searchWord) {
      navigate("/");
    } else {
      navigate(`/feed_list/search_feed?keyword=${searchWord}`);
      setSearchHistory([...searchHistory, searchWord]);
      setSearchWord("");
    }
  }

  useEffect(() => {
    localStorage.setItem("history", JSON.stringify(searchHistory));
  }, [searchHistory]);

  function onKeyDown(event) {
    if (event.key === "Enter") {
      handleNavigate();
    }
  }

  function onChangeSearchWord(e) {
    setSearchWord(e.target.value);
  }

  function onDeleteHistory() {
    localStorage.removeItem("history");
    setSearchHistory([]);
  }

  return (
    <div className={style["wrap_container"]}>
      <div
        className={`${style["search-box"]} ${
          brightMode === "dark" ? style["dark-mode"] : style["light-mode"]
        }`}
      >
        {/* <h4 className={style["wide-text"]}>검색</h4> */}
        <div className={style["search-bar"]}>
          <input
            type="text"
            value={searchWord}
            onChange={onChangeSearchWord}
            onKeyDown={onKeyDown}
          ></input>
          <button onClick={handleNavigate}>
            <img src={search_icon} className={style["icon-text"]}></img>
          </button>
        </div>
        <span className={style["search-memo"]}>
          <p>검색기록</p>
          <p onClick={onDeleteHistory}>X</p>
        </span>
        {searchHistory.length > 0 &&
          searchHistory.map((history, i) => {
            return <div>{history}</div>;
          })}
      </div>

      <div className={style["nova_direct-box"]}>
        <img src={direct_icon} alt="노바펀딩 바로가기" className={style["icon-text"]}></img>
        <Link to="/nova_funding" className={style["go-nova"]}>
          노바펀딩 바로가기
        </Link>
      </div>

      <div className={style["ad-container"]}>광고</div>
    </div>
  );
}
