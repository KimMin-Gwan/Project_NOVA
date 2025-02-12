import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Viewer } from "@toast-ui/react-editor";
import style from "./../pages/FeedPage/FeedPage.module.css";

import star from "./../img/favorite.png";
import link_pin_icon from "./../img/link_pin.svg";
import star_color from "./../img/favorite_color.png";
import comment from "./../img/comment.png";
import postApi from "../services/apis/postApi";

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

// 내용 별 피드 박스

export function ContentFeed({
  detailPage,
  feed,
  interaction,
  feedInteraction,
  handleCheckStar,
  handleInteraction,
  links,
}) {
  let navigate = useNavigate();
  let header = {
    "request-type": "default",
    "client-version": "v1.0.1",
    "client-ip": "127.0.0.1",
    uid: "1234-abcd-5678",
    endpoint: "/user_system/",
  };

  if (!feed) {
    return <div>loading 중..,.</div>;
  }
  console.log("deee", detailPage);

  return (
    <div
      className={`${style["wrapper-container"]} ${feed.fclass === "long" && style["long-wrapper"]}`}
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

      <div className={`${style["body-container"]} ${detailPage ? "" : style["long-form-hidden"]}`}>
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

      <LinkSection links={links} />

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

let header = {
  "request-type": "default",
  "client-version": "v1.0.1",
  "client-ip": "127.0.0.1",
  uid: "1234-abcd-5678",
  endpoint: "/user_system/",
};

function LinkSection({ links }) {
  const [isLoading, setIsLoading] = useState(true);
  const [linkImage, setLinkImage] = useState([]);

  async function fetchImageTag() {
    for (const item of links)
      await postApi
        .post("nova_sub_system/image_tag", {
          header: header,
          body: {
            url: item.url,
          },
        })
        .then((res) => {
          setLinkImage((prev) => [...prev, res.data.body.image]);
          console.log(res.data);
        });
    setIsLoading(false);
  }

  useEffect(() => {
    if (links) {
      fetchImageTag();
    }
    setIsLoading(false);
  }, [links]);

  function onClickLink(url) {
    window.open(url, "_blank", "noopener, noreferrer");
  }

  if (isLoading) {
    <div>loading...</div>;
  }
  return (
    <>
      {links && (
        <div className={style["link-line"]}>
          <div className={style["hr-sect"]}>첨부된 링크</div>
          <p>안전을 위해 신뢰할 수 있는 사이트에만 접속하세요.</p>
        </div>
      )}
      {links &&
        links.map((link, i) => {
          return (
            <div key={link.lid} className={style["Link_Container"]}>
              <div
                className={style["Link_box"]}
                onClick={() => {
                  onClickLink(link.url);
                }}
              >
                <div className={style["Link_thumbnail"]}>
                  <img src={linkImage[i]} alt="thumbnail" />
                </div>

                <div className={style["Link_info"]}>
                  <div className={style["Link_title"]}>{link.title}</div>
                  <div className={style["Link_domain"]}>{link.domain}</div>
                </div>
              </div>

              <div className={style["Link_explain"]}>
                <span>
                  <img src={link_pin_icon} alt="pin" />
                </span>
                <span>{link.explain}</span>
              </div>
            </div>
          );
        })}
    </>
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
