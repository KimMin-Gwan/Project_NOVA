import "./slider.css";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import style from "./AllPost/MainPart.module.css";
import { useNavigate } from "react-router-dom";
import React, { useEffect, useRef, useState } from "react";

import { getModeClass } from "./../App.js";
import { Autoplay } from "swiper/modules";
const SimpleSlider = ({ feedData, brightMode, type, className }) => {
  const showMaxCnt = 1;

  const settings = {
    className: "slider-items",
    dots: true,
    infinite: feedData.length > showMaxCnt,
    speed: 700,
    slidesToShow: 1,
    slidesToScroll: 1,
    centerMode: true,
    centerPadding: "0px",
    arrows: false,
    autoplay:true,
    autoplaySpeed:7000
  };
  // style안붙은 것은 slider.css에서 수정
  let navigate = useNavigate();

  const [isDragging, setIsDragging] = useState(false);
  const [startPosition, setStartPosition] = useState({ x: 0, y: 0 });
  const [moveDistance, setMoveDistance] = useState(0);

  function onClickMore(fid, e) {
    if (!isDragging) {
      navigate(`/feed_detail/${fid}`, { state: { commentClick: false } });
    }
  }

  const handleMouseDown = (e) => {
    setIsDragging(false);
    setStartPosition({ x: e.clientX, y: e.clientY });
    setMoveDistance(0); // 이동 거리를 초기화
  };

  const handleMouseMove = (e) => {
    if (startPosition.x && startPosition.y) {
      const distance = Math.sqrt(
        (e.clientX - startPosition.x) ** 2 + (e.clientY - startPosition.y) ** 2
      );
      setMoveDistance(distance);

      // 일정 거리 이상 이동하면 드래그로 간주
      if (distance > 5) {
        setIsDragging(true); // 드래그 상태로 설정
      }
    }
  };

  const handleMouseUp = (e) => {
    if (moveDistance <= 5 && !isDragging) {
      setIsDragging(false);
    }
  };

  const [mode, setMode] = useState(brightMode); // 초기 상태는 부모로부터 받은 brightMode 값
  useEffect(() => {
    setMode(brightMode); // brightMode 값이 바뀔 때마다 mode 업데이트
  }, [brightMode]);

  return (
    <div
      className={`slider-container ${brightMode === "dark" ? "dark-mode" : "bright-mode"} ${
        className || ""
      }`}
    >
      <Slider {...settings}>
        {feedData.length !== 0 &&
          feedData.map((feed, i) => {
            return (
              <div key={i} className="slick-slide">
                <div className="slide-box">
                  <div
                    className="slide-content"
                    onMouseDown={handleMouseDown}
                    onMouseMove={handleMouseMove}
                    onMouseUp={(e) => handleMouseUp(e)}
                    onClick={(e) => {
                      onClickMore(feed.feed.fid, e);
                    }}
                  >
                    {type === "bias" && (
                      <div className={style["name-container"]}>
                        <div className={style["profile"]}>{feed.feed.nickname}</div>
                      </div>
                    )}

                    {!type && (
                      <div className={style["img-container"]}>
                        <img
                          src={
                            feed.feed.image.length > 0
                              ? feed.feed.image[0]
                              : "https://kr.object.ncloudstorage.com/nova-feed-images/nova-platform.png"
                          }
                          alt="이미지"
                        />
                      </div>
                    )}

                    <section className={style["text-container"]}>
                      <div className={style["tag-text"]}>
                        {feed.feed.hashtag.map((tag, i) => {
                          return (
                            <span key={i} className={style["tag"]}>
                              #{tag}
                            </span>
                          );
                        })}
                      </div>
                      <div className={style["main-text"]}>{feed.feed.body}</div>
                    </section>
                    <footer className={style["like-comment"]}>
                      좋아요 {feed.feed.star}개 | 댓글 {feed.feed.num_comment}개
                    </footer>
                  </div>
                </div>
              </div>
            );
          })}
      </Slider>
    </div>
  );
};

export default SimpleSlider;
