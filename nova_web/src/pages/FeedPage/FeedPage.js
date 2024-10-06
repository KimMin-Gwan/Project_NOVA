import Feed, {
  InputFeed,
  InfoArea,
  Text,
  Comments,
} from "../../component/feed";

// import style from './../pages/FeedPage/FeedPage.module.css';
// import stylePlanet from './../pages/PlanetPage/Planet.module.css';
// import planet2 from './../img/planet2.png';

import style from "./FeedPage.module.css";
import stylePlanet from "./../PlanetPage/Planet.module.css";
import { FaStar } from "react-icons/fa";
import { TfiCommentAlt } from "react-icons/tfi";
import { PiShareFatLight } from "react-icons/pi";
import { MdOutlineReportProblem } from "react-icons/md";

import React, { useState, useEffect, useRef, createContext } from "react";
// import style from './../pages/FeedPage/FeedPage.module.css';
import { useLocation, useNavigate } from "react-router-dom";

export const FeedContext = createContext();
export const FeedDispatchContext = createContext();

const FeedPage = () => {
  const location = useLocation();

  // const queryParams = new URLSearchParams(location.search);
  // const fclass = queryParams.get("fclass");

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
    // setIsClickedComment(false);
    setTranslateY(-currentIndex * window.innerHeight + distance);
  };

  const handleMouseUp = () => {
    setIsDragging(false);

    const threshold = 100;
    if (dragDistance > threshold && currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
      setIsClickedComment(false);
    } else if (dragDistance < -threshold && currentIndex < banners.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setIsClickedComment(false);
    }

    setDragDistance(0);
  };

  // 휠로 배너 변경
  const handleWheel = (e) => {
    if (e.deltaY > 0 && currentIndex < banners.length - 1) {
      setCurrentIndex((prevIndex) => prevIndex + 1);
      setIsClickedComment(false);
    } else if (e.deltaY < 0 && currentIndex > 0) {
      setCurrentIndex((prevIndex) => prevIndex - 1);
      setIsClickedComment(false);
    }
  };

  const handleCommentsWheel = (event) => {
    const element = event.currentTarget;
    const atTop = element.scrollTop === 0;
    const atBottom = element.scrollHeight - element.scrollTop === element.clientHeight;

    // 댓글창이 맨 위나 맨 아래에 도달하지 않았을 때만 이벤트 전파를 막음
    if (!atTop && !atBottom) {
      event.stopPropagation();
    }
  };

  function fetchFeed() {
    fetch(`https://nova-platform.kr/feed_explore/get_feed?fclass=None`, {
      credentials: 'include'
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("11", data.body.feed);
        console.log('faftest',data)

        setBanners(data.body.feed);
        setNextData(data.body.key);
        // setNumStar([data.body.feed[0].star, data.body.feed[1].star]);
        // setNumComment([data.body.feed[0].num_comment, data.body.feed[1].num_comment])
      });
  }

  useEffect(() => {
    fetchFeed();
  }, []);

  // 서버에서 추가 데이터를 받아오는 함수
  const fetchMoreBanners = async () => {
    try {
      // 서버로부터 추가 배너 데이터를 가져옴
      const response = await fetch(
        `https://nova-platform.kr/feed_explore/get_feed?fclass=None&key=${nextData}`, {
        credentials: 'include'
      }
      ); // 예시 URL
      const newBanners = await response.json();
      const plusFeed = newBanners.body.feed;
      // const newStar = newBanners.body.feed[0].star;
      // const comments = newBanners.body.feed[0].num_comment;
      setNextData(newBanners.body.key);
      // 기존 배너에 새 배너를 추가
      setBanners((prevBanners) => [...prevBanners, ...plusFeed]);
      console.log('fffffffffffffffff', banners);
      // setNumStar((prevNumStar) => [...prevNumStar, newStar]);
      // setNumComment((prevNumComment) => [...prevNumComment, comments])
    } catch (error) {
      console.error("Error fetching additional banners:", error);
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
  let [numComment, setNumComment] = useState([]);
  // let [isClickedStar, setIsClickedStar] = useState(false);
  let [isClickedComment, setIsClickedComment] = useState(false);

  function handleCheckStar(fid, index) {
    // setIsClickedStar(!isClickedStar);
    fetch(`https://nova-platform.kr/feed_explore/check_star?fid=${fid}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setBanners((prevBanners) => {
          return prevBanners.map((banner) => {
            return banner.fid === fid
              ? { ...banner, star: data.body.feed[0].star, star_flag: data.body.feed[0].star_flag }
              : banner;
          });
        });
      });
  }

  function handleShowCommentWindow() {
    setIsClickedComment(!isClickedComment);
  }

  let header = {
    "request-type": "default",
    "client-version": "v1.0.1",
    "client-ip": "127.0.0.1",
    uid: "1234-abcd-5678",
    endpoint: "/core_system/",
  };

  let [inputValue, setInputValue] = useState("");

  function handleChange(e) {
    setInputValue(e.target.value);
  }

  let [newComments, setNewComments] = useState([]);

  function handleSubmit(fid, event) {
    event.preventDefault();

    fetch("https://nova-platform.kr/feed_explore/make_comment", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        header,
      },
      credentials: "include",
      body: JSON.stringify({
        header: header,
        body: {
          fid: `${fid}`,
          body: `${inputValue}`,
        },
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        // setNewComments(data.body.comments);
        setAllComments((prevAllComments) => {
          const newAllComments = [data.body.comments[0], ...prevAllComments];
          return newAllComments;
        });
        setBanners((prevBanners) => {
          return prevBanners.map((banner) => {
            return banner.fid === fid
              ? { ...banner, num_comment: data.body.feed[0].num_comment }
              : banner;
          });
        });
        setInputValue("");
      });
  }

  let [allComments, setAllComments] = useState([]);
  let [commentCount, setCommentCount] = useState(0);
  let [isClickedCommentWindow, setIsClickedCommentWindow] = useState(false);

  function handleShowComment(fid, event) {
    event.preventDefault();
    fetch(`https://nova-platform.kr/feed_explore/view_comment?fid=${fid}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("show", data.body);
        setAllComments(data.body.comments);
      });
  }

  useEffect(() => {
    console.log("pleae", allComments);
    // handleShowComment();
  }, [allComments]);

  let [isClickedLikeBtn, setIsClickedLikeBtn] = useState(false);
  let [commentLikes, setCommentLikes] = useState(0);
  function handleCommentLike(fid, cid, event) {
    event.preventDefault();
    fetch(
      `https://nova-platform.kr/feed_explore/like_comment?fid=${fid}&cid=${cid}`,
      {
        credentials: "include",
      }
    )
      .then((response) => response.json())
      .then((data) => {
        console.log("like", data.body.comments);

        setAllComments((prevAll) => {
          return prevAll.map((comment, i) => {
            return comment.cid === cid
              ? { ...comment, like: data.body.comments[i].like, like_user: data.body.comments[i].like_user }
              : comment;
          });
        });
        console.log("244241242414", allComments);
        setCommentLikes(data.body.comments);
      });
  }

  let [isClickedRemoveBtn, setIsClickedRemoveBtn] = useState(false);
  function handleRemoveComment(fid, cid, event) {
    event.preventDefault();

    const newAll = allComments.filter((comment) => comment.cid !== cid);
    setAllComments(newAll);

    fetch(
      `https://nova-platform.kr/feed_explore/remove_comment?fid=${fid}&cid=${cid}`,
      {
        credentials: "include",
      }
    )
      .then((response) => response.json())
      .then((data) => {
        console.log("remove", data);
        setAllComments(data.body.comments);
      });
  }

  return (
    <div
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
      onWheel={handleWheel}
      ref={sliderRef}
      className={style["test_container"]}
    >
      <div className={`${stylePlanet["top_area"]} ${style["top_bar_area"]}`}>
        <div
          onClick={() => {
            navigate(-1);
          }}
        >
          뒤로
        </div>
        <div>은하계 탐색</div>
      </div>

      <div
        className={style.test}
        style={{
          transform: `translateY(${translateY}px)`,
          transition: isDragging ? "none" : "transform 0.5s ease",
        }}
      >
        {banners.map((banner, i) => {
          return (
            <div key={banner.fid} className={style["short_form"]}>
              <div className={style["button_area"]}>
                {isClickedComment && (
                  <div className={style["comment_window"]}>
                    <div className={style["comment_top"]}>
                      <div className={style['close_btn']} onClick={handleShowCommentWindow}>닫기</div>
                      <div className={style["gray_bar"]}></div>
                      <div>댓글</div>
                    </div>
                    <div className={style.line}></div>

                    <div className={style["comment_body"]}>
                      <div onWheel={(e) => { e.stopPropagation() }} className={style["comment_box1"]}>
                        {allComments.length === 0 ? (
                          <div>댓글이 없습니다.</div>
                        ) : (
                          allComments.map((comment, i) => {
                            return (
                              <div key={comment.cid} className={`${style['comments_box']} ${style['feed_comments_box']}`}>
                                <div className={style['comment']}>
                                  <div className={style['user_name']}>
                                    <div>{comment.uname}</div>
                                    <div className={style['interaction_btn']}>
                                      {
                                        comment.owner ? (<div className={style['delete_btn']} onClick={(event) => handleRemoveComment(comment.fid, comment.cid, event)}>삭제</div>) : (<div className={style['delete_btn']}></div>)
                                      }
                                      <div className={style['report_star_btn']}>
                                        <div>신고</div>
                                        <div className={style['star_num']}>
                                          <FaStar style={comment.like_user ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }}
                                            onClick={(event) => handleCommentLike(comment.fid, comment.cid, event)} />
                                          <div style={{ marginLeft: '2px' }}>
                                            {comment.like}
                                          </div>
                                        </div>
                                      </div>
                                    </div>
                                  </div>
                                  <div className={style['comment_text']}>{comment.body}</div>
                                </div>
                              </div>
                            );
                          })
                        )}
                      </div>
                      <Comments
                        isClickedComment={true}
                        feed={banner}
                        setFeedData={setBanners}
                        allComments={allComments}
                        setAllComments={setAllComments}
                      ></Comments>
                    </div>
                  </div>
                )}

                <div className={style["short_form_container"]}>
                  <div className={style["short_box"]}>
                    <div className={style["img_circle"]}>
                      <img src={banner.image[0]} />
                    </div>
                    <div style={{ height: "110px" }}></div>
                    <Feed
                      className={style["short_feed"]}
                      feed={banner}
                      setFeedData={setBanners}
                      img_circle={true}
                    ></Feed>
                  </div>

                  <div className={style["function_button"]}>
                    <div className={style["func_btn"]}>
                      <button
                        onClick={() => {
                          handleCheckStar(banner.fid, i);
                        }}
                      >
                        <FaStar className={style["func_btn_img"]} style={banner.star_flag ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }} />
                        {/* <FaStar className={style["func_btn_img"]} /> */}
                      </button>
                      {/* <p>{numStar[i]}</p> */}
                      <p>{banner.star}</p>
                    </div>
                    <div className={style["func_btn"]}>
                      <button
                        onClick={(event) => {
                          handleShowComment(banner.fid, event);
                          handleShowCommentWindow();
                          // handleCheckComment(banner.fid, i);
                        }}
                      >
                        <TfiCommentAlt className={style["func_btn_img"]} />
                      </button>
                      <p>{banner.num_comment}</p>
                    </div>
                    <div className={style["func_btn"]}>
                      <button>
                        <PiShareFatLight className={style["func_btn_img"]} />
                      </button>
                      <p>공유</p>
                    </div>
                    <div className={style["func_btn"]}>
                      <button>
                        <MdOutlineReportProblem
                          className={style["func_btn_img"]}
                        />
                      </button>
                      <p>신고</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default FeedPage;

// function CommentWindow() {

//     return (
//         <div className={style.comment}>
//             <div>{allComments[0]}</div>
//             <div>{allComments[0]}</div>
//             <div>삭제</div>
//             <div>신고</div>
//             <div>{allComments[0].star}</div>
//         </div>
//     )
// }
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
