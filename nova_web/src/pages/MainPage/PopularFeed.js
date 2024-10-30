import { useEffect, useState } from "react";
import style from "./MainPart.module.css";
import more_icon from "./../../img/backword.png";
import SimpleSlider from "../../component/SimpleSlider";
export default function PopularFeed() {

  let [homeFeed, setHomeFeed] = useState([]);

  function fetchHomeFeed() {
    fetch(`https://nova-platform.kr/home/home_feed`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("11", data);
        setHomeFeed(data.body.feed);
      });
  }

  useEffect(() => {
    fetchHomeFeed();
  }, []);

  return (
    <div className={style["wrap-container"]}>
      <div className={style["top-area"]}>
        <div className={style["content-title"]}>
          <header className={style["header-text"]}>최근 인기 게시글</header>
          <img src={more_icon} alt='더보기' className={style["more-icon"]}></img>
        </div>
      </div>

      <div className={style["main-area"]}>
        <SimpleSlider homeFeed={homeFeed}/>
      {/* <SimpleSlider tagFeed={tagFeed} /> */}
        {/* {popularFeed.map((feed, i) => {
          return (
            <div key={i} className={style["popular-feed"]}>
              <div className={style["img-box"]}>img</div>
              <div className={style["popular-main"]}>
                <div className={style["tag-text"]}>
                  <span className={style["tag"]}>#미츄</span>
                  <span className={style["tag"]}>#아모몽</span>
                  <span className={style["tag"]}>#미녕이</span>
                </div>
                <div className={style["popular-text"]}>{feed.body}</div>
              </div>
            </div>
          );
        })} */}
      </div>
    </div>
  );
}
