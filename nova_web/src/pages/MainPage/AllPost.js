import { useEffect, useState } from "react";
import style from "./MainPart.module.css";
import more_icon from "../../img/Icon.png";
import { useNavigate } from "react-router-dom";
import { getModeClass } from "./../../App.js";
import useFetchData from "../../hooks/useFetchData.js";

export default function AllPost({ brightMode, allFeed }) {
  let navigate = useNavigate();
  const [mode, setMode] = useState(brightMode); // 초기 상태는 부모로부터 받은 brightMode 값

  useEffect(() => {
    setMode(brightMode); // brightMode 값이 바뀔 때마다 mode 업데이트
  }, [brightMode]);

  function onClick(fid) {
    navigate(`/feed_detail/${fid}`, { state: { commentClick: false } });
  }

  return (
    <div className={`${style["wrap-container"]} ${style["allpost-container"]}`}>
      <div className={`${style["top-area"]} ${style[getModeClass(mode)]}`}>
        <div className={`${style["main-area"]} ${style["all-main-area"]} `}>
          <ul className={`${style["all-list"]} `}>
            {allFeed.map((feed, i) => {
              return (
                <li key={feed.feed.fid} onClick={() => onClick(feed.feed.fid)}>
                  <div className={style["all-img"]}>
                    <img
                      src={
                        feed.feed.image.length > 0
                          ? feed.feed.image[0]
                          : "https://kr.object.ncloudstorage.com/nova-feed-images/nova-platform.png"
                      }
                      alt="이미지"
                    />
                  </div>
                  <div className={style["all-text"]}>
                    <div className={style["all-text_container"]}>
                      {feed.feed.hashtag.map((tag, i) => {
                        return <span key={i}>#{tag}</span>;
                      })}
                      <p>{feed.feed.body}</p>
                    </div>
                  </div>
                </li>
              );
            })}
          </ul>
        </div>
      </div>
    </div>
  );
}
