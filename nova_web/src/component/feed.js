import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Viewer } from "@toast-ui/react-editor";
import style from "./../pages/FeedPage/FeedPage.module.css";

import star from "./../img/favorite.png";
import star_color from "./../img/favorite_color.png";
import comment from "./../img/comment.png";

export function useBrightMode() {
  const params = new URLSearchParams(window.location.search);
  const brightModeFromUrl = params.get("brightMode");

  const initialMode = brightModeFromUrl || localStorage.getItem("brightMode") || "bright";

  const [mode, setMode] = useState(initialMode);

  useEffect(() => {
    localStorage.setItem("brightMode", mode);
  }, [mode]);

  return [mode, setMode];
}

export default function Feed({
  feed,
  feedData,
  interaction,
  feedInteraction,
  setFeedData,
  isUserState,
  handleInteraction,
}) {
  let navigate = useNavigate();
  let [isError, setIsError] = useState();
  // let [myAttend, setMyAttend] = useState(null);
  let [isClickedStar, setIsClickedStar] = useState(false);

  function handleCheckStar(fid, e) {
    // e.preventDefault();
    setIsClickedStar(!isClickedStar);
    fetch(`https://nova-platform.kr/feed_explore/check_star?fid=${fid}`, {
      credentials: "include",
    })
      .then((response) => {
        if (!response.ok) {
          if (response.status === 401) {
            setIsError(response.status);
            navigate("/novalogin");
          } else {
            throw new Error(`status: ${response.status}`);
          }
        }
        return response.json();
      })
      .then((data) => {
        setFeedData((prevFeeds) => {
          return prevFeeds.map((feed) => {
            return feed.feed.fid === fid
              ? {
                  ...feed,
                  feed: data.body.feed[0],
                }
              : feed;
          });
        });
      });
  }

  // let [isInteraction, setIsInteraction] = useState(false);
  // let [selectedIndex, setSelectedIndex] = useState(null);
  // const handleClick = (index) => {
  //   if (selectedIndex === index) {
  //     setSelectedIndex(null);
  //   } else {
  //     setSelectedIndex(index);
  //   }
  // };
  // function handleInteraction(event, fid, action) {
  //   event.preventDefault();
  //   console.log("fid", fid);

  //   fetch(`https://nova-platform.kr/feed_explore/interaction_feed?fid=${fid}&action=${action}`, {
  //     credentials: "include",
  //   })
  //     .then((response) => {
  //       if (!response.ok) {
  //         if (response.status === 401) {
  //           setIsError(response.status);
  //           navigate("/novalogin");
  //         } else {
  //           throw new Error(`status: ${response.status}`);
  //         }
  //       }
  //       return response.json();
  //     })
  //     .then((data) => {
  //       console.log(data);
  //       // setFeedData((prevFeeds) => {
  //       //   return prevFeeds.map((feed, i) =>
  //       //     feed.interaction.fid === fid
  //       //       ? {
  //       //           ...feed.interaction,
  //       //           attend: data.body.interaction.attend,
  //       //           result: data.body.interaction.result,
  //       //         }
  //       //       : feed.interaction
  //       //   );
  //       // });
  //       // setMyAttend(data.body.feed[0].attend);
  //       setFeedData((prevFeeds) => {
  //         return prevFeeds.map((feed) => {
  //           return feed.interaction.fid === fid
  //             ? {
  //                 ...feed.interaction,
  //                 attend: data.body.interaction.attend,
  //                 result: data.body.interaction.result,
  //               }
  //             : feed.interaction;
  //         });
  //       });
  //     });
  // }
  // 댓글 더보기 - 본문 보기
  // let [isClickedMoreSee, setIsClickedMoreSee] = useState(false);

  // function handleMoreSee() {
  //   setIsClickedMoreSee(!isClickedMoreSee);
  // }

  // let [allComments, setAllComments] = useState([]);
  // 댓글 보기
  // function handleShowComment(fid, event) {
  //   event.preventDefault();
  //   fetch(`https://nova-platform.kr/feed_explore/view_comment?fid=${fid}`, {
  //     credentials: "include",
  //   })
  //     .then((response) => response.json())
  //     .then((data) => {
  //       console.log("show", data.body);
  //       setAllComments(data.body.comments);
  //     });
  // }

  // let [isClickedLikeBtn, setIsClickedLikeBtn] = useState(false);

  // let [commentLikes, setCommentLikes] = useState(0);

  // 댓글 좋아요 기능
  // function handleCommentLike(fid, cid, event) {
  //   event.preventDefault();
  //   fetch(`https://nova-platform.kr/feed_explore/like_comment?fid=${fid}&cid=${cid}`, {
  //     credentials: "include",
  //   })
  //     .then((response) => {
  //       if (!response.ok) {
  //         if (response.status === 401) {
  //           setIsError(response.status);
  //           navigate("/novalogin");
  //         } else {
  //           throw new Error(`status: ${response.status}`);
  //         }
  //       }
  //       return response.json();
  //     })
  //     .then((data) => {
  //       setAllComments((prevAll) => {
  //         return prevAll.map((comment, i) => {
  //           return comment.cid === cid
  //             ? {
  //                 ...comment,
  //                 like: data.body.comments[i].like,
  //                 like_user: data.body.comments[i].like_user,
  //               }
  //             : comment;
  //         });
  //       });
  //       setCommentLikes(data.body.comments);
  //     });
  // }

  // 댓글 삭제 기능
  // function handleRemoveComment(fid, cid, event) {
  //   event.preventDefault();

  //   const newAll = allComments.filter((comment) => comment.cid !== cid);
  //   setAllComments(newAll);

  //   fetch(`https://nova-platform.kr/feed_explore/remove_comment?fid=${fid}&cid=${cid}`, {
  //     credentials: "include",
  //   })
  //     .then((response) => {
  //       if (!response.ok) {
  //         if (response.status === 401) {
  //           setIsError(response.status);
  //           navigate("/novalogin");
  //         } else {
  //           throw new Error(`status: ${response.status}`);
  //         }
  //       }
  //       return response.json();
  //     })
  //     .then((data) => {
  //       console.log("remove", data.body.comments);
  //       // setAllComments((prevAll)=>{
  //       //     const newAllComments = [data.body.comments];
  //       //     return newAllComments;
  //       // })
  //     });
  // }
  // let header = {
  //   "request-type": "default",
  //   "client-version": "v1.0.1",
  //   "client-ip": "127.0.0.1",
  //   uid: "1234-abcd-5678",
  //   endpoint: "/core_system/",
  // };

  // let [inputValue, setInputValue] = useState("");
  // function handleChange(e) {
  //   setInputValue(e.target.value);
  // }

  // function handleSubmit(fid, event) {
  //   event.preventDefault();

  //   fetch("https://nova-platform.kr/feed_explore/make_comment", {
  //     method: "POST",
  //     headers: {
  //       "Content-Type": "application/json",
  //       header,
  //     },
  //     credentials: "include",
  //     body: JSON.stringify({
  //       header: header,
  //       body: {
  //         fid: `${fid}`,
  //         body: `${inputValue}`,
  //       },
  //     }),
  //   })
  //     .then((response) => {
  //       if (!response.ok) {
  //         if (response.status === 401) {
  //           setIsError(response.status);
  //           navigate("/novalogin");
  //         } else {
  //           throw new Error(`status: ${response.status}`);
  //         }
  //       }
  //       return response.json();
  //     })
  //     .then((data) => {
  //       console.log(data);
  //       // setNewComments(data.body.comments);
  //       setAllComments((prevAllComments) => {
  //         const newAllComments = [data.body.comments[0], ...prevAllComments];
  //         return newAllComments;
  //       });
  //       setFeedData((prevFeeds) => {
  //         return prevFeeds.map((feed) => {
  //           return feed.fid === fid
  //             ? { ...feed, num_comment: data.body.feed[0].num_comment }
  //             : feed;
  //         });
  //       });
  //       setInputValue("");
  //     });
  // }

  // function handleRequestURL(url) {
  //   window.open(url, "_blank", "noopener, noreferrer");
  // }
  // const [mode, setMode] = useBrightMode();
  // function useBrightMode() {
  //   const params = new URLSearchParams(window.location.search);
  //   const brightModeFromUrl = params.get("brightMode");

  //   const initialMode = brightModeFromUrl || localStorage.getItem("brightMode") || "bright";

  //   const [mode, setMode] = useState(initialMode);

  //   useEffect(() => {
  //     localStorage.setItem("brightMode", mode);
  //   }, [mode]);

  //   return [mode, setMode];
  // }
  return (
    <>
      <ContentFeed
        feed={feed}
        interaction={interaction}
        feedInteraction={feedInteraction}
        handleCheckStar={handleCheckStar}
        handleInteraction={handleInteraction}
      />
    </>
  );
}

// export function InfoArea({ color, name, date, supporter }) {
//   return (
//     <div className={style["info_area"]}>
//       <div className={style["top_part"]}>
//         <div className={style["planet_name"]}>
//           {/* <img src={img}></img> */}
//           {/* <div className={style.circle} style={{ background: `${color}` }}></div> */}
//           {/*<p>{name}</p>*/}
//           <p className={style["write-date"]}>{date}</p>
//         </div>
//         <p className={style["sup_people"]}>{supporter}</p>
//       </div>
//     </div>
//   );
// }

// export function Text({ data, hashtag }) {
//   const [mode, setMode] = useBrightMode();
//   let navigate = useNavigate();

//   function onClickTag(tag) {
//     navigate(`/feed_list?keyword=${tag}`);
//   }

//   function useBrightMode() {
//     const params = new URLSearchParams(window.location.search);
//     const brightModeFromUrl = params.get("brightMode");

//     const initialMode = brightModeFromUrl || localStorage.getItem("brightMode") || "bright";

//     const [mode, setMode] = useState(initialMode);

//     useEffect(() => {
//       localStorage.setItem("brightMode", mode);
//     }, [mode]);

//     return [mode, setMode];
//   }
//   return (
//     <div>
//       {hashtag.map((tag, i) => {
//         return (
//           <span
//             className={`${style["tag-text"]} ${style[getModeClass(mode)]}`}
//             key={i}
//             onClick={() => onClickTag(tag)}
//           >
//             #{tag}
//           </span>
//         );
//       })}
//       <div className={`${style["feed-text"]} ${style[getModeClass(mode)]}`}>{<p>{data}</p>}</div>
//     </div>
//   );
// }

// export function Comments({
//   isClickedComment,
//   feed,
//   allComments,
//   setAllComments,
//   setFeedData,
//   isUserState,
// }) {
//   let [isError, setIsError] = useState();
//   let navigate = useNavigate();

//   let header = {
//     "request-type": "default",
//     "client-version": "v1.0.1",
//     "client-ip": "127.0.0.1",
//     uid: "1234-abcd-5678",
//     endpoint: "/core_system/",
//   };

//   let [inputValue, setInputValue] = useState("");

//   function handleChange(e) {
//     setInputValue(e.target.value);
//   }

//   function handleSubmit(fid, event) {
//     event.preventDefault();

//     fetch("https://nova-platform.kr/feed_explore/make_comment", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//         header,
//       },
//       credentials: "include",
//       body: JSON.stringify({
//         header: header,
//         body: {
//           fid: `${feed.fid}`,
//           body: `${inputValue}`,
//           target_cid: "",
//         },
//       }),
//     })
//       .then((response) => {
//         if (!response.ok) {
//           if (response.status === 401) {
//             setIsError(response.status);
//             navigate("/novalogin");
//           } else {
//             throw new Error(`status: ${response.status}`);
//           }
//         }
//         return response.json();
//       })
//       .then((data) => {
//         console.log(data);
//         // setNewComments(data.body.comments);
//         setAllComments((prevAllComments) => {
//           const newAllComments = [data.body.comments[0], ...prevAllComments];
//           return newAllComments;
//         });
//         setFeedData((prevFeeds) => {
//           return prevFeeds.map((feed) => {
//             return feed.fid === fid
//               ? { ...feed, num_comment: data.body.feed[0].num_comment }
//               : feed;
//           });
//         });
//         setInputValue("");
//         // console.log('asdjljsdlasdajld', allComments);
//       });
//   }
//   const [mode, setMode] = useBrightMode();
//   function useBrightMode() {
//     const params = new URLSearchParams(window.location.search);
//     const brightModeFromUrl = params.get("brightMode");

//     const initialMode = brightModeFromUrl || localStorage.getItem("brightMode") || "bright";

//     const [mode, setMode] = useState(initialMode);

//     useEffect(() => {
//       localStorage.setItem("brightMode", mode);
//     }, [mode]);

//     return [mode, setMode];
//   }
//   return (
//     <div className={style["comment_container"]}>
//       <div className={style["comment_box"]}>
//         {allComments.length === 0 ? (
//           <>
//             {/* <div className={style['comment_support']}>{feed.comment.uname}</div> */}
//             <div className={style["comment_data"]}>{feed.comment.body}</div>
//           </>
//         ) : (
//           !isClickedComment && (
//             <>
//               <div className={`${style["comment_support"]} ${style[getModeClass(mode)]}`}>
//                 {allComments[0].uname}
//               </div>
//               <div className={style["comment_data"]}>{allComments[0].body}</div>
//             </>
//           )
//         )}
//       </div>
//       <div className={style["comment_action"]}>
//         <form onSubmit={(event) => handleSubmit(feed.fid, event)}>
//           <input
//             type="text"
//             value={inputValue}
//             onChange={handleChange}
//             className={` ${style["comment-box"]} ${style[getModeClass(mode)]}`}
//           ></input>
//           <button
//             type="submit"
//             className={` ${style["comment-write"]} ${style[getModeClass(mode)]}`}
//           >
//             댓글 작성
//           </button>
//         </form>
//       </div>
//     </div>
//   );
// }

// 내용 별 피드 박스

export function ContentFeed({
  feed,
  interaction,
  feedInteraction,
  handleCheckStar,
  handleInteraction,
}) {
  let navigate = useNavigate();

  if (!feed) {
    return <div>loading 중</div>;
  }

  return (
    <div
      className={style["wrapper-container"]}
      onClick={(e) => {
        e.preventDefault();
        navigate(`/feed_detail/${feed.fid}`, {
          state: { commentClick: false },
        });
      }}
    >
      <div className={style["user-container"]}>
        <div>{feed.date}</div>
        <div>{feed.nickname}</div>
      </div>

      <div
        className={`${style["body-container"]} ${
          feed.fclass === "long" ? style["long-form-hidden"] : ""
        }`}
      >
        <div className={style["body-hashtag"]}>
          {feed?.hashtag?.length !== 0 &&
            feed?.hashtag?.map((tag, i) => {
              return <span key={i}>#{tag}</span>;
            })}
        </div>
        {feed.fclass === "short" && <div className={style["body-content"]}>{feed.body}</div>}
        {feed.image?.length > 0 && feed.fclass === "short" ? (
          <div className={style["image-container"]}>
            <img src={feed.image[0]} alt="image" />
          </div>
        ) : (
          <div></div>
        )}
        {/* {feed.fclass === "short" && <SelectOption feed={feed} interaction={interaction} />} */}
        {feed.fclass === "short" && (
          <QuizOption feed={feed} interaction={interaction} handleInteraction={handleInteraction} />
        )}
        {feed.fclass === "long" && <Viewer initialValue={feed.raw_body} />}
      </div>

      <div className={style["button-container"]}>
        <div>신고</div>
        <div className={style["button-box1"]}>
          <div className={style["action-button"]}>
            <button
              onClick={(e) => {
                e.stopPropagation();
                handleCheckStar(feed.fid, e);
              }}
            >
              <img src={feed.star_flag ? star_color : star} alt="star-icon" />
            </button>
            <span>{feed.star}</span>
          </div>

          <div className={style["action-button"]}>
            <button
              onClick={(e) => {
                e.stopPropagation();
                navigate(`/feed_detail/${feed.fid}`, {
                  state: { commentClick: true },
                });
              }}
            >
              <img src={comment} alt="comment-icon" />
            </button>
            <span>{feed.num_comment}</span>
          </div>
        </div>
      </div>
      {feed.fclass === "long" && interaction?.choice?.length > 0 && (
        <div
          className={style["long-form-container"]}
          onClick={(e) => {
            e.stopPropagation();
          }}
        >
          <div className={style["action-container"]}>
            {interaction.choice.map((option, i) => {
              return (
                <div
                  key={i}
                  className={style["action-box"]}
                  onClick={(e) => {
                    handleInteraction(e, feed.fid, i);
                  }}
                >
                  <div
                    className={style["action-result"]}
                    style={{ width: `${interaction.result[i]}%` }}
                  >
                    {option}
                  </div>

                  <div className={style["action-points"]}>{interaction.result[i]}%</div>
                </div>
              );
            })}
          </div>

          <div className={style["button-container"]}>
            <div>신고</div>
            <div className={style["button-box1"]}>
              <div className={style["action-button"]}>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleCheckStar(feed.fid, e);
                  }}
                >
                  <img src={feed.star_flag ? star_color : star} alt="star-icon" />
                </button>
                <span>{feed.star}</span>
              </div>

              <div className={style["action-button"]}>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    navigate(`/feed_detail/${feed.fid}`, {
                      state: { commentClick: true },
                    });
                  }}
                >
                  <img src={comment} alt="comment-icon" />
                </button>
                <span>{feed.num_comment}</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function QuizOption({ feed, interaction, handleInteraction }) {
  return (
    <ol className={style["quiz-container"]}>
      {interaction &&
        interaction?.choice?.map((option, i) => {
          return (
            <li
              key={i}
              onClick={(e) => {
                e.stopPropagation();
                handleInteraction(e, interaction.fid, i);
              }}
            >
              {i + 1}. {option} / {interaction.result[i]}
            </li>
          );
        })}
    </ol>
  );
}
// function SelectOption({ feed, feedInteraction }) {
//   return (
//     <div className={style["option-container"]}>
//       {/* <ProgressBar point={50} type={"feed"} /> */}
//       {feedInteraction.choice.map((option, i) => {
//         return (
//           <button key={i} className={style["option"]} onClick={(e) => e.stopPropagation()}>
//             {option}
//           </button>
//         );
//       })}
//     </div>
//   );
// }

{
  /* <ol className={style["quiz_box"]}>
                  {feed.choice.map((choi, i) => {
                    if (feed.attend === i) {
                      if (isUserState) {
                        return (
                          <li
                            onClick={(e) => {
                              handleInteraction(e, feed.fid, i);
                              handleClick(i);
                            }}
                            key={i}
                            style={{ backgroundColor: i === feed.attend ? "#D2C8F7" : "white" }}
                          >
                            {i + 1}. {choi}
                            <span>{feed.result[i]}</span>
                          </li>
                        );
                      } */
}

// 이미지 갯수 별 레이아웃
// {!img_circle && (
//   <div className={style["home_feed_img"]}>
//     {/* 1개이미지 */}
//     {feed.num_image === 1 && (
//       <img
//         style={{ cursor: "pointer" }}
//         src={feed.image[0]}
//         alt="img"
//         onClick={() => {
//           handleRequestURL(feed.image[0]);
//         }}
//       />
//     )}
//     {/* 2개이미지 */}
//     {feed.num_image === 2 && (
//       <div className={style["image-box"]}>
//         <div className={`${style["image-show"]} ${style["two-image"]}`}>
//           {feed.image.map((img, i) => {
//             return (
//               <img
//                 style={{ cursor: "pointer" }}
//                 key={i}
//                 src={img}
//                 alt="img"
//                 onClick={() => {
//                   handleRequestURL(img);
//                 }}
//               />
//             );
//           })}
//         </div>
//       </div>
//     )}
//     {/* 3개이미지 */}
//     {feed.num_image === 3 && (
//       <div className={style["image-box"]}>
//         <div className={`${style["image-show"]} ${style["three-image"]}`}>
//           {feed.image.map((img, i) => {
//             return (
//               <img
//                 style={{ cursor: "pointer" }}
//                 key={i}
//                 src={img}
//                 alt="img"
//                 onClick={() => {
//                   handleRequestURL(img);
//                 }}
//               />
//             );
//           })}
//         </div>
//       </div>
//     )}
//     {/* 4개이미지 */}
//     {feed.num_image === 4 && (
//       <div className={style["image-show"]}>
//         {feed.image.map((img, i) => {
//           return (
//             <img
//               style={{ cursor: "pointer" }}
//               key={i}
//               src={img}
//               alt="img"
//               onClick={() => {
//                 handleRequestURL(img);
//               }}
//             />
//           );
//         })}
//       </div>
//     )}
//     {/* 5개이상 */}
//     {feed.num_image >= 5 && (
//       <div className={style["image-box"]}>
//         <div className={`${style["image-origin"]} ${style["five-over-image"]}`}>
//           {feed.image.map((img, i) => {
//             return (
//               <img
//                 style={{ cursor: "pointer" }}
//                 key={i}
//                 src={img}
//                 alt="img"
//                 onClick={() => {
//                   handleRequestURL(img);
//                 }}
//               />
//             );
//           })}
//         </div>
//       </div>
//     )}
//   </div>
// )}
