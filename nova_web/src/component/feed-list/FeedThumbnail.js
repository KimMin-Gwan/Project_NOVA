import { useEffect, useState } from "react";
import SimpleSlider from "../SimpleSlider";
import style from "./FeedThumbnail.module.css";
import more_icon from "../../img/Icon.png";
import search_icon from "./../../img/search_icon.png";
import pin from "./../../img/pin.png";

import { useNavigate } from "react-router-dom";
import SearchBox from "../SearchBox";

export default function FeedThumbnail({
  title,
  feedData,
  brightMode,
  type,
  hasSearchBox,
  children,
  allPost,
  endPoint,
  customClassName,
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

      {/* {hasSearchBox && <SearchBox />} */}

      {allPost}
      {allPost ? null : type === "bias" ? (
        <SimpleSlider
          feedData={feedData}
          brightMode={brightMode}
          type={type}
          className={customClassName || ""}
        />
      ) : (
        <SimpleSlider feedData={feedData} brightMode={brightMode} />
      )}
    </section>
  );
}
