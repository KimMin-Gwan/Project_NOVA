import { useEffect, useState } from "react";
import style from "./MainPart.module.css";
import more_icon from "./../../img/backword.png";
export default function AllPost() {
  return (
    <div className={style["wrap-container"]}>
      <div className={style["top-area"]}>
        <div className={style["content-title"]}>
          <header className={style["header-text"]}>최근 인기 게시글</header>
          <img src={more_icon} className={style["more-icon"]}></img>

          <div className={style["main-area"]}></div>
        </div>
      </div>
    </div>
  );
}
