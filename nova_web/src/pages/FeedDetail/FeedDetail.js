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

  async function fetchFeed() {
    await fetch(`https://nova-platform.kr/feed_explore/get_feed?fid=${fid}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setFeedData(data.body.feed);
        setIsLoading(false);
      });
  }

  useEffect(() => {
    fetchFeed();
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
    console.log(e.target.value);
    setCommentValue(e.target.value);
  }

  function onKeyDownEnter(e) {
    if (e.key === "Enter") {
      setCommentValue("");
    }
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
        <div className={style["comment-box"]}>
          <div className={style["comment-wrapper"]}>
            <div className={style["comment-user"]}>
              <div>
                {feedData[0].comment.uname}
                <span>{feedData[0].comment.date}</span>
              </div>
              <div>신고</div>
            </div>

            <div className={style["comment-content"]}>{feedData[0].comment.body}</div>
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
                  <span>0</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* <div className={style["comment-box"]}>
          <div className={style["comment-wrapper"]}>
            <div className={style["comment-user"]}>
              <div>{feedData[0].comment.uname}</div>
              <div>{feedData[0].comment.date}</div>
              <div>신고</div>
            </div>

            <div className={style["comment-content"]}>{feedData[0].comment.body}</div>
            <div className={style["action-container"]}>상호작용</div>
          </div>
        </div> */}
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
