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

import './slider.css';
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import style from "./../pages/MainPage/MainPart.module.css";

const SimpleSlider = ({ tagFeed }) => {
  const settings = {
    className: 'slider-items',
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    centerMode: true,
    centerPadding: '0px',
    arrows: false,
  };
  // style안붙은 것은 slider.css에서 수정

  return (
    <div className="slider-container">
      <Slider {...settings}>
        {tagFeed && tagFeed.map((feed, i) => {
          return (
            <div key={i} className="slick-slide">
              <div className='slide-box'>
                <div className="slide-content">
                  <div className={style["name-container"]}>
                    <div className={style["profile"]}> </div>
                    <h2 className={style["name-text"]}>{feed.nickname}</h2>
                    <button className={style["more-see"]}>더보기</button>
                  </div>

                  <section className={style["text-container"]}>
                    <div className={style["tag-text"]}>
                      <span className={style["tag"]}>#시연</span>
                      <span className={style["tag"]}>#이쁘다</span>
                    </div>
                    <div className={style["main-text"]}>{feed.body}</div>
                  </section>

                  <footer className={style["like-comment"]}>좋아요 수 댓글 수</footer>
                </div>
              </div>
            </div>
          )
        })
        }
      </Slider>
    </div>
  );
};

export default SimpleSlider;