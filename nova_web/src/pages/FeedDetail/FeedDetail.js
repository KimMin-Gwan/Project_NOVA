import { useLocation, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { ContentFeed } from "../../component/feed";
import { useState } from "react";
import { useEffect } from "react";
import style from "./FeedDetail.module.css";
import { useRef } from "react";

import more_icon from "./../../img/more_icon.svg";
// import back from "./../../img/backword.png";
import back from "./../../img/detail_back.png";
import star from "./../../img/favorite.png";
import input from "./../../img/input.svg";
import axios from "axios";
import mainApi from "../../services/apis/mainApi";
//import reArrow from "./../../img/recomment2.svg";
import reArrow1 from "./../../img/reArrow1.svg";
import reArrow2 from "./../../img/reArrow2.svg";
import reArrow3 from "./../../img/reArrow3.svg";
import reArrow4 from "./../../img/reArrow4.svg";
export default function FeedDetail({}) {
  let navigate = useNavigate();
  let { fid } = useParams();

  let location = useLocation();
  let { state } = location;

  let commentRef = useRef(null);

  const [isLoading, setIsLoading] = useState(true); // 로딩 상태 관리
  const [isComment, setIsComment] = useState(false);
  let [feedData, setFeedData] = useState([]);
  let [comments, setComments] = useState([]);
  let [interaction, setInteraction] = useState();

  useEffect(() => {
    if (!isLoading && commentRef.current && state.commentClick) {
      commentRef.current.focus();
      //       // 렌더링이 완료된 후 focus를 지연시킴
      //       setTimeout(() => {
      //       }, 0); // 0초 후 실행
    }
  }, [isLoading]);

  const [links, setLinks] = useState([]);

  async function fetchFeed() {
    await fetch(`https://nova-platform.kr/feed_explore/feed_detail/feed_data?fid=${fid}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("detail", data);
        setInteraction(data.body.interaction);
        setFeedData(data.body.feed[0]);
        setLinks(data.body.links);
        setIsLoading(false);
        setIsComment(false);
      });
  }

  useEffect(() => {
    fetchFeed();
  }, [comments, fid]);

  // 상호작용
  async function handleInteraction(event, fid, action) {
    event.preventDefault();
    setIsLoading(true);
    await mainApi.get(`/feed_explore/interaction_feed?fid=${fid}&action=${action}`).then((res) => {
      setInteraction((prevData) => {
        return interaction.fid === fid ? res.data.body.interaction : prevData;
      });
      setIsLoading(false);
    });
  }

  async function fetchFeedComment() {
    await fetch(`https://nova-platform.kr/feed_explore/feed_detail/comment_data?fid=${fid}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setComments(data.body.comments);
        setIsLoading(false);
      });
  }

  useEffect(() => {
    fetchFeedComment();
  }, []);

  let [isClickedStar, setIsClickedStar] = useState(false);

  async function handleCheckStar(fid, e) {
    // e.preventDefault();
    setIsClickedStar(!isClickedStar);
    await fetch(`https://nova-platform.kr/feed_explore/check_star?fid=${fid}`, {
      credentials: "include",
    })
      .then((response) => {
        if (!response.ok) {
          if (response.status === 401) {
            navigate("/novalogin");
          } else {
            throw new Error(`status: ${response.status}`);
          }
        }
        return response.json();
      })
      .then((data) => {
        setFeedData((prevData) => {
          return prevData.fid === fid
            ? {
                ...prevData,
                star: data.body.feed[0].star,
                star_flag: data.body.feed[0].star_flag,
              }
            : prevData;
        });
      });
  }

  let [commentValue, setCommentValue] = useState("");

  function onChangeComment(e) {
    setCommentValue(e.target.value);
  }

  function onKeyDownEnter(e) {
    if (e.key === "Enter") {
      setIsComment(true);
      fetchMakeComment();
      setCommentValue("");
    }
  }

  function onClickInput() {
    fetchMakeComment();
    setCommentValue("");
  }

  let header = {
    "request-type": "default",
    "client-version": "v1.0.1",
    "client-ip": "127.0.0.1",
    uid: "1234-abcd-5678",
    endpoint: "/core_system/",
  };

  async function fetchMakeComment() {
    await fetch("https://nova-platform.kr/feed_explore/make_comment", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        header,
      },
      body: JSON.stringify({
        header: header,
        body: {
          fid: `${fid}`,
          body: `${commentValue}`,
          target_cid: commentId,
        },
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        setComments(data.body.comments);
        setCommentId("");
      });
  }

  let [commentId, setCommentId] = useState("");

  const onClickComment = (cid, targetCid, uname) => {
    setCommentId(targetCid || cid);
    setCommentValue(`@${uname} `);
    commentRef.current.focus();
  };

  function onClickNav() {
    navigate(-1);
  }

  function fetchRemoveFeed() {
    axios
      .get(`https://nova-platform.kr/feed_explore/try_remove_feed?fid=${fid}`, {
        withCredentials: true,
      })
      .then((res) => {
        if (res.data.body.result) {
          alert("삭제되었습니다.");
          navigate(-1);
        }
      });
  }

  const [showMoreOption, setShowMoreOption] = useState(false);
  function onClickOption(e) {
    e.preventDefault();
    e.stopPropagation();
    setShowMoreOption(!showMoreOption);
  }

  if (isLoading) {
    return <div>Loading</div>;
  }

  return (
    <div className={style["FeedDetail"]}>
      <div className={style["top-container"]}>
        <button className={style["back-button"]} onClick={onClickNav}>
          <img src={back} alt="back" />
          <span>뒤로</span>
        </button>
        {feedData.is_owner && (
          <button
            className={style["delete-button"]}
            onClick={(e) => {
              onClickOption(e);
            }}
          >
            <img src={more_icon} />
          </button>
        )}
        {showMoreOption && <OptionModal onClickOption={onClickOption} onClickDelete={fetchRemoveFeed} />}
      </div>

      <div>
        <ContentFeed detailPage feed={feedData} handleCheckStar={handleCheckStar} links={links} />
      </div>

      <div className={style["comment-container"]}>
        <div className={style["title-box"]}>
          <div>댓글</div>
          <div>총 {feedData && feedData.num_comment}건</div>
        </div>

        {/* 댓글 각각 */}
        {comments.length !== 0 &&
          comments.map((comment, i) => {
            return <Comment key={comment.cid} comment={comment} onClickComment={onClickComment} />;
          })}
        <div className={style["input-container"]}>
          <div className={style["input-wrapper"]}>
            <input ref={commentRef} type="text" id={style["comment"]} value={commentValue} onChange={onChangeComment} onKeyDown={onKeyDownEnter} placeholder="당신의 생각을 남겨보세요." />
            <button className={style["input-button"]} onClick={onClickInput}>
              <img src={input} alt="input" />
            </button>
          </div>
        </div>
      </div>
      {isComment && <p className={style["loading-st"]}>업로드 중입니다...</p>}
    </div>
  );
}

// 댓글
function Comment({ comment, onClickComment }) {
  async function fetchOriginalComment(cid) {
    await mainApi.get(`feed_explore/original_comment_data?cid=${cid}`).then((res) => {
      console.log("ccc", res.data);
    });
  }

  return (
    <div
      key={comment.cid}
      className={style["comment-box"]}
      onClick={() => {
        onClickComment(comment.cid, comment.target_cid, comment.uname);
      }}
    >
      <section>
        <div className={style["comment-user"]}>
          <div>
            {comment.uname}
            <span>{comment.date}</span>
          </div>

          <div className={style["function_button_container"]}>
            <button
              className={style["AI_text"]}
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                fetchOriginalComment(comment.cid);
              }}
            >
              원문 보기
            </button>
            <div>신고</div>
          </div>
        </div>

        <div className={style["comment-content"]}>{comment.body}</div>

        <span className={style["date-st"]}>{comment.date}</span>
      </section>

      {/* <div className={style["action-container"]}>
        <div className={style["button-box1"]}>
          <div className={style["action-button"]}>
            <button
              onClick={(e) => {
                e.stopPropagation();
              }}
            >
              <img src={star} alt="star-icon" />
            </button>
            <span>{comment.like}</span>
          </div>
        </div>
      </div> */}

      {comment.reply.length !== 0 &&
        comment.reply?.map((reply, i) => {
          return <ReplyComment key={reply.cid} index={i} length={comment.reply.length} reply={reply} fetchOriginalComment={fetchOriginalComment} />;
        })}
    </div>
  );
}

// 대댓글
function ReplyComment({ index, length, reply, fetchOriginalComment }) {
  const [firstWord, ...restWords] = reply.body.split(" ");

  let src;

  if (length === 1) {
    src = reArrow1;
  } else {
    if (index=== 0) {
      src = reArrow2;
    } else if (index+ 1 === length) {
      src = reArrow4;
    } else {
      src = reArrow3;
    }
  }

  return (
    <div className={style["img-container"]}>
      <img src={src} alt="대댓글" />
      <div key={reply.cid} className={`${style["reply-box"]}`} onClick={(e) => e.stopPropagation()}>
        <div className={style["comment-user"]}>
          <div>답변 : {reply.uname}</div>
          <div className={style["function_button_container"]}>
            <button
              className={style["AI_text"]}
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                fetchOriginalComment(reply.cid);
              }}
            >
              원문 보기
            </button>
            <div>신고</div>
          </div>
        </div>

        <div className={style["comment-content"]}>
          <span style={{ color: reply.mention ? "#2C59CD" : "black" }}>{firstWord} </span>
          {restWords.join("")}
        </div>

        <span className={style["date-st"]}> {reply.date}</span>

        {/* <div className={style["action-container"]}>
          <div className={style["button-box1"]}>
            <div className={style["action-button"]}>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                }}
              >
                <img src={star} alt="star-icon" />
              </button>
              <span>{reply.like}</span>
            </div>
          </div>
        </div> */}
      </div>
    </div>
  );
}

// 모달
function OptionModal({ onClickOption, onClickDelete }) {
  return (
    <div className={style["OptionModal"]} onClick={onClickOption}>
      <div className={style["modal_container"]}>
        <div className={style["modal_title"]}>설정</div>
        <div className={style["modal_content"]}>수정</div>
        <div className={`${style["modal_content"]} ${style["modal_content_accent"]}`} onClick={onClickDelete}>
          삭제
        </div>
      </div>
    </div>
  );
}
