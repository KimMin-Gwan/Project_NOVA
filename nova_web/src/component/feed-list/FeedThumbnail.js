import { useEffect, useState } from "react";
import SimpleSlider from "../SimpleSlider";
import style from "./FeedThumbnail.module.css";
import more_icon from "../../img/Icon.png";
import { useNavigate } from "react-router-dom";

export default function FeedThumbnail({ title, feedData, brightMode }) {
  let navigate = useNavigate();
  const [mode, setMode] = useState(brightMode); // 초기 상태는 부모로부터 받은 brightMode 값

  useEffect(() => {
    setMode(brightMode); // brightMode 값이 바뀔 때마다 mode 업데이트
  }, [brightMode]);

  return (
    <section className={style["FeedThumbnail"]}>
      <div className={style["title-section"]}>
        <div className={style["title"]}>{title}</div>
        <div className={`${style["more-icon"]}`}>
          <img src={more_icon} alt="더보기" onClick={() => navigate("/feed_hash_list")}></img>
        </div>
      </div>

      <SimpleSlider feedData={feedData} brightMode={brightMode} />
    </section>
  );
}
