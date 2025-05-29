import { useState, useEffect } from "react";
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
import useDragScroll from "../hooks/useDragScroll";
import useFeedActions from "../hooks/useFeedActions";

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

export default function Feed({ feed, setFeedData, type }) {
  const { handleCheckStar } = useFeedActions(setFeedData, type);

  const [report, setReport] = useState();

  async function fetchReportResult(fid) {
    await postApi.post("nova_sub_system/try_report", {
      header: header,
      body: {
        fid: fid,
      },
    });
    //.then((res) => //console.log("rerere", res.data));
  }

  return (
    <>
      <ContentFeed
        feed={feed}
        handleCheckStar={handleCheckStar}
        fetchReportResult={fetchReportResult}
        disableClick={false}
      />
    </>
  );
}

export function ContentFeed({ detailPage, feed, handleCheckStar, links, fetchReportResult, disableClick}) {
  let navigate = useNavigate();
  const { scrollRef, hasDragged, dragHandlers } = useDragScroll();

  async function fetchOriginalText(fid) {
    await mainApi.get(`feed_explore/original_feed_data?fid=${fid}`).then((res) => {
      console.log("done");
    });
  }

  if (!feed) {
    return <div>loading 중...</div>;
  }

  if (disableClick){
    return (
      <div
        className={`${style["wrapper-container"]} ${feed.fclass === "long" && style["long-wrapper"]}`}
      >
        <FeedHeader date={feed.date} nickname={feed.nickname} />
        {/**
        <AIFilter
          isReworked={feed.is_reworked}
          fid={feed.fid}
          fetchOriginalText={fetchOriginalText}
        />
         
         */}

        <div className={`${style["body-container"]} ${detailPage ? "" : style["long-form-hidden"]}`}>
          <HashTags hashtags={feed.hashtag} />

          {feed.fclass === "short" && <div className={style["body-content"]}>{feed.body}</div>}
          {feed.image?.length > 0 && feed.fclass === "short" ? (
            <div className={style["image-container"]}>
              <div
                ref={scrollRef}
                className={`${style["image-origin"]} ${style["two-over-image"]}`}
                onMouseDown={dragHandlers.onMouseDown}
                onMouseMove={dragHandlers.onMouseMove}
                onMouseUp={dragHandlers.onMouseUp}
              >
                {feed.num_image >= 2 ? (
                  feed.image.map((img, i) => {
                    return <img key={i} src={img} alt="image" />;
                  })
                ) : (
                  <img src={feed.image[0]} alt="image" />
                )}
              </div>
            </div>
          ) : null}

          {feed.fclass === "long" && <Viewer initialValue={feed.raw_body} />}
        </div>

        {links && <LinkSection links={links} />}

        <ActionButtons
          feed={feed}
          handleCheckStar={handleCheckStar}
          fetchReportResult={fetchReportResult}
        />
      </div>
    );
  }else{
    return (
      <div
        className={`${style["wrapper-container"]} ${feed.fclass === "long" && style["long-wrapper"]}`}
        onClick={(e) => {
          if (hasDragged) return;
          e.preventDefault();
          e.stopPropagation();
          navigate(`/feed_detail/${feed.fid}`, {
            state: { commentClick: false },
          });
        }}
      >
        <FeedHeader date={feed.date} nickname={feed.nickname} />
        <AIFilter
          isReworked={feed.is_reworked}
          fid={feed.fid}
          fetchOriginalText={fetchOriginalText}
        />

        <div className={`${style["body-container"]} ${detailPage ? "" : style["long-form-hidden"]}`}>
          <HashTags hashtags={feed.hashtag} />

          {feed.fclass === "short" && <div className={style["body-content"]}>{feed.body}</div>}
          {feed.image?.length > 0 && feed.fclass === "short" ? (
            <div className={style["image-container"]}>
              <div
                ref={scrollRef}
                className={`${style["image-origin"]} ${style["two-over-image"]}`}
                onMouseDown={dragHandlers.onMouseDown}
                onMouseMove={dragHandlers.onMouseMove}
                onMouseUp={dragHandlers.onMouseUp}
              >
                {feed.num_image >= 2 ? (
                  feed.image.map((img, i) => {
                    return <img key={i} src={img} alt="image" />;
                  })
                ) : (
                  <img src={feed.image[0]} alt="image" />
                )}
              </div>
            </div>
          ) : null}

          {feed.fclass === "long" && <Viewer initialValue={feed.raw_body} />}
        </div>

        {links && <LinkSection links={links} />}

        <ActionButtons
          feed={feed}
          handleCheckStar={handleCheckStar}
          fetchReportResult={fetchReportResult}
        />
      </div>
    );
  }
}

// 피드 날짜 및 작성자
function FeedHeader({ date, nickname }) {
  return (
    <div className={style["user-container"]}>
      <div>{date}</div>
      <div>{nickname}</div>
    </div>
  );
}

function AIFilter({ isReworked, fid, fetchOriginalText }) {
  if (!isReworked) {
    return null;
  }
  return (
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
          fetchOriginalText(fid);
        }}
      >
        원문 보기
      </button>
    </div>
  );
}

// 해시 태그
function HashTags({ hashtags }) {
  if (!hashtags || hashtags.length === 0) {
    return null;
  }

  return (
    <div className={style["body-hashtag"]}>
      {hashtags.length !== 0 &&
        hashtags.map((tag, i) => {
          return <span key={i}>#{tag}</span>;
        })}
    </div>
  );
}

function ActionButtons({ feed, handleCheckStar, fetchReportResult }) {
  const navigate = useNavigate();

  return (
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
          >
            <img src={comment} alt="comment-icon" />
          </button>
          <span>{feed.num_comment}</span>
        </div>
      </div>
    </div>
  );
}

function LinkSection({ links }) {
  const [isLoading, setIsLoading] = useState(true);
  const [linkImage, setLinkImage] = useState([]);

  async function fetchImageTag() {
    for (const item of links)
      await postApi
        .post("nova_sub_system/image_tag", {
          header: HEADER,
          body: {
            url: item.url,
          },
        })
        .then((res) => {
          setLinkImage((prev) => [...prev, res.data.body.image]);
          //console.log(res.data);
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
    return <div>loading...</div>;
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
                  console.log(link.url)
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
