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


export default function Feed({ feed, setFeedData, type }) {
  const header = HEADER;
  const { handleCheckStar } = useFeedActions(setFeedData, type);
  const navigate = useNavigate();

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
      <PreviewContentFeed
        feed={feed}
        handleCheckStar={handleCheckStar}
        fetchReportResult={fetchReportResult}
        navigate={navigate}
      />
    </>
  );
}

export const PreviewContentFeed = ({ 
    feed,
    handleCheckStar,
    links,
    fetchReportResult,
    navigate
  }) =>{
    const { scrollRef, hasDragged, dragHandlers } = useDragScroll();
    if (!feed) {
      return <div>loading 중...</div>;
    }

    return (
      <div className={style["preview-content-feed-wrapper"]}>
        <div className={style["wrapper-top-component"]}>
          {feed.bname && (
            <div className={style["meta-data-1"]}>
              <p>
                {feed.bname}
              </p>
            </div>
          )}
          <div className={style["meta-data-2"]}>
              <p>
                {feed.board_type}
              </p>
          </div>
        </div>
        <div
          className={`${style["wrapper-container2"]} ${style["long-wrapper"]}`}
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

          <div className={`${style["preview-body-container"]} `}>
            <HashTags hashtags={feed.hashtag} />
            <Viewer key={feed.raw_body} initialValue={feed.raw_body} />
          </div>

          {links && <LinkSection links={links} />}

          <ActionButtons
            feed={feed}
            handleCheckStar={handleCheckStar}
            fetchReportResult={fetchReportResult}
          />
        </div>
      </div>
    );
}


export function ContentFeed({ detailPage, feed, handleCheckStar, links, fetchReportResult}) {

  if (!feed) {
    return <div>loading 중...</div>;
  }

  return (
    <div style={{breakInside: "avoid", marginBottom: "20px"}}>
      <div className={style["wrapper-top-component"]}>
        {feed.bname && (
          <div className={style["meta-data-1"]}>
            <p>
              {feed.bname}
            </p>
          </div>
        )}
        <div className={style["meta-data-2"]}>
            <p>
              {feed.board_type}
            </p>
        </div>
      </div>
      <div
        className={`${style["wrapper-container"]} ${ style["long-wrapper"]}`}
      >
        <FeedHeader date={feed.date} nickname={feed.nickname} />

        <div className={`${style["body-container"]}`}>
          <HashTags hashtags={feed.hashtag} />
          <Viewer key={feed.raw_body} initialValue={feed.raw_body} />
        </div>

        {links && <LinkSection links={links} />}

        <ActionButtons
          feed={feed}
          handleCheckStar={handleCheckStar}
          fetchReportResult={fetchReportResult}
        />
      </div>
    </div>
  );
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
          <span>{feed.like}</span>
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
