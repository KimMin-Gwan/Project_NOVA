import { useLocation, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { ContentFeed } from "../../component/feed";
import { useState } from "react";
import { useEffect } from "react";
import style from "./FeedDetail.module.css";
import { useRef } from "react";

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

  function onClickNav() {
    navigate(-1);
  }

  if (isLoading) {
    return <div>Loading</div>;
  }

  return (
    <div className={style["FeedDetail"]}>
      <div className={style["top-container"]} onClick={onClickNav}>
        뒤로
      </div>

      <div>
        <ContentFeed feed={feedData[0]} />
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
              <div>{feedData[0].comment.uname}</div>
              <div>{feedData[0].comment.date}</div>
              <div>신고</div>
            </div>

            <div className={style["comment-content"]}>{feedData[0].comment.body}</div>
            <div className={style["action-container"]}>상호작용</div>
          </div>
        </div>

        <div className={style["input-container"]}>
          <input
            ref={commentRef}
            type="text"
            id={style["comment"]}
            placeholder="당신의 생각을 남겨보세요"
          />
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
    </div>
  );
}
