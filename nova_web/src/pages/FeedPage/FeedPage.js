import Feed, { InputFeed, InfoArea, Text, Comments } from '../../component/feed';

// import style from './../pages/FeedPage/FeedPage.module.css';
// import stylePlanet from './../pages/PlanetPage/Planet.module.css';
// import planet2 from './../img/planet2.png';

import style from './FeedPage.module.css';
import stylePlanet from './../PlanetPage/Planet.module.css';
import { CiStar } from "react-icons/ci";
import { TfiCommentAlt } from "react-icons/tfi";
import { PiShareFatLight } from "react-icons/pi";
import { MdOutlineReportProblem } from "react-icons/md";

import React, { useState, useEffect, useRef } from 'react';
// import style from './../pages/FeedPage/FeedPage.module.css';
import { useLocation, useNavigate } from 'react-router-dom';

const FeedPage = () => {

    const location = useLocation();

    const queryParams = new URLSearchParams(location.search);
    const fclass = queryParams.get('fclass');

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
        fetch(`https://nova-platform.kr/feed_explore/get_feed?fclass=${fclass}`)
            .then(response => response.json())
            .then(data => {
                console.log("11", data.body.feed);
                setBanners(data.body.feed);
                setNextData(data.body.key);
                setNumStar([data.body.feed[0].star, data.body.feed[1].star]);
            })
    }

    useEffect(() => {
        fetchFeed();
    }, [])

    // 서버에서 추가 데이터를 받아오는 함수
    const fetchMoreBanners = async () => {
        try {
            // 서버로부터 추가 배너 데이터를 가져옴
            const response = await fetch(`https://nova-platform.kr/feed_explore/get_feed?fclass=${fclass}&key=${nextData}`); // 예시 URL
            const newBanners = await response.json();
            const plusFeed = newBanners.body.feed;
            const newStar = newBanners.body.feed[0].star;
            setNextData(newBanners.body.key);
            // 기존 배너에 새 배너를 추가
            setBanners((prevBanners) => [...prevBanners, ...plusFeed]);
            setNumStar(((prevNumStar) => [...prevNumStar, newStar]));
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

    let [numStar, setNumStar] = useState([]);
    // let [numComment, setNumComment] = useState([]);
    // let [isClickedStar, setIsClickedStar] = useState(false);

    function handleCheckStar(fid, index) {
        // setIsClickedStar(!isClickedStar);
        fetch(`https://nova-platform.kr/feed_explore/check_star?fid=${fid}`, {
            credentials: 'include',
        })
            .then(response => response.json())
            .then(data => {
                setNumStar((prevItems) => {
                    const newItems = [...prevItems];
                    newItems[index] = data.body.feed[0].star;
                    return newItems;
                });
                console.log(data.body.feed[0].star);
                // setNumStar(data.body.feed[0].star);
                // console.log(numStar);
            })
    };


    // useEffect(() => {

    //     // fetchStar();
    //     handleCheckStar();
    //     console.log('gkgkgkgkgk')

    // }, []);



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
                            <div key={banner.fid} className={style['short_form']}>
                                <div className={style['button_area']}>
                                    {/* <div className={style['comment_window']}>
                                        <div>댓글</div>
                                        <div className={style.line}></div>
                                        <div>
                                            <div>
                                                <div>지지자</div>
                                                <div>내용</div>
                                            </div>
                                            <div className={style['comment_action']}>
                                                <input></input>
                                                <button>댓글 작성</button>
                                            </div>
                                        </div>
                                    </div> */}



                                    <div className={style['short_form_container']}>
                                        <div className={style['short_box']}>
                                            <div className={style['img_circle']}></div>
                                            <div style={{ height: '80px' }}></div>
                                            {/* <div className={style['short_feed']}> */}
                                            <Feed className={style['short_feed']} feed={banner} fclass={fclass}></Feed>
                                            {/* </div> */}

                                        </div>

                                        <div className={style['function_button']}>
                                            <div className={style['func_btn']}>
                                                <button onClick={() => {
                                                    handleCheckStar(banner.fid, i);
                                                }}>
                                                    <CiStar className={style['func_btn_img']} />
                                                </button>
                                                
                                                <p>{numStar[i]}</p>

                                                {/* <p>{banner.star}</p> */}
                                            </div>
                                            <div className={style['func_btn']}>
                                                <button>
                                                    <TfiCommentAlt className={style['func_btn_img']} />
                                                </button>
                                                <p>42</p>
                                            </div>
                                            <div className={style['func_btn']}>
                                                <button>
                                                    <PiShareFatLight className={style['func_btn_img']} />
                                                </button>
                                                <p>공유</p>
                                            </div>
                                            <div className={style['func_btn']}>
                                                <button>
                                                    <MdOutlineReportProblem className={style['func_btn_img']} />
                                                </button>
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

export default FeedPage;

// import style from './FeedPage.module.css';
// import stylePlanet from './../PlanetPage/Planet.module.css';

// import planet2 from './../../img/planet2.png';
// import { useEffect, useRef, useState } from 'react';
// import Feed, { InputFeed } from '../../component/feed';
// import { useNavigate } from 'react-router-dom';





// export default function FeedPage() {
//     //피드 드래그
//     const [isFeedDragging, setIsFeedDragging] = useState(false);
//     const [startY, setStartY] = useState(0);
//     const [currentFeedY, setCurrentFeedY] = useState(0);

//     function handleFeedMouseDown(e) {
//         setStartY(e.clientY);
//         setIsFeedDragging(true);
//     };

//     function handleFeedMouseMove(e) {
//         if (isFeedDragging) {
//             const moveY = e.clientY - startY;
//             setCurrentFeedY(moveY);

//             if (moveY < -50) {
//                 setSlideFeed(true);
//                 setUpFeed(true);
//                 setShowNewFeed(true);
//             }
//             // else {
//             //     setSlideFeed(false);
//             //     setUpFeed(false);
//             //     setShowNewFeed(false);
//             // }
//         }
//     };

//     function handleFeedMouseUp() {
//         setIsFeedDragging(false);
//         if (currentFeedY < -50) {
//             setCurrentFeedY(0);
//             // setSlideFeed(true);
//         } else {
//             setCurrentFeedY(100);
//         }
//     };


//     // 행성 드래그
//     const [isDragging, setIsDragging] = useState(false);
//     const [dragStartY, setDragStartY] = useState(null);
//     const [dragDirection, setDragDirection] = useState(null);
//     const [showFeed, setShowFeed] = useState(false);

//     const [slideFeed, setSlideFeed] = useState(false);
//     const [upFeed, setUpFeed] = useState(false);
//     const [showNewFeed, setShowNewFeed] = useState(false);

//     const inputFeedRef = useRef(null);

//     const [scrollPos, setScrollPos] = useState(0);

//     let navigate = useNavigate();

//     const [offsetY, setOffsetY] = useState(0);
//     const boxRef = useRef(null);

//     function handleMouseDown(e) {
//         setIsDragging(true);
//         setDragStartY(e.clientY);  // 드래그 시작 Y 좌표 기록
//     };

//     function handleMouseMove(e) {
//         if (isDragging && dragStartY !== null) {
//             const currentY = e.clientY;
//             if (currentY > dragStartY) {
//                 setDragDirection('down');
//                 boxRef.current.style.transform = 'translateY(50px)';
//                 inputFeedRef.current.style.opacity = 1;
//             } else if (currentY < dragStartY) {
//                 setDragDirection('up');
//                 boxRef.current.style.transform = 'translateY(-50px)';
//                 inputFeedRef.current.style.opacity = 0;

//             }
//         }
//     };

//     function handleMouseUp() {
//         setIsDragging(false);

//         if (dragDirection === 'down') {
//             setShowFeed(true);
//             // showFeed.current = true;  // 아래로 드래그하면 피드 표시

//         } else if (dragDirection === 'up') {
//             setShowFeed(false);

//             // showFeed.current = false;  // 위로 드래그하면 피드 숨기기
//         }
//         boxRef.current.style.transform = 'translateY(0)';

//         // 상태 초기화
//         setDragStartY(null);
//         setDragDirection(null);
//     };

//     function onClickBox() {
//         setSlideFeed(!slideFeed);
//         setUpFeed(!upFeed);
//         setShowNewFeed(!showNewFeed);
//     }

//     return (
//         <div className={style.container}>
//             <div className={stylePlanet['top_area']}>
//                 <div onClick={() => { navigate(-1) }}>뒤로</div>
//                 <div>은하계 탐색</div>
//             </div>
//             <div ref={inputFeedRef} className={`${style.boxx} ${showFeed ? '' : style.hidden}`}>
//                 <InputFeed></InputFeed>
//             </div>
//             <div ref={boxRef} className={style.databox}>
//                 <div className={style['img-area']} >
//                     <img src={planet2} alt="Planet"
//                         className={style.moving}
//                         onMouseDown={handleMouseDown}
//                         onMouseMove={handleMouseMove}
//                         onMouseUp={handleMouseUp}
//                         onMouseLeave={handleMouseUp}  // 마우스가 영역을 벗어날 때도 처리
//                         style={{ cursor: isDragging ? 'grabbing' : 'grab' }} />
//                 </div>

//                 <div className={style.area}>
//                     {showNewFeed && <Feed className={`${style.feedbox3}`}></Feed>}
//                     <div
//                         onMouseDown={handleFeedMouseDown}
//                         onMouseMove={handleFeedMouseMove}
//                         onMouseUp={handleFeedMouseUp}>
//                         <Feed className={`${style.feedbox1} ${upFeed ? style['up_animate'] : ''}`}></Feed>
//                         <Feed className={`${style.feedbox2} ${slideFeed ? style.animate : ''}`}></Feed>
//                     </div>

//                 </div>
//                 <button onClick={() => {
//                     onClickBox()
//                 }}>클릭</button>
//             </div>
//         </div >
//     );
// }
