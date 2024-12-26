// import React, { useState } from 'react';
// import './slider.css'; // 스타일을 위한 CSS 파일

// const SimpleSlider = () => {
//   const items = [
//     <div style={{ backgroundColor: 'red' }}>Slide 1</div>,
//     <div style={{ backgroundColor: 'blue' }}>Slide 2</div>,
//     <div style={{ backgroundColor: 'green' }}>Slide 3</div>,
//   ];

//   const [currentIndex, setCurrentIndex] = useState(0);

//   const nextSlide = () => {
//     setCurrentIndex((prevIndex) => (prevIndex + 1) % items.length);
//   };

//   const prevSlide = () => {
//     setCurrentIndex((prevIndex) =>
//       prevIndex === 0 ? items.length - 1 : prevIndex - 1
//     );
//   };

//   return (
//     <div className="carousel">
//       <button onClick={prevSlide}>&lt;</button>
//       <div className="carousel-content">
//         {items[currentIndex]}
//       </div>
//       <button onClick={nextSlide}>&gt;</button>
//     </div>
//   );
// };

// export default SimpleSlider;

import "./slider.css";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import style from "./../pages/MainPage/MainPart.module.css";
import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";

import { getModeClass } from "./../App.js";
const SimpleSlider = ({ feedData, brightMode }) => {
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
    navigate(`/feed_page?fid=${fid}`);
  }

  const [mode, setMode] = useState(brightMode); // 초기 상태는 부모로부터 받은 brightMode 값
  useEffect(() => {
    setMode(brightMode); // brightMode 값이 바뀔 때마다 mode 업데이트
  }, [brightMode]);

  return (
    <div className={`slider-container ${brightMode === "dark" ? "dark-mode" : "bright-mode"}`}>
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
                      // onClickMore(feed.fid);
                    }}
                  >
                    {/* <div className={style["name-container"]}> */}
                    {/* <div className={style["profile"]}> </div> */}
                    {/* </div> */}
                    <div className={style["img-container"]}>
                      <img
                        src={
                          feed.image.length > 0
                            ? feed.image[0]
                            : "https://kr.object.ncloudstorage.com/nova-feed-images/nova-platform.PNG"
                        }
                        alt="이미지"
                      />
                    </div>

                    <section className={style["text-container"]}>
                      <div className={style["tag-text"]}>
                        {feed.hashtag.map((tag, i) => {
                          return (
                            <span key={i} className={style["tag"]}>
                              #{tag}
                            </span>
                          );
                        })}
                      </div>
                      <div className={style["main-text"]}>{feed.body}</div>
                    </section>
                    <footer className={style["like-comment"]}>
                      좋아요 {feed.star}개 | 댓글 {feed.num_comment}개
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
