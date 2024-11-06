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

import write_gray from "./../../img/write_gray.png";
import report_gray from "./../../img/report_gray.png";
import problem_gray from "./../../img/not_gray.png";
import share_gray from "./../../img/share_gray.png";
// import like_gray from "./../../img/like_gray.png";
import comment_gray from "./../../img/comment_gray.png";
import star_gray from "./../../img/star_gray.png";
import LeftBar from "./../WideVer/LeftBar.js";
import RightBar from "./../WideVer/RightBar.js";

import likeStar from "./../../img/like_star.png";
import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

const FeedPage = () => {
  let navigate = useNavigate();

  const [banners, setBanners] = useState([]);
  const [nextData, setNextData] = useState(0);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  const [startY, setStartY] = useState(0);
  const [translateY, setTranslateY] = useState(0);
  const [dragDistance, setDragDistance] = useState(0);
  const sliderRef = useRef(null);

  // const [count, setCount] = useState(0);
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

  const handleTouchStart = (e) => {
    setIsDragging(true);
    setStartY(e.touches[0].clientY);
  };

  const handleTouchMove = (e) => {
    if (!isDragging) return;

    const distance = e.touches[0].clientY - startY;
    setDragDistance(distance);
    setTranslateY(-currentIndex * window.innerHeight + distance);
  };

  const handleTouchEnd = () => {
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

  // 피드 데이터 받기
  function fetchFeed() {
    fetch(`https://nova-platform.kr/feed_explore/get_feed?fclass=None`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setBanners(data.body.feed);
        setNextData(data.body.key);
        // console.log("fetchfeed", data);
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
      // console.log("newBanner", newBanners);
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

  let [isClickedComment, setIsClickedComment] = useState(false);

  // 피드 좋아요 부분(되긴되는데 반복되는 오류가 생김)
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

  // let [inputValue, setInputValue] = useState("");

  // function handleChange(e) {
  //   setInputValue(e.target.value);
  // }

  // let [newComments, setNewComments] = useState([]);
  let [allComments, setAllComments] = useState([]);
  // let [commentCount, setCommentCount] = useState(0);
  // let [isClickedCommentWindow, setIsClickedCommentWindow] = useState(false);

  // 댓글 창 보기(완료)
  function handleShowComment(fid, event) {
    event.preventDefault();
    fetch(`https://nova-platform.kr/feed_explore/view_comment?fid=${fid}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        // console.log("show", data.body);
        setAllComments(data.body.comments);
      });
  }

  // useEffect(() => {
  // console.log("pleae", allComments);
  // handleShowComment();
  // }, [allComments]);

  // let [isClickedLikeBtn, setIsClickedLikeBtn] = useState(false);
  // let [commentLikes, setCommentLikes] = useState(0);

  // 댓글 좋아요 부분(완료)
  function handleCommentLike(fid, cid, event) {
    event.preventDefault();
    fetch(`https://nova-platform.kr/feed_explore/like_comment?fid=${fid}&cid=${cid}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setAllComments((prevAll) => {
          return prevAll.map((comment, i) => {
            return comment.cid === cid ? { ...comment, like: data.body.comments[i].like, like_user: data.body.comments[i].like_user } : comment;
          });
        });
        // setCommentLikes(data.body.comments);
      });
  }

  // 댓글 삭제 부분(완료)
  function handleRemoveComment(fid, cid, event) {
    event.preventDefault();

    const newAll = allComments.filter((comment) => comment.cid !== cid);
    setAllComments(newAll);

    fetch(`https://nova-platform.kr/feed_explore/remove_comment?fid=${fid}&cid=${cid}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setAllComments(data.body.comments);
        setBanners((prevFeeds) => {
          return prevFeeds.map((feed) => {
            return feed.fid === fid ? { ...feed, num_comment: data.body.feed[0].num_comment } : feed;
          });
        });
      });
  }

  // 피드 상호작용(완료)
  function handleInteraction(event, fid, action) {
    event.preventDefault();

    fetch(`https://nova-platform.kr/feed_explore/interaction_feed?fid=${fid}&action=${action}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        // console.log("interactin", data);
        setBanners((prevFeeds) => {
          return prevFeeds.map((feed) => {
            return feed.fid === fid ? { ...feed, attend: data.body.feed[0].attend, result: data.body.feed[0].result } : feed;
          });
        });
      });
  }

  let [nowIndex, setNowIndex] = useState(0);

  function handleNext() {
    setNowIndex((prevIndex) => prevIndex + 1);
  }

  // 댓글 더보기에서 댓글입력(완료)
  let [inputValue, setInputValue] = useState("");

  function handleChange(e) {
    setInputValue(e.target.value);
  }

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
        setBanners((prevFeeds) => {
          return prevFeeds.map((feed) => {
            return feed.fid === fid ? { ...feed, num_comment: data.body.feed[0].num_comment } : feed;
          });
        });
        setInputValue("");
      });
  }

  function handleRequestURL(url) {
    window.open(url, "_blank", "noopener, noreferrer");
  }

  return (
    <div onMouseDown={handleMouseDown} onMouseMove={handleMouseMove} onMouseUp={handleMouseUp} onMouseLeave={handleMouseUp} onWheel={handleWheel} onTouchStart={handleTouchStart} onTouchMove={handleTouchMove} onTouchEnd={handleTouchEnd} ref={sliderRef}
      className={style["test_container"]}
    >
      <div
        className={style["slider-track"]}
        style={{
          transform: `translateY(${translateY}px)`,
          transition: isDragging ? "none" : "transform 0.5s ease",
        }}
      >
        {banners.map((banner, i) => {
          return (
            <div key={banner.fid} className={style["short_form"]}
            // style={{height:`${height}px`}}
            >
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
                  <div className={style["sup_info"]}>
                    <div className={style["nick_name"]}>{banner.nickname}</div>
                    <div className={style.date}>{banner.date}</div>
                  </div>

                  {/* 댓글 모달 창 */}
                  {isClickedComment && (
                    <div className={style["modal-container"]}>
                      <div className={style["comment-modal"]}>
                        <nav className={style["top_bar"]}>댓글 더보기</nav>
                        <nav onClick={handleShowCommentWindow} className={style["top_bar"]}>
                          닫기
                        </nav>
                        {allComments.length === 0 ? (
                          <div>댓글이 없습니다.</div>
                        ) : (
                          allComments.map((comment, i) => {
                            return (
                              <section key={comment.cid} className={style["text-section"]}>
                                <div className={style["text-box"]}>
                                  <p className={style["text-1"]}>{comment.uname}</p>
                                  <p className={style["text-2"]}>{comment.body}</p>
                                </div>
                                <div className={style["icon-modal"]}>
                                  {comment.owner ? (
                                    <button
                                      onClick={(e) => {
                                        handleRemoveComment(comment.fid, comment.cid, e);
                                      }}
                                      className={style["button-modal"]}
                                    >
                                      삭제
                                    </button>
                                  ) : (
                                    <button className={style["button-modal"]}></button>
                                  )}

                                  <button className={style["button-modal"]}>신고</button>
                                  <div className={style["star-modal"]}>
                                    <img
                                      src={comment.like_user ? star_color : star}
                                      alt="clickable"
                                      onClick={(e) => {
                                        handleCommentLike(comment.fid, comment.cid, e);
                                      }}
                                      className={style["img-star"]}
                                    />
                                    <p>{comment.like}</p>
                                  </div>
                                </div>
                              </section>
                            );
                          })
                        )}
                        <div className={`${style["comment_action"]} ${style["comment-input"]}`}>
                          <form onSubmit={(event) => handleSubmit(banner.fid, event)}>
                            <input type="text" value={inputValue} onChange={handleChange}></input>
                            <button type="submit">댓글 작성</button>
                          </form>
                        </div>
                      </div>
                    </div>
                  )}
                  {/* 여기까지  */}
                  <div className={style['hashtag-box']}>#해시태그</div>
                  <div className={style["feed-content"]}>{banner.body}</div>

                  {/* 1개이미지 */}
                  {
                    banner.num_image === 1 && (
                      <div className={style['image-box']}>
                        <div className={`${style["image-show"]} ${style['one-image']}`}>
                          <img
                            style={{ cursor: 'pointer' }}
                            src={banner.image[0]} alt="이미지" onClick={() => { handleRequestURL(banner.image[0]) }} />
                        </div>
                      </div>
                    )
                  }

                  {/* 2개이미지 */}
                  {
                    banner.num_image === 2 && (
                      <div className={style['image-box']}>
                        <div className={` ${style['two-image']}`}>
                          {banner.image.map((img, i) => {
                            return (
                              <img
                                style={{ cursor: 'pointer' }}
                                key={i} src={img} alt="이미지" onClick={() => { handleRequestURL(img) }} />
                            )
                          })}
                        </div>
                      </div>
                    )
                  }

                  {/* 3개 이미지 */}
                  {
                    banner.num_image === 3 && (
                      <div className={style['image-box']}>
                        <div className={`${style["image-show"]} ${style['three-image']}`}>
                          {banner.image.map((img, i) => {
                            return (
                              <img
                                style={{ cursor: 'pointer' }}
                                key={i} src={img} alt="이미지" onClick={() => { handleRequestURL(img) }} />
                            )
                          })}
                        </div>
                      </div>
                    )
                  }

                  {/* 4개 이미지 */}
                  {
                    banner.num_image === 4 && (
                      <div className={style["image-box"]}>
                        <div className={style["image-show"]}>
                          {banner.image.map((img, i) => {
                            return (
                              <img
                                style={{ cursor: 'pointer' }}
                                key={i} src={img} alt="이미지" onClick={() => { handleRequestURL(img) }} />
                            )
                          })}
                        </div>
                      </div>
                    )
                  }

                  {/* 5개 이미지 */}
                  {
                    banner.num_image >= 5 && (
                      <div className={style["image-box"]}>
                        <div className={`${style["image-origin"]} ${style["five-over-image"]}`}>
                          {banner.image.map((img, i) => {
                            return (
                              <img
                                style={{ cursor: 'pointer' }}
                                key={i} src={img} alt="이미지" onClick={() => { handleRequestURL(img) }} />
                            )
                          })}
                        </div>
                      </div>
                    )
                  }


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
                        src={write_gray}
                        alt="글쓰기"
                        onClick={() => {
                          navigate("/write_feed");
                        }}
                      />
                    </div>
                  </div>

                  <div className={style["not-recommend-box"]}>
                    <div className={`${style["btn-box"]}} ${style["not-recommend-btn"]}`}>
                      <img className={style["btn-img"]} src={problem_gray} alt="추천안함" />
                      <div id={style.text}>추천안함</div>
                    </div>
                  </div>

                  <div className={style["action-box"]}>
                    <div className={style["action-btn"]}>
                      <div className={`${style["btn-box"]}} ${style["action-btn-each"]}`}>
                        <img
                          className={`${style["btn-img"]}`}
                          src={banner.star_flag ? star_color : star_gray}
                          alt="관심표시"
                          onClick={() => {
                            handleCheckStar(banner.fid, i);
                          }}
                        />
                        <div id={style.text}>{banner.star}</div>
                      </div>

                      <div className={`${style["btn-box"]}} ${style["action-btn-each"]}`}>
                        <img
                          className={`${style["btn-img"]} ${style['comment-img']}`}
                          src={comment_gray}
                          alt="댓글"
                          onClick={(event) => {
                            handleShowCommentWindow();
                            handleShowComment(banner.fid, event);
                          }}
                        />
                        <div id={style.text}>{banner.num_comment}</div>
                      </div>

                      <div className={`${style["btn-box"]}} ${style["action-btn-each"]}`}>
                        <img className={style["btn-img"]} src={share_gray} alt="공유" />
                        <div id={style.text}>공유</div>
                      </div>

                      <div className={`${style["btn-box"]}} ${style["action-btn-each"]}`}>
                        <img className={style["btn-img"]} src={report_gray} alt="신고" />
                        <div id={style.text}>신고</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div >
    </div >
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
              style={{ backgroundColor: i === feed.attend ? "#D2C8F7" : "#5f5f5f" }}
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