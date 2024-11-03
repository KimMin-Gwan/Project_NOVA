import { useEffect, useState } from "react";
import style from "./MainPart.module.css";
import more_icon from "./../../img/backword.png";
import SimpleSlider from "../../component/SimpleSlider";
import { useNavigate } from "react-router-dom";

export default function PopularFeed() {
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
    navigate(`/feed_list/${fid}`)
  };

  return (
    <div className={style["wrap-container"]}>
      <div className={style["top-area"]}>
        <div className={style["content-title"]}>
          <header className={style["header-text"]}>최근 인기 게시글</header>
          <img src={more_icon} alt="더보기" onClick={() => navigate("/feed_list")} className={style["more-icon"]}></img>
        </div>
      </div>

      <div className={`${style["main-area"]} ${style["popular-feed-container"]}`}>
        {homeFeed.map((feed, i) => {
          return (
            <div key={i} className={style["popular-feed"]} onClick={() => handleNavigate(feed.fid)}>
              <div className={style["img-box"]}>
                <img src={`${feed.image}`} alt="img" />
              </div>
              <div className={style["popular-main"]}>
                <div className={style["tag-text"]}>
                  {
                    feed.hashtag.map((tag, i) => {
                      return (
                        <span key={i} className={style["tag"]}>#{tag}</span>
                      )
                    })
                  }
                </div>
                <div className={style["popular-text"]}>{feed.body}</div>
                <footer className={style["like-comment"]}>좋아요 {feed.star}개 | 댓글 {feed.num_comment}개</footer>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
