import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { Viewer } from "@toast-ui/react-editor";
import style from "./../pages/FeedPage/FeedPage.module.css";

import star from "./../img/favorite.png";
import link_pin_icon from "./../img/link_pin.svg";
import star_color from "./../img/favorite_color.png";
import info_icon from "./../img/Info.svg";
import comment from "./../img/comment.png";
import postApi from "../services/apis/postApi";
import HEADER from "../constant/header";
import mainApi from "../services/apis/mainApi";

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
const header = HEADER;

export default function Feed({
  feed,
  interaction,
  feedInteraction,
  setFeedData,
  handleInteraction,
}) {
  let navigate = useNavigate();
  let [isError, setIsError] = useState();
  let [isClickedStar, setIsClickedStar] = useState(false);

  function handleCheckStar(fid, e) {
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

  const [report, setReport] = useState();

  async function fetchReportResult(fid) {
    await postApi
      .post("nova_sub_system/try_report", {
        header: header,
        body: {
          fid: fid,
        },
      })
      .then((res) => console.log("rerere", res.data));
  }

  return (
    <>
      <ContentFeed
        feed={feed}
        interaction={interaction}
        feedInteraction={feedInteraction}
        handleCheckStar={handleCheckStar}
        handleInteraction={handleInteraction}
        fetchReportResult={fetchReportResult}
      />
    </>
  );
}

// 내용 별 피드 박스

export function ContentFeed({ detailPage, feed, handleCheckStar, links, fetchReportResult }) {
  let navigate = useNavigate();

  async function fetchOriginalText(fid) {
    await mainApi.get(`feed_explore/original_feed_data?fid=${fid}`).then((res) => {
      console.log(res.data);
    });
  }

  let scrollRef = useRef(null);
  let [isDrag, setIsDrag] = useState(false);
  let [dragStart, setDragStart] = useState("");
  let [hasDragged, setHasDragged] = useState(false);

  function onMouseDown(e) {
    e.preventDefault();
    setIsDrag(true);
    setDragStart(e.pageX + scrollRef.current.scrollLeft);
    setHasDragged(false);
  }

  function onMouseUp(e) {
    if (hasDragged) {
      e.stopPropagation();
      e.preventDefault();
    }
    setIsDrag(false);
  }

  function onMouseMove(e) {
    if (isDrag) {
      scrollRef.current.scrollLeft = dragStart - e.pageX;
      setHasDragged(true);
    }
  }

  if (!feed) {
    return <div>loading 중...</div>;
  }

  return (
    <div
      className={`${style["wrapper-container"]} ${feed.fclass === "long" && style["long-wrapper"]}`}
      onClick={(e) => {
        e.preventDefault();
        e.stopPropagation();
        navigate(`/feed_detail/${feed.fid}`, {
          state: { commentClick: false },
        });
      }}
    >
      <div className={style["user-container"]}>
        <div>{feed.date}</div>
        <div>{feed.nickname}</div>
      </div>

      <div className={style["AI_container"]}>
        <div className={style["AI_text_info"]}>
          <span>
            <img src={info_icon} alt="info" />
          </span>
          본 게시글의 본문은 AI에 의해 필터링 되었습니다.
        </div>
        <button
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            fetchOriginalText(feed.fid);
          }}
        >
          원문 보기
        </button>
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
            <div
              ref={scrollRef}
              className={`${style["image-origin"]} ${style["two-over-image"]}`}
              onMouseDown={onMouseDown}
              onMouseMove={onMouseMove}
              onMouseUp={onMouseUp}
              // onClick={(e) => {
              //   e.stopPropagation();
              // }}
            >
              <img src={feed.image[0]} alt="image" />
              {feed.num_image >= 2 &&
                feed.image.map((img, i) => {
                  return <img key={i} src={img} alt="image" />;
                })}
            </div>
          </div>
        ) : (
          <div></div>
        )}

        {feed.fclass === "long" && <Viewer initialValue={feed.raw_body} />}
      </div>

      {links && <LinkSection links={links} />}

      <div className={style["button-container"]}>
        <div
          onClick={(e) => {
            e.stopPropagation();
            fetchReportResult(feed.fid);
          }}
        >
          신고
        </div>
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
  );
}

function LinkSection({ links }) {
  const [isLoading, setIsLoading] = useState(true);
  const [linkImage, setLinkImage] = useState([]);
  console.log(links);
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
      {links.length > 0 && (
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

// function QuizOption({ feed, interaction, handleInteraction }) {
//   return (
//     <ol className={style["quiz-container"]}>
//       {interaction &&
//         interaction?.choice?.map((option, i) => {
//           return (
//             <li
//               key={i}
//               onClick={(e) => {
//                 e.stopPropagation();
//                 handleInteraction(e, interaction.fid, i);
//               }}
//             >
//               {i + 1}. {option} / {interaction.result[i]}
//             </li>
//           );
//         })}
//     </ol>
//   );
// }
