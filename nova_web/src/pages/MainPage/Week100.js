import React, { useCallback, useEffect, useRef, useState } from "react";
import style from "./MainPart.module.css";
import SimpleSlider from "../../component/SimpleSlider.js";
import more_icon from "./../../img/backword.png";
import { useNavigate } from "react-router-dom";
import { getModeClass } from "../../App.js";
export default function Week100({ brightMode }) {
  let [bias, setBias] = useState("");
  let [biasTag, setBiasTag] = useState([]);
  let [tagFeed, setTagFeed] = useState([]);
  let [hashTag, setHashTag] = useState("");
  let [clickIndex, setClickIndex] = useState(0);

  const navigate = useNavigate();
  const handleClick = (index) => {
    fetchTagFeed();
    setClickIndex(index);
  };

  function fetchHashTag() {
    fetch("https://nova-platform.kr/home/hot_hashtag", {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setBias(data.body);
        setBiasTag(data.body.hashtags);
      });
  }

  const fetchUrl = `https://nova-platform.kr/home/hot_hashtag_feed?hashtag=${hashTag}`;

  const fetchTagFeed = useCallback(() => {
    fetch(fetchUrl, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("14111", data);
        setTagFeed(data.body.feed);
      });
  }, [fetchUrl]);

  useEffect(() => {
    fetchHashTag();
    fetchTagFeed();
  }, [fetchTagFeed]);

  let scrollRef = useRef(null);
  let [isDrag, setIsDrag] = useState(false);
  let [dragStart, setDragStart] = useState("");

  function onMouseDown(e) {
    e.preventDefault();
    setIsDrag(true);
    setDragStart(e.pageX + scrollRef.current.scrollLeft);
  }

  function onMouseUp(e) {
    setIsDrag(false);
  }

  function onMouseMove(e) {
    if (isDrag) {
      scrollRef.current.scrollLeft = dragStart - e.pageX;
    }
  }

  const [mode, setMode] = useState(brightMode); // 초기 상태는 부모로부터 받은 brightMode 값
  useEffect(() => {
    setMode(brightMode); // brightMode 값이 바뀔 때마다 mode 업데이트
  }, [brightMode]);

  return (
    <div className={`${style["wrap-container"]} ${style[getModeClass(mode)]}`}>
      <div className={`${style["top-area"]} ${style[getModeClass(mode)]}`}>
        <div className={style["content-title"]}>
          <header className={style["header-text"]}>주간 TOP 100</header>
          <img src={more_icon} alt="menu" onClick={() => navigate("/feed_hash_list")} className={style["more-icon"]}></img>
        </div>
      </div>

      <div className={`${style["main-area"]} ${style[getModeClass(mode)]}`}>
        <SimpleSlider tagFeed={tagFeed} brightMode={brightMode} />
      </div>
      {/* </div> */}
    </div>
  );
}
