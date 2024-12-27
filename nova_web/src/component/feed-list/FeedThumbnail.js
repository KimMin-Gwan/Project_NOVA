import { useEffect, useState } from "react";
import SimpleSlider from "../SimpleSlider";
import style from "./FeedThumbnail.module.css";
import more_icon from "../../img/Icon.png";
import search_icon from "./../../img/search_icon.png";
import pin from "./../../img/pin.png";

import { useNavigate } from "react-router-dom";

export default function FeedThumbnail({
  title,
  feedData,
  brightMode,
  hasSearchBox,
  children,
  allPost,
  endPoint,
}) {
  let navigate = useNavigate();
  const [mode, setMode] = useState(brightMode); // 초기 상태는 부모로부터 받은 brightMode 값

  useEffect(() => {
    setMode(brightMode); // brightMode 값이 바뀔 때마다 mode 업데이트
  }, [brightMode]);

  return (
    <section className={style["FeedThumbnail"]}>
      <div className={style["title-section"]}>
        <div className={style["title"]}>
          <img src={pin} />
          {title}
        </div>
        <div className={`${style["more-icon"]}`}>
          <img src={more_icon} alt="더보기" onClick={() => navigate(endPoint)}></img>
        </div>
      </div>

      {children}

      {hasSearchBox && (
        <div className={style["search-section"]}>
          <input
            id="search-box"
            className={style["search-box"]}
            type="text"
            placeholder="보고 싶은 최애를 검색해보세요"
          ></input>
          <button className={style["search-btn"]}>
            <img src={search_icon}></img>
          </button>
        </div>
      )}

      {allPost}
      {!allPost && <SimpleSlider feedData={feedData} brightMode={brightMode} />}
    </section>
  );
}
