import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import SimpleSlider from "../SimpleSlider";
import style from "./FeedThumbnail.module.css";
import more_icon from "../../img/home_arrow.svg";
import NoneFeed from "../NoneFeed/NoneFeed";
import LoadingComponent from "../NoneFeed/LoadingComponent";

export default function FeedThumbnail({
  title,
  img_src,
  feedData,
  brightMode,
  type,
  children,
  allPost,
  endPoint,
  customClassName,
  loading
}) {
  let navigate = useNavigate();
  const [mode, setMode] = useState(brightMode); // 초기 상태는 부모로부터 받은 brightMode 값

  useEffect(() => {
    setMode(brightMode); // brightMode 값이 바뀔 때마다 mode 업데이트
  }, [brightMode]);


  if (loading) { 
    return (
      <section className={style["FeedThumbnail"]}>
        <LoadingComponent />
      </section>
    );
  }

  return (
    <section className={style["FeedThumbnail"]}>
      {title && (
        <div className={style["title-section"]} onClick={() => navigate(endPoint)}>
          <div className={style["title"]}>
            {title}
          </div>
          <div className={`${style["more-icon"]}`}>
              <img src={more_icon} alt="더보기"></img>
          </div>
        </div>
      )}
      {children}
      {feedData.length === 0 && <NoneFeed />}

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
