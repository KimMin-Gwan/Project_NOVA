import { useEffect, useState } from "react";
import style from "./MainPart.module.css";
import more_icon from "./../../img/backword.png";
import { useNavigate } from "react-router-dom";
import { getModeClass } from "./../../App.js";
export default function AllPost({ brightMode }) {
  let navigate = useNavigate();
  const [mode, setMode] = useState(brightMode); // 초기 상태는 부모로부터 받은 brightMode 값
  let [feeds, setFeeds] = useState([]);

  useEffect(() => {
    setMode(brightMode); // brightMode 값이 바뀔 때마다 mode 업데이트
  }, [brightMode]);

  function fetchFeed() {
    fetch("https://nova-platform.kr/home/all_feed", {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.body.feed);
        setFeeds(data.body.feed);
      });
  }

  useEffect(() => {
    fetchFeed();
  }, []);

  function onClick(fid) {
    navigate(`/feed_page?fid=${fid}`);
  }

  return (
    <div className={style["wrap-container"]}>
      <div className={`${style["top-area"]} ${style[getModeClass(mode)]}`}>
        <div className={style["content-title"]}>
          <header className={style["header-text"]}>전체 글</header>
        </div>
        <div
          className={`${style["main-area"]} ${style["all-main-area"]} ${
            style[getModeClass(mode)]
          }`}
        >
          <ul className={`${style["all-list"]} ${style[getModeClass(mode)]}`}>
            {feeds.map((feed, i) => {
              return (
                <li key={feed.fid} onClick={() => onClick(feed.fid)}>
                  <div className={style["all-img"]}>
                    <img src={feed.image[0]} alt="이미지" />
                  </div>
                  <div className={style["all-text"]}>
                    <div className={style["all-text_container"]}>
                      {feed.hashtag.map((tag, i) => {
                        return <span key={i}>{tag}</span>;
                      })}
                      <p>{feed.body}</p>
                    </div>
                    <footer className={style["like-comment"]}>
                      좋아요 {feed.star}개 | 댓글 {feed.num_comment}개
                    </footer>
                  </div>
                </li>
              );
            })}
          </ul>
          <button
            onClick={() => navigate("/feed_list?type=all")}
            className={style["all_see-button"]}
          >
            더보기
          </button>
        </div>
      </div>
    </div>
  );
}
