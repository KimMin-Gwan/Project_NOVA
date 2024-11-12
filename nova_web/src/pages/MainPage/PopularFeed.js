import { useEffect, useRef, useState } from "react";
import style from "./MainPart.module.css";
import more_icon from "./../../img/backword.png";
import { useNavigate } from "react-router-dom";
import { getModeClass } from "./../../App.js";
export default function PopularFeed({ brightMode }) {
  let [homeFeed, setHomeFeed] = useState([]);
  const navigate = useNavigate();
  function fetchHomeFeed() {
    fetch(`https://nova-platform.kr/home/home_feed`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setHomeFeed(data.body.feed);
      });
  }

  useEffect(() => {
    fetchHomeFeed();
  }, []);

  function handleNavigate(fid) {
    navigate(`/feed_list/${fid}`);
  }

  let scrollRef = useRef(null);
  let [isDrag, setIsDrag] = useState(false);
  let [dragStart, setDragStart] = useState("");
  let [hasDragged, setHasDragged] = useState(false);

  function onMouseDown(e) {
    e.preventDefault();
    setIsDrag(true);
    setDragStart(e.pageX + scrollRef.current.scrollLeft);
    setHasDragged(false); //드래그 여부 초기화
  }

  function onMouseUp(e) {
    setIsDrag(false);
  }

  function onMouseMove(e) {
    if (isDrag) {
      scrollRef.current.scrollLeft = dragStart - e.pageX;
      setHasDragged(true); //드래그 발생 표시
    }
  }

  function handleFeedClick(fid) {
    if (!hasDragged) {
      handleNavigate(fid);
    }
  }

  const [mode, setMode] = useState(brightMode); // 초기 상태는 부모로부터 받은 brightMode 값
  useEffect(() => {
    setMode(brightMode); // brightMode 값이 바뀔 때마다 mode 업데이트
  }, [brightMode]);

  return (
    <div className={style["wrap-container"]}>
      <div className={`${style["top-area"]} ${style[getModeClass(mode)]}`}>
        <div className={style["content-title"]}>
          <header className={style["header-text"]}>최근 인기 게시글</header>
          <img src={more_icon} alt="더보기" onClick={() => navigate("/feed_list?type=best")} className={style["more-icon"]}></img>
        </div>
      </div>

      <div className={`${style["main-area"]} ${style["popular-feed-container"]} ${style[getModeClass(mode)]}`}
        ref={scrollRef}
        onMouseDown={onMouseDown}
        onMouseMove={onMouseMove}
        onMouseUp={onMouseUp}>
        {homeFeed.map((feed, i) => {
          return (
            <div key={i} className={`${style["popular-feed"]} ${style[getModeClass(mode)]}`} 
            onClick={() => handleFeedClick(feed.fid)}>
              <div className={style["img-box"]}>
                <img src={`${feed.image[0]}`} alt="img" />
              </div>
              <div className={style["popular-main"]}>
                <div className={style["tag-text"]}>
                  {feed.hashtag.map((tag, i) => {
                    return (
                      <span key={i} className={style["tag"]}>
                        #{tag}
                      </span>
                    );
                  })}
                </div>
                <div className={`${style["popular-text"]} ${style[getModeClass(mode)]}`}>{feed.body}</div>
                <footer className={style["like-comment"]}>
                  좋아요 {feed.star}개 | 댓글 {feed.num_comment}개
                </footer>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
