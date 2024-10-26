import React, { useEffect, useState } from "react";
import style from "./MainPart.module.css";
import SimpleSlider from "../../component/SimpleSlider";
import more_icon from "./../../img/backword.png";
export default function MainPart() {
  const [isActive, setIsActive] = useState(false); // 버튼의 상태를 관리

  let [bias, setBias] = useState("");
  let [biasTag, setBiasTag] = useState([]);
  let [tagFeed, setTagFeed] = useState([]);
  let [hashTag, setHashTag] = useState("");

  const handleClick = () => {
    fetchTagFeed();
    setIsActive((prev) => !prev); // 상태 토글
  };

  function fetchHashTag() {
    fetch("https://nova-platform.kr/home/hot_hashtag", {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setBias(data.body);
        setBiasTag(data.body.hashtags);
        console.log("41241515", data);
      });
  }

  function fetchTagFeed() {
    fetch(`https://nova-platform.kr/home/hot_hashtag_feed?hashtag=${hashTag}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("14111", data);
        setTagFeed(data.body.feed);
      });
  }

  useEffect(() => {
    fetchHashTag();
  }, []);

  return (
    <div className={style["wrap-container"]}>
      <div className={style["top-area"]}>
        <div className={style["content-title"]}>
          {/* bid : ''이면 인기 해시태그
  -1이 아니면 [title] 관련 인기 해시트=ㅐ그 */}
          <header className={style["header-text"]}>[ {bias.title} ] 관련 인기 해시태그</header>
          <img src={more_icon} className={style["more-icon"]}></img>
        </div>

        <div className={style["tag-container"]}>
          {biasTag.map((tag, i) => {
            return (
              <button
                key={i}
                className={style["hashtag-text"]}
                onClick={() => {
                  handleClick();
                  setHashTag(tag);
                }}
                style={{
                  backgroundColor: isActive ? "#D2C8F7" : "#373737",
                  cursor: "pointer",
                }}
              >
                #{tag}
              </button>
            );
          })}
        </div>
      </div>

      <div className={style["main-area"]}>
        {/* <div className={style["feed-box"]}> */}
        {/*<div className={style["name-container"]}>
            <div className={style["profile"]}> </div>
            <h2 className={style["name-text"]}>익명 바위게</h2>
            <button className={style["more-see"]}>더보기</button>
          </div>
          <section className={style["text-container"]}>
            <div className={style["tag-text"]}>
              <span className={style["tag"]}>#시연</span>
              <span className={style["tag"]}>#이쁘다</span>
            </div>
            <div className={style["main-text"]}>젠타 나이 질문이요 젠타 98년생 아닌가요??</div>
          </section>

          <footer className={style["like-comment"]}>좋아요 수 댓글 수</footer>*/}
        <SimpleSlider tagFeed={tagFeed} />
      </div>
      {/* </div> */}
    </div>
  );
}
