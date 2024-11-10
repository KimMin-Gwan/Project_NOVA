import style from "./WideVer.module.css";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

import direct_icon from "./../../img/direct_icon.png";
import search_icon from "./../../img/search_icon.png";
import { Link } from "react-router-dom";

export default function RightBar({ brightMode }) {
  return (
    <div className={style["wrap_container"]}>
      <div className={`${style["search-box"]} ${brightMode === "dark" ? style["dark-mode"] : style["light-mode"]}`}>
        <h4 className={style["wide-text"]}>검색</h4>
        <div className={style["search-bar"]}>
          <input></input>
          <button>
            <img src={search_icon} className={style["icon-text"]}></img>
          </button>
        </div>
        <span className={style["search-memo"]}>
          <p>검색기록</p>
          <p>X</p>
        </span>
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
