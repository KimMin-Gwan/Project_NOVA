import { useLocation, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { ContentFeed } from "../../component/feed";
import { useState } from "react";
import { useEffect } from "react";
import style from "./FeedDetail.module.css";
import { useRef } from "react";

import more_icon from "./../../img/more_icon.svg";
import back from "./../../img/backword.png";
import star from "./../../img/favorite.png";
import axios from "axios";

export default function FeedDetail({ feed }) {
  let navigate = useNavigate();
  let { fid } = useParams();
  // let [searchParams] = useSearchParams();
  // let fid = searchParams.get("fid");

  let location = useLocation();
  let { state } = location;
  const [isLoading, setIsLoading] = useState(true); // 로딩 상태 관리

  let commentRef = useRef(null);
  useEffect(() => {
    if (!isLoading && commentRef.current && state.commentClick) {
      commentRef.current.focus();
      //       // 렌더링이 완료된 후 focus를 지연시킴
      //       setTimeout(() => {
      //       }, 0); // 0초 후 실행
    }
  }, [isLoading]);

  let [feedData, setFeedData] = useState([]);
  let [comments, setComments] = useState([]);
  let [interaction, setInteraction] = useState();

  async function fetchFeed() {
    await fetch(`https://nova-platform.kr/feed_explore/feed_detail/feed_data?fid=${fid}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("detail", data);
        setInteraction(data.body.interaction);
        setFeedData(data.body.feed[0]);
        setIsLoading(false);
      });
  }

  useEffect(() => {
    fetchFeed();
  }, [comments, fid]);

  async function fetchFeedComment() {
    await fetch(`https://nova-platform.kr/feed_explore/feed_detail/comment_data?fid=${fid}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("comment all", data);
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
      fetchMakeComment();
      setCommentValue("");
    }
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
        console.log("make", data);
        setComments(data.body.comments);
        // setComments((prevComments) => {
        //   return [data.body.comments[0], ...prevComments];
        // });
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
        console.log(res.data);
      });
  }

  if (isLoading) {
    return <div>Loading</div>;
  }

  return (
    <div className={style["FeedDetail"]}>
      <div className={style["top-container"]} onClick={onClickNav}>
        <button className={style["back-button"]}>
          <img src={back} alt="back" />
          <span>뒤로</span>
        </button>
        {feedData.is_owner && (
          <button
            className={style["delete-button"]}
            onClick={() => {
              fetchRemoveFeed();
            }}
          >
            <img src={more_icon} />
          </button>
        )}
      </div>

      <div>
        <ContentFeed feed={feedData} interaction={interaction} handleCheckStar={handleCheckStar} />
      </div>

      <div className={style["comment-container"]}>
        <div className={style["title-box"]}>
          <div>댓글</div>
          <div>총 {feedData && feedData.num_comment}건</div>
        </div>

        {/* 댓글 각각 */}
        {comments.length !== 0 &&
          comments.map((comment, i) => {
            const [firstWord, ...restWords] = comment.body.split(" ");
            return (
              <div
                key={comment.cid}
                className={`${style["comment-box"]} `}
                onClick={() => {
                  onClickComment(comment.cid, comment.target_cid, comment.uname);
                }}
              >
                <div
                  className={`${style["comment-wrapper"]}
                ${comment.target_cid && style["comment-recomment"]}`}
                >
                  <div className={style["comment-user"]}>
                    <div>
                      {comment.uname}
                      <span>{comment.date}</span>
                    </div>
                    <div>신고</div>
                  </div>

                  <div className={style["comment-content"]}>
                    <span style={{ color: comment.mention ? "#2C59CD" : "black" }}>
                      {firstWord}{" "}
                    </span>
                    {restWords.join("")}
                  </div>
                  <div className={style["action-container"]}>
                    <div className={style["button-box1"]}>
                      <div className={style["action-button"]}>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            // handleCheckStar(feed.fid, e);
                          }}
                        >
                          <img src={star} alt="star-icon" />
                        </button>
                        <span></span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        {comments.target_cid && <div>헤이</div>}
      </div>
      <div className={style["input-container"]}>
        <input
          ref={commentRef}
          type="text"
          id={style["comment"]}
          value={commentValue}
          onChange={onChangeComment}
          onKeyDown={onKeyDownEnter}
          placeholder="당신의 생각을 남겨보세요."
        />
      </div>
    </div>
  );
}
