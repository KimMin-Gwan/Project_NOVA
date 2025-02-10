import "./slider.css";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import style from "./../pages/MainPage/MainPart.module.css";
import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";

import { getModeClass } from "./../App.js";
const SimpleSlider = ({ feedData, brightMode, type, className }) => {
  const showMaxCnt = 1;
  const settings = {
    className: "slider-items",
    dots: true,
    infinite: feedData.length > showMaxCnt,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    centerMode: true,
    centerPadding: "0px",
    arrows: false,
  };
  // style안붙은 것은 slider.css에서 수정
  let navigate = useNavigate();

  function onClickMore(fid) {
    navigate(`/feed_detail/${fid}`, { state: { commentClick: false } });
  }

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
                    className={`slide-content ${getModeClass(mode)}`}
                    onClick={(e) => {
                      e.preventDefault();
                      onClickMore(feed.feed.fid);
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
