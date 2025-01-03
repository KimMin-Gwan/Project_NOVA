import { useLocation, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { ContentFeed } from "../../component/feed";
import { useState } from "react";
import { useEffect } from "react";
import style from "./FeedDetail.module.css";
import { useRef } from "react";

import back from "./../../img/backword.png";
import star from "./../../img/favorite.png";

export default function FeedDetail({ feed }) {
  let navigate = useNavigate();
  let { fid } = useParams();

  let location = useLocation();
  let { state } = location;
  const [isLoading, setIsLoading] = useState(true); // 로딩 상태 관리

  let commentRef = useRef(null);
  useEffect(() => {
    //     // isLoading이 false일 때만 focus()가 실행되도록
    if (!isLoading && commentRef.current && state.commentClick) {
      //       // 렌더링이 완료된 후 focus를 지연시킴
      //       setTimeout(() => {
      commentRef.current.focus();
      //       }, 0); // 0초 후 실행
    }
  }, [isLoading]);
  //   //   const [params] = useSearchParams();
  //   //   const FID = params.get("fid");

  let [feedData, setFeedData] = useState([]);
  let [comments, setComments] = useState([]);

  async function fetchFeed() {
    await fetch(`https://nova-platform.kr/feed_explore/feed_detail/feed_data?fid=${fid}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("detail", data);
        setFeedData(data.body.feed);
        setIsLoading(false);
      });
  }

  useEffect(() => {
    fetchFeed();
  }, [comments]);

  async function fetchFeedComment() {
    await fetch(`https://nova-platform.kr/feed_explore/feed_detail/comment_data?fid=${fid}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setComments(data.body.comments);
        setIsLoading(false);
      });
  }

  useEffect(() => {
    fetchFeedComment();
  }, []);

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
            navigate("/novalogin");
          } else {
            throw new Error(`status: ${response.status}`);
          }
        }
        return response.json();
      })
      .then((data) => {
        console.log("clickstar", data);
        setFeedData((prevFeeds) => {
          return prevFeeds.map((feed) => {
            return feed.fid === fid
              ? { ...feed, star_flag: data.body.feed[0].star_flag, star: data.body.feed[0].star }
              : feed;
          });
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
          target_cid: "",
        },
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("make", data);
        setComments((prevComments) => {
          return [data.body.comments[0], ...prevComments];
        });
      });
  }

  function onClickNav() {
    navigate(-1);
  }

  if (isLoading) {
    return <div>Loading</div>;
  }

  return (
    <div className={style["FeedDetail"]}>
      <div className={style["top-container"]} onClick={onClickNav}>
        <button className={style["back-button"]}>
          <img src={back} />
          <span>뒤로</span>
        </button>
      </div>

      <div>
        <ContentFeed feed={feedData[0]} handleCheckStar={handleCheckStar} />
      </div>

      <div className={style["comment-container"]}>
        <div className={style["title-box"]}>
          <div>댓글</div>
          <div>총 {feedData[0].num_comment}건</div>
        </div>

        {/* 댓글 각각 */}
        {comments.length !== 0 &&
          comments.map((comment, i) => {
            return (
              <div key={comment.cid} className={style["comment-box"]}>
                <div className={style["comment-wrapper"]}>
                  <div className={style["comment-user"]}>
                    <div>
                      {comment.uname}
                      <span>{comment.date}</span>
                    </div>
                    <div>신고</div>
                  </div>

                  <div className={style["comment-content"]}>{comment.body}</div>
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
