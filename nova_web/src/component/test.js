import Feed, { InputFeed, InfoArea, Text, Comments } from './feed';

// import style from './../pages/FeedPage/FeedPage.module.css';
import stylePlanet from './../pages/PlanetPage/Planet.module.css';
// import planet2 from './../img/planet2.png';

import React, { useState, useEffect, useRef } from 'react';
import style from './../pages/FeedPage/FeedPage.module.css';
import { useNavigate } from 'react-router-dom';




const Box = () => {
  const [banners, setBanners] = useState([]);

  const [nextData, setNextData] = useState(0);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  const [startY, setStartY] = useState(0);
  const [translateY, setTranslateY] = useState(0);
  const [dragDistance, setDragDistance] = useState(0);
  const sliderRef = useRef(null);

  useEffect(() => {
    setTranslateY(-currentIndex * window.innerHeight);
  }, [currentIndex]);

  const handleMouseDown = (e) => {
    setIsDragging(true);
    setStartY(e.clientY);
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;

    const distance = e.clientY - startY;
    setDragDistance(distance);
    setTranslateY(-currentIndex * window.innerHeight + distance);
  };

  const handleMouseUp = () => {
    setIsDragging(false);

    const threshold = 100;
    if (dragDistance > threshold && currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    } else if (dragDistance < -threshold && currentIndex < banners.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }

    setDragDistance(0);
  };

  // 휠로 배너 변경
  const handleWheel = (e) => {
    if (e.deltaY > 0 && currentIndex < banners.length - 1) {
      setCurrentIndex((prevIndex) => prevIndex + 1);
    } else if (e.deltaY < 0 && currentIndex > 0) {
      setCurrentIndex((prevIndex) => prevIndex - 1);
    }
  };

  function fetchFeed() {
    fetch('https://nova-platform.kr/feed_explore/get_feed?fclass=balance')
      .then(response => response.json())
      .then(data => {
        console.log("11", data.body.feed);
        setBanners(data.body.feed);
        setNextData(data.body.key);
      })
  }

  useEffect(() => {
    fetchFeed();
  }, [])

  // 서버에서 추가 데이터를 받아오는 함수
  const fetchMoreBanners = async () => {
    try {
      // 서버로부터 추가 배너 데이터를 가져옴
      const response = await fetch(`https://nova-platform.kr/feed_explore/get_feed?fclass=balance&key=${nextData}`); // 예시 URL
      const newBanners = await response.json();
      const plusFeed = newBanners.body.feed;
      setNextData(newBanners.body.key);
      console.log(plusFeed)

      // 기존 배너에 새 배너를 추가
      setBanners((prevBanners) => [...prevBanners, ...plusFeed]);
    } catch (error) {
      console.error('Error fetching additional banners:', error);
    }
  };

  // currentIndex가 마지막 배너일 때 추가 배너를 불러옴
  useEffect(() => {
    if (currentIndex === banners.length - 1) {
      fetchMoreBanners();
    }
  }, [currentIndex]);


  let navigate = useNavigate();



  return (
    <div
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
      onWheel={handleWheel}
      ref={sliderRef}
      className={style['test_container']}>
      <div className={`${stylePlanet['top_area']} ${style['top_bar_area']}`}>
        <div onClick={() => { navigate(-1) }}>뒤로</div>
        <div>은하계 탐색</div>
      </div>

      <div
        className={style.test}
        style={{
          transform: `translateY(${translateY}px)`,
          transition: isDragging ? 'none' : 'transform 0.5s ease'
        }}>

        {
          banners.map((banner, i) => {
            return (
              <div className={style['short_form']}>
                <div className={style['button_area']}>
                  <div className={style['short_form_container']}>
                    <div className={style['short_box']}>
                      <div className={style['img_circle']}></div>
                      <div style={{ height: '80px' }}></div>
                      <div className={style['short_feed']}>
                        <div>
                          <InfoArea color={'#7960EC'} name={`행성`} supporter='ㅇㅇㅇ'></InfoArea>
                          <Text title='하이' data='ㅇㄴㅁ'></Text>
                          <div className={`${style['button_container']} `}>
                            <button className={`${style['select_button']} `}>갑니다</button>
                            <button className={`${style['select_button']} `}>패스</button>
                          </div>
                        </div>

                        <div style={{ width: '100%', height: '10px' }}></div>
                        <div className={style.line}></div>
                        <Comments></Comments>
                      </div>

                    </div>

                    <div className={style['function_button']}>
                      <div className={style['func_btn']}>
                        <button></button>
                        <p>1.6k</p>
                      </div>
                      <div className={style['func_btn']}>
                        <button></button>
                        <p>42</p>
                      </div>
                      <div className={style['func_btn']}>
                        <button></button>
                        <p>공유</p>
                      </div>
                      <div className={style['func_btn']}>
                        <button></button>
                        <p>신고</p>
                      </div>
                    </div>

                  </div>

                </div>

              </div>
            )
          })
        }
      </div>
    </div >
  );
};

export default Box;