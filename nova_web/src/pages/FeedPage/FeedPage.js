import { Comments } from "../../component/feed";

import style from "./FeedPage.module.css";
import stylePlanet from "./../PlanetPage/Planet.module.css";

import backword from "./../../img/back_icon.png";
import write from "./../../img/new_feed.png";
import star from "./../../img/favorite.png";
import star_color from "./../../img/favorite_color.png";
import comment from "./../../img/comment.png";
import report from "./../../img/report.png";
import share from "./../../img/share.png";
import problem from "./../../img/problem.png";

import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

const FeedPage = () => {
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

  let [isUserState, setIsUserState] = useState(false);

  function handleValidCheck() {
    fetch("https://nova-platform.kr/home/is_valid", {
      credentials: "include", // 쿠키를 함께 포함한다는 것
    })
      .then((response) => {
        if (!response.ok) {
          if (response.status === 401) {
            setIsUserState(false);
          } else if (response.status === 200) {
            setIsUserState(true);
          } else {
            throw new Error(`status: ${response.status}`);
          }
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
      });
  }

  useEffect(() => {
    handleValidCheck();
  }, []);

  function fetchFeed() {
    fetch(`https://nova-platform.kr/feed_explore/get_feed?fclass=None`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setBanners(data.body.feed);
        setNextData(data.body.key);
        console.log("fetchfeed", data);
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
      const response = await fetch(`https://nova-platform.kr/feed_explore/get_feed?fclass=None&key=${nextData}`, {
        credentials: "include",
      }); // 예시 URL
      const newBanners = await response.json();
      const plusFeed = newBanners.body.feed;
      console.log("newBanner", newBanners);
      // const newStar = newBanners.body.feed[0].star;
      // const comments = newBanners.body.feed[0].num_comment;
      setNextData(newBanners.body.key);
      // 기존 배너에 새 배너를 추가
      setBanners((prevBanners) => [...prevBanners, ...plusFeed]);
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

  // let [numStar, setNumStar] = useState([]);
  // let [numComment, setNumComment] = useState([]);
  // let [isClickedStar, setIsClickedStar] = useState(false);
  let [isClickedComment, setIsClickedComment] = useState(false);
  // let [starColor, setStarColor] = useState('');

  function handleCheckStar(fid, index) {
    // setIsClickedStar(!isClickedStar);
    fetch(`https://nova-platform.kr/feed_explore/check_star?fid=${fid}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setBanners((prevBanners) => {
          return prevBanners.map((banner) => {
            return banner.fid === fid ? { ...banner, star: data.body.feed[0].star, star_flag: data.body.feed[0].star_flag } : banner;
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
    fetch(`https://nova-platform.kr/feed_explore/like_comment?fid=${fid}&cid=${cid}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("like", data.body.comments);

        setAllComments((prevAll) => {
          return prevAll.map((comment, i) => {
            return comment.cid === cid ? { ...comment, like: data.body.comments[i].like, like_user: data.body.comments[i].like_user } : comment;
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

    fetch(`https://nova-platform.kr/feed_explore/remove_comment?fid=${fid}&cid=${cid}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("remove", data);
        setAllComments(data.body.comments);
      });
  }

  function handleInteraction(event, fid, action) {
    event.preventDefault();

    fetch(`https://nova-platform.kr/feed_explore/interaction_feed?fid=${fid}&action=${action}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("interactin", data);
        setBanners((prevFeeds) => {
          return prevFeeds.map((feed) => {
            return feed.fid === fid ? { ...feed, attend: data.body.feed[0].attend, result: data.body.feed[0].result } : feed;
          });
        });
      });
  }

  return (
    <div onMouseDown={handleMouseDown} onMouseMove={handleMouseMove} onMouseUp={handleMouseUp} onMouseLeave={handleMouseUp} onWheel={handleWheel} ref={sliderRef} className={style["test_container"]}>
      <div
        className={style["slider-track"]}
        style={{
          transform: `translateY(${translateY}px)`,
          transition: isDragging ? "none" : "transform 0.5s ease",
        }}
      >
        {banners.map((banner, i) => {
          return (
            <div key={banner.fid} className={style["short_form"]}>
              <div className={style["content-box"]}>
                <div className={`${stylePlanet["top_area"]} ${style["top_bar_area"]}`}>
                  <img
                    src={backword}
                    alt="Arrow"
                    className={style.backword}
                    onClick={() => {
                      navigate(-1);
                    }}
                  />
                </div>

                {/* 왼쪽 컨텐츠 */}
                <div className={style["content-container"]}>
                  {/* {
                    isClickedComment ? <div>open</div> : <div>close</div>
                  } */}
                  <div className={style["sup_info"]}>
                    <div id={style["nick_name"]}>{banner.nickname}</div>
                    <div id={style.date}>{banner.date}</div>
                  </div>

                  {/* 댓글 모달 창 */}
                  {isClickedComment && (
                    <div className={style["modal-container"]}>
                      <div className={style["comment-modal"]}>
                        <nav className={style["top_bar"]}>댓글 더보기</nav>
                        <section className={style["text-section"]}>
                          <div className={style["text-box"]}>
                            <p className={style["text-1"]}>지지자</p>
                            <p className={style["text-2"]}>이런 글 쓰지 마쇼</p>
                          </div>
                          <div className={style["icon-box"]}>
                            <button className={style["button-box"]}>삭제</button>
                            <button className={style["button-box"]}>신고</button>
                            <p>별</p>
                          </div>
                        </section>
                      </div>
                    </div>
                  )}
                  {/* 여기까지  */}

                  <div className={style["feed-content"]}>{banner.body}</div>

                  <div className={style["image-box"]}>
                    <div className={style["image-show"]}>
                      <img src={banner.image[0]} alt="이미지" />
                    </div>
                  </div>
                  <div className={style["fclass-box"]}>
                    {banner.fclass === "multiple" && <MultiClass feed={banner} handleInteraction={handleInteraction} />}
                    {banner.fclass === "card" && <CardClass feed={banner} handleInteraction={handleInteraction} />}
                    {banner.fclass === "balance" && <BalanceClass feed={banner} handleInteraction={handleInteraction} />}
                    {banner.fclass === "station" && <StationClass feed={banner} />}
                  </div>
                  <div className={style["comment-box"]}>
                    <Comments isClickedComment={false} feed={banner} setFeedData={setBanners} allComments={allComments} setAllComments={setAllComments} />
                  </div>
                </div>
              </div>

              {/* 오른쪽 버튼 목록 */}
              <div className={style["interaction-box"]}>
                <div className={style["button-box"]}>
                  <div className={style["write-box"]}>
                    <div className={style["btn-box"]}>
                      <img
                        className={style["btn-img"]}
                        src={write}
                        alt="글쓰기"
                        onClick={() => {
                          navigate("/write_feed");
                        }}
                      />
                    </div>
                  </div>

                  <div className={style["not-recommend-box"]}>
                    <div className={`${style["btn-box"]}} ${style["not-recommend-btn"]}`}>
                      <img className={style["btn-img"]} src={problem} alt="추천안함" />
                      <div id={style.text}>추천안함</div>
                    </div>
                  </div>

                  <div className={style["action-box"]}>
                    <div className={style["action-btn"]}>
                      <div className={`${style["btn-box"]}} ${style["action-btn-each"]}`}>
                        <img
                          className={`${style["btn-img"]}`}
                          src={banner.star_flag ? star_color : star}
                          alt="관심표시"
                          onClick={() => {
                            handleCheckStar(banner.fid, i);
                          }}
                        />
                        <div id={style.text}>{banner.star}</div>
                      </div>

                      <div className={`${style["btn-box"]}} ${style["action-btn-each"]}`}>
                        <img
                          className={style["btn-img"]}
                          src={comment}
                          alt="댓글"
                          onClick={(event) => {
                            handleShowComment(banner.fid, event);
                            handleShowCommentWindow();
                          }}
                        />
                        <div id={style.text}>{banner.num_comment}</div>
                      </div>

                      <div className={`${style["btn-box"]}} ${style["action-btn-each"]}`}>
                        <img className={style["btn-img"]} src={share} alt="공유" />
                        <div id={style.text}>공유</div>
                      </div>

                      <div className={`${style["btn-box"]}} ${style["action-btn-each"]}`}>
                        <img className={style["btn-img"]} src={report} alt="신고" />
                        <div id={style.text}>신고</div>
                      </div>
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

function MultiClass({ feed, handleInteraction }) {
  return (
    <div className={style["fclass-container"]}>
      <ol className={style["quiz_box"]}>
        {feed.choice.map((choi, i) => {
          return (
            <li
              key={feed.fid + i}
              style={{ backgroundColor: i === feed.attend ? "#D2C8F7" : "white" }}
              onClick={(e) => {
                handleInteraction(e, feed.fid, i);
              }}
            >
              {i + 1}. {choi}
              <span>{feed.result[i]}</span>
            </li>
          );
        })}
      </ol>
    </div>
  );
}

function CardClass({ feed, handleInteraction }) {
  return (
    <div className={style["fclass-container"]}>
      <div className={style["empathy-box"]}>
        <div>축하하기</div>
        <div>8명</div>
      </div>
    </div>
  );
}

function BalanceClass({ feed, handleInteraction }) {
  return (
    <div className={style["fclass-container"]}>
      <div className={style["balance-box"]}>
        {feed.choice.map((sel, i) => {
          return (
            <div
              key={feed.fid + i}
              className={style["sel-btn"]}
              style={{ backgroundColor: i === feed.attend ? "#D2C8F7" : "white" }}
              onClick={(e) => {
                handleInteraction(e, feed.fid, i);
              }}
            >
              <div>{sel}</div>
              <div>{feed.result[i]}명</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function StationClass({ feed }) {
  return (
    <div className={style["fclass-container"]}>
      <div
        className={style["external-box"]}
        onClick={() => {
          window.open(feed.choice[2], "_blank", "noopener, noreferrer");
        }}
      >
        <div className={style["link-info-box"]}>
          <h1>{feed.choice[0]}</h1>
          <h5>{feed.choice[1]}</h5>
        </div>
      </div>
    </div>
  );
}

{
  /* <div className={style["button_area"]}>
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
                                        <div className={style.report}>신고</div>
                                        <div className={style['star_num']}>
                                          <FaStar className={style['comment_like']} style={comment.like_user ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }}
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
                )} */
}
{
  /*
                        <button
                            <FaStar className={style["func_btn_img"]} style={banner.star_flag ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }} />
                          </button>
                      */
}
